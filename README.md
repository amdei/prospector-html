# prospector-html
HTML and JSON report generator from [prospector](https://blog.landscape.io/prospector-python-static-analysis-for-humans.html) and [semgrep](https://semgrep.dev/docs/) static analyzer tools JSON output.
Handy when using with GitLab CI.


# Synopsis
## prospector
    pip3 install prospector
    pip3 install prospector2html
    cd <python-project-sources-dir>
    prospector --no-style-warnings --strictness medium --output-format json > prospector_report.json
    prospector-html --input prospector_report.json
    cat prospector-html-report.html


## semgrep
    pip3 install prospector2html
    cd <project-sources-dir>
    docker run --rm -v "${PWD}:/src" returntocorp/semgrep:latest semgrep scan --json --output semgrep-native-report.json --config=auto
    prospector-html --input semgrep-native-report --output filtered-report.html --filter semgrep
    cat filtered-report.html


## GitLab CI SAST
    pip3 install prospector2html
    cd <project-sources-dir>
    docker run --rm -v "${PWD}:/src" returntocorp/semgrep:latest semgrep ci --gitlab-sast --output gl-sast-report.json --config=auto
    prospector-html --input gl-sast-report.json --output filtered-report.json --json --filter gitlab-sast
    cat filtered-report.json


## Message filtering
 Sometimes it is necessary to filter analyzer results by content of the message,
rather than filter-out the whole error class by it's suppression.
For example prospector would always complains at usage of `_meta` member in Django projects.

 In this case one could fileter such messages by specifing it in prospector-html config file.
`.prospector-html.yaml` by default. See details in the source of sample config or use following example:

    # cat .prospector-html.yaml
    filter:
      message:
          # Filter by exact match
        - "Message to filter"
        - Oter message to filter
      message_re:
          # Regexps to filter
        - 'Exactly one space required after comma.*'
        - 'Exactly one space required before assignment.*'


## TODO
  - ???.
