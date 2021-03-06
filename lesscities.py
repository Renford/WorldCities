import re
import json
import chardet
import zlib
import urllib3

urllib3.disable_warnings()


# 网页数据解压
def htmlDecompress(response):
    html = response.data
    # encoding = response.info().get('Content-Encoding')
    # print('====encoding==========================,', zlib.MAX_WBITS | 16)
    # if encoding == 'gzip':
    #     print('====encoding==========================,1111111')
    #     # html = zlib.decompress(html, zlib.MAX_WBITS | 16)
    # elif encoding == 'zlib':
    #     html = zlib.decompress(html, zlib.MAX_WBITS)
    # elif encoding == 'deflate':
    #     try:
    #         html = zlib.decompress(html, -zlib.MAX_WBITS)
    #     except Exception as e:
    #         print('err===', e)
    #         html = zlib.decompress(html)

    # encoding = chardet.detect(html)["encoding"]
    # print('====encoding==========================,22222', encoding)

    return html


# 国家名称转换
def country2lower(country):
    country = country.replace("&", "and")
    country = country.replace(" ", "-")
    return country.lower()


# 获取国际所有城市
def getCities(url):
    manager = urllib3.PoolManager()
    response = manager.request('GET', url)
    if (response.status != 200):
        return []

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
    fileName = "lesscities/" + lowerName + ".json"
    cities = []

    try:
        index = 1
        while True:
            url = "https://place.qyer.com/" + lowerName + "/citylist-1-0-" + str(
                index) + "/"
            tempCities = getCities(url)
            index += 1
            cities += tempCities

            if len(tempCities) < 200:
                break

        if len(cities) == 0:
            cities = [{"zh": zhName, "en": enName}]

        cities = cities[:60]

        print('====cities count:', len(cities), url)
    except Exception as e:
        print('===get cities error: ', e)
    finally:
        fileData = json.dumps(cities, ensure_ascii=False)
        fp = open(fileName, "w")
        fp.write(fileData)
        fp.close()


# writeCities("Sweden", "瑞典")

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