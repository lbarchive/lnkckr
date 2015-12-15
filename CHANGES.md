CHANGES
=======

## Development

* [base] really fix CPU hogging
* [base] add option `-U` (`--unverified-certificates`) for not verifying certifcates

## Version 0.3.0 (2015-07-31T23:18:21Z)

* [base] fix CPU hogging
* [base] fix fragment check, href=#frag can also be anchor
* [base] adjust URL quoting, only quote when there is `%` in URL
* [blogger] add `LNKCKR_BLOGGER_TOPLIST_LIMIT` to control the amount of listed entries
* [html] fix empty post content in Blogger XML causing `lxml.etree.XMLSyntaxError: line 1: b'Tag mn invalid'`
* [test] add empty content test

## Version 0.2.1 (2013-07-25T02:53:45Z)

* fix `all` option of `--status`.

## Version 0.2.0 (2013-06-11T22:53:15Z)

* add `-x` (`--exclude-status`) option for specifying excluded statuses from report section. (#2)

## Version 0.1.5 (2013-04-29T16:15:30Z)

* [base] fix query string getting quoted by mistake by e79523b
* [base] make HEADERS per instance not per class
* [test] introduce `X-MatchPath` to ensure path/querystring is correct

## Version 0.1.4 (2013-04-22T22:41:51Z)

 * [blogger] skip scheduled posts because of no post URLs
 * [base] fix encoding issue with URL with non-ISO-8859-1 characters in path

## Version 0.1.3 (2013-03-24T23:15:55Z)

 * add `--version` option
 * fix HTML unquoted attribute names for id and name matching

## Version 0.1.2 (2013-02-23T06:08:12Z)

 * [base] add `local_html` for checking local fragment
 * [html] use `local_html` to check local fragment
 * add `print_toplist` for a list of worse post/entry/etc
 * add HTML attribute `name` to search list of fragment and use regular expression to match
 * fix #1: url not checked when same url with fragment also being checked
 * url with fragment has return text/html type or it will be `[###]`
 * fragment now has to be valid ASCII or will not be found
 * add total numbers in summary

## Version 0.1.1 (2013-02-15T12:07:09Z)

 * add `--update` option to update JSON if input file is updated
 * urls with different fragments now only be checked once
 * ignore blank local fragment, i.e. url has only `#`
 * fix deadlock issue

## Version 0.1 (2013-02-13T13:18:32Z)

 * first version
