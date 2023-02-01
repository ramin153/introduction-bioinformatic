import sys


def read_scoring_matrix(location):
    with open(location, 'r') as f:
        lines = f.readlines()
        matrix = []
        guide = []
        for line in lines:
                if len(guide) == 0:
                    guide = line.split()
                    continue
                matrix.append(line.split()[1:])
        return matrix,guide

def get_score(matrix,guide:list,char1,char2):
    i = guide.index(char1)
    j = guide.index(char2)
    return matrix[i][j]



def create_matrix_distance(n:int,m:int,v):
    return [[[-100 if i + j == 0 else sys.maxsize*-1,""]  for i in range(m)] for j in range(n)]



def create_graph(n,m):
    return {"I":create_matrix_distance(n,m,sys.maxsize),
            "D":create_matrix_distance(n,m,sys.maxsize),
            "M":create_matrix_distance(n,m,sys.maxsize)}




def insert(graph:dict,i,j):
    help_i = i - 1
    location_ins = graph.get("I")[help_i][j][0]
    ins_value = location_ins -1
    m_value = graph.get("M")[help_i][j][0]  - (11 )

    if ins_value >= m_value:
        graph.get("I")[i][j][0] = ins_value
        graph.get("I")[i][j][1] = "I"
    else:
        graph.get("I")[i][j][0] = m_value
        graph.get("I")[i][j][1] = "M"


def delete(graph: dict, i, j):
    help_j = j-1
    delete_ins = graph.get("D")[i][help_j][0]
    delete_value = delete_ins -1
    m_value = graph.get("M")[i][help_j][0] - (11 )

    if delete_value >= m_value:
        graph.get("D")[i][j][0] = delete_value
        graph.get("D")[i][j][1] = "D"
    else:
        graph.get("D")[i][j][0] = m_value
        graph.get("D")[i][j][1] = "M"

def mis_match(graph: dict,score, i, j):
    ins = graph.get("I")[i][j][0]
    dele = graph.get("D")[i][j][0]
    m = graph.get("M")[i-1][j-1][0] + int(score)

    max_val = max(ins,dele,m)

    graph.get("M")[i][j][0] = max_val
    if max_val == m:
        graph.get("M")[i][j][1] = "M"
    elif max_val == dele :
        graph.get("M")[i][j][1] = "D"
    else:
        graph.get("M")[i][j][1] = "I"


def global_aligment(matrix,guide,sentence_1,sentence_2):
    n, m = len(sentence_1), len(sentence_2)
    graph = create_graph(n+1, m+1)
    graph.get("M")[0][0][0] = 0

    for i in range(0,n+1):
        for j in range(0,m+1):
            if i + j == 0 :
                continue
            if i > 0:
                insert(graph,i,j)
            else:
                graph.get("I")[i][j][0] = 0
                graph.get("I")[i][j][1] = "I"
            if j > 0 :
                delete(graph, i, j)
            else:
                graph.get("D")[i][j][0] = 0
                graph.get("D")[i][j][1] = "D"

            if i > 0 and j > 0:
                mis_match(graph,get_score(matrix,guide,sentence_1[i-1],sentence_2[j-1]),i,j)



    return graph,graph.get("M")[n][m][0]

def check_M(graph,i,j,score):
    val = graph.get("M")[i][j][0]
    if graph.get("M")[i-1][j-1][0] == val- int(score):
        return "M"
    elif graph.get("I")[i][j][0] == val:
        return "I"
    else:
        return "D"

def check_I(graph,i,j):
    val = graph.get("I")[i][j][0]
    if graph.get("M")[i-1][j][0] - 11 == val:
        return "M"
    return "I"


def check_D(graph, i, j):
    val = graph.get("D")[i][j][0]

    if graph.get("M")[i][j-1][0] -  11  == val:
        return "M"
    return "D"


def tracer(graph,sentence_1,sentence_2):
    n = len(sentence_1)
    m = len(sentence_2)
    first = ""
    seconde = ""
    pos = "M"
    while m > 0 and n > 0:
        newpos = ""

        if pos == "M":
            newpos = check_M(graph,n,m,get_score(matrix,guide,sentence_1[n-1],sentence_2[m-1]))
            if newpos == "M":
                n -= 1
                m -= 1
                first = sentence_1[n] + first
                seconde = sentence_2[m] + seconde
        elif pos == "I":
            newpos = check_I(graph,n,m)
            n-=1
            first = sentence_1[n] + first
            seconde = "-" + seconde

        else:
            newpos = check_D(graph,n,m)
            m -= 1
            first = "-" + first
            seconde = sentence_2[m] + seconde

        pos = newpos
    while n > 0:
        n -= 1
        first = sentence_1[n]+first

        seconde = "-"+seconde
    while m > 0:
        m -= 1
        seconde =sentence_2[m] + seconde
        first = "-"+first



    return first, seconde

input = []
with open('rosalind_gaff.txt', 'r') as f:
    lines = f.readlines()
    input_line = ""
    for line in lines:
       if ">" in line:
           if len(input_line) != 0 :
               input.append(input_line.strip())
           input_line = ""
           continue
       input_line += line.strip()
    input.append(input_line.strip())

line_1,line_2 = input[0],input[1]


matrix ,guide = read_scoring_matrix("BLOSUM62.txt")

g,final= global_aligment(matrix,guide,line_1,line_2)

for h,i in g.items():
    print(h)
    for j in i:
        print(j)

one , two  = tracer(g,line_1,line_2)


with open('rosalind_gaff_output.txt', 'w') as f:
    f.write(str(final)+"\n"+one+"\n"+two)