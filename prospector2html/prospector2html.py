#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import argparse
import json
import yaml
from json2html import *

class Prospector2HTML(object):

    PRH_CONFIG_FILE = '.prospector-html.yaml'
    PRH_DEF_OUTPUT_FILE = 'report.html'

    # Default - empty message filters config
    prh_config = {'filter': {'message': [], 'message_re': []}}


    def filter_message_by_match(self, x):
        if not self.prh_config or not self.prh_config['filter'] or not self.prh_config['filter']['message']:
            return True
        return not any(x['message'] in m for m in self.prh_config['filter']['message'])


    def filter_message_by_re(self, x):
        if not self.prh_config or not self.prh_config['filter'] or not self.prh_config['filter']['message_re']:
            return True
        return not any((re.search(rre, x['message']) is not None) for rre in self.prh_config['filter']['message_re'])


    def filter_message(self, x):
        return self.filter_message_by_match(x) and self.filter_message_by_re(x)


    def get_report_body(self, obj):
        return json2html.convert(json=obj, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")


    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input', help='input JSON file name', required=True,
                            action='store', type=str)
        parser.add_argument('-o', '--output', help='output file name', required=False,
                            default=self.PRH_DEF_OUTPUT_FILE, action='store', type=str)
        parser.add_argument('-c', '--config', help='config file name', required=False,
                            default=self.PRH_CONFIG_FILE, action='store', type=str)
        args = parser.parse_args()

        try:
            with open(args.config, 'r') as stream:
                try:
                    self.prh_config = yaml.safe_load(stream)
                    print("Using config file '" + args.config + "'")
                except yaml.YAMLError as exc:
                    print("Can't parse config file '" + args.config + "': " + str(exc))
                    return 3
        except IOError as e:
            if args.config != self.PRH_CONFIG_FILE:
                print("Can't open config file '" + args.config + "': " + e.strerror)
                return 3

        with open(args.input, 'r') as f:
            json_str = f.read()

        json_obj = json.loads(json_str)

        deduplicated_msgs = []
        for msg in json_obj['messages']:
            if msg not in deduplicated_msgs:
                deduplicated_msgs.append(dict(msg))

        filtered_msg = list(filter(self.filter_message, deduplicated_msgs))
        filtered_msg.sort(key=lambda x: (x['location']['path'], x['location']['line']))

        html_string = '''
        <html>
            <head>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
                <style>body{ margin:0 100; background:whitesmoke; }</style>
            </head>
            <body>
        ''' + self.get_report_body(filtered_msg) + '''
            </body>
        </html>'''

        with open(args.output, 'w') as f:
            f.write(html_string)

        if filtered_msg:
            print('Still ' + str(len(filtered_msg)) + ' messages after filtering...')
            return 1

        return 0


if __name__ == '__main__':
    prh = Prospector2HTML()
    sys.exit(prh.main())
