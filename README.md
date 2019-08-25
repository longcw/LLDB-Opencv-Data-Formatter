# LLDB OpenCV Data Formatter

LLDB Data Formatter for dense matrices of Opencv.

## Example
Output in LLDB

```
(lldb) print A
(cv::Mat_<float>) $13 = flags: 1124024325
type: CV_32F
channels: 1
rows: 3, cols: 3
line step: 12
data address: 0x7ffc34c5fb90
[[ 0.74204689  0.          0.5       ]
 [ 0.          1.31919444  0.5       ]
 [ 0.          0.          1.        ]]
```

## Installation

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/longcw/LLDB-Opencv-Data-Formatter/master/tools/install.sh)"
```

__Uninstallation__

```bash
rm -fr ~/.lldb-opencv-data-formatter
```

Afterwards remove the `command script import` command in `~/.lldbinit`.

## License

Distributed under the GNU GENERAL PUBLIC LICENSE.
