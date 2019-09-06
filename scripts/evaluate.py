import json
import csv


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

def Winogrande_data_creation():
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

def main():
    problems = "../data_sets/winogrande/dev.jsonl"
    f = open(problems,"r")
    all_probs = f.read()
    wino_grande_problems = all_probs.split('\n')
    output = []
    itr = 1
    for i in range(0, len(wino_grande_problems)):
        each = json.loads(wino_grande_problems[i])
        sentence = each['sentence']
        obj = {}
        obj['sentence'] = sentence
        with open('../data_sets/winogrande/winogrande_qasrl_input.txt', 'a') as outfile:
            json.dump(obj, outfile)
            outfile.write('\n')
        #if each["answer"] == "1":
        #    sentence = sentence.replace('_', each['option1'])
        #else:
        #    sentence = sentence.replace('_', each['option2'])
        #sentence = sentence.replace('"', '')
        
        #train
        #obj1 = []
        #obj1.append(str(itr))
        #obj1.append(sentence)
        #obj1.append(int(each['answer']) - 1)
        #obj1.append(each['domain'])
        #output.append(obj1)
        
        #dev
        #obj1 = []
        #obj1.append(str(itr))
        #obj1.append(sentence.replace('_', each['option1']))
        #if(each['answer'] == "1"):
        #    obj1.append(1)
        #else:
        #    obj1.append(0)  
        
        #obj1.append(each['domain'])
        #output.append(obj1)
       
        #obj2 = []
        #obj2.append(str(itr))
        #obj2.append(sentence.replace('_', each['option2']))
        #if(each['answer'] == "2"):
        #    obj2.append(1)
        #else:
        #    obj2.append(0)  
        #obj2.append(each['domain'])
        #output.append(obj2)
        itr = itr + 1
     
    #with open('../data_sets/winogrande/winogrande_train.csv', 'w') as csvFile:
    #    writer = csv.writer(csvFile)
    #    writer.writerows(output)
    #csvFile.close()

if __name__=="__main__":
    main()
