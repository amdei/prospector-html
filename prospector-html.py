#!/usr/bin/env python

import argparse
import json
from json2html import *


def get_report_body(obj):
    return json2html.convert(json=obj, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='input JSON file name', required=True, action='store', type=str)
args = parser.parse_args()

print args.input


with open(args.input, 'r') as f:
    json_str = f.read()

json_obj = json.loads(json_str)
json_obj['messages'].sort(key=lambda x: (x['location']['path'], x['location']['line']))

html_string = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
''' + get_report_body(json_obj['messages']) + '''
    </body>
</html>'''

with open('report.html', 'w') as f:
    f.write(html_string)
