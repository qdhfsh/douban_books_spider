import requests
from bs4 import BeautifulSoup


url = "https://book.douban.com/tag/?view=cloud"

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
    }

r = requests.get(url, headers = headers)

soup = BeautifulSoup(r.text, 'lxml')
tags = soup.find_all('td')

for tag in tags:
    with open('tag.txt', 'a', encoding='utf-8') as f:
        f.write(tag.text.split('(')[0] + '\n')