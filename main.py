# -*- coding: utf-8 -*-

import json
import re
import tkinter as tk
from threading import Thread
from tkinter import messagebox, ttk

import requests
from lxml import etree


class transfer(object):
    def hisSubscribe(self, page) -> set:
        data = {
            'page': page,
            'type_id': '1',
            'letter_id': '0',
            'hisUid': self.uid,
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

    def turnPage(self):
        p = 1
        comicList = []
        while True:
            try:
                comicList += [{
                    "manga": [
                        f"/comic/comic_{comic[0]}.json?version=2.7.019",
                        comic[1], self.comicSourceID, 0, 0
                    ]
                } for comic in self.hisSubscribe(p)]
            except ValueError:
                break
            p += 1

        backupData = {
            "version": 2,
            "mangas": comicList,
            "categories": [],
            "extensions": [f"{self.comicSourceID}:动漫之家"]
        }
        with open('dmzj2tachiyomi.json', 'w', encoding='utf-8-sig') as f:
            json.dump(backupData, f, ensure_ascii=False)

    def check(self):
        self.comicSourceID = self.sourceIDBox.get()
        self.uid = self.userIDBox.get()
        if self.comicSourceID.isdigit() and self.uid.isdigit():
            self.turnPage()
        else:
            messagebox.showwarning(u'ERROR', u'无效的源ID或用户ID')
            return None
        messagebox.showwarning(u'FINISH', u'已导出文件 dmzj2tachiyomi.json')

    def run(self):
        task = Thread(target=self.check)
        task.setDaemon(True)
        task.start()

    def __init__(self):
        window = tk.Tk()
        window.title("dmzj -> tachiomi")
        window.resizable(False, False)
        mainFrame = ttk.LabelFrame(window, width=200, text='主界面')
        mainFrame.grid(column=0, row=0)
        ttk.Label(mainFrame, text='Tachiyomi 图源ID').grid(column=0, row=0)
        self.sourceIDBox = tk.StringVar()
        sourceIDBox_entered = ttk.Entry(mainFrame,
                                        width=20,
                                        textvariable=self.sourceIDBox)
        sourceIDBox_entered.grid(column=1, row=0)

        ttk.Label(mainFrame, text='动漫之家 用户ID').grid(column=2, row=0)
        self.userIDBox = tk.StringVar()
        userIDBox_entered = ttk.Entry(mainFrame,
                                      width=20,
                                      textvariable=self.userIDBox)
        userIDBox_entered.grid(column=3, row=0)

        RunButton = ttk.Button(mainFrame, text='Start', command=self.run)
        RunButton.grid(column=4, row=0)
        window.mainloop()


if __name__ == "__main__":
    transfer()
