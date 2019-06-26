from random import choice
import json
from pprint import pprint
import pandas as pd

import requests
from bs4 import BeautifulSoup

_user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']


class InstagramScraper:

    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def __request_url(self, url):
        with open('non_existent.txt', 'w') as wr:
            try:
                response = requests.get(url, headers={'User-Agent': self.__random_agent()}, proxies={'http': self.proxy,
                                                                                                 'https': self.proxy})
                response.raise_for_status()
            except requests.HTTPError:
                wr.write('Received non 200 status code from Instagram for: ')
                wr.write(url)
                wr.write('\n')
                # raise requests.HTTPError('Received non 200 status code from Instagram')
            except requests.RequestException:
                raise requests.RequestException
            else:
                return response.text

    @staticmethod
    def extract_json_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def profile_page_metrics(self, profile_url):
        results = {}
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                        results[key] = value
                    elif value:
                        results[key] = value
        return results

    def get_single_posts(self, post_url):
        results = []
        response = self.__request_url(post_url)
        if response is None:
            return
        json_data = self.extract_json_data(response)

        post_text = \
        json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0][
            'node']['text']
        post_shortcode = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['shortcode']

        results.append(post_text)

        return results

    def profile_page_recent_posts(self, profile_url):
        results = []
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
                "edges"]
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results

"""
k = InstagramScraper()
results = k.get_single_posts('https://www.instagram.com/p/Bc8Zsihhp5A/?taken-by=tradedny')
print(results)
with open('json_log.txt', 'w') as json_log:
    json.dump(results, json_log)

"""

count = 727

with open('links_info.txt') as links_info:
    with open('posts_info.txt', 'w', encoding="UTF-8") as posts_info:
        with open('non_existent.txt', 'w') as non_existent:
            k = InstagramScraper()
            for line in links_info:
                count += 1
                results = k.get_single_posts(line)
                if results is None:
                    non_existent.write("Deal: ")
                    non_existent.write(str(count))
                    non_existent.write("\n")
                    non_existent.write('Received non 200 status code from Instagram for: ')
                    non_existent.write(line)
                    non_existent.write('\n')
                    continue
                for entry in results:
                    posts_info.write('Deal: ')
                    posts_info.write(str(count))
                    posts_info.write('\n')
                    posts_info.write(str(entry))
                    posts_info.write('\n')
                    posts_info.write('LINK: ')
                    posts_info.write(line)
                    posts_info.write('\n\n')

