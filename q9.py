import sys
import time


def read_scoring_matrix(location):
    with open(location, 'r') as f:
        lines = f.readlines()
        matrix = []
        guide = []
        for line in lines:
                if len(guide) == 0:
                    guide = line.split()
                    continue
                matrix.append( list(map(int,line.split()[1:])))
        return matrix,guide

def get_score(matrix,guide:list,char1,char2):
    i = guide.index(char1)
    j = guide.index(char2)
    return matrix[i][j]



def create_matrix_distance(n:int,m:int,v):
    return [[0  for i in range(m)] for j in range(n)]



def create_graph(n,m):
    # Insert == 0,Delete == 2,Match = 1
    return [create_matrix_distance(n,m,sys.maxsize) for i in range(3)]




def insert(graph:dict,i,j):
    help_i = i - 1
    location_ins = graph[0][help_i][j]
    ins_value = location_ins -1

    m_value = graph[1][help_i][j]  - 11


    save = max(0,m_value,ins_value)
    graph[0][i][j] = save

    return save

def delete(graph: dict, i, j):
    help_j = j-1
    delete_ins = graph[2][i][help_j]
    delete_value = delete_ins -1

    m_value = graph[1][i][help_j] - (11 )

    save = max(0,delete_value,m_value)
    graph[2][i][j] = save


    return save

def mis_match(graph: dict,score, i, j):
    ins = graph[0][i][j]
    dele = graph[2][i][j]
    m = graph[1][i-1][j-1] + score

    save = max(ins,dele,m,0)

    graph[1][i][j] = save

    return save

def local_aligment_gap(matrix,guide,sentence_1,sentence_2):
    n, m = len(sentence_1), len(sentence_2)
    graph = create_graph(n+1, m+1)
    graph[1][0][0] = 0
    max_val = 0
    x,y = 0,0
    help =0
    for i in range(0,n+1):
        for j in range(0,m+1):
            if i + j == 0 :
                continue
            if i > 0:
                insert(graph,i,j)


            if j > 0 :
                delete(graph, i, j)



            if i > 0 and j > 0:
                help = mis_match(graph, get_score(matrix, guide, sentence_1[i - 1], sentence_2[j - 1]), i, j)

            if help > max_val:
                max_val = help
                x, y = i, j



    return graph,max_val,x,y

def find_max_pos(local_matrix,local_max):
    x, y = 0, 0
    n = len(local_matrix.get("M"))
    m = len(local_matrix.get("M")[0])
    x, y = 0, 0
    end = False
    for i in range(n - 1, 0, -1):
        for j in range(m - 1, 0, -1):

            if local_max == local_matrix.get("M")[i][j][0]:
                x, y = i, j
                end = True
                break
        if end:
            break
    return x,y
def check_M(graph,i,j,score):
    val = graph[1][i][j]
    if graph[1][i-1][j-1] == val- score:
        return 1
    elif graph[0][i][j] == val:
        return 0
    else:
        return 2

def check_I(graph,i,j):
    val = graph[0][i][j]
    if graph[1][i-1][j] - 11 == val:
        return 1
    return 0


def check_D(graph, i, j):
    val = graph[2][i][j]

    if graph[1][i][j-1] -  11  == val:
        return 1
    return 2


def tracer(graph,sentence_1,sentence_2,n,m):

    first = ""
    seconde = ""
    points = graph[1][n][m]
    pos = 1
    while m > 0 and n > 0 and points != 0 :
        newpos = -1

        if pos == 1:
            newpos = check_M(graph,n,m,get_score(matrix,guide,sentence_1[n-1],sentence_2[m-1]))
            if newpos == 1:
                n -= 1
                m -= 1
                first = sentence_1[n] + first
                seconde = sentence_2[m] + seconde
        elif pos == 0:
            newpos = check_I(graph,n,m)
            n-=1
            first = sentence_1[n] + first
            seconde =  seconde
        else:
            newpos = check_D(graph,n,m)
            m -= 1
            first =  first
            seconde = sentence_2[m] + seconde

        pos = newpos

    return first, seconde

input = []
with open('rosalind_laff.txt', 'r') as f:
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
g,final,x,y= local_aligment_gap(matrix,guide,line_1,line_2)

one , two  = tracer(g,line_1,line_2,x,y)


with open('rosalind_laff_output.txt', 'w') as f:
    f.write(str(final)+"\n"+one+"\n"+two)



