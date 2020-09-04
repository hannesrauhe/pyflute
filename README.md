# pyflute
Python script to send image files to pixelflut servers. Options are controlled via env variables.

## Examples

Send 500x500px thumbnail of test.png to pixelflut:1234 (default) in 10 second intervals and ignore black pixels
```
SLEEP=10 SIZEX=500 SIZEY=500 TRANSPARENT=1 IMAGE=test.png python3 pixelflut.py
```
