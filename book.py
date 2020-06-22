# -*- coding: utf-8 -*-

import requests
import time
import random
import json
import pyodbc
from bs4 import BeautifulSoup

# book = {
#     'id': '',
#     'title': '',
#     'pic': '',
#     'author': '',
#     'rating': '',
#     'content_intro': '',
#     'tag': ''
# }

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
}


def run():
    for url in open('url.txt', 'r', encoding='utf-8'):
        try:
            r = requests.get(url.rstrip('\n'), headers=headers, timeout=(3,7))
        except requests.exceptions.ConnectionError as e:
            print("连接超时")
        print(time.strftime('%Y-%m-%d %H:%M:%S'))

        if(r.status_code == 200):
            id = url[32:-2]
            print(id)
            get_html(r, id)
            time.sleep(random.uniform(3, 4))

def download_image(url, id):
    try:
        r = requests.get(url, headers=headers,  timeout=(3,7))
    except requests.exceptions.ConnectionError as e: 
        print("图片下载超时")

    path = 'pic/' + str(id) + '.jpg'
    if r.status_code == 200:
        open(path, 'wb').write(r.content)
        return True
    else:
        return False

def get_title(soup):
    if soup.find('h1').find('span') != None:
        return soup.find('h1').find('span').text
    else:
        return ''

# def get_image(soup):
#     if soup.find('a', 'nbg').get('href') != None:
#         return soup.find('a', 'nbg').get('href')
#     else:
#         return ''

def get_author(soup):
    if soup.find('div', id='info').find('a') != None:
        return soup.find('div', id='info').find('a').text.replace('\n', '').replace('\r', '').replace(' ','')
    else:
        return ''

def get_content_intro(soup):
    if soup.find('div', class_='intro') != None:
        return soup.find('div', class_='intro').text
    else:
        return ''

def get_tag(soup):
    tag = ''
    if soup.find('div', id='db-tags-section') != None:
        for item in soup.find('div', id='db-tags-section').find_all('a'):
            tag += item.text + '\n'
        return tag
    else:
        return ''

def get_html(r, id):
    soup = BeautifulSoup(r.text, 'lxml')

    id = id

    title = get_title(soup)

    img_url = soup.find('a', 'nbg').get('href')
    if(download_image(img_url, id)):
        pic = 'pic/' + str(id) + '.jpg'
    else:
        pic = ''

    author = get_author(soup)
    
    rating = soup.find('div', class_='rating_self clearfix').find('strong').text.strip()

    content_intro = get_content_intro(soup)

    tag = get_tag(soup)

    print(get_book(id, title, pic, author, rating, content_intro, tag))
    # write_json(get_book(id, title, pic, author, rating, content_intro, tag))
    sql_insert(get_book(id, title, pic, author, rating, content_intro, tag))

def get_book(id, title, pic, author, rating, content_intro, tag):
    book = {
        "id": id,
        "title": title,
        "pic": pic,
        "author": author,
        "rating": rating,
        "content_intro": content_intro,
        "tag": tag
    }
    return book

def write_json(book):
    with open('db.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(book, ensure_ascii=False) + ',')

def sql_insert(book):
    db = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-8359RE3I\SQLEXPRESS;DATABASE=BooksRecommendedSys;UID=sa;PWD=1234')

    cursor = db.cursor()

    insert_sql = "insert into Books(id, title, pic, author, rating, content_intro, tag) values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')"

    cursor.execute(insert_sql.format(book["id"], book["title"], book["pic"], book["author"], book["rating"], book["content_intro"], book["tag"]))

    db.commit()
    db.close()


run()
