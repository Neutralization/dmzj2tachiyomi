# -*- coding: utf-8 -*-

import json
import re
import time
import tkinter as tk
from threading import Thread
from tkinter import messagebox, ttk
from typing import Generator

import requests
from lxml import etree


class transfer(object):
    def hisSubscribe(self, page) -> Generator:
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
            title = x.xpath('./dd/a[@class="title"]/text()')[0]
            comicid = x.xpath('./dd/a[@class="addSubBtn dread_btn"]/@onclick')[0]
            comicid = re.findall(r'\d+', comicid)[0]
            print(comicid)
            cover = x.xpath('./dt/a/img/@src')[0]
            yield (comicid, title, cover)

    def turnPage(self):
        p = 1
        self.comicList = []
        while True:
            try:
                self.comicList += [
                    {
                        "id": comic[0],
                        "title": comic[1],
                        "cover": comic[2]  # Comic 必须要此字段
                    } for comic in self.hisSubscribe(p)
                ]
            except ValueError:
                break
            p += 1

    def check(self, dist):
        self.comicSourceID = self.sourceIDBox.get()
        self.uid = self.userIDBox.get()
        if not self.uid.isdigit():
            messagebox.showwarning(u'ERROR', u'无效的用户ID')
            return None
        favorite = round(time.time()) * 1000  # Comic 必须要此字段
        if dist == 1:
            if not self.comicSourceID.isdigit():
                messagebox.showwarning(u'ERROR', u'无效的源ID')
                return None
            self.turnPage()
            comicList = [{
                "manga": [
                    f"/comic/comic_{comic['id']}.json?version=2.7.019",
                    comic['title'], self.comicSourceID, 0, 0
                ]
            } for comic in self.comicList]
            backup = {
                "version": 2,
                "mangas": comicList,
                "categories": [],
                "extensions": [f"{self.comicSourceID}:动漫之家"]
            }
            with open(f'Tachiyomi-{favorite}.json', 'w',
                      encoding='utf-8-sig') as f:
                json.dump(backup, f, ensure_ascii=False)
            messagebox.showwarning(u'FINISH',
                                   f'已导出文件 Tachiyomi-{favorite}.json')
        elif dist == 2:
            self.turnPage()
            comicList = [{
                "source": 10,
                "cid": f"{comic['id']}",
                "title": f"{comic['title']}",
                "cover": f"{comic['cover']}",
                "finish": False,
                "favorite": favorite
            } for comic in self.comicList]
            backup = {
                "version": 1,
                "comic": comicList,
            }
            with open(f'Cimoc-{favorite}.cfbf', 'w',
                      encoding='utf-8-sig') as f:
                json.dump(backup, f, ensure_ascii=False,
                          separators=(',', ':'))  # Comic 备份文件不能有换行和空格
            messagebox.showwarning(u'FINISH', f'已导出文件 Cimoc-{favorite}.cfbf')

    def run(self, dist):
        task = Thread(target=self.check, args=(dist, ))
        task.setDaemon(True)
        task.start()

    def __init__(self):
        window = tk.Tk()
        window.title("dmzj -> Tachiomi/Cimoc")
        window.resizable(False, False)
        mainFrame = ttk.LabelFrame(window, width=200, text='主界面')
        mainFrame.grid(column=0, row=0)
        ttk.Label(mainFrame, text='Tachiyomi 图源ID').grid(column=0, row=0)
        self.sourceIDBox = tk.StringVar()
        sourceIDBox_entered = ttk.Entry(mainFrame,
                                        width=20,
                                        textvariable=self.sourceIDBox)
        sourceIDBox_entered.grid(column=1, row=0)

        ttk.Label(mainFrame, text='动漫之家 用户ID').grid(column=0, row=1)
        self.userIDBox = tk.StringVar()
        userIDBox_entered = ttk.Entry(mainFrame,
                                      width=20,
                                      textvariable=self.userIDBox)
        userIDBox_entered.grid(column=1, row=1)

        RunButton = ttk.Button(mainFrame,
                               text='Tachiyomi',
                               command=lambda: self.run(1))
        RunButton.grid(column=2, row=0)
        RunButton = ttk.Button(mainFrame,
                               text='Cimoc',
                               command=lambda: self.run(2))
        RunButton.grid(column=2, row=1)
        window.mainloop()


if __name__ == "__main__":
    transfer()
