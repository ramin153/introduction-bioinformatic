import sys
def read_file(file_naem):
    with open(file_naem, 'r') as f:
        lines = list(map(str.strip,f.readlines()))
    return lines

def map_alphabet(charechter):
    if charechter == 'A':
        return 0
    elif charechter == 'C':
        return 1
    elif charechter == 'G':
        return 2
    else:
        return 3
def rev_mapping(number):
    if number == 0:
        return 'A'
    elif number == 1:
        return 'C'
    elif number == 2:
        return 'G'
    else:
        return 'T'

def split_data(data):
    save =  [ i.split("->") for i in data]
    return [[int(i[0]),i[1]] for i in save]
def create_item(item,size,next_node,pre1,pre2):
    dp = []
    if item != None:
        for i in item:
            convert_char = map_alphabet(i)
            new_char = [[sys.maxsize,None,None] for i in range(4)]
            new_char[convert_char] = [0,convert_char,convert_char]
            dp.append(new_char)
    else:
        dp = [ [ [sys.maxsize , None,None]  for j in range(4)]  for i in range(size) ]

    return [dp,next_node,pre1,pre2]
def find_pre(edge,node):
    val = []
    for i in edge:
        if i[1] == node:
            val.append(i[0])

    return val
def find_next_node(edges,node):
    for i in edges:
        if i[0] == node:
            return i[1]
    return None
def create_special_matrix(data,size):
    matrix = dict()

    size_string = len(data[0][1])
    edge = []

    for i in range(size):
        edge.append([i,data[i][0]])
        matrix[i] = create_item(data[i][1],size_string,int(data[i][0]),None,None)
    for i in range(size,2*size - 2):
        edge.append([int(data[i][1]), int (data[i][0])])

    for i in range(size,2*size - 1):
        pre = find_pre(edge,i)
        nex_node = None

        nex_node = find_next_node(edge,i)

        save =  create_item(None,size_string,nex_node,pre[0],pre[1])
        matrix[i] = save
    # print("====")
    # for i in range(len(matrix)):
    #     print(i, matrix[i][1], matrix[i][2], matrix[i][3])
    return matrix,edge

def caclute_two_item_cell(pre,i):
    min_val, pre_index = sys.maxsize, -1

    for j in range(4):
        add_val = 0 if i == j else 1
        add_val += pre[j][0]
        if min_val > add_val :
            min_val = add_val
            pre_index = j

    return min_val,pre_index

def calcute_item(pre1,pre2):
    result = []
    for i in range(4):

        min_val1,pre_index1 = caclute_two_item_cell(pre1,i)

        min_val2, pre_index2 = caclute_two_item_cell( pre2, i)

        val = [min_val1+min_val2, pre_index1, pre_index2]

        result.append(val)

    return result
def compute_dp_inner(row,pre_1,pre_2):
    row_item = row[0]
    pre_1_item = pre_1[0]
    pre_2_item = pre_2[0]

    for i in range(len(row_item)):

        pre_1_item_i = pre_1_item[i]
        pre_2_item_i = pre_2_item[i]
        row_item[i] = calcute_item(pre_1_item_i, pre_2_item_i)

    return row_item
def compute_dp(matrix,size,size_string):

    for i in range(0,2*size - 1):

        row = matrix.get(i)
        if row[2] == None:
            continue
        pre_1= matrix.get(row[2])
        pre_2 = matrix.get(row[3])

        row[0] = compute_dp_inner(row,pre_1,pre_2)

    return matrix
def compute_string_first(i,matrix):
    node_i = matrix.get(i)
    string = ""
    sum_small = 0
    for j in range(len(node_i[0])):
        min_val = sys.maxsize;
        min_index = -1
        for k in range(4):
            if min_val > node_i[0][j][k][0]:
                min_index = k
                min_val = node_i[0][j][k][0]
        sum_small += min_val
        string += rev_mapping(min_index)
    return string,sum_small

def compute_string(i,matrix,string_dict):
    node_i = matrix.get(i)
    parent = node_i[1]
    next_node = matrix.get(parent)
    next_node_string = string_dict.get(parent)
    which_one = -1
    if next_node[2] == i:
        which_one = 1
    elif next_node[3] == i:
        which_one = 2

    string = ""
    for j in range(len(next_node_string)):
        char = map_alphabet(next_node_string[j])
        char_maped = next_node[0][j][char][which_one]
        string += rev_mapping(char_maped)
    return string

def back_track(matrix,size):
    strings = dict()
    strings[2*size - 2] , min = compute_string_first(2*size - 2,matrix)
    # print("====")
    # for i in range(len(matrix)):
    #     print(i,matrix[i][1],matrix[i][2],matrix[i][3])
    for i in range(2*size - 3,-1,-1):
        if matrix[i][2] == None:
            continue
        s = compute_string(i,matrix,strings)
        strings[i] = s

    return strings,min

def back_track_rec(matrix,parent,par_sting,leaf,side,dict_string):
    if leaf == None:
        return
    string = ""

    for i in range(len(par_sting)):
        char_index = map_alphabet(par_sting[i])
        char = parent[0][i][char_index]
        choes_char_leaf = char[side]
        string += rev_mapping(choes_char_leaf)
    dict_string[leaf] = string
    leaf = matrix[leaf]
    back_track_rec(matrix,leaf,string,leaf[2],1,dict_string)
    back_track_rec(matrix, leaf,string, leaf[3], 2, dict_string)
    return dict_string

def back_track_2(matrix,size):
    strings = dict()
    strings[2 * size - 2], min = compute_string_first(2 * size - 2, matrix)
    root = matrix[2 * size - 2]
    back_track_rec(matrix,root,strings[2 * size - 2],root[2],1,strings)
    back_track_rec(matrix, root,strings[2 * size - 2], root[3], 2, strings)
    return strings,min

def ham_distance(s1,s2):
    sum = 0
    for i in range(len(s1)):
        sum += 0 if s1[i] == s2[i] else 1
    return sum
def write_format(edges,strings):
    result = ""
    test = 0
    # print(len(edges))
    for i in edges:
        s1 = strings.get(int(i[0]))
        s2 = strings.get(int(i[1]))
        ham = ham_distance(s1,s2)


        result += s1 + '->' +s2 +":"+str(ham)+"\n"
        result += s2 + '->' + s1 + ":" + str(ham) + "\n"

    return result
file = read_file("rosalind_ba7f.txt")
size = int(file[0])
edge_save = split_data(file[1:])
matrix,edge = create_special_matrix(edge_save,size)
size_string = len(file[1][1])
matrix = compute_dp(matrix,size,size_string)
strings,min = back_track(matrix,size)
for i in range(size):
    strings[i] = edge_save[i][1]



with open('rosalind_ba7f_final.txt', 'w') as f:

    f.write(str(min) + "\n"+write_format(edge,strings))