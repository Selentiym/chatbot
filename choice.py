import json
import re
import datetime
import requests


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def removeBrackets(str):
    startpos = str.find('{')
    endpos = str.rfind('}')
    if startpos == -1 or endpos == -1:
        return str
    return str[:startpos] + str[endpos + 1:]

def choice_main(type_of_events):
    url = "https://kudago.com/public-api/v1.3/search/?q=" + type_of_events + "&page_size=5&location=msk"
    request = requests.get(url).text
    json_events = json.loads(request)["results"]
    json_events_main = []
    for i in range(len(json_events)):
        url_short = requests.get("http://qps.ru/api?url=" + json_events[i]["item_url"]).text
        json_events_mid = {"title": json_events[i]["title"],
                           "content": removeBrackets(cleanhtml(json_events[i]["description"])),
                           "url": url_short}
        json_events_main.append(json_events_mid)
    if json_events_main:
        return json_events_main
    else:
        return 'По вашему запросу событий не найдено'


def location_search(lat, lon, radius = 50000):
    url = "https://kudago.com/public-api/v1.3/search/?q=event&page_size=5&ctype=event&lat=" + \
          str(lat) + "&lon=" + str(lon) + "&radius=" + str(radius)
    answer = json.loads(requests.get(url).text)["results"]

    json_events_main = []
    for i in range(len(answer)):
        url_short = requests.get("http://qps.ru/api?url=" + answer[i]["item_url"]).text
        json_events_mid = {"title": answer[i]["title"],
                           "content": cleanhtml(answer[i]["description"]),
                           "url": url_short,
                           "start": datetime.datetime.fromtimestamp(int(answer[i]["daterange"]["start"])).strftime(
                               '%Y-%m-%d %H:%M'),
                           "end": datetime.datetime.fromtimestamp(int(answer[i]["daterange"]["end"])).strftime(
                               '%Y-%m-%d %H:%M')}
        json_events_main.append(json_events_mid)
    if json_events_main:
        return json_events_main
    else:
        return None