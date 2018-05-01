 import sys
import pandas as pd
import xlrd
sys.path.append(r'/Users/leo2swag/Leo/Files')
import network
import gcircle

def selectSource(readinData):
    print("Start selecting source")
    datalist = readinData['source'].drop_duplicates()
    datalist = datalist.head(100)
    print (datalist)
    print("Finish selecting source")
    return datalist.values.tolist()

def main():
    readinData = pd.read_excel("Data/new_network_v2.xls")  # 修改读入的数据路径
    sourceList = selectSource(readinData)  # 修改目标人群
    levels = 4  # 修改运行的等级
    output = 'results/new_network_results.csv'  # 修改输出的结果路径
    output2 = 'results/new_circle_results.csv'  # 修改输出的结果路径
    grep = '房产'  # 修改需要的关键词信息
    option = [2,1] #根据列名从大到小排序, 其中 1为输出个数 2为被连接个数 3为间接中心性 4为紧密中心性
    network.buildGraph(readinData, sourceList, levels, output, grep)
    gcircle.buildCircle(readinData, sourceList, output2, option)
if __name__ == "__main__":
    main()