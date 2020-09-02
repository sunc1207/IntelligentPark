# author    : Charles
# time      ：2020/7/22  14:04 
# file      ：get_temperature.PY
# project   ：apiToy
# IDE       : PyCharm

import requests
from lxml import etree
import pymongo


def update_current_temperature_to_mongodb():
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"}
    url = "https://www.baidu.com/s?wd=%E4%B8%8A%E6%B5%B7%E6%B0%94%E6%B8%A9&ie=UTF-8"
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    path1 = "/html/body/div/div[3]/div[1]/div[3]/div[1]/div[1]/div[1]/a[1]/div[1]/div[2]/span[1]"
    results = selector.xpath(path1)
    temperature_now = results[0].text
    if len(temperature_now):
        my_client = pymongo.MongoClient(
        'mongodb://huaxin:inesa2014@10.200.43.5:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
        my_db = my_client['huaxin']
        my_column = my_db['temperature']
        my_query = {
        "location": "Shanghai",
        }
        new_values = {
            "$set": {"temperature": temperature_now}
        }
        my_column.update_one(my_query, new_values)
        print("update temperature done!")


def get_temperature_shanghai():
    my_client = pymongo.MongoClient(
        'mongodb://huaxin:inesa2014@10.200.43.5:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
    my_db = my_client['huaxin']
    my_column = my_db['temperature']
    my_dict = {
        "location": "Shanghai",
    }
    x = my_column.find_one(my_dict)
    return x["temperature"]


if __name__ == '__main__':
    update_current_temperature_to_mongodb()
