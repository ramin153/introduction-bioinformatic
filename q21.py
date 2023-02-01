import sys
def read_file(file_naem):
    with open(file_naem, 'r') as f:
        lines = list(map(str.strip,f.readlines()))
    return lines
def create_matrix(lines,size):
    return [[int(j) for j in list(map(int,lines[i].split() ))] for i in range(size)]

def create_matrix_special(inputs,size):
    inputs = create_matrix(inputs,size)
    return [[i,[inputs[i][j] for j in range(size) ]] for i in range(size)]

def find_min(matrix,size):
    nodei = -1
    nodej = -1
    result = sys.maxsize

    for i in range(size):
        for j in range(size):
            if i != j:
                min = matrix[i][j]
                if result > min:
                    result = min
                    nodej = j
                    nodei = i
    return nodei,nodej

def creat_star(matrix,size,R):
    result =[ [0 if i == j else (size - 2) * matrix[j][1][i] - (R[i] + R[j]) for i in range(size)] for j in range(size)]
    return result

def create_R(matrix,size):
    R = [ sum([matrix[i][1][j] for j in range(size)]) for i in range(size)]
    return R


def  add_edge(matrix,size,i,j,R,node_name):

    if R[j] > R[i]:
        j,i=i,j

    delta = (R[i]-R[j])/((size-2))
    dij = matrix[i][1][j]
    Siu = 1/2 * (dij + delta)
    Sju = 1/2 * (dij - delta)
    if Sju < 0:
        print("fuck")

    return [[node_name,matrix[i][0],Siu],[node_name,matrix[j][0],Sju]]
def combine_vertice(matrix,i,j,size,node_name):
    node_i = matrix[i]
    node_j = matrix[j]
    dij = matrix[i][1][j]
    row_one = [node_name,[0]]

    for t in range(size):
        if t == i or t == j:
            continue
        row_one[1].append((node_i[1][t]+node_j[1][t]-dij)/2)
    new_matrix = [row_one]

    for t in range(len(matrix)):
        if t == i or t == j:
            continue

        old_row = matrix[t]
        new_row = [old_row[0]]
        new_distance_t = [i for i in old_row[1]]

        if i > j:
            i, j = j, i

        new_distance_t.pop(j)
        new_distance_t.pop(i)

        index = len(new_matrix)
        row_one_value = row_one[1][index]
        new_distance_t = [row_one_value] + new_distance_t

        index = new_distance_t.index(0)
        new_distance_t.pop(index)
        new_distance_t.insert(len(new_matrix), 0)

        new_row.append(new_distance_t)
        new_matrix.append(new_row)

    return new_matrix


def create_tree(matrix,size):
    edge = []
    node_name = size
    while len(matrix) > 2:
        R = create_R(matrix,size)
        matrix_s = creat_star(matrix,size,R)
        i,j = find_min(matrix_s,size)
        edge += add_edge(matrix,size,i,j,R,node_name)
        matrix = combine_vertice(matrix,i,j,size,node_name)
        node_name+=1
        size-=1
    edge += [[matrix[0][0],matrix[1][0],matrix[1][1][0]]]
    return edge

def two_way(graph):
    result = []
    for i in graph:
        value = f'{float(i[2]):.3f}'
        result.append([i[0],i[1],value])
        result.append([i[1], i[0], value])
    return result

def convert_to_format(tree):
    result = ""
    for i in tree:
        result += f"{i[0]}->{i[1]}:{i[2]}\n"
    return result
def is_edge_prior (item1,item2):
    if item1[0] < item2[0]:
        return True
    return False

def sort_tree(tree):
    result = []
    for i in tree:
        isAdded = False
        for index in range(len(result)):
            j = result[index]
            if is_edge_prior(i,j):
                result.insert(index,i)
                isAdded = True
                break
        if not isAdded:
            result.append(i)
    return result

inputs = read_file("rosalind_ba7e.txt")
size = int(inputs[0])
matrix = create_matrix_special(inputs[1:],size)
edge_matrix = create_tree(matrix,size)
create_result = convert_to_format(sort_tree(two_way(edge_matrix)))
with open('rosalind_ba7e_final.txt', 'w') as f:
    f.write(create_result)