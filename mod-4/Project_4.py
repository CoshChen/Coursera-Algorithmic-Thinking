"""
Author: Ko-Shin Chen
Algorithmic Thinking (Part 2)
Project 4: Computing Alignments of Sequences
"""
import random

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    The function returns a dictionary of dictionaries whose entries are 
    indexed by pairs of characters in alphabet.
    """
    
    score_matrix = {}
    
    for row_char in alphabet:
        score_matrix[row_char] = {}
        for col_char in alphabet:
            if row_char == col_char:
                score_matrix[row_char][col_char] = diag_score
            else:
                score_matrix[row_char][col_char] = off_diag_score
                
    score_matrix['-'] = {}
    
    for char in alphabet:
        score_matrix['-'][char] = dash_score
        score_matrix[char]['-'] = dash_score
        
    score_matrix['-']['-'] = dash_score
    
    return score_matrix
    
    

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    The function computes either a global alignment matrix (list of lists) or 
    a local alignment matrix depending on the value of global_flag.
    """
    
    len_x = len(seq_x)
    len_y = len(seq_y)
        
    ali_matrix = [[0 for _ in range(len_y+1)] for _ in range(len_x+1)]
        
    for row in range(1,len_x+1):
        ali_matrix[row][0] = ali_matrix[row-1][0] + scoring_matrix[seq_x[row-1]]['-']
        
        if not global_flag and ali_matrix[row][0] < 0:
            ali_matrix[row][0] = 0
            
    for col in range(1,len_y+1):
        ali_matrix[0][col] = ali_matrix[0][col-1] + scoring_matrix['-'][seq_y[col-1]]
        
        if not global_flag and ali_matrix[0][col] < 0:
            ali_matrix[0][col] = 0
            
    for row in range(1,len_x+1):
        for col in range(1, len_y+1):
            score1 = ali_matrix[row-1][col-1] + scoring_matrix[seq_x[row-1]][seq_y[col-1]]
            if not global_flag and score1 < 0:
                score1 = 0
            
            score2 = ali_matrix[row-1][col] + scoring_matrix[seq_x[row-1]]['-']
            if not global_flag and score2 < 0:
                score2 = 0 
            
            score3 = ali_matrix[row][col-1] + scoring_matrix['-'][seq_y[col-1]]
            if not global_flag and score3 < 0:
                score3 = 0 
            
            ali_matrix[row][col] = max(score1, score2, score3)
                
    return ali_matrix
        


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    This function computes a global alignment of seq_x and seq_y using the 
    global alignment matrix alignment_matrix.
    The function returns a tuple of the form (score, align_x, align_y) where 
    score is the score of the global alignment align_x and align_y.
    """
    
    score = 0
    align_x = ''
    align_y = ''
    
    row = len(seq_x)
    col = len(seq_y)
    
    while row != 0 and col !=0:
        if alignment_matrix[row][col] == alignment_matrix[row-1][col-1] + scoring_matrix[seq_x[row-1]][seq_y[col-1]]:
            align_x = seq_x[row-1] + align_x
            align_y = seq_y[col-1] + align_y
            score += scoring_matrix[seq_x[row-1]][seq_y[col-1]]
            row -= 1
            col -= 1
            
        else:
            if alignment_matrix[row][col] == alignment_matrix[row-1][col] + scoring_matrix[seq_x[row-1]]['-']:
                align_x = seq_x[row-1] + align_x
                align_y = '-' + align_y
                score += scoring_matrix[seq_x[row-1]]['-']
                row -= 1
                
            else:
                align_x = '-' + align_x
                align_y = seq_y[col-1] + align_y
                score += scoring_matrix['-'][seq_y[col-1]]
                col -= 1
                
    while row != 0:
        align_x = seq_x[row-1] + align_x
        align_y = '-' + align_y
        score += scoring_matrix[seq_x[row-1]]['-']
        row -= 1
        
    while col != 0:
        align_x = '-' + align_x
        align_y = seq_y[col-1] + align_y
        score += scoring_matrix['-'][seq_y[col-1]]
        col -= 1
        
    return (score, align_x, align_y)
    


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    This function computes a local alignment of seq_x and seq_y using the 
    local alignment matrix alignment_matrix.
    The function returns a tuple of the form (score, align_x, align_y) where 
    score is the score of the optimal local alignment align_x and align_y.
    """
    
    row = 0
    col = 0
    maximum = 0
    
    for id_x in range(len(seq_x)+1):
        for id_y in range(len(seq_y)+1):
            if alignment_matrix[id_x][id_y] >= maximum:
                row = id_x
                col = id_y
                maximum = alignment_matrix[id_x][id_y]
                
                
    score = 0
    align_x = ''
    align_y = ''
    
    while row != 0 and col !=0 and alignment_matrix[row][col] != 0:
        if alignment_matrix[row][col] == alignment_matrix[row-1][col-1] + scoring_matrix[seq_x[row-1]][seq_y[col-1]]:
            align_x = seq_x[row-1] + align_x
            align_y = seq_y[col-1] + align_y
            score += scoring_matrix[seq_x[row-1]][seq_y[col-1]]
            row -= 1
            col -= 1
            
        else:
            if alignment_matrix[row][col] == alignment_matrix[row-1][col] + scoring_matrix[seq_x[row-1]]['-']:
                align_x = seq_x[row-1] + align_x
                align_y = '-' + align_y
                score += scoring_matrix[seq_x[row-1]]['-']
                row -= 1
                
            else:
                align_x = '-' + align_x
                align_y = seq_y[col-1] + align_y
                score += scoring_matrix['-'][seq_y[col-1]]
                col -= 1
        
    return (score, align_x, align_y)



#############################################################################
# For Application

def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    The function returns a dictionary scoring_distribution that represents an 
    un-normalized distribution generated by computing scores of local alignment 
    between seq_x and randomly reparametrized seq_y. 
    """
    
    scoring_distribution = {}
    time = 0
    
    while time < num_trials:
        list_y = list(seq_y)
        random.shuffle(list_y)
        rand_y = ''.join(list_y)
        local_alignment_matrix = compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        result = compute_local_alignment(seq_x, rand_y, scoring_matrix, local_alignment_matrix)
        
        if scoring_distribution.has_key(result[0]):
            scoring_distribution[result[0]] += 1.0
        else:
            scoring_distribution[result[0]] = 1.0
            
        time += 1
        
    return scoring_distribution
    
    
    
def check_spelling(checked_word, dist, word_list):
    """
    The function iterates through word_list and returns the set of all words 
    that are within edit distance dist of the string checked_word.
    """
    
    len_checked = len(checked_word)
    alphabet = ''.join(chr(i) for i in range(ord('a'), ord('z')+1))
    scoring_matrix = build_scoring_matrix(alphabet, 2, 1, 0)
    ans = set([])
    
    for word in word_list:
        global_ali_mx = compute_alignment_matrix(checked_word, word, scoring_matrix, True)
        score = compute_global_alignment(checked_word, word, scoring_matrix, global_ali_mx)
        
        if len_checked + len(word) - score[0] <= dist:
            ans.add(word)
            
    return ans