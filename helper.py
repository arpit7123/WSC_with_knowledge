import re
import json
import ast
from pprint import pprint 

def process1(text):
    text = text.replace("."," .")
    text = text.replace(","," ,")
    text = text.replace(";"," ;")
    text = text.replace("\"Dibs!\"","Dibs")
    text = text.replace("\"Check\"","Check")
    text = text.replace("20 ,000","20,000")
    text = text.replace("couldn't","could not")
    text = text.replace("didn't","did not")
    text = text.replace("doesn't","does not")
    text = text.replace("wasn't","was not")
    text = text.replace("can't","can not")
    text = text.replace("don't","do not")
    text = text.replace("hadn't","had not")
    text = text.replace("won't","would not")
    text = text.replace("wouldn't","would not")
    #text = text.replace("Sam's","Sam 's")
    #text = text.replace("Tina's","Tina 's")
    #text = text.replace("Ann's","Ann 's")
    #text = text.replace("Joe's","Joe 's")
    #text = text.replace("Charlie's","Charlie 's")
    #text = text.replace("Cooper's","Cooper 's")
    #text = text.replace("Yakutsk's","Yakutsk 's")
    text = text.replace("he's","he is")
    #text = text.replace("Fred's","Fred 's")
    #text = text.replace("Goodman's","Goodman 's")
    #text = text.replace("Emma's","Emma 's")
    #text = text.replace("Susan's","Susan 's")
    #text = text.replace("Pam's","Pam 's")
    #text = text.replace("Mark's","Mark 's")
    #text = text.replace("Amy's","Amy 's")
    #text = text.replace("Paul's","Paul 's")
    text = text.replace("I'm","I am")
    re.sub('\s+', ' ', text).strip()
    return text

if __name__=="__main1__":
    all_probs_file = "wsc_problems_file.json"
    f = open(all_probs_file,"r")
    all_probs = f.read()
    probs = json.loads(all_probs)
    all_probs = []
    for prob in probs:
        new_prob = {}
        ws_sent = prob["ws_sent"]
        ws_sent = process1(ws_sent)
        pronoun = prob["pronoun"]
        ans = prob["ans"]
        choice1 = prob["choice1"]
        choice2 = prob["choice2"]
        if "know_sent" in prob:
            know_sent = prob["know_sent"]
            know_sent = process1(know_sent)
            search_query = prob["search_query"]
            know_url = prob["know_url"]
        else:
            know_sent = None
            search_query = None
            know_url = None


        new_prob["ws_sent"] = ws_sent
        new_prob["pronoun"] = pronoun
        new_prob["ans"] = ans
        new_prob["choice1"] = choice1
        new_prob["choice2"] = choice2
        if know_sent is not None:
            new_prob["know_sent"] = know_sent
            new_prob["search_query"] = search_query
            new_prob["know_url"] = know_url

        all_probs.append(new_prob)
    with open('wsc_problems_file1.json', 'w') as outfile:
        json.dump(all_probs, outfile)


if __name__=="__main__":
    all_probs_file = "./inputs/wsc_problems_final.json"
    f = open(all_probs_file,"r")
    all_probs = f.read()
    probs = ast.literal_eval(all_probs)        
    
    all_probs_dict = {}
    for prob in probs:
        all_probs_dict[prob["ws_sent"]] = prob

    
    all_probs_final = []
    tsv_file = "./inputs/newer_wsc_probs.tsv"
    f = open(tsv_file,'r')
    for line in f:
        sents = line.split("\t")
        ws_sent = sents[0]
        know_sent = sents[1]
        if ws_sent in all_probs_dict.keys():
            prob = all_probs_dict[ws_sent]
            prob["know_sent"] = know_sent
            all_probs_final.append(prob)

    with open('./inputs/wsc_problems_final_latest.json', 'wt') as out:
        pprint(all_probs_final, stream=out)


    
