import networkx as nx
import pygraphviz as pgv
import matplotlib.pyplot as plt


def inference(graphDict, bufString):
    # 检查输入合法性
    assert isinstance(graphDict, dict)
    assert isinstance(bufString, list)
    # 定义初始状态
    # 定义开始位置
    i = 0
    # 定义起始状态
    state = 'q1'
    # 如果不为接受或拒绝状态
    while state != 'qaccept' and state != 'qreject':
        # 获取输入
        input = bufString[i]
        # 查看是否存在对应状态转移
        if (state, input) in graphDict.keys():
            # 存在, 获得下一状态转移结果
            nextState, output, moving = graphDict[(state, input)]
        # 不存在
        else:
            # 返回拒绝结果
            return 'qreject'
        # 输出中间过程
        print(state, input, nextState, output, moving, i, "".join(bufString), sep=',')
        # 修改状态
        bufString[i] = output
        i = i + moving
        state = nextState
        # 检查是否越界
        if (i < 0 or i >= len(bufString)) and state != 'qaccept':
            # 越界，返回拒绝结果
            return 'qreject'
    # 返回结果
    return state


if __name__ == '__main__':
    # Step 0. 定义状态机
    # 常量定义
    R = 1  # 右(Right)
    L = -1  # 左(Left)
    # 输入字母表
    inputAlphabet = ['a', 'b', 'c', '#']
    # 状态机
    graphDict = dict()
    # 状态机定义
    # 状态机定义如下，以下行为例：当前状态为q1且目前输入为'0'时，
    #                        状态转换为q2，当前带子位置字符变为'#', 指针向右(R)走一步
    graphDict[('q1', 'a')] = ('q2', 'A', R)
    graphDict[('q2', 'a')] = ('q2', 'a', R)
    graphDict[('q2', 'b')] = ('q3', 'b', R)
    graphDict[('q3', 'b')] = ('q3', 'b', R)
    graphDict[('q3', 'c')] = ('q4', 'c', R)
    graphDict[('q4', 'c')] = ('q4', 'c', R)
    graphDict[('q4', '#')] = ('q5', '#', L)
    graphDict[('q5', 'a')] = ('q5', 'a', L)
    graphDict[('q5', 'b')] = ('q5', 'b', L)
    graphDict[('q5', 'c')] = ('q5', 'c', L)
    graphDict[('q5', 'A')] = ('q6', 'A', R)
    graphDict[('q6', 'a')] = ('q6', 'a', R)
    graphDict[('q6', 'b')] = ('q6', 'b', R)
    graphDict[('q6', 'C')] = ('q7', 'C', L)
    graphDict[('q6', 'c')] = ('q7', 'c', L)
    graphDict[('q7', 'c')] = ('q7', 'c', L)
    graphDict[('q7', 'C')] = ('q7', 'C', L)
    graphDict[('q7', 'B')] = ('q7', 'B', L)
    graphDict[('q7', 'b')] = ('q8', 'B', R)
    graphDict[('q7', 'a')] = ('q9', 'a', R)
    graphDict[('q7', 'A')] = ('q12', 'A', R)
    graphDict[('q8', 'c')] = ('q7', 'C', L)
    graphDict[('q8', 'B')] = ('q8', 'B', R)
    graphDict[('q8', 'C')] = ('q8', 'C', R)
    graphDict[('q9', 'B')] = ('q9', 'b', R)
    graphDict[('q9', 'C')] = ('q10', 'C', L)
    graphDict[('q10', 'b')] = ('q10', 'b', L)
    graphDict[('q10', 'a')] = ('q10', 'a', L)
    graphDict[('q10', 'A')] = ('q11', 'A', R)
    graphDict[('q11', 'a')] = ('q6', 'A', R)
    graphDict[('q12', 'A')] = ('q12', 'A', R)
    graphDict[('q12', 'B')] = ('q12', 'B', R)
    graphDict[('q12', 'C')] = ('q12', 'C', R)
    graphDict[('q12', '#')] = ('qaccept', '#', R)
    graphDict[('q12', 'c')] = ('qreject', 'c', R)
    # 生成状态集与带子字母表
    # 初始状态集
    stateTable = ['qaccept', 'qreject']
    allAlphabet = ['#']
    # 查看状态转移的输入端
    for state, input in graphDict.keys():
        if state not in stateTable:  # 如果状态集中不包含该状态
            stateTable.append(state)  # 加入状态集
        if input not in allAlphabet:  # 如果字母表中不存在该字母
            allAlphabet.append(input)  # 加入字母表
        nextState, output, _ = graphDict[(state, input)]  # 查看状态转移的输出端
        if nextState not in stateTable:  # 如果状态集中不包含该状态
            stateTable.append(nextState)  # 加入状态集
        if output not in allAlphabet:  # 如果字母表中不存在该字母
            allAlphabet.append(output)  # 加入字母表
    # 补全状态转移表
    for state in stateTable:
        for code in allAlphabet:
            # 显然，两种停机状态不应补全
            if state != 'qaccept' and state != 'qreject':
                if (state, code) not in graphDict.keys():
                    graphDict[(state, code)] = ('qreject', code, R)

    # 输出
    print('状态集:', stateTable)
    print('输入字母表:', inputAlphabet)
    print('带子字母表:', allAlphabet)
    print('起始状态:q0, 接受状态:qaccept, 拒绝状态: qreject')
    print('状态转移表:')
    for state, input in graphDict.keys():
        nextState, output, moving = graphDict[(state, input)]
        moving = 'R' if moving == 1 else 'L'
        print(state, input, nextState, output, moving, sep=',')
    # Step 1. 检查输入合法性
    # 获取输入

    bufString = list("aabbcccc#")
    # 检测输入合法性
    flag = False
    for char in bufString:
        # 如果发现了不存在于输入字母表的字符
        # 则直接拒绝
        if char not in inputAlphabet:
            flag = True
            break
    # 发现了不存在于输入字母表的字符,拒绝
    if flag:
        print('qreject')

    # Step 2. 推理
    print('状态转移过程:')
    answer = inference(graphDict, bufString)
    # 输出结果
    print(answer)

# Step 3. 绘图
# 注意到这部分代码已经跟本实验无关，只是为了实验报告出图方便而撰写的
# 由于这一块使用了networkx,pygraphviz与matplotlib等第三方绘图库
# 这一部分的代码注释并不保证能够让审阅者看懂
# 下面的代码将默认审阅者拥有相关库的对应知识

# 定义状态转移图
G = nx.DiGraph()
# 从状态集中生成图的节点
G.add_nodes_from(stateTable)

# 从自动机中生成图的边
edgeDict = dict()
# 遍历所有可能边
for state in stateTable:
    for input in allAlphabet:
        # 检查存在性，理论上所有边都应该存在
        if (state, input) in graphDict.keys():
            # 获得状态转移方程
            nextState, output, moving = graphDict[(state, input)]
            # 维护边的信息
            if (state, nextState) not in edgeDict.keys():
                edgeDict[(state, nextState)] = ([input], [output], [moving])
            else:
                inputList, outputList, movingList = edgeDict[(state, nextState)]
                inputList.append(input)
                outputList.append(output)
                movingList.append(moving)
                edgeDict[(state, nextState)] = (inputList, outputList, movingList)
            # 向图中添加边
            G.add_edge(state, nextState)

# 定义pgv图
AG = pgv.AGraph(strict=True, directed=True)
# 从nx中加载图的节点
AG.add_nodes_from(G.nodes())
# 从nx中加载图的边
for e in G.edges:
    # 生成边的信息
    labelIO = ""
    labelMoving = ""
    # 获取边的信息
    inputList, outputList, movingList = edgeDict[(e[0], e[1])]
    # 生成边的信息
    for i, (input, output) in enumerate(zip(inputList, outputList)):
        # 格式化
        if input == output:
            labelIO += input + '->'
        else:
            labelIO += input + '->' + output
        labelIO += ','
    if movingList[0] == -1:
        labelMoving = "L"
    else:
        labelMoving = "R"
    # 添加边
    AG.add_edge(e[0], e[1], label=labelIO + labelMoving, fontsize=12)

# 定义操作
AG.layout('dot')
# 生成png图
AG.draw('Experiment2.png')
AG.draw('Experiment2.pdf')

# # 显示图片
# image = plt.imread('Experiment2.png')
# plt.imshow(image)
# plt.show()
