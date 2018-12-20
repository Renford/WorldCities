from urllib import request
import re
import json
import chardet
import zlib

fp = open('./china/china.json', 'r')
provinces = fp.read()
provs = json.loads(provinces)
fp.close()
print('==========result', provs)

def mapfunc(item):
  return {
    "zh":item["zh"],
    "en":item["en"]
  }

aaaa = map(mapfunc, provs)

fp = open('chinas.json', "w")
fp.write(json.dumps(aaaa, ensure_ascii=False))
fp.close()

# for prov in provs: 
#   print('==========prov', prov)
#   fp = open(prov["en"], "w")
#   fp.write(json.dumps(prov["cities"], ensure_ascii=False))
#   fp.close()