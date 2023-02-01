input = []
with open('rosalind_pdst.txt', 'r') as f:
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

size = len(input)
def create_quare_matrix(n:int):
    return [[0 for j in range(n)] for i in range(n)]
matrix_distance = create_quare_matrix(size)

for i in range(size):
    for j in range(size):
        matrix_distance[i][j] = sum([ 0 if input[i][k] == input[j][k] else 1 for k in range(len(input[i])) ])/len(input[i])
result = ""
for line in matrix_distance:
    for d in line:
        result += str(d) +"\t"
    result += "\n"

with open('rosalind_pdst_output.txt', 'w') as f:
    f.write(result)