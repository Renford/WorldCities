from urllib import request
import re
import json
import chardet
import zlib


# 网页数据解压
def htmlDecompress(response):
    html = response.read()
    encoding = response.info().get('Content-Encoding')

    if encoding == 'gzip':
        html = zlib.decompress(html, zlib.MAX_WBITS + 16)
    elif encoding == 'deflate':
        try:
            html = zlib.decompress(html, -zlib.MAX_WBITS)
        except Exception as e:
            print('err===', e)
            html = zlib.decompress(html)

    encoding = chardet.detect(html)["encoding"]

    return html


# 国家名称转换
def country2lower(country):
    country = country.replace("&", "and")
    country = country.replace(" ", "-")
    return country.lower()


# 获取国际所有城市
def getCities(url):
    response = request.urlopen(url)
    html = htmlDecompress(response)
    html = html.decode('utf-8')

    pattern = re.compile(r'\"place-citylist-text-city-1\".*</span>')
    items = pattern.findall(html)

    cities = []
    for item in items:
        zhObj = re.search(r'\"place-citylist-text-city-1\">.*&nbsp;', item)
        zhName = re.sub(r'\"place-citylist-text-city-1\">', "", zhObj.group())
        zhName = re.sub(r'&nbsp;&nbsp;', "", zhName)

        enObj = re.search(r'\"en\".*</span>', item)
        enName = re.sub(r'\"en\">', "", enObj.group())
        enName = re.sub(r'</span>', "", enName)

        cities.append({'zh': zhName, 'en': enName})

    return cities


# 各国城市写入文件
def writeCities(enName, zhName):
    lowerName = country2lower(enName)
    fileName = "countries/" + lowerName + ".json"
    cities = [{"zh": zhName, "en": enName}]

    try:
        url = "https://place.qyer.com/" + lowerName + "/citylist-1-0-1/"
        cities = getCities(url)
    except Exception as e:
        print('===write cities error: ', e)
    finally:
        fileData = json.dumps(cities, ensure_ascii=False)
        fp = open(fileName, "w")
        fp.write(fileData)
        fp.close()


paths = [
    "africa", "antarctica", "asia", "europe", "north-america", "oceania",
    "south-america"
]
for path in paths:
    path = "continents/" + path + ".json"
    fp = open(path)
    array = json.loads(fp.read())

    for item in array:
        print('=======item:', path, item["enName"], item["zhName"])
        writeCities(item["enName"], item["zhName"])

# def formateJson(path):
#     fp = open(path)
#     content = fp.read()
#     array = content.split('\n')

#     result = []
#     for item in array:
#         arr = item.split(" ")
#         zhName = arr[0]
#         enName = item.replace(zhName, "").strip()
#         result.append({'zhName': zhName, 'enName': enName})
#     print("content===", result)

#     fileData = json.dumps(result, ensure_ascii=False)
#     fp = open(path, "w")
#     fp.write(fileData)
#     fp.close()
