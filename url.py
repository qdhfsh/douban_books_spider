import requests
import time
import random
from bs4 import BeautifulSoup

def get_html(tag, start):
    url = "https://book.douban.com/tag/{0}?start={1}&type=T".format(tag, start)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
    }

    r = requests.get(url, headers = headers)

    if(r.status_code == 200):
        exec(r)
        time.sleep(random.uniform(2, 3))
        return True
    else:
        return False

def exec(r):
    soup = BeautifulSoup(r.text, 'lxml')
    subject_items = soup.find_all('li', 'subject-item')

    for item in subject_items:
        with open('url.txt', 'a', encoding='utf-8') as f:
            f.write(item.find('a', 'nbg').get('href') + '\n')

for tag in open('tag.txt', 'r', encoding='utf-8'):
    for num in range(0, 1000, 20):
        get_html(tag.rstrip("\n"), num)
        print(tag.rstrip("\n") + " " + str(num))


# print(random.uniform(1, 2))




