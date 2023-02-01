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


