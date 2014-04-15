"""
    Created on 29 Mar 2014

    @author: Max Demian
"""

from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
import re
import sys


# FIXME: This regex catches e-mail addresses, too.
# negative lookahead: href=(?!mailto:) should exclude mails.
LINK_REGEX = re.compile("<a [^>]*href=['\"]([^'\"]+)['\"][^>]*>")


class LinkCollector(object):

    def __init__(self, url):
        self.url = "http://" + urlparse(url).netloc
        self.collected_links = {}
        self.visited_links = set()

    def collect_links(self, path="/"):
        full_url = self.url + path
        self.visited_links.add(full_url)
        page = str(urlopen(full_url).read())
        links = LINK_REGEX.findall(page)
        links = {self.normalize_url(path, link) for link in links}
        self.collected_links[full_url] = links
        for link in links:
            self.collected_links.setdefault(link, set())
        unvisited_links = links.difference(self.visited_links)
        # 404 will raise a HTTPError so we ignore those.
        try:
            for link in unvisited_links:
                if link.startswith(self.url):
                    self.collect_links(urlparse(link).path)
        except HTTPError:
            pass

    def normalize_url(self, path, link):
        if link.startswith("http://"):
            return link
        elif link.startswith("/"):
            return self.url + link
        else:
            return self.url + path.rpartition("/")[0] + "/" + link



if __name__ == "__main__":
    c = LinkCollector("http://localhost:8000")
    c.collect_links()
    for link, item in c.collected_links.items():
        print("{}: {}".format(link, item))

    # With LXML (python2 only) we could do somethiing like this:
#     from lxml import html
#     tree = html.parse(filename)
#     for element,attribute, link, pos in tree.getroot().iterlinks():
#         print link
    # Amazing, isn't it?
    # And for real scraping we would probably use BeautifulSoup and requests.