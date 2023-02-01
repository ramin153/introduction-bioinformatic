import sys


def read_file(file_naem):
    with open(file_naem, 'r') as f:
        lines = list(map(str.strip,f.readlines()))
    return lines

def create_matrix(lines,size):
    return [[int(j) for j in list(map(int,lines[i].split() ))] for i in range(size)]

def limb_Length(matrix,i):
    size = len(matrix)
    result = sys.maxsize
    for j in range(size):
        if i != j:
            dij = matrix[i][j]
            for k in range(size):
                if i != k:
                    dik = matrix[i][k]
                    djk = matrix[j][k]
                    result = min(result,(dij+dik-djk)/2)
    return result


inputs = read_file("rosalind_ba7b.txt")
size = int(inputs[0])
i = int(inputs[1])
matrix = create_matrix(inputs[2:],size)
limb = limb_Length(matrix,i)

with open('rosalind_ba7b_final.txt', 'w') as f:
    f.write(str(int(limb)))



