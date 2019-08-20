import json
def main():

    problems = "COPA/bert_output.json"
    f = open(problems,"r")
    all_probs = f.read()
    copa_problems = json.loads(all_probs)

    correct = 0
    incorrect = 0
    for i in range(0, len(copa_problems)):
        each = copa_problems[i]
        answer = int(each['answer'])
        choice1_score = each['choice1_score']
        choice2_score = each['choice2_score']
        if ((choice1_score[1] > choice2_score[1] and answer == 1) or (choice1_score[1] < choice2_score[1] and answer == 2)):
            correct = correct + 1  
        else:
            incorrect = incorrect + 1

    print("Correct : ", correct)
    print("Incorrect : ", incorrect)
    print("Total: ", len(copa_problems))

if __name__=="__main__":
    main()
