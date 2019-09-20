# prospector-html
HTML report generator from [prospector](https://blog.landscape.io/prospector-python-static-analysis-for-humans.html) static analyzer tool JSON output.


## Synopsis
    pip install json2html
    cd <python-project-sources-dir>
    prospector --no-style-warnings --strictness medium --output-format json > prospector_report.json
    prospector-html --input prospector_report.json
    cat report.html
    
## Message filtering
 Sometime it is necessary to filter prospector result by content of the message, 
rather than filter-out the whole error class by it's suppression.
For example prospector would always complains at usage of `_meta` member in Django projects.

 In this case one could fileter such messages by specifing it in prospector-html config file.
`.prospector-html.yaml` by default. See details in source of sample config.      

## TODO
  - Filter messages by regular expressions.  