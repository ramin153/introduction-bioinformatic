def read_file(file_naem):
    with open(file_naem, 'r') as f:
        lines = list(map(str.strip,f.readlines()))
    return lines

def create_unique(items):
    help_item = dict()
    result = []

    for i in items:
        get_val = help_item.get(i)
        if get_val == None:
            get_val = 0
        get_val += 1
        result.append(i+str(get_val))
        help_item[i] = get_val

    return result

def last_to_first_create(last_col,first_col):
    last_col_item = create_unique(last_col)
    first_col_item = create_unique(first_col)
    result = []
    for i in last_col_item:
        result.append(first_col_item.index(i))

    return result

def find_last_pos(items,symbol):
    res = -1
    for i in range(len(items)):
        if items[i] == symbol:
            res = i
    if res == -1 :
        raise Exception("something went wrong")
    return res

def  BW_matching(first_col, last_col, pattern, last_to_first):
    top = 0
    bottom = len(last_col) - 1
    pattern = [i for i in pattern]
    while top <= bottom:
        if len(pattern) != 0:

            symbol = pattern.pop(len(pattern) -1)

            top_to_bottom = [last_col[i] for i in range(top,bottom+1)]

            if symbol in top_to_bottom:
                top_index  = top_to_bottom.index(symbol) + top
                bottom_index  = find_last_pos(top_to_bottom,symbol) + top
                top    = last_to_first[top_index]
                bottom = last_to_first[bottom_index]

            else:
                return 0

        else:
            return bottom - top + 1
def matching(last_col,first_col,pattern):
    last_to_first = last_to_first_create(last_col,first_col)
    result = []
    for i in pattern:
        result.append(BW_matching(first_col, last_col, i, last_to_first))
    return " ".join([str(i) for i in result])


file = "rosalind_ba9l"

inputs = read_file(file + ".txt")
last = [i for i in inputs[0]]
first = sorted([i for i in last])

with open(file+"_output.txt", 'w') as f:
    f.write(matching(last,first,inputs[1].split()))


