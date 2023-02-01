#rosalind_ba7a.txt
import re
import sys
def read_file(file_naem):
    with open('rosalind_ba7a.txt', 'r') as f:
        lines = list(map(str.strip,f.readlines()))
    return lines


def adjensity_matrix(list_input):
    result = dict()
    size = 0
    for i in list_input:
        splited = list(map(int,re.split(r":|->",i)))
        if not splited[0] in result.keys():
            result[splited[0]] = []
        result[splited[0]].append([splited[1],splited[2]])
        size =  max(size,splited[1],splited[0])
    return result,size

def shortest_path( adjensity : dict,size : int):

    matrix = [[0 if i == j else sys.maxsize for i in range(size)] for j in range(size)]
    for i,values in adjensity.items():
        for j,w in values:
            matrix[i][j] = w
            matrix[j][i] = w

    for k in range(size):
        for i in range(size):
            for j in range(size):
                new_path = matrix[i][k] + matrix[k][j]
                if new_path < matrix[i][j]:
                    matrix[i][j] = new_path
                    matrix[j][i] = new_path
    return matrix



lines = read_file("rosalind_ba7a.txt")
number_leaf = int(lines[0])
adjensity,size = adjensity_matrix(lines[1:])
pre_result = shortest_path(adjensity,size+1)
result =[[pre_result[i][j] for j in range(number_leaf)] for i in range(number_leaf)]


with open('rosalind_ba7a_final.txt', 'w') as f:
    for r in result:
        f.write(' '.join([str(i) for i in r])+"\n")
