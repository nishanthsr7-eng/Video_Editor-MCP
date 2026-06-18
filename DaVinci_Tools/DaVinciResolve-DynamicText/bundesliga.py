#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# This module fetches the most recent Bundesliga headlines and places them in a
# crawl-ready string while keeping Unicode characters intact.

import requests
import xml.etree.ElementTree as ET


class Bundesliga(object):
    def __init__(self):
        # URL of Bundesliga news RSS feed
        self.url = 'https://www.dfb.de/news/rss/feed/?tx_news_pi1[overwriteDemand][categories]=10071'

    def get_RSS(self):
        return requests.get(self.url).text

    def get_headlines(self, rss):
        root = ET.fromstring(rss)

        # Find title items
        rssList = []
        for i in root.iter(tag='title'):
            if i.text:
                headline = ' '.join(i.text.split())
                rssList.append(headline)

        # Join into a string and strip off the word 'Feed' from the top
        whitespace = '      '
        headlineString = whitespace.join(rssList)[7:]
        # Remove quotes
        headlineString = ''.join(headlineString.split('"'))
        return headlineString


if __name__ == '__main__':
    football = Bundesliga()

    # RSS XML to string
    rss = football.get_RSS()

    # Parse xml and build crawl string
    crawl = football.get_headlines(rss)
    print(crawl)
