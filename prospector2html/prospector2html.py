#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
from datetime import datetime
import argparse
import json
import yaml
from json2html import *

class Prospector2HTML:

    PRH_CONFIG_FILE = '.prospector-html.yaml'
    PRH_DEF_OUTPUT_FILE = 'prospector-html-report'

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


    def normalize_prospector(self, x):
        result = []
        for item in x:
            result.append({
                'tool': item['source'],
                'code': item['code'],
                'severity': 'unknown',
                'confidence': 'unknown',
                'function': item['location']['function'],
                'file': item['location']['path'],
                'line': item['location']['line'],
                'position': item['location']['character'],
                'message': item['message']
            })

        return result


    def normalize_gitlab_sast(self, x):
        result = []
        for item in x:
            result.append({
                'tool': item['scanner']['id'],
                'code': ', '.join([i['value'] for i in item['identifiers']]),
                'severity': item['severity'],
                'confidence': item['confidence'],
                'function': 'unknown',
                'file': item['location']['file'],
                'line': item['location']['start_line'],
                'position': 0,
                'message': item['message']
            })

        return result

    def normalize_semgrep(self, x):
        result = []
        for item in x:
            result.append({
                'tool': 'semgrep',
                'code': item['check_id'],
                'severity': item['extra']['severity'],
                'confidence': item['extra']['metadata']['confidence'],
                'function': 'unknown',
                'file': item['path'],
                'line': item['start']['line'],
                'position': item['start']['col'],
                'message': item['extra']['message']
            })

        return result



    def get_report_body(self, obj):
        return json2html.convert(json=obj, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")


    def main(self):
        parser = argparse.ArgumentParser(prog='propsector-html')
        parser.add_argument('-i', '--input', help='input JSON file name', required=True,
                            action='store', type=str)
        parser.add_argument('-o', '--output', help='output file name', required=False,
                            default=self.PRH_DEF_OUTPUT_FILE, action='store', type=str)
        parser.add_argument('-c', '--config', help='config file name', required=False,
                            default=self.PRH_CONFIG_FILE, action='store', type=str)
        parser.add_argument('-j', '--json', help='dump output as JSON', required=False,
                            default=False, action=argparse.BooleanOptionalAction)
        parser.add_argument("-z", "--zero-exit", action="store_true", default=False,
                            help="Always exit with zero return code.")
        parser.add_argument('-f', '--filter', help='apply tool filter for input JSON', required=False,
                            default='prospector', choices = ['none', 'prospector', 'semgrep', 'gitlab-sast'])

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
        msgs = json_obj

        if args.filter == 'gitlab-sast':
            msgs = json_obj['vulnerabilities']
        elif args.filter == 'semgrep':
            msgs = json_obj['results']
        elif args.filter == 'prospector':
            msgs = json_obj['messages']

        deduplicated_msgs = []
        for msg in msgs:
            if msg not in deduplicated_msgs:
                deduplicated_msgs.append(dict(msg))

        if args.filter == 'gitlab-sast':
            deduplicated_msgs = self.normalize_gitlab_sast(deduplicated_msgs)
        elif args.filter == 'semgrep':
            deduplicated_msgs = self.normalize_semgrep(deduplicated_msgs)
        elif args.filter == 'prospector':
            deduplicated_msgs = self.normalize_prospector(deduplicated_msgs)

        filtered_msgs = list(filter(self.filter_message, deduplicated_msgs))
        filtered_msgs.sort(key=lambda x: (x['file'], x['line']))

        meta_info = {
            'report_date': str(datetime.now()),
            'commit_date': os.environ.get('CI_COMMIT_TIMESTAMP', None),
            'commit_author': os.environ.get('CI_COMMIT_AUTHOR', 'unknown'),
            'commit_description': os.environ.get('CI_COMMIT_DESCRIPTION', 'unknown'),
            'mr_source_branch': os.environ.get('CI_MERGE_REQUEST_SOURCE_BRANCH_NAME', 'unknown'),
            'mr_target_branch': os.environ.get('CI_MERGE_REQUEST_TARGET_BRANCH_NAME', 'unknown'),
            'mr_title': os.environ.get('CI_MERGE_REQUEST_TITLE', 'unknown'),
            'pipeliine_job_image': os.environ.get('CI_JOB_IMAGE', 'unknown'),
            'pipeliine_job_name': os.environ.get('CI_JOB_NAME', 'unknown'),
            'pipeliine_job_stage': os.environ.get('CI_JOB_STAGE', 'unknown'),
            'pipeliine_pipeline_url': os.environ.get('CI_PIPELINE_URL', 'unknown'),
            'pipeliine_job_url': os.environ.get('CI_JOB_URL', 'unknown'),
            'pipeliine_project_path': os.environ.get('CI_PROJECT_PATH', 'unknown'),
            'pipeliine_project_name': os.environ.get('CI_PROJECT_NAME', 'unknown'),
            'pipeliine_project_group': os.environ.get('CI_PROJECT_NAMESPACE', 'unknown'),
            'pipeliine_project_url': os.environ.get('CI_PROJECT_URL', 'unknown'),
            'pipeliine_server_url': os.environ.get('CI_SERVER_URL', 'unknown'),
            'filtered_message_count': len(deduplicated_msgs),
            'total_message_count': len(filtered_msgs)
        }

        report_string = ''
        if args.json:
            report_content = {
                'meta': meta_info,
                'data': filtered_msgs
            }
            report_string = json.dumps(report_content, indent=2, sort_keys=True)
        else:
            report_string = '''
            <html>
                <head>
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
                    <style>body{ margin:0 100; background:whitesmoke; }</style>
                </head>
                <!-- 
                ''' + json.dumps({ 'meta': meta_info }, indent=2, sort_keys=True) + '''
                -->
                <body>
            ''' + self.get_report_body(filtered_msgs) + '''
                </body>
            </html>'''

        report_file = args.output
        if report_file == self.PRH_DEF_OUTPUT_FILE:
            if args.json:
                report_file += '.json'
            else:
                report_file += '.html'

        with open(report_file, 'w') as f:
            f.write(report_string)

        ret_code = 5
        if filtered_msgs:
            print('Still ' + str(len(filtered_msgs)) + ' messages after filtering...')
            ret_code = 1
        else:
            print('No messages after filtering...')
            ret_code = 0

        if args.zero_exit:
            ret_code = 0

        return ret_code


if __name__ == '__main__':
    prh = Prospector2HTML()
    sys.exit(prh.main())
