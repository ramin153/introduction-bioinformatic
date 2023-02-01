import sys


def read_file(file_naem):
    with open(file_naem, 'r') as f:
        lines = list(map(str.strip,f.readlines()))
    return lines
def create_matrix(lines,size):
    return [[int(j) for j in list(map(int,lines[i].split() ))] for i in range(size)]

def create_matrix_special(inputs,size):
    inputs = create_matrix(inputs,size)
    return [[i,1,0,[inputs[i][j] for j in range(size) ]] for i in range(size)]
def find_min(matrix,size):
    nodei = -1
    nodej = -1
    result = sys.maxsize

    for i in range(size):
        for j in range(size):
            if i != j:
                min = matrix[i][3][j]
                if result > min:
                    result = min
                    nodej = j
                    nodei = i
    return result,nodei,nodej
def new_edge(matrix,i,j,min,new_node):
    node_i = matrix[i]
    node_j = matrix[j]
    min /= 2

    result = []
    result.append([new_node,node_i[0],min-node_i[2]])
    result.append([new_node,node_j[0], min - node_j[2]])
    return result
def combine_two_column(matrix,i,j,node_name,size,min_weight):

    node_i = matrix[i]
    node_j = matrix[j]
    new_distance = [0]
    weight_i = node_i[1]
    weight_j = node_j[1]
    for t in range(size+1):
        if t == i or t == j:
            continue
        new_distance.append((weight_i*node_i[3][t] + weight_j*node_j[3][t])/(weight_i+weight_j))
    row_one = [node_name,weight_i+weight_j,min_weight/2,new_distance]
    new_matrix = [row_one]
    for t in range(len(matrix)):
        if t == i or t == j:
            continue
        old_row = matrix[t]
        new_row = [old_row[0],old_row[1],old_row[2]]
        new_distance_t = [i for i in old_row[3]]
        if i > j:
            i,j = j,i
        new_distance_t.pop(j)
        new_distance_t.pop(i)
        index = len(new_matrix)
        index = row_one[3][index]
        new_distance_t = [index]+new_distance_t
        index = new_distance_t.index(0)
        new_distance_t.pop(index)
        new_distance_t.insert(len(new_matrix),0)
        new_row.append(new_distance_t)
        new_matrix.append(new_row)

    return new_matrix
def create_tree(matrix,size):
    edge_matrix = []
    node_name = size
    while len(matrix) > 1:
        min,i,j = find_min(matrix,size)
        edge_matrix += new_edge(matrix,i,j,min,node_name)
        size-=1
        matrix = combine_two_column(matrix, i, j, node_name,size,min)
        node_name+=1
    return edge_matrix
def two_way(graph):
    result = []
    for i in graph:
        value = f'{i[2]:.3f}'
        result.append([i[0],i[1],value])
        result.append([i[1], i[0], value])
    return result

def convert_to_format(tree):
    result = ""
    for i in tree:
        result += f"{i[0]}->{i[1]}:{i[2]}\n"
    return result

inputs = read_file("rosalind_ba7d.txt")
size = int(inputs[0])
matrix = create_matrix_special(inputs[1:],size)
edge_matrix = create_tree(matrix,size)
create_result = convert_to_format(two_way(edge_matrix))
with open('rosalind_ba7d_final.txt', 'w') as f:
    f.write(create_result)