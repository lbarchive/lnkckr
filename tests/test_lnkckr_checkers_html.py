# Copyright (c) 2013, 2015 Yu-Jie Lin
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

from lnkckr.checkers.html import Checker
from test_lnkckr_checkers_base import BaseCheckerTestCase, H


class HTMLCheckerTestCase(BaseCheckerTestCase):

  def setUp(self):

    self.checker = Checker()
    self.checker.do_update = lambda url, link: None

  # =====

  def test_load(self):

    checker = self.checker

    codes = (H + '200', H + '403', H + '404')
    html = '\n'.join('<a href="%s">text</a>' % href for href in codes)
    src = StringIO(html)
    checker.load(src)
    expect = {
      H + '200': {'status': None},
      H + '403': {'status': None},
      H + '404': {'status': None},
    }
    self.assertEqual(checker.links, expect)

    checker.check()
    expect = {
      H + '200': {'status': '200', 'redirection': None},
      H + '403': {'status': '403', 'redirection': None},
      H + '404': {'status': '404', 'redirection': None},
    }
    self.assertEqual(checker.links, expect)

  # =====

  def test_local_html(self):

    checker = self.checker

    html = '<a href="#foo1">blah</a><span id="foo1">blah</span>'
    html += '<a href="#foo2">blah</a>'
    checker.process(StringIO(html))

    checker.check()
    expect = {
      '#foo1': {'status': '200', 'redirection': None},
      '#foo2': {'status': '200', 'redirection': None},
    }
    self.assertEqual(checker.links, expect)

  # =====

  def test_empty_html(self):

    checker = self.checker

    html = ''
    checker.process(StringIO(html))

    checker.check()
    expect = {}
    self.assertEqual(checker.links, expect)

    html = None
    checker.process(StringIO(html))

    checker.check()
    expect = {}
    self.assertEqual(checker.links, expect)
