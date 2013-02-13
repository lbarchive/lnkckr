#!/usr/bin/env python3
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


import argparse
import json
import http.client
from itertools import chain, groupby
from lxml import etree, html
import multiprocessing as mp
from multiprocessing import Process, Queue
from queue import Empty
from os import path
import socket
from urllib.parse import urljoin, urlparse, unquote


__program__ = 'BloggerLinkChecker'
__version__ = '0.1dev'

default_timeout = socket.getdefaulttimeout()
socket.setdefaulttimeout(10)

# User-Agent for some website like Wikipedia. Without it, most of requests
# result in 403.
HEADERS = {'User-Agent': '%s/%s' % (__program__.replace(' ', ''), __version__)}


def check_url(url):

  method = 'HEAD'
  original_url = unquote(url)
  status = ''

  while not status:
    if url.startswith('//'):
      url = 'http:' + url
    url_comp = urlparse(url)
    if url_comp.scheme == 'http':
      conn = http.client.HTTPConnection(url_comp.netloc)
    elif url_comp.scheme == 'https':
      conn = http.client.HTTPSConnection(url_comp.netloc)
    else:
      status = 'SCH'
      if url_comp.scheme in ('about', 'javascript'):
        status = 'SKP'
      break

    try:
      p = url_comp.path
      if url_comp.query:
        p += '?' + url_comp.query
      conn.request(method, p, headers=HEADERS)
      res = conn.getresponse()
      if 300 <= res.status < 400:
        url = urljoin(url, res.getheader('location'))
        method = 'HEAD'
      elif res.status == 405 and method == 'HEAD':
        method = 'GET'
      else:
        status = str(res.status)
      conn.close()
    except socket.error as e:
      status = '000'
    except Exception as e:
      print(e)
      status = 'UKN'

  if original_url == url:
    url = None
  return status, url


def check_worker(q, r):

  name = mp.current_process().name
  try:
    while True:
      link = q.get(timeout=1)
      r.put((link, check_url(link)))
  except (Empty, KeyboardInterrupt):
    pass
  print('%s done.' % name)


class BloggerLinkChecker():

  MAX_WORKERS = 10
  QUEUE_SIZE = 20
  SAVE_INT = 100

  def __init__(self, filename):

    self.filename = filename
    self.filename_json = filename_json = filename + '.json'

    if path.exists(filename_json):
      print('found json: ' + filename_json)
      with open(filename_json, 'r') as f:
        self.links = json.load(f)
    else:
      d = etree.parse(filename)
      self.set_links(d)
      self.save_json()

  def get_links(self, status=None):

    return list(link for link, data in self.links.items() if status == 'all' or status == data['status'])

  def set_links(self, d):

    SCHEME_KIND = "http://schemas.google.com/g/2005#kind"
    VALID_KINDS = ("http://schemas.google.com/blogger/2008/kind#post",
                   "http://schemas.google.com/blogger/2008/kind#page")
    NS = {'ns': 'http://www.w3.org/2005/Atom'}

    links = {}

    entries = d.xpath('//ns:feed/ns:entry', namespaces=NS)
    for entry in entries:
      kind = entry.find("ns:category[@scheme='%s']" % SCHEME_KIND, namespaces=NS)
      if kind.attrib.get('term') not in VALID_KINDS:
        continue

      content = entry.find('ns:content', namespaces=NS)
      post = html.fromstring(content.text)
      post_link = entry.find("ns:link[@rel='alternate']", namespaces=NS).attrib.get('href')
      for e in post.xpath('*[@href|@src]'):
        link = e.attrib.get('href') or e.attrib.get('src')
        if link not in links:
          links[link] = {'status': None, 'posts': []}
        if post_link not in links[link]['posts']:
          links[link]['posts'].append(post_link)
    self.links = links

  def save_json(self):

    with open(self.filename_json, 'w') as f:
      json.dump(self.links, f)
    print('%s saved.' % self.filename_json)

  def check(self, check_list):

    if not check_list:
      return

    print('Starting to check %d links with %d checkers...' % (len(check_list), self.MAX_WORKERS))
    q = Queue(self.QUEUE_SIZE)
    r = Queue(self.QUEUE_SIZE*2)
    workers = []
    for i in range(self.MAX_WORKERS):
      worker = Process(name='checker #%d' % i, target=check_worker, args=(q, r))
      worker.start()
      workers.append(worker)

    try:
      for idx, link in enumerate(check_list, start=1):
        q.put(link)
        self.update_links(r)
        if idx % self.SAVE_INT == 0:
          self.save_json()
      self.update_links(r)
    except KeyboardInterrupt:
      print('Interrupted')
    finally:
      for worker in workers:
        worker.join()
      self.update_links(r)
    self.save_json()

  def color_status(self, status):

    if status == '000':
      return '\033[1;36m[%s]\033[0m' % status
    if status == '200':
      return '\033[1;32m[%s]\033[0m' % status
    if status == 'SKP':
      return '\033[1;33m[%s]\033[0m' % status
    else:
      return '\033[1;31m[%s]\033[0m' % status

  def format_status(self, status, link, url):

    print('%s %s' % (self.color_status(status), link), end='')
    if url:
      print(' \033[1;33m->\033[0m %s' % url, end='')
    print()

  def update_links(self, r):

    while not r.empty():
      link, data = r.get(block=False)
      status, url = data
      self.links[link]['status'] = status
      self.links[link]['redirection'] = url
      self.format_status(status, link, url)

  def print_report(self):

    print('==========')
    print('* report *')
    print('==========')
    print()
    for link, data in self.links.items():
      status = data['status']
      if status in (None, '200', 'SKP'):
        continue
      self.format_status(status, link, data.get('redirection'))
      for post in data['posts']:
        print('  %s' % post)
      print()

    unchecked = sum(1 for link in self.links.values() if link['status'] is None)
    if unchecked:
      print('*** checking process is not finished, %d links have not been checked. ***' % unchecked)
      print()

  def print_summary(self):

    print('===========')
    print('* summary *')
    print('===========')
    print()

    key = lambda link: link['status'] or '---'
    for status, g in groupby(sorted(self.links.values(), key=key), key=key):
      links = list(g)
      nlinks = len(links)
      nposts = len(set(chain.from_iterable(link['posts'] for link in links)))

      print('%s %5d links from %5d posts' % (self.color_status(status), nlinks, nposts))


def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('xml', metavar='blog-MM-DD-YYYY.xml',
                      help='Exported XML file')
  parser.add_argument('-s', '--status',
                      help=('re-check links with status. '
                            'Valid values: all, HTTP status code'))
  args = parser.parse_args()

  checker = BloggerLinkChecker(args.xml)
  links = checker.links

  posts = set(chain.from_iterable(link['posts'] for link in links.values()))
  print('total: %d links from %d posts' % (len(links), len(posts)))
  print()

  check_list = checker.get_links(args.status)
  checker.check(check_list)
  print()
  checker.print_report()
  checker.print_summary()


if __name__ == '__main__':
  main()
