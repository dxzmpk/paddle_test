import sys
import time
from bs4 import BeautifulSoup
import re
import urllib
import openpyxl
from collections import Counter

def askURL(url):
    request= urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request)
        html = response.read()
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


# 获取相关内容
# Warning: 解析页面的代码和页面结构强相关, 当页面html结构发生变化的时候必须同步升级, 否则当场作废
"""
<div class="titlelink box" style="width:645px;">
<a href="/29578175.html" class="truetit" target="_blank">联盟鲁智深？杰伦-布朗展示自己剪完头发后的自拍</a>
<span class="light_r  ">
<a title="有19个亮了的回帖">&nbsp;</a>
</span>
[&nbsp;<span class="multipage">
<a href="/29578175-2.html" target="_blank">2</a>
<a href="/29578175-3.html" target="_blank">3</a>...<a href="/29578175-8.html" target="_blank">8</a>
</span>
&nbsp;]&nbsp;</div>
"""
def getData(baseurl):
    findLink = re.compile(r'<a class="truetit" href="(.*?)" target="_blank">')  # 找到影片详情链接
    # findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # 找到影片图片
    findTitle = re.compile(r'<a class="truetit" href=".*?" target="_blank">(.*)</a>')  # 找到片名
    # 找到评分
    # findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
    # 找到评价人数
    # findJudge = re.compile(r'<span>(\d*)人评价</span>')
    # 找到概况
    # findInq = re.compile(r'<span class="inq">(.*)</span>')
    # 找到影片相关内容：导演，主演，年份，地区，类别
    # findBd = re.compile(r'<p class="">(.*?)</p>', re.S)
    # 去掉无关内容
    # remove = re.compile(r'                            |\n|</br>|\.*')
    datalist = []
    for i in range(1, 10):
        url = baseurl + str(i)
        html = askURL(url)
        print(html)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_='titlelink box'):  # 找到每一个影片项
            data = []
            item = str(item)  # 转换成字符串
            # 影片详情链接
            link_list = re.findall(findLink, item)
            if len(link_list)>0:
                link ="https://bbs.hupu.com"+ link_list[0]
            else:
                link = "没有俩姐"
            # imgSrc = re.findall(findImgSrc, item)[0]
            # data.append(imgSrc)  # 添加图片链接
            title_list = re.findall(findTitle, item)
            if len(title_list)>0:
                title = title_list[0]
            else:
                title ="没有台头"
            if title.count('詹姆斯')!=0:
                data.append(link)
                data.append(title)
            else:
                continue
            # 片名可能只有一个中文名，没有外国名
            # if (len(titles) == 2):
            #     ctitle = titles[0]
            #     data.append(ctitle)  # 添加中文片名
            #     otitle = titles[1].replace("/", "")  # 去掉无关符号
            #     data.append(otitle)  # 添加外国片名
            # else:
            #     data.append(titles[0])  # 添加中文片名
            #     data.append(' ')  # 留空
            #
            # rating = re.findall(findRating, item)[0]
            # data.append(rating)  # 添加评分
            # judgeNum = re.findall(findJudge, item)[0]
            # data.append(judgeNum)  # 添加评论人数
            # inq = re.findall(findInq, item)
            #
            # # 可能没有概况
            # if len(inq) != 0:
            #     inq = inq[0].replace("。", "")  # 去掉句号
            #     data.append(inq)  # 添加概况
            # else:
            #     data.append(' ')  # 留空
            # bd = re.findall(findBd, item)[0]
            # bd = re.sub(remove, "", bd)
            # bd = re.sub('<br(\s+)?\/?>(\s+)?', " ", bd)  # 去掉<br >
            # bd = re.sub('/', " ", bd)  # 替换/
            # data.append(bd.strip())
            datalist.append(data)

    time.sleep(5)
    return datalist


# 将相关数据写入excel中

def saveData(datalist, savepath):
    book = openpyxl.Workbook()
    sheet = book.get_active_sheet()
    # sheet=book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
    col = ('新闻链接', '新闻标题')

    sheet.append(col)  # 添加列头

    for i in range(0, len(datalist)):
        data = datalist[i]
        for j in range(0, 2):
            sheet.cell(row=(i + 2), column=(j + 1), value=data[j])

        # openpyxl中的单元格计数从1开始, 加上第一行是列头, 要多跳一个
    # openpyxl中的计数和Excel内的计数方式一致, 但和常规编程从0开始的方式相左

    book.save(savepath)  # 保存


def main():

    print ("开始爬取......")
    baseurl='https://bbs.hupu.com/vote-'
    datalist=getData(baseurl)
    savapath=u'湿乎乎的话题1006.xlsx'
    saveData(datalist,savapath)


main()

print ("爬取完成，请查看.xlsx文件")
