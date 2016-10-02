#!/usr/bin/env python
 
import requests
import urllib.parse
import urllib.request
import re
import time
import datetime
import os
import html
import logging
import traceback
import bs4


def imgs(soup):
  img_els = soup.find_all("img", src=True)[1:]
  img_urls = []
  for el in img_els:
    el = str(el)
    match = re.search('src="(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"', el)
    img_url = match.group(1)
    img_urls.append(img_url)
  return img_urls



def tags(soup):
  tag_els = soup.find_all("a", title=True)
  tagnames = ''
  for el in tag_els:
    tagnames = tagnames + el.get_text() + ', '
  return tagnames


def rate(soup):
  rating_el = str(soup.find("span", {"class" : "post_rating"}))
  rating = re.search('<span>([\.\w]+)<div', rating_el).group(1)
  return rating


def user(soup):
  user_el = str(soup.find("a", {"class" : "offline_username"}))
  username = re.search('">([\w]+)</a>', user_el).group(1)
  return username


def get_otherinfo(first_list):
  # ratings and uploader names
  print(len(first_list))
  astring = first_list[-2]
  soup = bs4.BeautifulSoup(astring, 'html.parser')

  username = user(soup)
  rating = rate(soup)
  tagnames = tags(soup)
  img_urls = imgs(soup)

  print(username)
  print(rating)
  print(tagnames)
  print(img_urls)



def parse_data(data):
  first_list = data.split('class="post_top"')[1:]
  first_list[-1] = str(first_list[-1].split('id="Pagination"')[:1])
  get_otherinfo(first_list)



  #otherinfo = get_otherinfo(first_list)
  #print(first_list)


def main():
  r = requests.get('http://thatpervert.com/tag/porn%2Bcomics')
  print('got the contents')
  data = r.text
  print(type(data))
  links = parse_data(data)
  #match = re.search('c[\w]', data)
  #print(match.group())


if __name__ == '__main__':
  main()
