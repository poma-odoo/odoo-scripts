#!/usr/bin/env python3
import base64, os, mimetypes

encoded = []

for file in os.listdir('.'):
    with open(file, 'rb') as f:
        print("converting: " + file)
        mime = mimetypes.guess_type(file)[0]
        # fix for old operating systems
        extension = os.path.splitext(file)[1]
        if not mime and extension == '.woff2':
            mime = 'font/woff2'

        prefix = "data:{};charset=utf-8;base64,".format(mime)
        encoded.append("{}: {}{}".format(file, prefix, base64.standard_b64encode(f.read()).decode("utf-8")))

with open("result.base64", 'wt') as fw:
    fw.write("\n".join(encoded))
print('all data saved in `result.base64`')
