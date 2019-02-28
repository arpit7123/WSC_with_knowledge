import json
import ast

def merge_prob_problem():
    with open('scr_wsc_prob.json') as f:
        wsc_proabablities = json.load(f)

    with open('scr_wsc285.json') as f:
        problems = json.load(f)

    output = []
    for i in range(0,len(problems)): 
        prob = problems[i]
        obj = {}
        obj['substitution'] = prob["substitution"]
        obj['correctness'] = prob["correctness"]
        obj['question_id'] = prob["question_id"]
        obj['score'] = wsc_proabablities[i]
        output.append(obj)
    

    with open('wsc_scr_scores.json', 'w') as outfile:
        json.dump(output, outfile)

def merge_probability_finalprob():
    all_probs_file = 'inputs/wsc_problems_final.json'
    f = open(all_probs_file,"r")
    all_probs = f.read()
    problems = ast.literal_eval(all_probs)
    
    with open('scr_wsc_prob.json') as f:
        scr_scores = json.load(f)
    
    j = 0
    for i in range(0,len(problems)): 
        prob = problems[i]
        prob["scr_score"] ={'choice1': scr_scores[j], 'choice2': scr_scores[j+1]}
        j = j+2
        
    with open('final_problems.json', 'w') as outfile:
        json.dump(problems, outfile)
    
def calculate_285():
    with open('final_problems.json') as f:
        problems = json.load(f)
        
    correct = 0
    incorrect = 0
    for i in range(0,len(problems)): 
        prob = problems[i]
        isChoice1 = False
        isChoice2 = False
        
        if prob['choice1'].lower() == prob['ans'].lower():
            isChoice1 = True
        else:
            isChoice2 = True
            
        if prob['scr_score']['choice1'] < prob['scr_score']['choice2']:
            if isChoice2:
                correct = correct + 1
            else:
                incorrect = incorrect + 1
        else:
            if isChoice1:
                correct = correct + 1
            else:
                incorrect = incorrect + 1
    
    print("Correct : ", correct)
    print("Incorrect : ", incorrect)
    print("Total: ", len(problems))
   
def calculate_273():
    with open('wsc273_scr_scores.json') as f:
        problems = json.load(f)
        
    correct = 0
    incorrect = 0
    j = 0
    for i in range(0, len(problems)): 
        if j > len(problems) - 1:
            break
        prob_choice1 = problems[j]
        prob_choice2 = problems[j+1]
        isChoice1 = prob_choice1["correctness"]
        isChoice2 = prob_choice2["correctness"]
            
        if prob_choice1['score'] < prob_choice2['score']:
            if isChoice2:
                correct = correct + 1
            else:
                incorrect = incorrect + 1
        else:
            if isChoice1:
                correct = correct + 1
            else:
                incorrect = incorrect + 1
        j = j+2
        
    
    print("Correct : ", correct)
    print("Incorrect : ", incorrect)
    print("Total: ", len(problems)/2)
    
if __name__ == "__main__":    
    calculate_273()
    