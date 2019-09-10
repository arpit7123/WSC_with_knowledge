import json
import random

def winogrande_bert_score():
    problems = "../data_sets/winogrande/winogrande_problems.json"
    f = open(problems, "r")
    all_probs = f.read()
    winogrande_problems = json.loads(all_probs)

    log_out = "../data_sets/winogrande/slurm-1730983.out"
    f_log = open(log_out, "r")
    slurm_log = f_log.read()
    slurm_objects = slurm_log.split('of  2863')
    
    for i in range(0, len(slurm_objects)):
        each = slurm_objects[i]
        grande = winogrande_problems[i]
        values = each.split('\n')
        score1 = False
        for v in values:
            if 'tensor' in v:
                v =  v.replace('tensor([[', '')
                v =  v.replace(']], grad_fn=<AddmmBackward>)',  '')
                scores = v.split(',')
                if not score1:
                    score1 = True
                    grande['choice1_score'] = []
                    grande['choice1_score'].append(float(scores[0]))
                    grande['choice1_score'].append(float(scores[1]))
                else:
                    grande['choice2_score'] = []
                    grande['choice2_score'].append(float(scores[0]))
                    grande['choice2_score'].append(float(scores[1]))
                    break
        print(grande)
                
    with open('../data_sets/winogrande/winogrande_problems.json', 'w') as outfile:
       json.dump(winogrande_problems, outfile)

def combine_qasrl():
    problems = "../data_sets/winogrande/knowledge_queries.json"
    f = open(problems, "r")
    all_probs = f.read()
    knowledge_queries = json.loads(all_probs)

    qasrl_out_file = "../data_sets/winogrande/QASRL_OUT/winogrande_knowledge_score_qasrl_out.txt"
    qasrl_out_file_r = open(qasrl_out_file, "r")
    qasrl_out = qasrl_out_file_r.read()
    qasrl_objects = qasrl_out.split('\n')
    
    start = 0
    for i in range(0, len(knowledge_queries)):
        each  = knowledge_queries[i][0]
        end = start + 10
        if(len(each['knowledge']) < 10):
            end = start + len(each['knowledge'])
        m  = 0
        output_k = []
        for j in range(start, len(qasrl_objects)):
            if (j >=  end):
                start = end
                break
            qasrl = json.loads(qasrl_objects[j])
            each_k =  each['knowledge'][m]
            each_k['qasrl'] = qasrl
            output_k.append(each_k)
            m  = m + 1
        each['knowledge'] = output_k
        print("***************************************")
        
    with open('../data_sets/winogrande/knowledge_queries_with_qasrl.json', 'w') as outfile:
        json.dump(knowledge_queries, outfile)
    
def check_bert_score():
    problems = "../data_sets/winogrande/bert_winogrande_problems_fine_tuned.json"
    f = open(problems, "r")
    all_probs = f.read()
    winogrande_problems = json.loads(all_probs)
    correct =  0
    for i in range(0, len(winogrande_problems)):
        each = winogrande_problems[i]
        score1 = max(each['choice1_score'][0], each['choice1_score'][1])
        score2 = max(each['choice2_score'][0], each['choice2_score'][1])
        if(score1  > score2 and each['answer']  == '1'):
            correct = correct + 1
        elif(score1 <  score2 and each['answer']  == '2'):
            correct = correct + 1
    print(correct)


if __name__=="__main__":
    check_bert_score()



