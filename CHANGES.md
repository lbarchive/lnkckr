CHANGES
=======

## Development

 * [blogger] skip scheduled posts because of no post URLs

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
