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


def headers(soup):
  header3 = soup.find('h3')
  if header3:
    header3 = header3.get_text()
  header4 = soup.find('h4')
  if header4:
    header4 = header4.get_text()
  #header4 = soup.find_all('h4')
  #if header4[1]:
    #header4 = str(header4[1])
    #match = re.search('<h4>([\w\s\(\)-,]+)<div', header4)
    #header4 = match.group(1)
  if header3 and header4:
    header = header3 + '\n' + header4
  elif header3 and not header4:
    header = header3
  elif header4 and not header3:
    header = header4
  else:
    header = 'no header'
  return header



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
  rating = re.search('<span>([-\.\w]+)<div', rating_el).group(1)
  return rating


def user(soup):
  user_el = str(soup.find("a", {"class" : "offline_username"}))
  username = re.search('">([\w]+)</a>', user_el).group(1)
  return username


def download_images(img_urls, foldername):
  path = os.path.abspath(foldername)
  for img in img_urls:
    match = re.findall('/([\.\w-]+)', img)[-1]
    print(match)
    filename = os.path.join(path, match)
    urllib.request.urlretrieve(img, '{!s}'.format(filename))




def create_dir_txt(username, rating, header, tagnames):
  foldername = username + ' ' + rating
  if not os.path.isdir(foldername):
    os.mkdir(foldername)
  path = os.path.abspath(foldername)
  txt = open(os.path.join(foldername, header + ".txt"), "a")
  txt.write(tagnames)
  txt.close()
  return foldername



def get_otherinfo(first_list):
  # ratings and uploader names
  print(len(first_list))
  for l in first_list:
    soup = bs4.BeautifulSoup(l, 'html.parser')

    header = headers(soup)
    username = user(soup)
    rating = rate(soup)
    tagnames = tags(soup)
    img_urls = imgs(soup)

    print(username)
    print(rating)
    print(tagnames)
    # print(img_urls)
    print(header)

    # create folders and txt files
    foldername = create_dir_txt(username, rating, header, tagnames)
  
    download_images(img_urls, foldername)



def parse_data(data):
  first_list = data.split('class="post_top"')[1:]
  first_list[-1] = str(first_list[-1].split('id="Pagination"')[:1])
  get_otherinfo(first_list)




def main():
  r = requests.get('http://thatpervert.com/tag/porn%2Bcomics')
  print('got the contents')
  data = r.text
  print(type(data))
  links = parse_data(data)


if __name__ == '__main__':
  main()
