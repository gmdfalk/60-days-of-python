#!/usr/bin/env python
"""A webcrawler using asyncio, written by Guido van Rossum, slightly adapted

Usage:
  crawl.py [-h] [--iocp] [--select] [--max-redirect N] [--max-tries N]
           [--max-tasks N] [--max-pool N] [--exclude REGEX] [--strict]
           [--lenient] [-v N] [-q]
           <root>...

Arguments:
  root    Root URL (may be repeated)

Options:
  -h, --help        show this help message and exit
  --iocp            Use IOCP event loop (Windows only)
  --select          Use Select event loop instead of default
  --max-redirect N  Limit redirection chains (for 301, 302 etc.) [default: 10]
  --max-tries N     Limit retries on network errors [default: 4]
  --max-tasks N     Limit concurrent connections [default: 100]
  --max-pool N      Limit connection pool size [default: 100]
  --exclude REGEX   Exclude matching URLs
  --strict          Strict host matching (default)
  --lenient         Lenient host matching
  -v, --verbose N   Verbose logging (0-3) [default: 1]
  -q, --quiet       Quiet logging
"""

from docopt import docopt
import asyncio
import logging
import sys
import crawling
import reporting


def fix_url(url):
    """Prefix a schema-less URL with http://."""
    if "://" not in url:
        url = "http://" + url
    return url


def main():
    "Parse arguments, set up event loop, run crawler and print a report."

    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    if args["--quiet"]:
        logging.basicConfig(level=levels[0])
    else:
        logging.basicConfig(level=levels[int(args["--verbose"])])

    # Not sure how to set --strict to True by default with docopts. So this is
    # where we handle strict vs lenient.
    if args["--lenient"]:
        args["--strict"] = False
    else:
        args["--strict"] = True

    if args["--iocp"]:
        from asyncio.windows_events import ProactorEventLoop
        loop = ProactorEventLoop()
        asyncio.set_event_loop(loop)
    elif args["--select"]:
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    # Set comprehension to avoid redundancy.
    roots = {fix_url(root) for root in args["<root>"]}

    # Instantiating the crawler with our arguments.
    crawler = crawling.Crawler(roots,
                               exclude=args["--exclude"],
                               strict=args["--strict"],
                               max_redirect=int(args["--max-redirect"]),
                               max_tries=int(args["--max-tries"]),
                               max_tasks=int(args["--max-tasks"]),
                               max_pool=int(args["--max-pool"])
                               )

    # "And this is where the magic happens."
    try:
        loop.run_until_complete(crawler.crawl())
    except KeyboardInterrupt:
        sys.stderr.flush()
        print('\nInterrupted\n')
    finally:
        reporting.report(crawler)
        crawler.close()
        loop.close()


if __name__ == "__main__":
    args = docopt(__doc__, version="0.1")
    main()
