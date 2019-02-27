# -*- coding: utf-8 -*-

import json
import shlex, subprocess
import sys;

parent_dir = '/Users/ash/Documents/Study/Research/psl-examples/winograd/'
PIPE= '/Users/ash/Documents/Study/Research/psl-examples/winograd/log/run.txt'
def create_psl_exec_files(coref_txt, coref_truth_txt, context_pair_txt, domain_txt, entailment_txt, commonsense_txt):

    coref_file = open('../data/coref_targets.txt', 'w')
    coref_file.write(coref_txt)

    coref_truth_file = open('../data/coref_truth.txt', 'w')
    coref_truth_file.write(coref_truth_txt)

    context_file = open('../data/context_obs.txt', 'w')
    context_file.write(context_pair_txt)

    domain_file = open('../data/domain_obs.txt', 'w')
    domain_file.write(domain_txt)

    entailment_file = open('../data/entailment_obs.txt', 'w')
    entailment_file.write(entailment_txt)

    commonsense_file = open('../data/commonsense_obs.txt', 'w')
    commonsense_file.write(commonsense_txt)

    coref_file.close()
    coref_truth_file.close()
    context_file.close()
    domain_file.close()
    entailment_file.close()
    commonsense_file.close()

def run_psl():
    process = subprocess.Popen(['/Users/ash/Documents/Study/Research/psl-examples/winograd/cli/run.sh'])
    #process = subprocess.Popen(['/home/apraka23/Winograd/WSC_with_knowledge/winograd/cli/run.sh'])
    process.wait()

def get_ans(prob, bert):
    coref_file = open('inferred-predicates/COREF.txt', 'r')
    inferred_predicate = coref_file.read()
    inferred = inferred_predicate.split('\n')
    print("inferred", inferred)
    max = sys.float_info.min
    inferred_ans = ''
    bert_isChoice1 = False;
    if bert['choice1_score'] > bert['choice2_score']:
        bert_isChoice1 = True

    for each in inferred:
        coref_score = each.split('\t')
        if len(coref_score) < 2:
            continue
    
        if max < float(coref_score[2]):
            coref_score[0] = coref_score[0][1:-1]
            coref_score[1] = coref_score[1][1:-1]
            coref_score[0] = coref_score[0].replace("\\", "")
            coref_score[1] = coref_score[1].replace("\\", "")
            # print("pronoun:", prob['pronoun'])
            # print("coref_score 0", coref_score[0])
            # print("coref_score 1", coref_score[1])
            max = float(coref_score[2])
            if prob['pronoun'].lower() == coref_score[0].lower():
                inferred_ans = coref_score[1]
            else:
                inferred_ans = coref_score[0]

    # if not (inferred_ans.lower() == bert['choice1'].lower() and not bert_isChoice1 and bert['ans'].lower() == bert['choice1'].lower()):
    #     inferred_ans = bert['choice2']

    # if not (bert['ans'].lower() ==  bert['choice2'].lower() and bert_isChoice1 and inferred_ans.lower() == bert['choice2'].lower()):
    #     inferred_ans = bert['choice1']

    return inferred_ans, max

def main():

    #probs_with_context_file = "../data/wsc_problem_psl.json"
    probs_with_context_file = "../data/new_psl_problems.json"
    bert_scores_file = open("../data/bert_wsc_problems.json", "r") 
    bert_scores = json.loads(bert_scores_file.read())
    #probs_with_context_file = "../data/test.json"
    f = open(probs_with_context_file,"r")
    all_probs = f.read()
    probs_and_context = json.loads(all_probs)

    correct = 0
    incorrect = 0
    total = 0
    isCommonsense = True

    for i in range(0, len(probs_and_context)):
        each = probs_and_context[i]
        bert = bert_scores[i]
        coref_target = each['coref_target']
        coref_target_truth = each['coref_target_truth']
        if 'context' in each:
            context = each['context']
        else: 
            context = []
        if 'entailment' in each:
            entailment = each['entailment']
        else: 
            entailment = []

        domain = each['domain']
        commonsense = each['scr_score']
        coref_txt=''
        coref_truth_txt=''
        context_pair_txt= ''
        domain_txt = ''
        entailment_txt = ''
        commonsense_txt = ''

        for coref in coref_target:
            token = coref.split('$$')
            coref_txt = coref_txt+token[0]+'\t'+token[1]+'\n'

        for coref_truth in coref_target_truth:
            token = coref_truth.split('$$')
            coref_truth_txt = coref_truth_txt+token[0]+'\t'+token[1]+'\t'+token[2]+'\n'

        for con in context:
            token = con.split('$$')
            context_pair_txt = context_pair_txt+token[0]+'\t'+token[1]+'\t'+token[2]+'\n'

        domain_txt = domain_txt+domain[0]+'\t'+'can'+'\n'
        domain_txt = domain_txt+domain[1]+'\t'+'can'+'\n'
        domain_txt = domain_txt+domain[2]+'\t'+'p'+'\n'

        if isCommonsense:
            score1 = bert["choice1_score"] / (bert["choice1_score"] + bert["choice2_score"]) 
            score2 = bert["choice2_score"] / (bert["choice1_score"] + bert["choice2_score"]) 
            commonsense_txt = commonsense_txt+bert["choice1"]+'\t'+bert["pronoun"]+'\t'+str(score1)+'\n'
            commonsense_txt = commonsense_txt+bert["choice2"]+'\t'+bert["pronoun"]+'\t'+str(score2)+'\n'

        if len(entailment) == 2:
            ch1_tokens = entailment[0].split('$$')
            ch2_tokens = entailment[1].split('$$')
            ch1_score = float(ch1_tokens[3])
            ch2_score = float(ch2_tokens[3])
            print("ch1_score was :"+str(ch1_score))
            print("ch2_score was :"+str(ch2_score))
            if ch1_score < 0.01 and ch2_score < 0.01:
               ch1_score = ch1_score * 100
               ch2_score = ch2_score * 100
            if ch1_score < 0.1 and ch2_score < 0.1:
               ch1_score = ch1_score * 10
               ch2_score = ch2_score * 10
            if ch1_score < 0.3 and ch2_score < 0.3:
               ch1_score = ch1_score * 3
               ch2_score = ch2_score * 3
            if ch1_score < 0.5 and ch2_score < 0.5:
               ch1_score = ch1_score * 2
               ch2_score = ch2_score * 2
            print("updated ch1_score :"+str(ch1_score))
            print("updated ch2_score :"+str(ch2_score))
            entailment_txt = entailment_txt+ch1_tokens[0]+'\t'+ch1_tokens[1]+'\t'+ch1_tokens[2]+'\t'+str(ch1_score)+'\n'
            entailment_txt = entailment_txt+ch2_tokens[0]+'\t'+ch2_tokens[1]+'\t'+ch1_tokens[2]+'\t'+str(ch2_score)+'\n'

            # commonsense_txt = commonsense_txt+ch1_tokens[0]+'\t'+ch1_tokens[1]+'\t'+str(each["bert_choice1"] / (each["bert_choice1"] + each["bert_choice2"]))+'\n'
            # commonsense_txt = commonsense_txt+ch2_tokens[0]+'\t'+ch2_tokens[1]+'\t'+str(each["bert_choice2"] / (each["bert_choice1"] + each["bert_choice2"]))+'\n'
        else:
            for ent in entailment:
                token = ent.split('$$')
                if float(token[3]) < 0.1:
                    entailment_txt = entailment_txt+token[0]+'\t'+token[1]+'\t'+token[2]+'\t'+token[3]+'\n'

        # for com in commonsense:
        #     token = com.split('$$')
        #     commonsense_txt = commonsense_txt+token[0]+'\t'+token[1]+'\t'+token[2]+'\n'

        create_psl_exec_files(coref_txt, coref_truth_txt, context_pair_txt, domain_txt, entailment_txt, commonsense_txt)
        run_psl();
        inferred_ans, max = get_ans(each, bert);
        print('INFERRED_ANS: ', inferred_ans)
        if inferred_ans.lower() == each['ans'].lower():
            correct = correct + 1
            each["predicted"] = "CORRECT"
        else:
            incorrect = incorrect + 1
            each["predicted"] = "INCORRECT"
        each['bert_choice1'] = bert["choice1_score"]
        each['bert_choice2'] = bert["choice2_score"]
        print("WS_SENT: "+each["ws_sent"])
        total = total + 1

    print("Correct : ", correct)
    print("Incorrect : ", incorrect)
    print("Total: ", total)
    with open('../data/new_psl_problems_scores.json', 'w') as outfile:
        json.dump(probs_and_context, outfile)

if __name__=="__main__":
    main()
