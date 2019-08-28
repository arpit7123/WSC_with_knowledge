import json


def COPA_evaluate():
    problems = "../COPA/bert_output.json"
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


def main():
    problems = "../data_sets/winogrande/dev.jsonl"
    f = open(problems,"r")
    all_probs = f.read()
    wino_grande_problems = all_probs.split('\n')
    output = []
    itr = 1
    for i in range(0, len(wino_grande_problems)):
        obj = {}
        each = json.loads(wino_grande_problems[i])
        obj["question"] = each["sentence"]
        obj["choice1"] = each["option1"]
        obj["choice2"] = each["option2"]
        obj["answer"] = each["answer"]
        obj["domain"] = each["domain"]
        words = each["sentence"].split(' ')
        index = 0
        for w in words:
            index = index + 1
            if(w == '_'):
                break
        words[index - 3] = ' ? ' + words[index - 3]
        sentence = " ".join(words)
        obj["alternate1"] = sentence.replace('_', each["option1"])
        obj["alternate2"] = sentence.replace('_', each["option2"])
        obj["questionId"] = itr
        itr = itr + 1
        output.append(obj)
        
    with open('../data_sets/winogrande/bert_dev_alternates.json', 'w') as outfile:
        json.dump(output, outfile)


if __name__=="__main__":
    main()
