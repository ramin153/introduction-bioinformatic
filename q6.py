
input = []
with open('rosalind_edta.txt', 'r') as f:
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


def create_matrix_distance(n:int,m:int):
    return [[[i+j,""] for i in range(m)] for j in range(n)]

def edit_distance_alignment(line_1,line_2):
    size_1 = len(line_1)+1
    size_2 = len(line_2)+1

    matrix_distance = create_matrix_distance(size_1,size_2)
    for i in range(1,size_1):
        for j in range(1,size_2):
            move = ""
            diff = size_2*size_1
            if line_1[i-1] == line_2[j-1]:
                diff = matrix_distance[i-1][j-1][0]
                move = "match"
            if matrix_distance[i][j-1][0] + 1 < diff:
                diff = matrix_distance[i][j-1][0] + 1
                move = "insert"
            if matrix_distance[i-1][j][0] + 1 < diff:
                diff = matrix_distance[i-1][j][0] + 1
                move = "delete"
            if matrix_distance[i-1][j-1][0] + 1 < diff:
                diff = matrix_distance[i-1][j-1][0] + 1
                move = "mismatch"

            matrix_distance[i][j][0] = diff
            matrix_distance[i][j][1] = move
    return matrix_distance,matrix_distance[size_1-1][size_2-1][0]






def create_sentence(matrix,line_1,line_2):
    n = len(line_1)
    m = len(line_2)

    first = ""
    seconde = ""

    while m != 0 or n != 0:

        if matrix[n][m][1] in ["match","mismatch"] :
            m -=1
            n -=1
            first = line_1[n] + first
            seconde = line_2[m] + seconde

        elif matrix[n][m][1] == "delete":
            n -= 1
            first = line_1[n] + first
            seconde = "-" + seconde
        else:
            m -= 1
            first = "-" + first
            seconde = line_2[m] + seconde
    return first,seconde


mat,final = edit_distance_alignment(input[0], input[1])
result_1,result_2 = create_sentence(mat,input[0],input[1])
with open('rosalind_edta_output.txt', 'w') as f:
    f.write(str(final)+"\n"+result_1+"\n"+result_2)