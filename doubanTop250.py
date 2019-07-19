import requests
from lxml import html

movieNum = 1

url = 'https://movie.douban.com/top250'
h = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
cookie = 'll="118281"; bid=PEYq1axn34Q; push_noty_num=0; push_doumail_num=0; __yadk_uid=1zv8cSE9AS8i2VOz6y6vQRA4n4VLQSJA; ps=y; dbcl2="189889726:B7BXiJfGr7Q"; ck=gZQ6; _pk_id.100001.4cf6=af91472b23f8ea50.1563516422.3.1563525244.1563519986.; _pk_ses.100001.4cf6=*'
# 准备cookie字典
c = {i.split('=')[0]: i.split('=')[1] for i in cookie.split('; ')}

# response = requests.get(url, headers=h, cookies=c)
# print(response.text)

# print(response.content.decode())

d = {}

with open('doubanTop250.txt', 'w', encoding='utf8') as f:
    f.seek(0, 0)

while True:
    print(movieNum)
    movieNum += 1

    response = requests.get(url, headers=h, cookies=c)
    strM = response.text

    element = html.fromstring(strM)
    list = element.xpath('//div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/ol/li')

    for li in list:
        movieName = li.xpath('./div/div[@class="info"]/div[@class="hd"]/a/span[1]/text()')+\
                    li.xpath('./div/div[@class="info"]/div[@class="hd"]/a/span[2]/text()')
        movieAYNT = li.xpath('./div/div[@class="info"]/div[@class="bd"]/p/text()')
        movieLink = li.xpath('./div/div[@class="pic"]/a/@href')
        movieScore = li.xpath('./div/div[@class="info"]/div[@class="bd"]/div/span[@class="rating_num"]/text()')

        movieN = (movieName[0].strip().replace(u'\xa0', u' ') + movieName[1].strip().replace(u'\xa0', u' ')).replace(u'\xa0', u' ')
        movieInfo = (movieAYNT[0].strip().replace(u'\xa0', u' ') + '， 其他信息： ' + movieAYNT[1].strip() + ' ， 图片连接： ' + movieLink[0].strip() + ' ， 评分： ' + movieScore[0].strip()).replace(u'\xa0', u' ')

        movieDic = {'电影': movieN, '信息': movieInfo}
        with open('doubanTop250.txt', 'a', encoding='utf-8') as f:
            print(str(movieDic).replace(u'\xa0', u' ') + "\n")
            f.write(str(movieDic).replace(u'\xa0', u' ') + "\n")

    try:
        url = "https://movie.douban.com/top250" + element.xpath('//span[@class="next"]/a/@href')[0]
    except:
        break


