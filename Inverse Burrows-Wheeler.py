def read_file(file_naem):
    with open(file_naem, 'r') as f:
        lines = list(map(str.strip,f.readlines()))
    return lines
def compute_inverse(input):
    size = len(input)
    result = [ "" for i in range(size)]

    for i in range(size):
        result = sorted([ input[j] + result[j] for j in range(size) ])

    final = result[0]
    return final[1:]+final[0]

file = "rosalind_ba9j"
input = [i for i in read_file(file+".txt")[0]]

with open(file+"_output.txt", 'w') as f:

    f.write((compute_inverse(input)))
