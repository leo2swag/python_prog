import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xlrd

DG = nx.DiGraph()

def selectSource(readinData):
    print("Start selecting source ...")
    datalist = readinData['source'].drop_duplicates()
    datalist = datalist.head(100)
    print (datalist)
    print("Finish selecting source ...")
    return datalist.values.tolist()

#是否存在关键词信息
def if_contain(ff, gerp):
    flen = len(ff)
    for f in range(flen):
        if ff[f].find(gerp) != -1:
           return 1
    return 0


def together(edges, result, num, save, title, resultcheck, grep):
    temp = []
    elen = len(edges)
    front = edges[0][0]
    next = edges[0][1]
    temp.append(front)
    save.append(temp)
    temp = temp.copy()
    temp.append(next)
    save.append(temp)
    save.pop(0)
    for i in range(elen-1):
        front = edges[i]
        next = edges[i+1]

        templen = len(temp)
        if((front[1] == next[0]) & (front[0] == temp[templen-2]) & (front[1] == temp[templen-1])):
            if (len(temp) < num):
                temp = temp.copy()
                temp.append(next[1])

                if ((len(temp) == num) | (i == elen-2)):
                        if_c = if_contain(temp, grep)
                        tt = temp.copy()
                        if (len(temp) < num):
                            tlen = (num - len(temp))
                            for t in range(tlen):
                                tt.append('.')
                        ff = []
                        for q in range(len(tt)-1):
                            first = tt[q]
                            second = tt[q+1]
                            ff.append(first)
                            if ((first == '.') or (second == '.')):
                                value = 0
                            else:
                                value = DG.get_edge_data(first, second)['weight']
                            ff.append(value)
                        ff.append(second)
                        ff.append(if_c)
                        dtemp = pd.DataFrame([ff], columns=title)
                        result = pd.concat([result,dtemp],ignore_index=True)
                        resultcheck.append(temp)
                else: #长度小于num
                    save.append(temp)
        else:
            for k in range(len(save)):
                compare = save[k]
                cpos = len(compare)-1
                if (next[0] == compare[cpos]):
                    if (len(temp) < num):
                        if_c = if_contain(temp, grep)
                        tt = temp.copy()
                        if (len(temp) <= num):
                            tlen = (num - len(temp))
                            for t in range(tlen):
                                tt.append('.')

                            ff = []
                            for q in range(len(tt) - 1):
                                first = tt[q]
                                second = tt[q + 1]
                                ff.append(first)
                                if ((first == '.') or (second == '.')):
                                    value = 0
                                else:
                                    value = DG.get_edge_data(first, second)['weight']
                                ff.append(value)
                            ff.append(second)
                            ff.append(if_c)
                            dtemp = pd.DataFrame([ff], columns=title)
                            result = pd.concat([result, dtemp], ignore_index=True)
                            resultcheck.append(temp)

                    temp = compare.copy()
                    temp.append(next[1])

                    if (len(temp) < num):
                        save.append(temp)
                    if ((len(temp) == num) | (i == elen - 2)):
                        if_c = if_contain(temp, grep)
                        tt = temp.copy()
                        tlen = (num - len(temp))
                        for t in range(tlen):
                            tt.append('.')

                        ff = []
                        for q in range(len(tt) - 1):
                            first = tt[q]
                            second = tt[q + 1]
                            ff.append(first)
                            if ((first == '.') or (second == '.')):
                                value = 0
                            else:
                                value = DG.get_edge_data(first, second)['weight']
                            ff.append(value)
                        ff.append(second)
                        ff.append(if_c)
                        dtemp = pd.DataFrame([ff], columns=title)
                        result = pd.concat([result, dtemp], ignore_index=True)
                        resultcheck.append(temp)
                    break
    return result


def printResult(result,output):
    print("Start printing result")
    result.to_csv(output , encoding='utf_8_sig', index=False)
    print("Done printing results")


def getSource(DG,sourceList,num,title,grep):
    print("Start analzing source")
    dLen = len(sourceList)
    result = pd.DataFrame(columns=title)
    resultcheck = [[]]
    for i in range(dLen):
        save = [[]]
        source = sourceList[i]
        edges = list(nx.edge_dfs(DG, source))
        tree_nodes = list(nx.dfs_tree(DG,source,num-2))
        labels = ['test_A', 'test_B']
        df_test = pd.DataFrame.from_records(edges,columns=labels)
        df_test = df_test[df_test['test_A'].isin(tree_nodes)] #筛选等级内的点
        dic = df_test.values.tolist()
        result = together(dic, result, num, save, title, resultcheck, grep)
    return result


def plotGraph(DG):
    print('Start drawing Graph ...')
    pos = nx.spring_layout(DG)
    nx.draw_networkx_nodes(DG,pos,node_shape='o',node_size=1,label=None)
    nx.draw_networkx_edges(DG,pos,label=None,width=0.1)
    plt.show()
    print('Finish drawing Graph ...')


def buildGraph(readinData, sourceList, num, output, grep):
    num = num + 1
    print('Start Building Graph ...')
    title = []
    for k in range(num):
        name = "第" + str(k) + "级"
        title.append(name)
        if k < num-1:
            title.append('数据')
    title.append('是否存在')
    for i,elrow in readinData.iterrows():
        try:
            tempNume = DG.get_edge_data(elrow[0], elrow[1])['weight']
            tempNume = tempNume + elrow[2]
        except:
            tempNume = elrow[2]
        DG.add_weighted_edges_from([(elrow[0], elrow[1],tempNume)])

    print(DG.number_of_edges())
    print ('Finish building Graph ...')

    result = getSource(DG,sourceList,num,title,grep)
    printResult(result,output)


def main():
    readinData = pd.read_excel("Data/input_new_network_v2.xls") #修改读入的数据路径
    sourceList = selectSource(readinData) #修改目标人群
    levels = 4 #修改运行的等级
    output = 'results/output_new_network_results.csv'  # 修改输出的结果路径
    grep = '房产' #修改需要的关键词信息
    buildGraph(readinData, sourceList, levels, output, grep)


if __name__ == "__main__":
    main()