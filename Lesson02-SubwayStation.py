import requests
import re
import networkx as nx
url = 'https://www.bjsubway.com/station/xltcx/'
response = requests.get(url,verify=False)
response.encoding = 'gbk'
html = response.text
station = {}
pattern1 = re.compile('<div\sclass="station">.*?line1/2.*?>(.+?)</a>')
pattern2 = re.compile('<div\sclass="station">.*?line2/2.*?>(.+?)</a>')
#pattern4 = re.compile('<div\sclass="station">(.+?)</div>')   #这个可能有问题<div class="station">新街口</div>
pattern5 = re.compile('<div\sclass="station">.*?line5/2.*?>(.+?)</a>')
pattern6 = re.compile('<div\sclass="station">.*?line6/2.*?>(.+?)</a>')
pattern7 = re.compile('<div\sclass="station">.*?lines7/2.*?>(.+?)</a>')
pattern8 = re.compile('<div\sclass="station">.*?line8/2.*?>(.+?)</a>')
pattern9 = re.compile('<div\sclass="station">.*?line9/2.*?>(.+?)</a>')
pattern10 = re.compile('<div\sclass="station">.*?line10/2.*?>(.+?)</a>')
pattern13 = re.compile('<div\sclass="station">.*?line13/2.*?>(.+?)</a>')
#pattern14 = re.compile('<div\sclass="station">.*?line1/2.*?>(.+?)</a>')   #<div class="station">蒲黄榆</div>
pattern15 = re.compile('<div\sclass="station">.*?line15/2.*?>(.+?)</a>')
#16号线也没有输出
pattern_bt = re.compile('<div\sclass="station">.*?linebt/2.*?>(.+?)</a>')   #八通线
pattern_cp = re.compile('<div\sclass="station">.*?linecp/2.*?>(.+?)</a>')   #昌平线
pattern_yz = re.compile('<div\sclass="station">.*?lineyz/2.*?>(.+?)</a>')   #亦庄线
pattern_fs = re.compile('<div\sclass="station">.*?linefs/2.*?>(.+?)</a>')   #亦庄线


line1 = re.findall(pattern1,html)
line2 = re.findall(pattern2,html)
#line4 = re.findall(pattern4,html)
line5 = re.findall(pattern5,html)
line6 = re.findall(pattern6,html)
line7 = re.findall(pattern7,html)
line8 = re.findall(pattern8,html)
line9 = re.findall(pattern9,html)
line10 = re.findall(pattern10,html)
line13 = re.findall(pattern13,html)
#line14 = re.findall(pattern14,html)
line15 = re.findall(pattern15,html)
line_bt = re.findall(pattern_bt,html)
line_cp = re.findall(pattern_cp,html)
line_yz = re.findall(pattern_yz,html)
line_fs = re.findall(pattern_fs,html)

station["1号线"] = line1
station["2号线"] = line2
#station["4号线"] = line4
station["5号线"] = line5
station["6号线"] = line6
station["7号线"] = line7
station["8号线"] = line8
station["9号线"] = line9
station["10号线"] = line10
station["13号线"] = line13
#station["14号线"] = line14
station["15号线"] = line15
station["八通线"] = line_bt
station["昌平线"] = line_cp
station["亦庄线"] = line_yz
station["房山线"] = line_fs

# with open('./线路图/BJSubwayStation.txt','w') as f:
#     for key in station.keys():
#         f.write(key+":")
#         for item in station[key]:
#             f.write(item+"  ")
#         f.write('\n')
g = nx.Graph(station)
nx.draw(g)
# print(station1)
#print(station)
#print(response.text)