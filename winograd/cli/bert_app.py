import json
import matplotlib.pyplot as plt
def main():

    bert_scores_file = open("../data/bert_wsc_problems.json", "r") 
    bert_scores = json.loads(bert_scores_file.read())
    
    correct = 0
    incorrect = 0
    total = 0
    diff_arr = []
    for i in range(0, len(bert_scores)):
        each = bert_scores[i]
        diff = 0.0
        if each["choice1_score"] > each["choice2_score"]:
            diff = each["choice1_score"] - each["choice2_score"];
        else:
            diff = each["choice2_score"] - each["choice1_score"];
        diff_arr.append(diff)
        print("WS_SENT: "+each["question"])
        total = total + 1

    print("Correct : ", correct)
    print("Incorrect : ", incorrect)
    print("Total: ", total)
    plt.plot(diff_arr)
    plt.ylabel('diff scores')
    plt.show()

if __name__=="__main__":
    main()