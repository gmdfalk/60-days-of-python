Web Crawler
==================

Okay, so i've cheated a bit with this one as this web crawler is written by Guido van Rossum  
but it seemed like a great opportunity to study idiomatic code and some interesting  
new features of Python 3.4 (concurrency in web requests, yield from and others).  
I modified it to use docopts instead of argparse and am adding some commentary.  
Other modifications could be:
  * BeautifulSoup instead of regex for parsing 
  * requests (urllib3) instead of urllib for http actions

You can find the original [here](https://github.com/aosabook/500lines/tree/master/crawler).  
  
[This](https://github.com/mikar/60-days-of-code/tree/master/oop/datastructs/scraping) is the first draft, which lead me to look at more optimized versions of web scrapers.