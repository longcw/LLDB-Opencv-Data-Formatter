import sys

sys.path.insert(0, '/home/longc/anaconda3/lib/python3.6/site-packages')

import lldb
import numpy as np


def __lldb_init_module(debugger, dict):
    debugger.HandleCommand(
        "type summary add -x \"cv::Mat\" -F LLDB_Opencv_Data_Formatter.format_matrix")


def printMatInfo(matInfo):
    text = ""

    # Print the info of the mat
    text += "flags: " + str(matInfo['flags']) + "\n"
    text += "type: " + matInfo['cv_type_name'] + "\n"
    text += "channels: " + str(matInfo['channels']) + "\n"
    text += "rows: " + str(matInfo['rows']) + ", cols: " + str(matInfo['cols']) + "\n"
    text += "line step: " + str(matInfo['line_step']) + "\n"
    text += "data address: " + str(hex(matInfo['data_address'])) + "\n"

    return text


def getMatInfo(root):
    # Flags.
    flags = int(root.GetChildMemberWithName("flags").GetValue())

    # Channels.
    channels = 1 + (flags >> 3) & 63

    # Type of cvMat.
    cv_type_name = None
    depth = flags & 7
    if depth == 0:
        cv_type_name = 'CV_8U'
    elif depth == 1:
        cv_type_name = 'CV_8S'
    elif depth == 2:
        cv_type_name = 'CV_16U'
    elif depth == 3:
        cv_type_name = 'CV_16S'
    elif depth == 4:
        cv_type_name = 'CV_32S'
    elif depth == 5:
        cv_type_name = 'CV_32F'
    elif depth == 6:
        cv_type_name = 'CV_64F'
    else:
        print("cvMat Type not sypported")

    # Rows and columns.
    rows = int(root.GetChildMemberWithName("rows").GetValue())
    cols = int(root.GetChildMemberWithName("cols").GetValue())

    # Get the step (access to value of a buffer with GetUnsignedInt16()).
    error = lldb.SBError()
    line_step = root.GetChildMemberWithName("step").GetChildMemberWithName(
        'buf').GetData().GetUnsignedInt16(error, 0)

    # Get data address.
    data_address = int(root.GetChildMemberWithName("data").GetValue(), 16)

    # Create a dictionary for the output.
    matInfo = {'cols': cols, 'rows': rows, 'channels': channels, 'line_step': line_step,
               'data_address': data_address, 'flags': flags,
               'cv_type_name': cv_type_name, }
    # Return.
    return matInfo


def getArray(valobj, matInfo):
    # Get the info of the Mat.
    width = matInfo['cols']
    height = matInfo['rows']
    n_channel = matInfo['channels']
    line_step = matInfo['line_step']
    data_address = matInfo['data_address']
    cv_type_name = matInfo['cv_type_name']

    np_dtype = {
        'CV_8U': np.uint8,
        'CV_16U': np.uint16,
        'CV_32F': np.float32,
        'CV_64F': np.float64,
    }.get(cv_type_name, None)
    if np_dtype is None:
        return None

    error = lldb.SBError()
    memory_data = valobj.GetProcess().ReadMemory(data_address, line_step * height,
                                                 error)
    arr = np.fromstring(memory_data, dtype=np_dtype)
    arr = arr.reshape(height, width)
    return arr


def format_matrix(valobj, internal_dict):
    if valobj.GetValueForExpressionPath(".flags").IsValid():
        matInfo = getMatInfo(valobj)
        arr = getArray(valobj, matInfo)
        summary = printMatInfo(matInfo) + str(arr)
        return summary
    else:
        return valobj.GetSummary()
