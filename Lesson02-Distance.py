import re
import requests
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt


def get_one_page(url):   #对网页进行爬取，并返回相邻站点之间的距离，行成列表,并写入到StationDistance.txt文件中
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['font.family'] = 'sans-serif'
    response = requests.get(url,verify=False)
    response.encoding = 'gbk'
    html = response.text
    pattern = re.compile('<th>(.*?)——(.*?)</th>.*?<td.*?>(\d+)</td>.*?<td.*?>上行/下行</td>',re.S)
    StationDistance = re.findall(pattern,html)      #所有的站间距行成一个列表，列表中的元素为元祖
    with open('./线路图/StationDistance.txt','w') as f:
        for item in StationDistance:
            f.write(item[0]+"  "+item[1]+"  "+item[2])
            f.write('\n')
    return StationDistance


def create_dict(StationDistance):   #将所有站点写入到字典中，字典的键为每个站，value为该站直接连接的站点,并将该字典写入到StationConnected.txt文件中
    length = len(StationDistance)
    dict = defaultdict(list)
    for i in range(0,length):
        dict[StationDistance[i][0]].append(StationDistance[i][1])
        dict[StationDistance[i][1]].append(StationDistance[i][0])
    with open('./线路图/StationConnected.txt','w') as f:   #记录每个站点及与之相连接的站点
        for key in dict.keys():
            f.write(key+":")
            f.write(str(dict.get(key)))
            f.write('\n')
    return dict

def search(start,destination,connection_graph,sort_candidate):  #搜索从起点到终点的路线,这个函数还有点问题，只能返回两三条站点最少的路线
    pathes = [[start]]
    start_to_destination = []
    #visited2 = set()
    while pathes:
        path = pathes.pop(0)   #移除pathes中的第一个值，并且返回path
        visited = set()
        #if(len(visited2) == len(connection_graph)):
           # break
        froninter = path[-1]    #取最后一个元素
        for i in range(0,len(path)-1):
            visited.add(path[i])
        if froninter in visited:   #如果最后一个站点已经访问过，则跳过
            continue
        if froninter == destination:
            break
        successors = connection_graph[froninter]   #从字典中查找最后一个站点连接的所有站,successors是一个列表
        for station in successors:
            if station in path:   #如果该站点已经在path中，则跳过
                continue
            new_path = path+[station]
            pathes.append(new_path)
            if station == destination:
                start_to_destination.append(new_path)
        visited.add(froninter)
    pathes = sort_candidate(start_to_destination)
    return pathes[0]
    #return start_to_destination
def get_path_distance(path):  #用之前的站间距列表计算路径的长度
    distance = 0
    for i in range(0,len(path)-1):
        s1 = path[i]
        s2 = path[i+1]
        with open('./线路图/StationDistance.txt','r') as f:
            for line in f:
                if s1 in line and s2 in line:
                    pattern = re.compile('.*?(\d+)')
                    d = int(re.findall(pattern,line)[0])
        distance = distance + d
    return distance
#print("天安门西到中关村的距离为：%d 米" % get_path_distance(pathes[0]))
def shortest_path_first(pathes):
    if len(pathes)<=1:
        return pathes
    return sorted(pathes,key=get_path_distance)

if __name__ == "__main__":
    url = 'https://www.bjsubway.com/station/zjgls/'
    StationDistance = get_one_page(url)
    # StationGraph = nx.Graph()
    # StationGraph.add_weighted_edges_from(StationDistance)  # 画北京市地铁线路图,还缺经纬度
    # nx.draw(StationGraph, with_labels=True, node_size=20, font_size=10)
    # plt.show()
    dict = create_dict(StationDistance)
    start = input("请输入起点站：")
    destination = input("请输入终点站：")
    path = search(start,destination,dict,sort_candidate=shortest_path_first)    #求天安门西到中关村的所有路线,这个函数还有点问题，本想返回所有路线，但是只能返回一两条站点少的，但是可能换乘很多
    print("您要走的最短路线为：",'—>'.join(path))   #打印出最短路线

    distance = get_path_distance(path)
    print("从{0}到{1}的最短路线距离为{2}公里".format(start,destination,distance/1000))


