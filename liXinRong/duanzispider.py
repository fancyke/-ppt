import requests
from lxml import etree
import json


raw_data = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

while True:
    try:
        pages = int(input('请输入您想要爬取的页数:'))
        break
    except:
        print("请输入数字！")
# 抓起原生网站
for page in range(pages):
    raw_url = "https://www.qiushibaike.com/8hr/page/" + str(page+1)
    print(raw_url)

    request = requests.get(raw_url, headers=headers)
    request.encoding = 'utf-8'
    raw_html = request.content
    html = etree.HTML(raw_html)

    # 得到文章序列号
    raw_articlenames = html.xpath('//div[@class="col1"]/div/a[@target="_blank"]/@href')
    midcast = []
    articlenames = []
    for art in raw_articlenames:
        if art not in midcast:
            midcast.append(art)
    for art in midcast:
        articlenames.append(art.strip('/article'))
    print('文章序列号的个数是' + str(len(articlenames)))

    # #得到用户用户名信息
    # usernames = html.xpath("//div[@class=\"col1\"]//div/a/h2/text()")
    # print('用户名个人信息的数量是'+ str(len(usernames)))


    # 包含图片信息文章的目录index
    raw_pictures = html.xpath('//div[@class="thumb"]/a/img/@src')
    indexlist = [''] * len(articlenames)
    for pictures in raw_pictures:
        indexlist[articlenames.index(pictures.split('/')[6])] = pictures

    print('序列的index长度是' + str(len(indexlist)))

    # #用户名的图片信息
    # userpictures = []
    # # for i in usernames:
    # #     print(i)
    # #     phase = "//div/a/img[@alt=\"" + i.strip('\n') + "\"]/@src"
    # #     url = html.xpath("//div/a/img[@alt=\"" + i.strip('\n') + "\"]/@src")
    # #     print(url)
    # raw_userpictures = html.xpath("//div/div/a/img/@src")
    # for i in raw_userpictures:
    #     if '?imageView2/1/w/90/h/90' in i:
    #         userpictures.append(i)
    # print('用户头像的图片数量是' + str(len(userpictures)))

    # 用户的文章内容
    articles = []
    for name in articlenames:
        raw_xpath = '//div/a[@href=\"/article/' + name + "\"]/div[@class=\"content\"]/span/text()"
        raw_articles = html.xpath(raw_xpath)
        articles.append(list(raw_articles))

    print("文章的数量是" + str(len(articles)))

    # 保存为json格式
    # 这里我遇到一个问题，字典是不会保留重复的keys，这就导致我的信息保存不完整
    for i in range(len(articles)):
        item = [{"文章序列号": articlenames[i],"文章图片信息" : indexlist[i],"文章内容": articles[i]}]
        raw_data.append(item[0])

    print("第" + str(page+1) + "页爬取成功！")



with open("C://Code//rawdata.txt",'a',encoding='utf-8') as file:
    for s_data in raw_data:
        file.write(str(s_data) + ',\n')

with open("C://Code//data.json",'a',encoding='utf-8') as f:
    for s in raw_data:
        f.write(json.dumps(s) + ',\n')



print('json文件爬取成功')
