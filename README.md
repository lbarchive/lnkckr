lnkckr
======

**lnkckr** is a link checking library with command-line script `linkcheck`. It's intended to be used to check broken links and it can be interrupted at any time, then resumes from saved JSON file.

It supports Python 2.7 and Python 3.

Installation
------------

    pip install lnkckr

Usage
-----

    linkcheck [-c CHECKER] [-u|--update] [-f FILE] [-j JSON] [-s STATUS]

* `CHECKER` is what checker used to process `FILE`.
* `-u` or `--update` instructs lnkckr to update the JSON with input file. Normally, when `-j JSON` presents, lnkckr ignore the input file.
* `FILE` is the input filename or URL.
* `JSON` is the filename of saved progress file. If the `FILE` is a filename, then `FILE` can be omitted, an filename is assigned automatically unless using different filename is desired.
* `STATUS` indicates re-check url with specific status.

Here is a sample:

![Using lnkckr to check a Blogger XML Export file](https://lh5.googleusercontent.com/-JBBe-HVH_0M/URuaB0yeZHI/AAAAAAAAEc8/E6O7uL9gmJI/s800/lnkckr-blogger.png)

Checkers
--------

* `list`: input file is a list of links, one URL per line.
* `html`: input file is a HTML file.
* `blogger`: input file is a Blogger XML Export file.

Results
-------

* `[---]`: the url hasn't been checked.
* `[???]`: where the `???` is the HTTP status code.
* `[###]`: means the fragment in the URL can't be found in the response body in format of `id="<fragment>"` or `name="<fragment>"`.
* `[SCH]`: unsupported HTTP scheme.
* `[SKP]`: the url is skipped.
* `[RRR]`: the url results reaching maximal redirection limit.
* `[XXX]`: unknown error.
* `[000]`: timeout when trying to check the url.

Note
----

The output of lnkckr is similar to my two-year-old shell script `linkckr.sh`, I have also included it in the repository since lnkckr is kind of continuation of `linkckr.sh`, here is a [blog post about it](http://blog.yjl.im/2011/02/link-checker-bash-script-using-xmllint.html).

Related links
-------------

* [bea][]: Blogger Export Analyzer, not directly related, but also uses the Blogger XML Export file.
* [announcement][]: the blog post of lnkckr. 
* [b.py][]: Command-line posting script, it uses lnkckr to check links.

[bea]: https://bitbucket.org/livibetter/bea
[announcement]: http://blog.yjl.im/2013/02/checking-broken-links-with-blogger-xml.html
[b.py]: https://bitbucket.org/livibetter/b.py

License
-------

    lnkckr is licensed under the MIT License, see COPYING.
    Copyright (C) 2013 by Yu-Jie Lin
