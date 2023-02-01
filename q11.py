
#https://teaching.healthtech.dtu.dk/22110/index.php/Codon_list
count = {"I":3,"L":6,"V":4,"F":2,"M":1,"C":2,"A":4,"G":4,"P":4,"T":4,
         "S":6,"Y":2,"W":1,"Q":2,"N":2,"H":2,"E":2,"D":2,"K":2,"R":6}

input_file = ""
with open('rosalind_mrna.txt', 'r') as f:
    input_file = f.readline().strip()

result = 1
for i in input_file:

    result = (result * count.get(i)) % 1_000_000

result = (result * 3) % 1_000_000 # stop codon
with open('rosalind_mrna_output.txt', 'w') as f:
    f.write(str(result))