import json
import numpy as np
import matplotlib.pyplot as plt


def parse_wsc_out():
    split_str = "************************************************************"
    wsc_out_file = open("../data/output_wsc_nov.json", "r") 
    output_str = wsc_out_file.read()
    output_str_arr = output_str.split(split_str) 
    wsc_output = []
    for each in output_str_arr:
        obj = {}
        values = each.split('\n')
        if len(values) > 7:
            obj['ws_sent'] = values[1].replace('SENT:  ', '') 
            obj['pronoun'] = values[2].replace('PRONOUN:  ', '')
            obj['ans'] = values[4].replace('ANSWER:  ', '')
            obj['choice1'] = values[5].replace('CHOICE1:  ', '')
            obj['choice2'] = values[6].replace('CHOICE2:  ', '')
            obj["result"] = values[-2].replace('RESULT:  ', '')
            wsc_output.append(obj)
    with open('../data/wsc_prev_output.json', 'w') as outfile:
        json.dump(wsc_output, outfile)
    return wsc_output


def calculate_bert_scores():
    bert_scores_file = open("../data/bert_wsc_problems.json", "r") 
    bert_scores = json.loads(bert_scores_file.read())
    correct = 0
    incorrect = 0
    total = 0
    correct_diff = []
    incorrect_diff = []
    correct_grt_1 = 0
    correct_lt_1 = 0
    incorrect_grt_1 = 0
    incorrect_lt_1 = 0

    for i in range(0, len(bert_scores)):
        each = bert_scores[i]
        diff = 0.0
        if each["choice1_score"] > each["choice2_score"]:
            diff = each["choice1_score"] - each["choice2_score"]
            if each['choice1'].lower() == each['ans'].lower():
                correct_diff.append([i, diff]);
                if diff < 1.0:
                    correct_lt_1 = correct_lt_1 + 1 
                else:
                    correct_grt_1 = correct_grt_1 + 1
            else:
                incorrect_diff.append([i, diff]);
                if diff < 1.0:
                    incorrect_lt_1 = incorrect_lt_1 + 1 
                else:
                    incorrect_grt_1 = incorrect_grt_1 + 1

        else:
            diff = each["choice2_score"] - each["choice1_score"]
            if each['choice2'].lower() == each['ans'].lower():
                correct_diff.append([i, diff]);
                if diff < 1.0:
                    correct_lt_1 = correct_lt_1 + 1 
                else:
                    correct_grt_1 = correct_grt_1 + 1
            else:
                incorrect_diff.append([i, diff]);
                if diff < 1.0:
                    incorrect_lt_1 = incorrect_lt_1 + 1 
                else:
                    incorrect_grt_1 = incorrect_grt_1 + 1

        print("WS_SENT: "+each["question"])
        total = total + 1

    print("Correct : ", correct)
    print("Incorrect : ", incorrect)
    print("Total: ", total)
    correct = np.array(correct_diff)
    incorrect = np.array(incorrect_diff)
    print(correct_lt_1)
    print(correct_grt_1)
    print(incorrect_lt_1)
    print(incorrect_grt_1)
    print("Correct Lesser than 1", str(correct_lt_1 / (correct_lt_1 + incorrect_lt_1)))
    print("Correct Greater than 1", str(correct_grt_1 / (correct_grt_1 + incorrect_grt_1)))
    print("Incorrect Lesser than 1", str(incorrect_lt_1 / (correct_lt_1 + incorrect_lt_1)))
    print("Incorrect Greater than 1", str(incorrect_grt_1 / (correct_grt_1 + incorrect_grt_1)))
    # c_x, c_y = correct.T
    # i_x, i_y = incorrect.T
    # plt.scatter(c_x, c_y, c='b', marker='x', label='correct')
    # plt.scatter(i_x, i_y, c='r', marker='s', label='incorrect')
    # plt.legend(loc='upper left')
    # plt.show()

def compare_psl_wsc_prev(wsc_output_scores, psl_scores, bert_scores):
    wsc_output_map = {}
    bert_output_map = {}
    for wsc_each in wsc_output_scores:
        wsc_output_map[wsc_each['ws_sent']] = wsc_each

    for i in range(0, len(bert_scores)):
        bert_output_map[psl_scores[i]['ws_sent']] = bert_scores[i]

    for psl in psl_scores:

        if psl['ws_sent'] in bert_output_map: 
            bert_out = bert_output_map[psl['ws_sent']]
            isBert_correct = False
            if bert_out['ans'].lower() == bert_out['choice1'].lower() and bert_out['choice1_score'] > bert_out['choice2_score']:
                isBert_correct = True
            if bert_out['ans'].lower() == bert_out['choice2'].lower() and bert_out['choice2_score'] > bert_out['choice1_score']:
                isBert_correct = True
        
            if psl['predicted'] == 'INCORRECT' and isBert_correct:
                if 'context' in psl and len(psl['context']) == 0:
                     print('PSL no context')
                print('PSL INCORRECT, BERT CORRECT: '+psl['ws_sent'])


        if psl['ws_sent'] in wsc_output_map: 
            wsc_out = wsc_output_map[psl['ws_sent']]
            
            # if psl['predicted'] == 'CORRECT' and wsc_out['result'] == 'incorrect':
            #     if 'context' in psl and len(psl['context']) == 0:
            #         print('PSL no context')
            #     print('PSL CORRECT, PREV_SYS INCORRECT: '+wsc_out['ws_sent'])
            if psl['predicted'] == 'INCORRECT' and wsc_out['result'] == 'correct':
                if 'context' in psl and len(psl['context']) == 0:
                    print('PSL no context')
                print('PSL INCORRECT, PREV_SYS CORRECT: '+wsc_out['ws_sent'])

        # else:
        #     if psl['predicted'] == 'CORRECT':
        #         if 'context' in psl and len(psl['context']) == 0:
        #             print('PSL no context')
        #         print('PSL CORRECT: Knowledge doesnt exist: '+psl['ws_sent'])

def main():
    bert_scores_file = open("../data/bert_wsc_problems.json", "r") 
    bert_scores = json.loads(bert_scores_file.read())

    wsc_output_file = open("../data/wsc_prev_output.json", "r") 
    wsc_output_scores = json.loads(wsc_output_file.read())

    psl_scores_file = open("../data/new_psl_problems.json", "r") 
    psl_scores = json.loads(psl_scores_file.read())

    compare_psl_wsc_prev(wsc_output_scores, psl_scores, bert_scores)
    correct = 0
    incorrect = 0
    for psl in psl_scores:
        if psl['predicted'] == 'CORRECT':
            correct = correct + 1
        else:
            incorrect = incorrect + 1

    print("correct : "+str(correct))
    print("incorrect : "+str(incorrect))

if __name__=="__main__":
    main()