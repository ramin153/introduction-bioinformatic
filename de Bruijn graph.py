
def read_file(file_naem):
    with open(file_naem, 'r') as f:
        lines = list(map(str.strip,f.readlines()))
    return lines


file = "rosalind_pcov.txt"
print(len(read_file(file)))