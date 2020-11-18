import json
import re

import requests
from lxml import etree

comicSourceID = 1234567890123456789
uid = 1


def hisSubscribe(page) -> set:
    data = {
        'page': page,
        'type_id': '1',
        'letter_id': '0',
        'hisUid': uid,
        'read_id': '1',
        'rightFlag': '1',
        'rightLevel': '1'
    }

    response = requests.post(
        'https://i.dmzj.com/otherCenter/ajaxGetHisSubscribe', data=data)
    result = etree.HTML(response.text)
    table = result.xpath('//dl')
    if len(table) <= 0:
        raise ValueError
    for x in table:
        title = ''.join(x.xpath('./dd/a[@class="title"]/text()'))
        comicid = ''.join(
            x.xpath('./dd/a[@class="addSubBtn dread_btn"]/@onclick'))
        comicid = ''.join(re.findall(r'\d+', comicid))
        yield (comicid, title)


def turnPage():
    p = 1
    comicList = []
    while True:
        try:
            comicList += [{
                "manga": [
                    f"/comic/comic_{comic[0]}.json?version=2.7.019", comic[1],
                    comicSourceID, 0, 0
                ]
            } for comic in hisSubscribe(p)]
        except ValueError:
            break
        p += 1

    backupData = {
        "version": 2,
        "mangas": comicList,
        "categories": [],
        "extensions": [f"{comicSourceID}:动漫之家"]
    }
    with open('dmzj2tachiyomi.json', 'w', encoding='utf-8-sig') as f:
        json.dump(backupData, f, ensure_ascii=False)


def main():
    turnPage()


if __name__ == "__main__":
    main()
