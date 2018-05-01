import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xlrd

DG = nx.DiGraph()

def selectSource(DG):
    print("Start selecting source ...")
    ddlist = list(DG.node)
    return ddlist


def printResult(result,output):
    print("Start printing result")
    result.to_csv(output , encoding='utf_8_sig', index=False)
    print("Done printing results")


def getSource(DG,sourceList,title):
    print("Start analzing source")
    dLen = len(sourceList)
    result = pd.DataFrame(columns=title)
    deg_dict = nx.degree_centrality(DG)
    bet_dict = nx.betweenness_centrality(DG)
    close_dict = nx.closeness_centrality(DG)
    for i in range(dLen):
        source = sourceList[i]
        #print (source)
        outputs = list(DG.successors(source))  #输出(from source)
        inputs = list(DG.predecessors(source)) #被连接 (to source)
        deg_value = deg_dict[source]
        bet_value = bet_dict[source]
        close_value = close_dict[source]
        temp = pd.DataFrame([[source,len(outputs),len(inputs),deg_value, bet_value,close_value]],columns=title)
        result = pd.concat([result, temp], ignore_index=True)

    print ('Source has been analzed ')
    return result


def plotGraph(DG):
    print('Start drawing Graph ...')
    pos = nx.spring_layout(DG)
    nx.draw_networkx_nodes(DG,pos,node_shape='o',node_size=1,label=None)
    nx.draw_networkx_edges(DG,pos,label=None,width=0.1)
    plt.show()
    print('Finish drawing Graph ...')


def compputer_section_one(DG, result, elist, output2):
    #section_one = pd.DataFrame(columns=['客户', '对象', '关系'])
    tlistbig = {}
    #print (elist)
    for j in range(len(elist)):
        tlistbig[elist[j]] = pd.DataFrame(columns=[str(elist[j]) + '_客户',str(elist[j]) + '_对象'])
    section_one = pd.DataFrame()
    print ("Computing section_one")
    namelist = result['客户'].values.tolist()
    for i in range(len(namelist)):
        source = namelist[i]
        outputs = list(DG.successors(source))
        outputs_p = list(DG.predecessors(source))
        for k in range(len(outputs)):
            dict = list(DG[source][outputs[k]])
            namel = [source, outputs[k]]
            temp = namel + dict
            tempdf = pd.DataFrame([temp])
            for j in range(len(dict)):

                tempfile = pd.DataFrame([[source, outputs[k]]],columns=[str(dict[j]) + '_客户', str(dict[j]) + '_对象'])
                tlistbig[dict[j]] = pd.concat([tlistbig[dict[j]], tempfile])
            section_one = pd.concat([section_one, tempdf])

        for q in range(len(outputs_p)):
            dict_p = list(DG[outputs_p[q]][source])
            namel_p = [outputs_p[q],source]
            temp_p = namel_p + dict_p
            tempdf_p = pd.DataFrame([temp_p])
            for x in range(len(dict_p)):
                tempfile_p = pd.DataFrame([[outputs_p[q],source]],
                                        columns=[str(dict_p[x]) + '_客户', str(dict_p[x]) + '_对象'])
                tlistbig[dict_p[x]] = pd.concat([tlistbig[dict_p[x]], tempfile_p])

            section_one = pd.concat([section_one, tempdf_p])
    section_one = section_one.fillna('')
    printResult(section_one, output2)
    return tlistbig

def printlistbig(listbig, name, output3):
    tempdf = listbig[name]
    tempdf.to_csv(output3, encoding='utf_8_sig', index=False)

def buildCircle(readinData, output, output2, option=[1], percent=0.5):
    print('Start Building Graph ...')

    title = ['客户','输出个数','被连接的个数','度数中心性','间接中心性','紧密中心性']
    elist = []
    for i,elrow in readinData.iterrows():
        DG.add_edges_from([(elrow[0], elrow[1])])
        #nx.set_edge_attributes(DG,elrow[2],(elrow[0],elrow[1]))
        attrs = {(elrow[0],elrow[1]):{elrow[2]:elrow[2]}}
        if (elrow[2] not in elist):
            elist.append(elrow[2])
        #print (attrs)
        nx.set_edge_attributes(DG,attrs)

    sourceList = selectSource(DG)  # 修改目标人群

    #tt = list(DG['Wang,Jun']['Zhang,Liangfang'])
    print(DG.number_of_edges())
    print ('Finish building Graph ...')

    result = getSource(DG,sourceList,title)
    clist = list(result.columns.values)

    column_Name = []
    for i in range(len(option)):
        column_Name.append(clist[option[i]])
    #print(column_Name)
    result = result.sort_values(by=column_Name, ascending=[False,False])
    shape = result.shape
    num = int(round(percent*(shape[0]),0))
    result = result.head(num)
    #print (result)
    printResult(result, output)
    listbig = compputer_section_one(DG, result, elist, output2)
    return listbig

def main():
    readinData = pd.read_excel("Data/input_new_network_v2.xls") #修改读入的数据路径
    readinData = readinData.drop('freq',1)
    readinData['relations'] = np.random.randint(1, 9, size=len(readinData['source']))
    print (readinData)
    output = 'results/output_overview_new_Gcircle_results.csv'  # 修改输出的结果路径
    output2 = 'results/output_overview_new_Gcircle_results_2.csv'  # 修改输出的结果路径
    option = [2,1] #根据列名从大到小排序, 其中 1为输出个数 2为被连接个数 3为间接中心性 4为紧密中心性
    percent = 0.25
    listbig = buildCircle(readinData, output, output2, option, percent)
    name = 1
    output3 = 'results/output_overview_new_Gcircle_results_3.csv'  # 修改输出的结果路径
    printlistbig(listbig, name, output3)
    name = 2
    output3 = 'results/output_overview_new_Gcircle_results_4.csv'  # 修改输出的结果路径
    printlistbig(listbig, name, output3)

if __name__ == "__main__":
    main()