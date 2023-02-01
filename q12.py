def haming_distance(line_1,line_2):
    return sum([ 0 if line_1[i] == line_2[i] else 1 for i in range(len(line_1))])

def convertor(character):
    if character == 'A':
        return 'T'
    elif character == 'T':
        return 'A'
    elif character == 'G':
        return 'C'
    else:
        return 'G'

def  reverse_complement(line):
    new_line = line[::-1]
    return "".join([convertor(i) for i in new_line])

def compare_lines(line_1,line_2):
    if haming_distance(line_1,line_2) == 1:
        return True,line_1,line_2
    elif haming_distance(line_1,reverse_complement(line_2)) == 1:
        return True,line_1,reverse_complement(line_2)
    return False,line_1,line_2

def compare(lines):
    result = []
    correct = []
    wrong = []
    for i in range(len(lines)):
        add_wrong = True
        first = lines[i]
        for j in range(len(lines)):
            second = lines[j]
            if i != j and (haming_distance(first,second) == 0 or haming_distance(first,reverse_complement(second)) == 0):
                add_wrong = False
                break

        if add_wrong:
            wrong.append(lines[i])
        else:
            correct.append(lines[i])

    for i in wrong:
        for j in correct:
            state, old, right = compare_lines(i, j)
            if state:
                result.append((old, right))
                break

    return result

def create_write_format(raw_format):
    return [i[0]+"->"+i[1] for i in raw_format]


inputs = []
with open('rosalind_corr.txt', 'r') as f:
    lines = f.readlines()
    input_line = ""
    for line in lines:
       if ">" in line:
           if len(input_line) != 0 :
               inputs.append(input_line.strip())
           input_line = ""
           continue
       input_line += line.strip()
    inputs.append(input_line.strip())

with open('rosalind_corr_output.txt', 'w') as f:
    f.write("\n".join(create_write_format(compare(inputs))))

