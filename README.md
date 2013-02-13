lnkckr
======

**lnkckr** is a link checking library with command-line script `linkcheck`. It's intended to be used to checking broken links and it can be interrupted at any time, then resumes from saved JSON file.

It supports Python 2.7 and Python 3.

Installation
------------

    pip install lnkckr

Usage
-----

    linkcheck [-c CHECKER] [-f FILE] [-j JSON] [-s STATUS]

* `CHECKER` is what checker used to process `FILE`.
* `FILE` is the input filename or URL.
* `JSON` is the filename of saved progress file. If the `FILE` is a filename, then `FILE` can be omitted, an filename is assigned automatically unless using different filename is desired.
* `STATUS` indicates re-check url with specific status.

Checkers
--------

* `list`: input file is a list of links, one URL per line.
* `html`: input file is a HTML file.
* `blogger`: input file is a Blogger XML Export file.

Results
-------

* `[---]`: the url hasn't been checked.
* `[xxx]`: where the xxx is the HTTP status code.
* `[###]`: means the fragment in the URL can't be found in the response body in format of `id="<fragment>"`.
* `[SCH]`: unsupported HTTP scheme.
* `[SKP]`: the url is skipped.
* `[RRR]`: the url results reaching maximal redirection limit.
* `[UKN]`: unknown error.
* `[000]`: timeout when trying to check the url.

License
-------

    Copyright (C) 2013 by Yu-Jie Lin
