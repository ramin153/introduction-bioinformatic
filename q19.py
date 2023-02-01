import sys

class MYTree :
    def __init__(self,node_name):
        self.name = node_name
        self.neighbor = []

    def add_edge(self,node,weight):
        self.neighbor.append([node,weight])
        node.inner_add(self,weight)

    def inner_add(self,node,weight):
        self.neighbor.append([node, weight])

    def path_to_k(self,point_see,k):
        if k == self.name:
            return [],True
        for i in self.neighbor:
            if i[0].name not in point_see:
                result,is_find = i[0].path_to_k(point_see + [self.name],k)
                if is_find :
                    return [i] + result ,True
        return None,False

    def remov_edge(self,oldNode):
        for i in range(len(self.neighbor)):
            item = self.neighbor[i]
            if item[0].name == oldNode.name:
                save = self.neighbor.pop(i)

                return


    def x_distance(self,cost,limbo,limbo_node_name,node_name,path):

        for i in range(len(path)):
            item = path[i]
            if cost < item[1]:


                item[0].remov_edge(self)
                self.remov_edge(item[0])
                self.my_print([])
                newNode = MYTree(node_name)
                limbo_node = MYTree(limbo_node_name)

                newNode.add_edge(limbo_node,limbo)
                newNode.add_edge(self,item[1] - cost)
                newNode.add_edge(item[0],cost)
                self.my_print([])
                break
            cost -= item[1]

    def find_node(self,name,seen):
        if self.name == name:
            return True,self
        for i in self.neighbor:
            if i[0].name not in seen:
                item =  i[0]

                is_find,node = item.find_node(name,seen + [self.name])

                if is_find:
                    return True,node
        return  False,None
    def add_vertix(self,i,j,k,x,limbo,new_node_name):

        garbage,node = self.find_node(j,[])

        path,garbage = node.path_to_k([],k)
        self.my_print([])
        node.x_distance(x,limbo,i,new_node_name,path)

    def my_print(self,seen):
        if seen == []:
            print("===========")
        for i in self.neighbor:
            if i[0].name not in seen:
                print(self.name,i[0].name,i[1])

                i[0].my_print(seen+[i[0].name])

    def creat_list(self,seen):

        result = []
        for i in self.neighbor:
            if i[0].name not in seen:
                result += [[self.name,i[0].name,i[1]]]
                result += [[i[0].name, self.name, i[1]]]

                result += i[0].creat_list(seen+[i[0].name])
        return result

    def __str__(self):
        return str(self.name)



def read_file(file_naem):
    with open(file_naem, 'r') as f:
        lines = list(map(str.strip,f.readlines()))
    return lines

def create_matrix(lines,size):
    return [[int(j) for j in list(map(int,lines[i].split() ))] for i in range(size)]

def limb_Length(matrix,i,size):

    result = sys.maxsize
    neighbor = -1
    dest = -1
    for j in range(size):
        if i != j:
            dij = matrix[i][j]
            for k in range(size):
                if i != k and k != j:
                    dik = matrix[i][k]
                    djk = matrix[j][k]
                    if result > (dij+dik-djk)/2 :
                        result = (dij+dik-djk)/2
                        neighbor = j
                        dest = k
    return result,neighbor,dest

def path_to_k(tree,now,k):
    for i in range(len(tree)):

        item = tree[i]
        if item[0] == now or item[1] == now:
            if item[0] == k or item[1] == k:
                return True,[item]
            help_item =  item[:2]
            help_now =  help_item[ help_item.index(now) -1 ]
            isT , save = path_to_k(tree[:i]+ tree[i+1:] , help_now, k)
            if isT:
                return True, save + [item]
    return False,None


def remove_edge(path,start,cost):
    for i in range(len(path)):
        item = path[i]
        if item[0] == start or item[1] == start:
            if cost < item[2]:
                return item,start,cost
            help_item = item[:2]
            help_start = help_item[help_item.index(start) - 1]

            return remove_edge(path[:i]+path[i+1:],help_start,cost - item[2])
    return False,False,False

def add_new_vector(tree,i,j,k,x,limb,new_node):
    garbage,path = path_to_k(tree,j,k)
    edge , start , remain_cost = remove_edge(path,j,x)
    for t in range(len(tree)):
        if tree[t] == edge:
            tree.pop(t)
            tree.append([start,new_node,remain_cost])
            tree.append([i, new_node, limb])
            help_edge = edge[:2]
            other_v = help_edge[help_edge.index(start) - 1]
            tree.append([other_v, new_node,edge[2] - remain_cost])
            break
    return tree

def additive_phylogeny(matrix,size):
    if size  == 2:
        # newTree = MYTree(0)
        # newTree2 = MYTree(1)
        # newTree.add_edge(newTree2,matrix[0][1])
        # return newTree,len(matrix)
        return [[0,1,matrix[0][1]]],len(matrix)

    limb,j,k = limb_Length(matrix,size-1,size)



    for t in range(size-1):
        matrix[size-1][t] -= limb
        matrix[t][size-1] -= limb

    x = matrix[j][size - 1]
    tree,node_name = additive_phylogeny(matrix,size-1)

    #tree.add_vertix(size - 1,j,k,x,limb,node_name)

    tree = add_new_vector(tree,size - 1,j,k,x,limb,node_name)

    return tree,node_name + 1
def is_edge_prior (item1,item2):
    if item1[0] < item2[0]:
        return True
    return False

def sort_tree(tree):
    result = []
    for i in tree:
        isAdded = False
        for index in range(len(result)):
            j = result[index]
            if is_edge_prior(i,j):
                result.insert(index,i)
                isAdded = True
                break
        if not isAdded:
            result.append(i)
    return result
def convert_to_format(tree):
    result = ""
    for i in tree:
        result += f"{i[0]}->{i[1]}:{int(i[2])}\n"
    return result

def help_print_tree(tree):
    two_way_grahp = tree + [ [i[1],i[0],i[2]] for i in tree]
    result = sort_tree(two_way_grahp)
    return convert_to_format(result)

def help_print_MYtree(tree):

    result = sort_tree(tree)
    return convert_to_format(result)

inputs = read_file("rosalind_ba7c.txt")
size = int(inputs[0])
matrix = create_matrix(inputs[1:],size)



tree,last = additive_phylogeny(matrix,size)
# result = tree.creat_list([])
# with open('rosalind_ba7c_final.txt', 'w') as f:
#     f.write(help_print_MYtree(result))

with open('rosalind_ba7c_final.txt', 'w') as f:
    f.write(help_print_tree(tree))

