
def read_file(file_naem):
    with open(file_naem, 'r') as f:
        lines = list(map(str.strip,f.readlines()))
    return lines
def quality(qulaity_percent,input):
    sum_q = sum(input)* qulaity_percent
    for i in input:
        sum_q -= i
        if sum_q < 0:
            return i
    return None

file = "rosalind_asmq.txt"
input = sorted(list(map(len,read_file(file))))[::-1]

with open('rosalind_asmq_output.txt', 'w') as f:

    f.write(str(quality(0.5,input)) + " "+str(quality(0.75,input)))

