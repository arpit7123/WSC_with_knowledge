import re
import json
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
#from allennlp.predictors.predictor import Predictor

#predictor = Predictor.from_path("./decomposable-attention-elmo-2018.02.19.tar.gz")
wn_lemmatizer = WordNetLemmatizer()

#ques_type_lists = [["What V?"],["What was V?"],["Who V someone something ?","Who V to do something ?"]]

all_ques = set()
aux_verbs_list = ["does","was","am","is","did","are","were","have","has","had","be"]
sim_verbs_lists = [["rushed","zoomed"],["upset","frustrated"],["made","gotten"],["fell","fall"],["protect","guard"],["beat","defeated"],["appeared","emerged"],["stop","prevent"],["conveys","showing"],["respond","answer"],["offered","gave"],["passed","gave"],["lifting","carried"],["ached","hurting"],["pass","gave"]]

def populate_ques_type_list():
    global ques_type_lists
    file_path = "similar_questions_lists.txt"
    with open(file_path,"r") as f:
        ques_type_lists = json.loads(f.read())
    

def get_ques_with_ans(word, qa_pairs):
    list_of_qas = []
    for qa_pair in qa_pairs:
        ques = qa_pair["ques"]
        ans = qa_pair["ans"]
        ans_tokens = ans.split(" ")
        for ans_token in ans_tokens:
            if word==ans_token:
                list_of_qas.append((ques,ans,qa_pair["verb"]))
                break
    return list_of_qas 


def generate_qa_dict(qa_pairs):
    ques_ans_dict = {}
    for qa_pair in qa_pairs:
        ques_ans_dict[qa_pair["ques"]] = qa_pair["ans"]
    return ques_ans_dict

def same_type_from_list(ques1,ques2):
    #print("IN TOP TOP: ",ques1,"   ",ques2)
    for ques_type_list in ques_type_lists:
        if (ques1 in ques_type_list) and (ques2 in ques_type_list):
            #print("IN TOP: ",ques1,"   ",ques2)
            return True
        #else:
        #    print("NO")    

def same_type_score(ques1, ques2):
    #print("QUES1: ",ques1)
    #print("QUES2: ",ques2)
    if ques1==ques2:
        return 1.0
    elif same_type_from_list(ques1,ques2):
        return 1.0
    else:
        return 0.0
'''
    else:
        if ques1[-1]=="?":
            ques1_without_qm = ques1[0:-1]
        else:
            ques1_without_qm = ques1

        if ques2[-1]=="?":
            ques2_without_qm = ques2[0:-1]
        else:
            ques2_without_qm = ques2

        ques1_tokens = ques1_without_qm.split(" ")
        ques2_tokens = ques2_without_qm.split(" ")
        tokens_matched = 0
        for i in range(0,len(ques1_tokens)):
            if i < len(ques2_tokens):
                if ques1_tokens[i]==ques2_tokens[i]:
                    tokens_matched += 1
                elif ques1_tokens[i]=="someone" and ques2_tokens[i]=="something":
                    tokens_matched += 1
                elif ques1_tokens[i]=="something" and ques2_tokens[i]=="someone":
                    tokens_matched += 1
        sim_score = tokens_matched/float(len(ques1_tokens))
        
        #if sim_score > 0.8:
        #    return True
        return sim_score
        #for ques_type_list in ques_type_lists:
        #    if (ques1 in ques_type_list) and (ques2 in ques_type_list):
        #        return True
    return False
'''

def get_words_similarity(word1,word2):
    if word1==word2:
        return 1.0
    if word1 in aux_verbs_list and word2 in aux_verbs_list:
        return 1.0

    for sim_verbs_list in sim_verbs_lists:
        if word1 in sim_verbs_list and word2 in sim_verbs_list:
            return 1.0

    syn1s = wn.synsets(word1)
    if syn1s==[]:
        return 0.0
    syn1 = syn1s[0]
    syn2s = wn.synsets(word2)
    if syn2s==[]:
        return 0.0
    syn2 = syn2s[0]
    sim = syn1.path_similarity(syn2)
    return sim

def get_lemma(word,pos_tag):
    if word.lower()=="felt":
        return "feel"
    lemma = wn_lemmatizer.lemmatize(word.lower(),pos=pos_tag)
    return lemma

def is_similar(ws_qa_pair,know_qa_pair):
    ws_ques = ws_qa_pair["ques"]
    ws_verb = ws_qa_pair["verb"]
    know_ques = know_qa_pair["ques"]
    know_verb = know_qa_pair["verb"]
    
    all_ques.add(ws_ques)
    all_ques.add(know_ques)

#    print(ws_qa_pair,know_qa_pair)
    total_sim_score = 0.0
    #print("WS QUESTION",ws_ques)
    #print("KNOW QUESTION",know_ques)
    total_sim_score += same_type_score(ws_ques,know_ques)
    #print(total_sim_score)
    #print(ws_verb, know_verb)
    ws_verb_lemma = get_lemma(ws_verb,'v')
    know_verb_lemma = get_lemma(know_verb,'v')
    #print(ws_verb_lemma, know_verb_lemma)
    if ws_verb_lemma==know_verb_lemma:
        total_sim_score += 1.0
    else:
        verb_sim = get_words_similarity(ws_verb,know_verb)
        if verb_sim is not None:
            total_sim_score += verb_sim
            #if verb_sim > 0.7:
            #    return 1.0
            #else:
            #    return 0.0
        else:
            total_sim_score += 0.0
    
    #print(total_sim_score)
    if total_sim_score > 1.4:
        return True
    else:
        return False
'''   
    if ws_verb==know_verb:
        if same_type():
            return 1.0
'''

def get_similar_ques(ws_qa_pairs, know_qa_pairs):
    dict_of_similar_ques = {}
    dict_of_similar_ans = {}
    for ws_qa_pair in ws_qa_pairs:
        sim_ques = ""
        sim_ans = ""
        for know_qa_pair in know_qa_pairs:
            #print("WS Pair: ",ws_qa_pair)
            #print("KNOW Pair: ",know_qa_pair)
            #print("Sim Score: ",sim_score)
            sim_score = is_similar(ws_qa_pair,know_qa_pair)
            #print("WS Pair: ",ws_qa_pair)
            #print("KNOW Pair: ",know_qa_pair)
            #print("Sim Score: ",sim_score)
            if sim_score is True:
                #print("WS_PAIR: ",ws_qa_pair)
                #print("KNOW_PAIR: ",know_qa_pair)
                sim_ques = know_qa_pair["ques"]
                sim_ans = know_qa_pair["ans"]
                dict_of_similar_ques[(ws_qa_pair["ques"],ws_qa_pair["verb"])] = (sim_ques,ws_qa_pair["verb"])
                if (ws_qa_pair["ans"],ws_qa_pair["verb"]) in dict_of_similar_ans:
                    set_of_sim_ans = dict_of_similar_ans[(ws_qa_pair["ans"],ws_qa_pair["verb"])]
                else:
                    set_of_sim_ans = set()
                set_of_sim_ans.add((sim_ans,ws_qa_pair["verb"]))
                dict_of_similar_ans[(ws_qa_pair["ans"],ws_qa_pair["verb"])] = set_of_sim_ans
        if (ws_qa_pair["ques"],ws_qa_pair["verb"]) not in dict_of_similar_ques.keys():
            dict_of_similar_ques[(ws_qa_pair["ques"],ws_qa_pair["verb"])] = ("",ws_qa_pair["verb"])
            ans_set = set()
            dict_of_similar_ans[(ws_qa_pair["ans"],ws_qa_pair["verb"])] = ans_set
        
    return dict_of_similar_ques,dict_of_similar_ans
        

def main(problem,ws_qa_pairs,know_qa_pairs):
    #print(ws_qa_pairs)
    #print(know_qa_pairs)

    choice1_count = 0
    choice2_count = 0
    
    ws_sent = problem["ws_sent"]
    ws_pronoun = problem["pronoun"]
    ws_ans = problem["ans"]
    ws_choice1 = problem["choice1"]
    ws_choice2 = problem["choice2"]
    know_sent = problem["know_sent"]
    
    print("SENT: ",ws_sent)
    print("PRONOUN: ",ws_pronoun)
    print("KNOW SENT: ",know_sent)
    print("ANSWER: ",ws_ans)
    print("CHOICE1: ",ws_choice1)
    print("CHOICE2: ",ws_choice2)    
    
    ans_is_choice1 = False
    if ws_ans.lower()==ws_choice1.lower():
        ans_is_choice1 = True
    
    # Converting WSC and Knowledge question/answers into dictionaries for easy access
    ws_qa_dict = generate_qa_dict(ws_qa_pairs)
    know_qa_dict = generate_qa_dict(know_qa_pairs)
    #print(ws_qa_dict)
    #print(know_qa_dict)

    # Getting similar (corresponding) questions and answers from WSC sentence and Knowledge sentence
    dict_of_similar_ques,dict_of_sim_ans = get_similar_ques(ws_qa_pairs,know_qa_pairs)
    print(dict_of_similar_ques)
    print(dict_of_sim_ans)

    # Getting WSC question/answers which contain the concerned pronoun in the answers
    ws_qas_with_pronoun_in_ans = get_ques_with_ans(ws_pronoun,ws_qa_pairs)
    #print(ws_qas_with_pronoun_in_ans)

    # Finding if an answer exists in the WSC question/answers with just the concerned pronoun as the answer
    one_word_pronoun_ans_exists = False
    for (ques,ans,verb) in ws_qas_with_pronoun_in_ans:
        if ans==ws_pronoun or ans.lower()==ws_pronoun:
            one_word_pronoun_ans_exists = True
    
    # Finding the questions/answers such that the answer(s) correspond to the choice 1 of the given problem
    choice1_set_of_sim_ans = set()
    sim_ans_keys = dict_of_sim_ans.keys()
    for (ans1,verb1) in sim_ans_keys:
        if ans1.lower()==ws_choice1.lower():
            choice1_set_of_sim_ans = choice1_set_of_sim_ans | dict_of_sim_ans[(ans1,verb1)]
        else:
            ans1_tokens = ans1.split(" ")
            if ws_choice1.lower() in ans1_tokens or ws_choice1 in ans1_tokens:
                choice1_set_of_sim_ans = choice1_set_of_sim_ans | dict_of_sim_ans[(ans1,verb1)]

    # Finding the questions/answers such that the answer(s) correspond to the choice 2 of the given problem
    choice2_set_of_sim_ans = set()
    sim_ans_keys = dict_of_sim_ans.keys()
    for (ans1,verb1) in sim_ans_keys:
        if ans1==ws_choice2.lower() or ans1==ws_choice2:
            choice2_set_of_sim_ans = choice2_set_of_sim_ans | dict_of_sim_ans[(ans1,verb1)]
        else:
            ans1_tokens = ans1.split(" ")
            if ws_choice2.lower() in ans1_tokens or ws_choice2 in ans1_tokens:
                choice2_set_of_sim_ans = choice2_set_of_sim_ans | dict_of_sim_ans[(ans1,verb1)]
    
    # There are 8 possibilities based on the questions/answers found in the knowledge sentence corresponding to the questions/answers wrt answer choice 1, answer choice2 and the concerned pronoun in the WSC sentence.
    
    
    list_of_avg_ent_scores_for_choice1 = []
    list_of_avg_ent_scores_for_choice2 = []
    choice1_comps = []
    choice2_comps = []
    for (ques,ans,verb) in ws_qas_with_pronoun_in_ans:
        #if ans.strip() == ws_pronoun:
#            print("THIS ISSUE FACED")
        #    continue
        #if one_word_pronoun_ans_exists:
        #    if ans!=ws_pronoun and ans.lower()!=ws_pronoun:
        #        continue

        #print(ques,ans,verb)
        k_ques_list = dict_of_similar_ques[(ques,verb)] 
        if (ans,verb) in dict_of_sim_ans.keys():
            k_ans_list = dict_of_sim_ans[(ans,verb)]
        elif (ans.lower(),verb) in dict_of_sim_ans.keys():
            k_ans_list = dict_of_sim_ans[(ans.lower(),verb)]
        else:
            k_ans_list = []

#        k_ans_list = dict_of_sim_ans[(ans,verb)]
        #print(dict_of_sim_ans)
        
        #print(ans) 
        ans_tokens = ans.split(" ")
        
#        print("CHOICE 1: ",ws_choice1)
        anss_wrt_choice1 = []
        
        #choice1_set_of_sim_ans = set()
        #sim_ans_keys = dict_of_sim_ans.keys()
        #for (ans1,verb1) in sim_ans_keys:
        #    if ans1.lower()==ws_choice1.lower():
        #        choice1_set_of_sim_ans = choice1_set_of_sim_ans | dict_of_sim_ans[(ans1,verb1)]
        #    else:
        #        ans1_tokens = ans1.split(" ")
        #        if ws_choice1.lower() in ans1_tokens or ws_choice1 in ans1_tokens:
        #            choice1_set_of_sim_ans = choice1_set_of_sim_ans | dict_of_sim_ans[(ans1,verb1)]
        for (know_choice,verb2) in choice1_set_of_sim_ans:
            #if verb!=verb2:
            #    continue
            new_ans = ""
            for ans_token in ans_tokens:
                if ans_token==ws_pronoun:
                    new_ans += " " + know_choice
                else:
                    new_ans += " " + ans_token
            anss_wrt_choice1.append(new_ans.strip())
        #print("CHOICE1 ANS OPTION: ",anss_wrt_choice1)
        
        
        anss_wrt_choice2 = []
        #choice2_set_of_sim_ans = set()
        #sim_ans_keys = dict_of_sim_ans.keys()
        #for (ans1,verb1) in sim_ans_keys:
        #    if ans1==ws_choice2.lower() or ans1==ws_choice2:
        #        choice2_set_of_sim_ans = choice2_set_of_sim_ans | dict_of_sim_ans[(ans1,verb1)]
        #    else:
        #        ans1_tokens = ans1.split(" ")
        #        if ws_choice2.lower() in ans1_tokens or ws_choice2 in ans1_tokens:
        #            choice2_set_of_sim_ans = choice2_set_of_sim_ans | dict_of_sim_ans[(ans1,verb1)]

#        print(choice2_set_of_sim_ans)

        for (know_choice,verb2) in choice2_set_of_sim_ans:
            #if verb!=verb2:
            #    continue
            if know_choice == "":
                continue
            new_ans = ""
            for ans_token in ans_tokens:
                if ans_token==ws_pronoun:
                    new_ans += " " + know_choice
                else:
                    new_ans += " " + ans_token
            anss_wrt_choice2.append(new_ans.strip())
        #print("CHOICE2 ANS OPTION: ",anss_wrt_choice2)

#        if ws_choice2 in dict_of_sim_ans:
#            choice2s_in_know = dict_of_sim_ans[ws_choice2]
#            
#        if ws_choice2.lower() in dict_of_sim_ans:
#            choice2s_in_know = dict_of_sim_ans[ws_choice2.lower()]
#
#        if choice2s_in_know=={''}:
#            choice2s_in_know = []
#
#        for know_choice in choice2s_in_know:
#            new_ans = ""
#            for ans_token in ans_tokens:
#                if ans_token==ws_pronoun:
#                    new_ans += " " + know_choice
#                else:
#                    new_ans += " " + ans_token
#            anss_wrt_choice2.append(new_ans.strip())
        
        choice1_ent_scores = []
        choice2_ent_scores = []    
#        print("K ANSWERS",k_ans_list)
        for (k_ans,k_verb) in k_ans_list:
            if k_ans=="":
                continue
            for ans_wrt_choice1 in anss_wrt_choice1:
                choice1_comps.append("Compare: "+k_ans+" WITH "+ans_wrt_choice1)
                print("Compare 1: ",k_ans," WITH ",ans_wrt_choice1) 
#                comp1_score = predictor.predict(hypothesis=k_ans,premise=ans_wrt_choice1)
#                comp1_ent_score = comp1_score["label_probs"][0]
#                choice1_ent_scores.append(comp1_ent_score)
##                print("Entailment Score: ",comp1_ent_score)
            for ans_wrt_choice2 in anss_wrt_choice2:
                choice2_comps.append("Compare: "+k_ans+" WITH "+ans_wrt_choice2) 
                print("Compare 2: ",k_ans," WITH ",ans_wrt_choice2)
#                comp2_score = predictor.predict(hypothesis=k_ans,premise=ans_wrt_choice2)
#                comp2_ent_score = comp2_score["label_probs"][0]
#                choice2_ent_scores.append(comp2_ent_score)
##            print("Entailment Score: ",comp1_ent_score)
            
#        avg_ent_score_choice1 = sum(choice1_ent_scores) / (float(len(choice1_ent_scores))+1)
#        list_of_avg_ent_scores_for_choice1.append(avg_ent_score_choice1)
#        avg_ent_score_choice2 = sum(choice2_ent_scores) / (float(len(choice2_ent_scores))+1)
#        list_of_avg_ent_scores_for_choice2.append(avg_ent_score_choice2)
    if len(choice1_comps)==0 and len(choice2_comps)!=0:
        if not ans_is_choice1:
            choice2_count+=1
        print("Answer is choice2")

    if len(choice1_comps)!=0 and len(choice2_comps)==0:
        if ans_is_choice1:
            choice1_count+=1
        print("Answer is choice1")

    if len(choice1_comps)==0  and len(choice2_comps)==0:
        for (ques,ans,verb) in ws_qas_with_pronoun_in_ans:
            #print(ans)
            if (ans,verb) in dict_of_sim_ans.keys():
                know_ans = dict_of_sim_ans[(ans,verb)]
            else:
                know_ans = []
            for (k_a,k_v) in know_ans:
                for (a,v) in dict_of_sim_ans.keys():
                    #print(a,v)
                    aas = dict_of_sim_ans[(a,v)]
                    #print(aas)
                    for (a1,v1) in aas:
                        #print(a1,ans)
                        if a1==k_a and ans!=a:
                            print(a)
                            if a.lower()==ws_choice1.lower():
                                choice1_count += 1
                            elif a.lower()==ws_choice2.lower():
                                choice2_count += 1
    result = "unknown"
    if ans_is_choice1:
        if choice1_count > choice2_count:
            result = "correct"
        elif choice2_count > choice1_count:
            result = "incorrect"
    else:
        if choice2_count > choice1_count:
            result = "correct"
        elif choice1_count > choice2_count:
            result = "incorrect"
#    avg_choice1_score = sum(list_of_avg_ent_scores_for_choice1) / (float(len(list_of_avg_ent_scores_for_choice1))+1)
#    avg_choice2_score = sum(list_of_avg_ent_scores_for_choice2) / (float(len(list_of_avg_ent_scores_for_choice2))+1)
#    print("Choice 1: ",ws_choice1,"Average Scores: ",list_of_avg_ent_scores_for_choice1,"Avg Score: ",avg_choice1_score)
#    print("Choice 2: ",ws_choice2,"Average Scores: ",list_of_avg_ent_scores_for_choice2,"Avg Score: ",avg_choice2_score)    
        
#    print(wsc_qa_pairs[0]["ques"])
    print("ANS CHOICE IS 1: ",ans_is_choice1)
    print("RESULT: ",result)
    return result

def process_qasrl_output(qasrl_output, pronoun):
    qa_pairs_array = []
    json_obj = qasrl_output
    sent_tokens = json_obj["words"]
    verbs_objs = json_obj["verbs"]
    for verbs_obj in verbs_objs:
        verb = verbs_obj["verb"]
        qa_pairs = verbs_obj["qa_pairs"]
        for qa_pair in qa_pairs:
            ques = qa_pair["question"]
            
            new_ques_tokens = []
            ques_last_char = ques[-1]
            if ques_last_char=="?":
                ques = ques[0:-1] + " ?"
            ques_tokens = ques.split(" ")
            for ques_token in ques_tokens:
                if ques_token.lower()==verb.lower() or wn_lemmatizer.lemmatize(ques_token.lower(),pos='v')==wn_lemmatizer.lemmatize(verb.lower(),pos='v'):
                    new_ques_tokens.append("V")
                else:
                    new_ques_tokens.append(ques_token)
            new_ques = " ".join(new_ques_tokens)
            answers = qa_pair["spans"]
            ans_is_pronoun = False
            if pronoun is not None:
                for ans in answers:
                    ans_text = ans["text"]
                    if ans_text==pronoun:
                        ans_is_pronoun = True
                        break
            if ans_is_pronoun:
                qa_pair = {'ques':new_ques, 'ans':pronoun, 'verb':verb}#wn_lemmatizer.lemmatize(verb, pos='v')}
                qa_pairs_array.append(qa_pair)
            else:
                for ans in answers:
                    qa_pair = {'ques':new_ques, 'ans':ans["text"], 'verb':verb}#wn_lemmatizer.lemmatize(verb, pos='v')}
                    qa_pairs_array.append(qa_pair)

    return qa_pairs_array

def process(text):
    #text = text.replace("."," .")
    #text = text.replace(","," ,")
    #text = text.replace(";"," ;")
    #text = text.replace("\"Dibs!\"","Dibs")
    #text = text.replace("\"Check\"","\" Check \"")
    #text = text.replace("20 ,000","20,000")
    #text = text.replace("couldn't","could n't")
    #text = text.replace("didn't","did n't")
    #text = text.replace("doesn't","does n't")
    #text = text.replace("wasn't","was n't")
    #text = text.replace("can't","ca n't")
    #text = text.replace("don't","do n't")
    #text = text.replace("hadn't","had n't")
    #text = text.replace("won't","wo n't")
    #text = text.replace("wouldn't","would n't")
    text = text.replace("Sam's","Sam 's")
    text = text.replace("Tina's","Tina 's") 
    text = text.replace("Ann's","Ann 's")
    text = text.replace("Joe's","Joe 's")
    text = text.replace("Charlie's","Charlie 's")
    text = text.replace("Cooper's","Cooper 's")
    text = text.replace("Yakutsk's","Yakutsk 's")
    text = text.replace("he's","he 's")
    text = text.replace("Fred's","Fred 's")
    text = text.replace("Goodman's","Goodman 's")
    text = text.replace("Emma's","Emma 's")
    text = text.replace("Susan's","Susan 's")
    text = text.replace("Pam's","Pam 's")
    text = text.replace("Mark's","Mark 's")
    text = text.replace("Amy's","Amy 's")
    text = text.replace("Paul's","Paul 's")
    text = text.replace("I'm","I 'm")
    re.sub( '\s+', ' ', text ).strip()
    return text

if __name__=="__main__":
    populate_ques_type_list()
    #print(len(ques_type_lists))
    
    #print(same_type_from_list("What did someone V ?","What does someone V ?"))
    #print(same_type_from_list("What did someone V ?","What does someone V ?"))    
    
    #all_probs_file = "test_inputs/test_problems_file.json"
    all_probs_file = "wsc_problems_file.json"
    f = open(all_probs_file,"r")
    all_probs = f.read()    
    probs = json.loads(all_probs)
    
    qasrl_output_dict = {}
    qasrl_ws_sent_file = "test_inputs/test_ws_sents_and_qasrl_out.txt"
    #qasrl_ws_sent_file = "ws_sents_and_qasrl_out.txt"
    f = open(qasrl_ws_sent_file,"r")
    for line in f:
        sent_and_qasrl = line.rstrip().split("$$$$")
        json_obj = json.loads(sent_and_qasrl[1])
        sentence = sent_and_qasrl[0]
        qasrl_output_dict[sentence] = json_obj

    qasrl_know_sent_file = "test_inputs/test_know_sents_and_qasrl_out.txt"
    #qasrl_know_sent_file = "know_sents_and_qasrl_out.txt"
    f = open(qasrl_know_sent_file,"r")
    for line in f:
        sent_and_qasrl = line.rstrip().split("$$$$")
        json_obj = json.loads(sent_and_qasrl[1])
        sentence = sent_and_qasrl[0]
        qasrl_output_dict[sentence] = json_obj
   
    #print("QASRL_DICT= ", qasrl_output_dict) 
    know_not_parsed = 0
    wssent_not_parsed = 0
    correct = 0
    incorrect = 0
    unknown = 0 
    for i in range(0,len(probs)):
        prob = probs[i]
        ws_sent = prob["ws_sent"]
        #ws_sent = process(ws_sent)
        if ws_sent in qasrl_output_dict:
            ws_sent_qasrl_pairs = qasrl_output_dict[ws_sent]
            if "know_sent" in prob:
                if prob["know_sent"] in qasrl_output_dict:
                    know_sent_qasrl_pairs = qasrl_output_dict[prob["know_sent"]]
                    pronoun = prob["pronoun"]
        
                    ws_sent_qa_pairs = process_qasrl_output(ws_sent_qasrl_pairs,pronoun)
                    know_sent_qa_pairs = process_qasrl_output(know_sent_qasrl_pairs,None)
                    #print(ws_sent_qa_pairs)
                    #print(know_sent_qa_pairs)
                    print("************************************************************")
                    result = main(prob,ws_sent_qa_pairs,know_sent_qa_pairs)
                    if result=="correct":
                        correct += 1
                    elif result=="incorrect":
                        incorrect += 1
                    else:
                        unknown += 1
                    print("************************************************************")
                else:
                    print(prob["know_sent"])
                    know_not_parsed+=1
        else:
            print(ws_sent)
            wssent_not_parsed+=1
    
    #print("know sents not parsed: ",know_not_parsed)
    #print("ws sents not parsed: ",wssent_not_parsed)
    
    print("CORRECT: ",correct)
    print("INCORRECT: ",incorrect)
    print("UNKNOWN: ",unknown)    

    '''
    for ques in all_ques:
        print(ques)
    '''
