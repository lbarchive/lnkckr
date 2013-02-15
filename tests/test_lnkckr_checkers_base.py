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
  from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
  from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
try:
  from StringIO import StringIO
except ImportError:
  from io import StringIO
import json
from multiprocessing import Process, Value
import re
import unittest

from lnkckr.checkers.base import Checker


HOST = 'localhost'
PORT = 8000
H = 'http://%s:%s/' % (HOST, PORT)


class Handler(BaseHTTPRequestHandler):

  RE_CODE = re.compile(r'/(\d{3})')

  def do_GET(self):

    # counting the requests
    self.server.requests.value += 1
    redir = H
    m = self.RE_CODE.match(self.path)
    if m:
      code = int(m.group(1))
    elif self.path == '/':
      code = 200
    elif self.path == '/loop':
      code = 302
      redir = '/loop'
    else:
      code = 404

    self.send_response(code)
    if code in (301, 302):
      self.send_header('Location', redir)
    else:
      self.send_header("Content-Type", "text/html")
    self.end_headers()

    if code == 200:
      data = self.headers.get('X-Echo')
      if data:
        self.wfile.write(data.encode('utf8'))

  def do_HEAD(self):

    self.do_GET()

  def log_message(self, *args):

    pass


def run_httpd(running, requests):

  httpd = HTTPServer((HOST, PORT), Handler)
  httpd.requests = requests
  httpd.requests.value = 0
  httpd.timeout = 0.01
  while running.value:
    httpd.handle_request()


class BaseCheckerTestCase(unittest.TestCase):

  @classmethod
  def setUpClass(self):

    self.httpd_running = Value('b', 1)
    self.httpd_requests = Value('L', 1)
    args = (self.httpd_running, self.httpd_requests)
    self.httpd_process = Process(target=run_httpd, args=args)
    self.httpd_process.start()

  @classmethod
  def tearDownClass(self):

    self.httpd_running.value = 0
    self.httpd_process.join()

  def setUp(self):

    self.checker = Checker()
    self.checker.do_update = lambda url, link: None

  def tearDown(self):

    self.checker = None

  def test_init(self):

    self.assertEqual(self.checker.links, {})

  # =====

  def test_load_json(self):

    checker = self.checker

    links = {'http://example.com': {'status': None, 'data': 'foobar'}}
    src = StringIO(json.dumps(links))
    checker.load_json(src)
    self.assertEqual(checker.links, links)

  def test_save_json(self):

    checker = self.checker
    links = {'http://example.com': {'status': None, 'data': 'foobar'}}
    checker.add_link('http://example.com', {'data': 'foobar'})
    dest = StringIO()
    checker.save_json(dest)
    self.assertEqual(dest.getvalue(), json.dumps(links))

  # =====

  def test_update_links(self):

    checker = self.checker
    checker.add_link('http://example.com', {'data': 'foobar'})
    checker.update_links({})
    self.assertEqual(checker.links, {})

    new_links = {'http://example.com/': {'status': None, 'data': 'blah'}}
    checker.update_links(new_links)
    self.assertEqual(checker.links, new_links)

    new_links = {'http://example.com/': {'status': 123, 'data': 'duh'}}
    expect = {'http://example.com/': {'status': None, 'data': 'duh'}}
    checker.update_links(new_links)
    self.assertEqual(checker.links, expect)

    checker.update_links(new_links, update_status=True)
    self.assertEqual(checker.links, new_links)

  # =====

  def test_check(self):

    checker = self.checker

    checker.add_link(H + '200')
    checker.check()
    expect = {H + '200': {'status': '200', 'redirection': None}}
    self.assertEqual(checker.links, expect)

    checker.add_link(H + '200')
    checker.add_link(H + '301')
    checker.check(lambda item: item[0].endswith('301'))
    expect = {
      H + '200': {
        'status': None,
      },
      H + '301': {
        'status': '200',
        'redirection': H,
      },
    }
    self.assertEqual(checker.links, expect)

  def test_check_max_redirection(self):

    checker = self.checker

    checker.add_link(H + 'loop')
    checker.check()
    expect = {H + 'loop': {'status': 'RRR', 'redirection': H + 'loop'}}
    self.assertEqual(checker.links, expect)

  def test_check_fragment(self):

    checker = self.checker

    checker.add_link(H + '200#foobar')
    checker.HEADERS['X-Echo'] = '<h1 id="foobar">blah</h1>'
    checker.check()
    expect = {H + '200#foobar': {'status': '200', 'redirection': None}}
    self.assertEqual(checker.links, expect)

  def test_check_fragment_missing(self):

    checker = self.checker

    checker.add_link(H + '200#foobar')
    checker.HEADERS['X-Echo'] = '<h1>blah</h1>'
    checker.check()
    expect = {H + '200#foobar': {'status': '###', 'redirection': None}}
    self.assertEqual(checker.links, expect)

  def test_check_fragments(self):
    """Test same url with different fragments and only make HTTP request
    once.
    """
    checker = self.checker

    req_count = self.httpd_requests.value
    checker.add_link(H + '200#foobar')
    checker.add_link(H + '200#foobar1')
    checker.HEADERS['X-Echo'] = '<h1 id="foobar">blah</h1>'
    checker.check()

    expect = {
      H + '200#foobar': {'status': '200', 'redirection': None},
      H + '200#foobar1': {'status': '###', 'redirection': None},
    }
    self.assertEqual(checker.links, expect)
    self.assertEqual(self.httpd_requests.value, req_count + 1)
