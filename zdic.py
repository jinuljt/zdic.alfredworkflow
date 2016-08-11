#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import requests
from bs4 import BeautifulSoup, Tag

from workflow import Workflow


def main(wf):
    if not wf.args:
        return

    word = wf.args[0].strip()
    resp = requests.post("http://www.zdic.net/sousuo/", data={"q": word})
    soup = BeautifulSoup(resp.content, "html.parser")
    #soup = BeautifulSoup(open("./test/%s.html"% word, "rb").read(), "html.parser")

    # 拼音, 拼音作为title用
    title= None
    pinyin = soup.find("span", attrs={"class": "dicpy"})
    if pinyin:
        title = pinyin.string
        if not title and pinyin.find("a"):
            title = pinyin.find("a").string

    if not title:
        title = word

    # 获取解释
    explain = None
    for py in soup.findAll("span", attrs={"class": "dicpy"}):
        p =  py.findParent()
        if p.name == "p" and p.attrs.get("class", [""])[0].startswith("zdct"):
            explain = p
            break

    texts = []
    if explain:
        for e in explain.nextSiblingGenerator():
            if not isinstance(e, Tag): continue
            if e.attrs.get("class", [""])[0] != explain.attrs['class'][0]:
                break

            texts.append(e.text)


    wf.add_item(title, " ".join(texts), arg=resp.url, valid=True, largetext="\n".join(texts))
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
