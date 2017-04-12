# prospector-html
HTML report generator from [prospector](https://blog.landscape.io/prospector-python-static-analysis-for-humans.html) static analyzer tool JSON output.


## Synopsis
    pip install json2html
    cd <python-project-sources-dir>
    prospector --no-style-warnings --strictness medium --output-format json > prospector_report.json
    prospector-html --input prospector_report.json
    cat report.html