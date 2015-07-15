# Copyright (C) 2013 by Yu-Jie Lin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


try:
  from StringIO import StringIO
except ImportError:
  from io import StringIO

from lnkckr.checkers.blogger import Checker
from test_lnkckr_checkers_base import H, BaseCheckerTestCase


# encoding declaration in "<?xml version="1.0" encoding="UTF-8"?>" results in
#
#   ValueError: Unicode strings with encoding declaration are not supported.
#
# see http://lxml.de/parsing.html#python-unicode-strings
XML1 = '''<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <category scheme="http://schemas.google.com/g/2005#kind"
              term="http://schemas.google.com/blogger/2008/kind#post"/>
    <content type="html">%s</content>
    <link rel="alternate" type="text/html" href="%s" title="test"/>
  </entry>
</feed>'''


class BloggerCheckerTestCase(BaseCheckerTestCase):

  def setUp(self):

    self.checker = Checker()
    self.checker.do_update = lambda url, link: None

  # =====

  def test_process_local_fragment(self):

    checker = self.checker
    frag = 'test-id'
    content = '&lt;a href=&quot;#%s&quot;&gt;foobar&lt;/a&gt;' % frag
    url = H + '2013/01/test.html'
    xml = XML1 % (content, url)
    checker.process(StringIO(xml))
    expect = {
      url + '#' + frag: {
        'status': None,
        'posts': [url],
      }
    }
    self.assertEqual(checker.links, expect)

  def test_process_local_blank_fragment(self):

    checker = self.checker

    content = '&lt;a href=&quot;#&quot;&gt;foobar&lt;/a&gt;'
    url = H + '2013/01/test.html'
    xml = XML1 % (content, url)
    checker.process(StringIO(xml))
    self.assertEqual(checker.links, {})

    url = H + '2013/01/test.html'
    content = '&lt;a href=&quot;%s&quot;&gt;foobar&lt;/a&gt;' % (url + '#')
    xml = XML1 % (content, url)
    checker.process(StringIO(xml))
    self.assertEqual(checker.links, {})
