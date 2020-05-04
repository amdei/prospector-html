# prospector-html
HTML report generator from [prospector](https://blog.landscape.io/prospector-python-static-analysis-for-humans.html) static analyzer tool JSON output.


## Synopsis
    pip install prospector
    pip install prospector2html
    cd <python-project-sources-dir>
    prospector --no-style-warnings --strictness medium --output-format json > prospector_report.json
    prospector-html --input prospector_report.json
    cat report.html
    
## Message filtering
 Sometimes it is necessary to filter prospector result by content of the message, 
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
