"""
Author: Ko-Shin Chen
Algorithmic Thinking (Part 2)
Application 4: Applications to Genomics and Beyond
"""


import Project_4
import alg_application4_provided as provided
import math
import matplotlib.pyplot as plt

"""
Question 1
"""
seq_human = provided.read_protein(provided.HUMAN_EYELESS_URL)
seq_fly = provided.read_protein(provided.FRUITFLY_EYELESS_URL)
scoring_matrix = provided.read_scoring_matrix(provided.PAM50_URL)

local_alignment_mx = Project_4.compute_alignment_matrix(seq_human, seq_fly, scoring_matrix, False)
result = Project_4.compute_local_alignment(seq_human, seq_fly, scoring_matrix, local_alignment_mx)


print 'Score:' + str(result[0])
print 'Human: ' + result[1]
print 'Fly: ' + result[2]


"""
Question 2
"""
ali_human = result[1]
ali_fly = result[2]
seq_con = provided.read_protein(provided.CONSENSUS_PAX_URL)

ali_human = ali_human.replace('-', '')
ali_fly = ali_fly.replace('-', '')

global_alignment_mx_human = Project_4.compute_alignment_matrix(ali_human, seq_con, scoring_matrix, True) 
global_alignment_mx_fly = Project_4.compute_alignment_matrix(ali_fly, seq_con, scoring_matrix, True)

result2_human = Project_4.compute_global_alignment(ali_human, seq_con, scoring_matrix, global_alignment_mx_human)
result2_fly = Project_4.compute_global_alignment(ali_fly, seq_con, scoring_matrix, global_alignment_mx_fly)


print 'Score: ' + str(result2_human[0])
print 'Local Human: ' + result2_human[1]
print 'Consensus: ' + result2_human[2]
print
print 'Score: ' + str(result2_fly[0])
print 'Local Fly: ' + result2_fly[1]
print 'Consensus: ' + result2_fly[2]


len_human = len(result2_human[1])
len_fly = len(result2_fly[1])

count_human = 0
count_fly = 0

for idx in range(len_human):
    if result2_human[1][idx] == result2_human[2][idx]:
        count_human += 1
        
for idx in range(len_fly):
    if result2_fly[1][idx] == result2_fly[2][idx]:
        count_fly += 1

print 1.0*count_human/len_human
print 1.0*count_fly/len_fly


"""
Question 3
"""
scoring_distribution = Project_4.generate_null_distribution(seq_human, seq_fly, scoring_matrix, 1000)

plt.bar(scoring_distribution.keys(), scoring_distribution.values(), 1/1.5, color ="blue")
plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Normalized Number")
plt.show()

# Compute mean  
mean = 0.0
for score in scoring_distribution.keys():
    mean += score*scoring_distribution[score]

mean = mean/1000.0

# Compute standard deviation
dev = 0.0
for score in scoring_distribution.keys():
    dev += math.pow(score - mean, 2) * scoring_distribution[score]
    
dev = dev/1000.0
dev = math.pow(dev,0.5)

print mean
print dev


"""
Question 8
"""
word_list = provided.read_words(provided.WORD_LIST_URL)
print Project_4.check_spelling('humble', 1, word_list)
print
print Project_4.check_spelling('firefly', 2, word_list)