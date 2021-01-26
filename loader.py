file1 = open('Vocabulary_Lists/three_star.txt', 'r') 
lines = file1.readlines() 

# example
# 1.	abandon[ә'bændәn]vt.丢弃,放弃,抛弃
noun_list = []
type_vocabulary = 'n'

for line in lines: 
    rear_bracket_split = line.split("]")

    num_split = rear_bracket_split[0].split(".")

    front_bracket_split = num_split[1].split("[")

    for rear_part in rear_bracket_split[1]:
        if type_vocabulary in rear_part:
            noun_list.append(front_bracket_split[0].strip())

import random
top_50_random = random.sample(noun_list, 50)

print("Noun typle:")

for word in top_50_random:
    # print(word)
    print( '{{pause}}{{pause}}{{pause}}{{pause}}' + word)