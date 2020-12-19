#!/usr/bin/env python3
import argparse
import json

from bs4 import BeautifulSoup
import re
import sys
from dateutil import parser as dateparser
import time

# Grequests needs to be monkey patched to not infinitely recure on SSL
from gevent import monkey as curious_george

curious_george.patch_all(thread=False, select=False)

import requests
import grequests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from dataclasses import dataclass

FORUMS_URL_PATTERN = re.compile(
    r"^(https://secure\.runescape\.com/m=forum/forums\?\d{2,3},\d{2,3},\d{3},\d{8})(?:,goto,\d+)?$"
)
FORUMS_QFC_PATTERN = re.compile(r"^\d{2,3}-\d{2,3}-\d{3}-\d{8}$")
LAST_EDIT_PATTERN = re.compile(r"^- Last edited on (.+) by .+$")
POSTS_PER_PAGE = 10


@dataclass
class FetchCounter:
    total: int
    quiet: bool
    counter: int = 0

    def feedback(self, r, **kwargs):
        self.counter += 1
        if not self.quiet:
            print(
                f"[{self.counter}/{self.total}] - Fetched page {r.url.split(',')[-1]}",
                file=sys.stderr,
                end="\r",
            )
        return r


def exception_handler(request, exception):
    print(exception, file=sys.stderr)


def qfc_to_url(qfc):
    return f"https://secure.runescape.com/m=forum/forums?{qfc.replace('-', ',')}"


def grab_posts_from_page(pageidx, page):
    posts = page.findAll("article")
    result = []
    for idx, post in enumerate(posts):
        created, lastedited = extract_post_timeinfo(post)
        p = {
            "id": POSTS_PER_PAGE * pageidx + idx,
            "page": pageidx + 1,
            "poster": extract_poster(post),
            "message": extract_post_message(post),
            "created": created,
            "lastedited": lastedited,
        }
        result.append(p)

    return result


def extract_post_message(post):
    message = post.find("span", {"class": "forum-post__body"})

    for br in message.find_all("br"):
        # Jagex wraps some messages with <br> for some reason
        if not br.isSelfClosing:
            br.unwrap()
        else:
            br.replace_with("\n")
    # Remove trailing whitespace
    content = message.get_text()
    clean_content = "\n".join((line.strip() for line in content.split("\n")))
    # When you quote a message Jagex encodes nbsp in names as \u00a0 instead of the normal %A0
    return clean_content.replace("\u00a0", " ")


def extract_poster(post):
    name = post.find("h3", {"class": "post-avatar__name"})
    if name is not None:
        # Jagex uses &nbsp for player names
        return name["data-displayname"].replace("%A0", " ")
    return None


def extract_post_timeinfo(post):
    timeinfo = post.find("p", {"class": "forum-post__time-below"})
    if timeinfo is None:
        return None, None

    times = timeinfo.get_text().strip().split("\n")

    created = dateparser.parse(times[0]).isoformat()
    if len(times) == 1:
        return created, None

    m = LAST_EDIT_PATTERN.match(times[1])
    if m:
        last_updated = dateparser.parse(m.group(1)).isoformat()
    else:
        last_updated = None

    return created, last_updated


def rsforums_thread(arg_value):
    urlmatch = FORUMS_URL_PATTERN.match(arg_value)
    if urlmatch:
        return urlmatch.group(1)
    elif FORUMS_QFC_PATTERN.match(arg_value):
        return qfc_to_url(arg_value)
    raise argparse.ArgumentTypeError("thread must be either forum thread url or qfc")


def main():
    parser = argparse.ArgumentParser(description="dump an RSforums thread to json")
    parser.add_argument(
        "thread",
        action="store",
        type=rsforums_thread,
        help="the forums url or qfc to dump",
    )
    parser.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help="do not display output"
    )
    parser.add_argument(
        "-o",
        "--output-file",
        dest="outfile",
        action="store",
        help="output result to a file",
    )
    parser.add_argument(
        "-w",
        "--workers",
        action="store",
        dest="workers",
        type=int,
        default=4,
        help="set the amount of workers to fetch webpages",
    )
    parser.add_argument(
        "-i",
        "--indent",
        action="store",
        dest="indent",
        type=int,
        default=None,
        help="set the indentation of the json output",
    )

    args = vars(parser.parse_args())

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0",
    }

    response = requests.get(args["thread"], headers=headers)

    if response.status_code != 200:
        response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    not_found = soup.find("p", {"class": "forum-error"})

    incapsula_limited = soup.find("iframe")

    if incapsula_limited:
        raise ValueError(f'You are being limited by incapsula')

    if not_found:
        raise ValueError(f'The thread {args["thread"]} cannot be found')

    page_select = soup.find("input", {"class": "forum-pagination__input-number"})
    n_pages = 1

    if page_select is not None:
        n_pages = int(page_select["max"])

    thread_title = soup.find("h2", {"class": "thread-view__heading"})

    if thread_title is not None:
        thread_title = thread_title.get_text()
    if not args["quiet"]:
        print(f"Found thread with {n_pages} page(s) and topic \"{thread_title}\"", file=sys.stderr)
        start = time.time()

    urls = [f"{args['thread']},goto,{pagenum}" for pagenum in range(1, n_pages + 1)]

    fetch_counter = FetchCounter(n_pages, args["quiet"])
    s = requests.Session()
    retries = Retry(
        total=10,
        backoff_factor=0.2,
        status_forcelist=[500, 502, 503, 504],
        raise_on_redirect=True,
        raise_on_status=True,
    )
    s.mount("http://", HTTPAdapter(max_retries=retries))
    s.mount("https://", HTTPAdapter(max_retries=retries))
    rs = (
        grequests.get(u, headers=headers, callback=fetch_counter.feedback, session=s)
        for u in urls
    )

    reqs = grequests.map(rs, size=args["workers"], exception_handler=exception_handler)

    pages = (BeautifulSoup(r.content, "html.parser") for r in reqs if r is not None)

    if not args["quiet"]:
        print(f"Grabbing data from pages...", file=sys.stderr)

    threadposts = []
    for pageidx, page in enumerate(pages):
        if not args["quiet"]:
            print(
                f"[{pageidx}/{n_pages}] - Extracting posts from page {pageidx}",
                file=sys.stderr,
                end="\r",
            )
        threadposts += grab_posts_from_page(pageidx, page)

    info = {
        "thread": args["thread"],
        "qfc": args["thread"].split("?")[-1].replace(",", "-"),
        "title": thread_title,
        "pagecount": n_pages,
        "postcount": len(threadposts),
        "posts": threadposts,
    }

    if not args["quiet"]:
        print(
            f"Dumped {n_pages} pages with {len(threadposts)} posts in {time.time()-start:.1f} seconds",
            file=sys.stderr,
        )

    outfile = args["outfile"]
    if outfile is None:
        print(json.dumps(info, indent=args["indent"]))
    else:
        with open(outfile, "w") as out:
            json.dump(info, out, indent=args["indent"])


if __name__ == "__main__":
    main()
