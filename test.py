import requests
import time
import random
import os
from bs4 import BeautifulSoup

url = 'https://book.douban.com/subject/6953273/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
}

# r = requests.get(url, headers = headers)

# soup = BeautifulSoup(r.text, 'lxml')

# c = soup.find('h1').find('span').text

# print(url[32:-1])

# os.mkdir('./pic/123')

# url = 'https://img9.doubanio.com/view/subject/l/public/s33639436.jpg'
# def download_image(url, path):
#     r = requests.get(url, headers=headers)
#     if r.status_code == 200:
#         open(path, 'wb').write(r.content)

# download_image(url, 'pic/' + str(123) + '.jpg')

# print(soup.find('div', id='info').find('a').text)

# print(soup.find('div', class_='rating_self clearfix').find('strong').text.strip())

# print(soup.find_all('div', class_='intro')[0].text)

# for tag in soup.find('div', id='db-tags-section').find_all('a'):
#     print(tag.text)

# print(soup.find('div', class_='rating_self clearfix'))

def download_image(url, id):
    r = requests.get(url, headers=headers,  timeout=(3,7))
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
        return soup.find('div', id='info').find('a').text
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
    write_txt(get_book(id, title, pic, author, rating, content_intro, tag))

def get_book(id, title, pic, author, rating, content_intro, tag):
    book = {
        'id': id,
        'title': title,
        'pic': pic,
        'author': author,
        'rating': rating,
        'content_intro': content_intro,
        'tag': tag
    },
    return book

def write_txt(book):
    with open('db.txt', 'a', encoding='utf-8') as f:
        f.write(str(book)[1:-1] + '\n')


r = requests.get(url.rstrip('\n'), headers=headers, timeout=(3,7))
get_html(r, 6953273)
