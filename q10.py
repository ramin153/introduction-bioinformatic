import sys
def creat_matrix(n,m,p,t):
    return [[[ [sys.maxsize * -1 for z in range(t)  ] for k in range(p)] for j in range(m)] for i in range(n)]
def create_path_matrix(n,m,p,t):
    return [[[ [ [0, 0, 0, 0] for z in range(t)  ] for k in range(p)] for j in range(m)] for i in range(n)]
def init_matrix(n,m,p,t):
    matrix = creat_matrix(n,m,p,t)
    path = create_path_matrix(n,m,p,t)
    for i in range(1,n):
        matrix[i][0][0][0] = -i*3
        path[i][0][0][0] = [i-1,0,0,0]
    for i in range(1,m):
        matrix[0][i][0][0] = -i*3
        path[0][i][0][0] = [ 0,i-1, 0, 0]
    for i in range(1,p):
        matrix[0][0][i][0] = -i*3
        path[0][0][i][0] = [0, 0, i - 1, 0]
    for i in range(1,t):
        matrix[0][0][0][i] = -i*3
        path[0][0][0][i] = [0, 0, 0, i - 1]
    matrix[0][0][0][0] = 0
    return matrix,path

def calculate_diff(chars):
    if len(chars) == 0:
        return 0,[]
    calcualte = chars[0]
    sum_val,others = calculate_diff(chars[1:])
    return sum([-1 if   calcualte != i else 0 for i in chars[1:]])+sum_val,chars


def calculate_matrix_value(i,j,k,z,line_1,line_2,line_3,line_4,index):
    char_1 = line_1[i-1] if (index&1) == 1 and i != 0 else '-'
    char_2 = line_2[j-1] if (index&2) == 2 and j != 0 else '-'
    char_3 = line_3[k-1] if (index&4) == 4 and k != 0else '-'
    char_4 = line_4[z- 1] if (index & 8) == 8 and z !=0 else '-'

    chars = [char_1,char_2,char_3,char_4 ]

    sum_val,chars = calculate_diff(chars)
    return sum_val

def gap_or_in(i,help_i):
    if i == help_i:
        return "gap"
    else :
        return "in"

def get_matrix_value(i,j,k,z,matrix,index):
    help_1 = i-1 if (index&1) == 1 and i != 0 else i
    help_2 = j-1 if (index & 2) == 2 and j != 0else j
    help_3 = k-1 if (index & 4) == 4 and k != 0 else k
    help_4 = z-1 if (index & 8) == 8 and z != 0 else z


    save =  matrix[help_1][help_2][help_3][help_4]
    return save,[help_1,help_2,help_3,help_4]

def  multiple_alignment(line_1,line_2,line_3,line_4):
    n = len(line_1) + 1
    m = len(line_2) + 1
    p = len(line_3) + 1
    t = len(line_4) + 1

    distance_matrix,path = init_matrix(n,m,p,t)

    for i in range(0,n):
        for j in range(0,m):
            for k in range(0,p):
                for z in range(0,t):
                    if (i == j and j == k and k == z and z == 0):
                        continue
                    result = sys.maxsize * -1
                    location_result = [i,j,k,z]
                    for index in range(1,16):
                        save = calculate_matrix_value(i,j,k,z,line_1,line_2,line_3,line_4,index)
                        debug,location = get_matrix_value(i,j,k,z,distance_matrix,index)
                        save += debug
                        if result < save:
                            result = save
                            location_result = location
                    distance_matrix[i][j][k][z] = result
                    path[i][j][k][z] = location_result
                    #print(distance_matrix[i][j][k][z],i,j,k,z)


    return distance_matrix,path,distance_matrix[n-1][m-1][p-1][t-1]




def help_tacer(dm,i,j,k,z):
    max_val = sys.maxsize*-1
    locations = []
    for index in range(1,16):
        new_max_val,new_locations = get_matrix_value(i,j,k,z,dm,index)
        if new_max_val > max_val:
            max_val = new_max_val
            locations = new_locations
    return locations


def trace(path,s1,s2,s3,s4):
    n, m, p, t = len(s1),len(s2),len(s3),len(s4)
    line_1,line_2,line_3,line_4 = "","","",""
    while n != 0 or m !=0 or p != 0 or t !=0 :
        locations = path[n][m][p][t]
        if n == locations[0]:
            line_1 = "-"+line_1
        else:
            line_1 = s1[locations[0]] + line_1

        if m == locations[1]:
            line_2 = "-"+line_2
        else:
            line_2 = s2[locations[1]] + line_2

        if p == locations[2]:
            line_3 = "-"+line_3
        else:
            line_3 = s3[locations[2]] + line_3

        if t == locations[3]:
            line_4 = "-"+line_4
        else:
            line_4 = s4[locations[3]] + line_4
        n,m,p,t = locations
    return [line_1,line_2,line_3,line_4]
inputs = []

with open('rosalind_mult.txt', 'r') as f:
    lines = f.readlines()
    inputs = [lines[i].strip() for i in range(1,len(lines),2)]


dm,path,final = multiple_alignment(inputs[0],inputs[1],inputs[2],inputs[3])
result = trace(path,inputs[0],inputs[1],inputs[2],inputs[3])

with open('rosalind_mult_output.txt', 'w') as f:
    f.write(str(final)+"\n"+result[0]+"\n"+result[1]+"\n"+result[2]+"\n"+result[3])
