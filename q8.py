def create_matrix_distance(n:int,m:int):
    return [[[(i+j)*(-100),""] for i in range(m)] for j in range(n)]

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
    return int(matrix[i][j])

def local_aligment(sentence_1,sentence_2,matrix,guide):
    n = len(sentence_1)
    m = len(sentence_2)
    local_max = 0
    local_matrix = create_matrix_distance(n+1,m+1)
    for i in range(1,n+1):
        for j in range(1,m+1):
            match = get_score(matrix,guide,sentence_1[i-1],sentence_2[j-1]) +local_matrix[i-1][j-1][0]
            dele = -5 + local_matrix[i][j-1][0]
            insert = -5 + local_matrix[i-1][j][0]

            max_val = max(match,dele,insert)
            local_matrix[i][j][0] = max_val
            if max_val < 0:
                local_matrix[i][j][0] = 0
            elif match == max_val:
                local_matrix[i][j][1] = "M"
            elif dele == max_val:
                local_matrix[i][j][1] = "D"
            else:
                local_matrix[i][j][1] = "I"

            local_max = max(local_matrix[i][j][0],local_max)

    return local_matrix,local_max

def create_sentence(local_matrix,local_max):
    n = len(local_matrix)
    m = len(local_matrix[0])
    x,y = 0,0
    end = False
    for i in range(n-1,0,-1):
        for j in range(m-1,0,-1):

            if local_max == local_matrix[i][j][0]:
                x,y =i,j
                end = True
                break
        if end:
            break
    first = ""
    seconde = ""
    while local_matrix[x][y][0] != 0 and not (x ==0 or y == 0) :
        if local_matrix[x][y][1] == "M":
            x -=1
            y -=1
            first = line_1[x] + first
            seconde = line_2[y] + seconde

        elif local_matrix[x][y][1] == "I":
            x -= 1
            first = line_1[x] + first
        else:
            y -= 1
            seconde = line_2[y] + seconde

    return first,seconde

input = []
with open('rosalind_loca.txt', 'r') as f:
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

line_1 ,line_2 = input[0],input[1]
matrix ,guide = read_scoring_matrix("PAM250.txt")
local , final = local_aligment(line_1,line_2,matrix,guide)

first ,second = create_sentence(local,final)


with open('rosalind_loca_output.txt', 'w') as f:
    f.write(str(final)+"\n"+first+"\n"+second)