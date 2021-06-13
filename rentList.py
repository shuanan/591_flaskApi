from os import truncate
from decouple import config
from flask.json import jsonify
import requests
from bs4 import BeautifulSoup
import lxml
import json
import re

def setHeader(region):
    XSRF_TOKEN = config("XSRF_TOKEN")
    s91_new_session = config("s91_new_session")
    #region=""
    cookie = "webp=1; XSRF-TOKEN=" + XSRF_TOKEN + "; 591_new_session=" + s91_new_session + "; urlJumpIp=" +region
    headers = {
        'X-CSRF-TOKEN' : 'vZ8ncTleQazqy4wPjqpYVNN5lyvAtY8VfldqyzAr',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'Cookie' : cookie
    }
    return headers

#status/hasNextPage/page/data
def analyUrl(headers, page, param):

    url ="https://rent.591.com.tw/?" + param + "firstRow=" + str( (page-1)*30 )
    #print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    house_list = soup.select('ul.listInfo.clearfix')
    result_list = []
    for house in house_list:
        info = dict()

        imagebox = house.select_one('li.pull-left.imageBox')
        info["image"] = imagebox.find('img')['data-original'].replace("\n", "").replace(" ", "").replace(u'\xa0', u' ')

        title = house.select_one('li.pull-left.infoContent')
        info["link"] = "https:" + title.find('h3').find('a')["href"].replace("\n", "").replace(" ", "").replace(u'\xa0', u' ')
        info["title"] = title.find('h3').find('a').text.replace("\n", "").replace(" ", "").replace(u'\xa0', u' ')
        info["isAd"] = title.find('span').text

        content = house.select('p.lightBox')
        info['content']= content[0].text.replace("\n", "").replace(" ", "").replace(u'\xa0', u' ')
        info['address'] =  re.findall( r'\w+.*\w+', content[1].text)
        info['post'] = content[1].find_next_sibling().text.replace("\n", "").replace(" ", "").replace(u'\xa0', u' ')
        info['price'] = house.select_one('div.price').text.replace("\n", "").replace(" ", "").replace(u'\xa0', u' ')
        result_list.append(info)
    
    #page
    hasNextPage = 0
    pages = soup.select_one('span.R').get_text(strip=True)
    if int(pages) - page*30 >0:
        hasNextPage=1

    result = {
        "status": "success",
        "pages":pages,
        "hasNextPage" : hasNextPage,
        "data": result_list
    }

    return result

def dealJson(request):
    page = request["page"]
    data_dict = request["data"]
    headers = setHeader(data_dict["region"])
    param = ""
    for key in data_dict:
        value = data_dict[key]
        param += key + "=" +value + "&"
    
    result = analyUrl(headers, page, param)
        
    return result


dic = {
    "page":1,
    "data":{
        "region":"3",
        "section":"26,41,39"

    }
}
test = dealJson(dic)
print(test)
