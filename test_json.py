import json



def exec(id, title, pic, author, rating, content_intro, tag):
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

with open('db.json', 'a', encoding='utf-8') as f:
    f.write(json.dumps(exec(1,2,3,4,5,6,7)) + ',')