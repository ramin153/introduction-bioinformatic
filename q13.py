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


def create_De_Bruijn(lines):
    node = set()
    edge = []
    for i in lines:
        help = i
        first = help[:-1]
        second = help[1:]
        node.add(first)
        node.add(second)
        edge.append((first,second))

        help = reverse_complement(i)
        first = help[:-1]
        second = help[1:]
        node.add(first)
        node.add(second)
        edge.append((first,second))
    return node,edge

def is_smaller(edge_1,edge_2):
    strat_1,end_1 = edge_1
    start_2,end_2 = edge_2
    for i in range(len(strat_1)):
        if(strat_1[i] < start_2[i]):
            return True
        elif(strat_1[i] > start_2[i]):
            return False

    for i in range(len(end_1)):
        if (end_1[i] < end_2[i]):
            return True
        elif (end_1[i] > end_2[i]):
            return False
    return True

def sort_graph(edges):
    result = []
    for i in edges:
        not_add = True
        if i in result:
            continue
        for index in range(len(result)):
            if(is_smaller(i,result[index])):
                result.insert(index,i)
                not_add = False
                break
        if not_add:
            result.append(i)
    return result
inputs = []
with open('rosalind_dbru.txt', 'r') as f:
    lines = f.readlines()
    inputs = list(map(str.strip, lines))

nodes,edges = create_De_Bruijn(inputs)

with open('rosalind_dbru_output.txt', 'w') as f:
    f.write("\n".join(["("+i[0]+", "+i[1]+")" for i in sort_graph(edges)]))
