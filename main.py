
import json
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from allennlp.predictors.predictor import Predictor

predictor = Predictor.from_path("./decomposable-attention-elmo-2018.02.19.tar.gz")
wn_lemmatizer = WordNetLemmatizer()

ques_type_lists = [["What V?"],["What was V?"]]

def get_ques_with_ans(word, qa_pairs):
    list_of_qas = []
    for qa_pair in qa_pairs:
        ques = qa_pair["ques"]
        ans = qa_pair["ans"]
        ans_tokens = ans.split(" ")
        for ans_token in ans_tokens:
            if word==ans_token:
                list_of_qas.append((ques,ans))
                break
    return list_of_qas 


def generate_qa_dict(qa_pairs):
    ques_ans_dict = {}
    for qa_pair in qa_pairs:
        ques_ans_dict[qa_pair["ques"]] = qa_pair["ans"]
    return ques_ans_dict

def same_type(ques1, ques2):
    if ques1==ques2:
        return True
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
            if ques1_tokens[i]==ques2_tokens[i]:
                tokens_matched += 1
            elif ques1_tokens[i]=="someone" and ques2_tokens[i]=="something":
                tokens_matched += 1
            elif ques1_tokens[i]=="something" and ques2_tokens[i]=="someone":
                tokens_matched += 1
        sim_score = tokens_matched/float(len(ques1_tokens))
        
        if sim_score > 0.8:
            return True
        #for ques_type_list in ques_type_lists:
        #    if (ques1 in ques_type_list) and (ques2 in ques_type_list):
        #        return True
    return False

def get_words_similarity(word1,word2):
    return wn.synsets(word1)[0].path_similarity(wn.synsets(word2)[0])

def is_similar(ws_qa_pair,know_qa_pair):
    ws_ques = ws_qa_pair["ques"]
    ws_verb = ws_qa_pair["verb"]
    know_ques = know_qa_pair["ques"]
    know_verb = know_qa_pair["verb"]
    
#    print(ws_qa_pair,know_qa_pair)
    if same_type(ws_ques,know_ques):
        if ws_verb==know_verb:
            return 1.0
        else:
#            print(ws_verb, know_verb)
            verb_sim = get_words_similarity(ws_verb,know_verb)
            if verb_sim is not None:
                if verb_sim > 0.7:
                    return 1.0
                else:
                    return 0.0
            else:
                return 0.0
    else:
        return 0.0
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
            sim_score = is_similar(ws_qa_pair,know_qa_pair)
            if sim_score > 0.7:
                sim_ques = know_qa_pair["ques"]
                sim_ans = know_qa_pair["ans"]
        dict_of_similar_ques[ws_qa_pair["ques"]] = sim_ques
        if ws_qa_pair["ans"] in dict_of_similar_ans:
            set_of_sim_ans = dict_of_similar_ans[ws_qa_pair["ans"]]
        else:
            set_of_sim_ans = set()
        set_of_sim_ans.add(sim_ans)
        dict_of_similar_ans[ws_qa_pair["ans"]] = set_of_sim_ans
        
    return dict_of_similar_ques,dict_of_similar_ans
        

def main(problem,ws_qa_pairs,know_qa_pairs):
    ws_sent = problem["ws_sent"]
    ws_pronoun = problem["pronoun"]
    ws_ans = problem["ans"]
    ws_choice1 = problem["choice1"]
    ws_choice2 = problem["choice2"]
    know_sent = problem["know_sent"]
    
    #ws_qa_pairs = json.loads(ws_qa_pairs_json)
    #know_qa_pairs = json.loads(know_qa_pairs_json)
    
    #print(ws_qa_pairs)
    #print(know_qa_pairs)
    dict_of_similar_ques,dict_of_sim_ans = get_similar_ques(ws_qa_pairs,know_qa_pairs)
    
    #print(dict_of_similar_ques)
    #print(dict_of_sim_ans)

    ws_qa_dict = generate_qa_dict(ws_qa_pairs)
    know_qa_dict = generate_qa_dict(know_qa_pairs)
    
    #print(ws_qa_dict)
    #print(know_qa_dict)

    ws_qas_with_pronoun_in_ans = get_ques_with_ans(ws_pronoun,ws_qa_pairs)
    
#    print(dict_of_similar_ques)
#    print(dict_of_sim_ans)
#    print(ws_qas_with_pronoun_in_ans)

    list_of_avg_ent_scores_for_choice1 = []
    list_of_avg_ent_scores_for_choice2 = []
    choice2_conf = 0
    for (ques,ans) in ws_qas_with_pronoun_in_ans:
        k_ques_list = dict_of_similar_ques[ques]
        k_ans_list = dict_of_sim_ans[ans]
        #print(dict_of_sim_ans)
                
        ans_tokens = ans.split(" ")
        
        anss_wrt_choice1 = []
        choice1s_in_know = dict_of_sim_ans[ws_choice1]
        for know_choice in choice1s_in_know:
            new_ans = ""
            for ans_token in ans_tokens:
                if ans_token==ws_pronoun:
                    new_ans += " " + know_choice
                else:
                    new_ans += " " + ans_token
            anss_wrt_choice1.append(new_ans.strip())
        
        anss_wrt_choice2 = []
        choice2s_in_know = dict_of_sim_ans[ws_choice2]
        for know_choice in choice2s_in_know:
            new_ans = ""
            for ans_token in ans_tokens:
                if ans_token==ws_pronoun:
                    new_ans += " " + know_choice
                else:
                    new_ans += " " + ans_token
            anss_wrt_choice2.append(new_ans.strip())
        
        choice1_ent_scores = []
        choice2_ent_scores = []    
        for k_ans in k_ans_list:
            for ans_wrt_choice1 in anss_wrt_choice1:
                print("Compare 1: ",k_ans," with ",ans_wrt_choice1) 
                comp1_score = predictor.predict(hypothesis=k_ans,premise=ans_wrt_choice1)
                comp1_ent_score = comp1_score["label_probs"][0]
                choice1_ent_scores.append(comp1_ent_score)
#                print("Entailment Score: ",comp1_ent_score)
            for ans_wrt_choice2 in anss_wrt_choice2:
                print("Compare 2: ",k_ans," with ",ans_wrt_choice2)
                comp2_score = predictor.predict(hypothesis=k_ans,premise=ans_wrt_choice2)
                comp2_ent_score = comp2_score["label_probs"][0]
                choice2_ent_scores.append(comp2_ent_score)
#            print("Entailment Score: ",comp1_ent_score)
            
        avg_ent_score_choice1 = sum(choice1_ent_scores) / float(len(choice1_ent_scores))
        list_of_avg_ent_scores_for_choice1.append(avg_ent_score_choice1)
        avg_ent_score_choice2 = sum(choice2_ent_scores) / float(len(choice2_ent_scores))
        list_of_avg_ent_scores_for_choice2.append(avg_ent_score_choice2)
    
    avg_choice1_score = sum(list_of_avg_ent_scores_for_choice1) / float(len(list_of_avg_ent_scores_for_choice1))
    avg_choice2_score = sum(list_of_avg_ent_scores_for_choice2) / float(len(list_of_avg_ent_scores_for_choice2))
    print("Choice 1: ",ws_choice1,"Average Scores: ",list_of_avg_ent_scores_for_choice1,"Avg Score: ",avg_choice1_score)
    print("Choice 2: ",ws_choice2,"Average Scores: ",list_of_avg_ent_scores_for_choice2,"Avg Score: ",avg_choice2_score)    
        
#    print(wsc_qa_pairs[0]["ques"])

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
                if ques_token==verb or ques_token==wn_lemmatizer.lemmatize(verb,pos='v'):
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



if __name__=="__main__":
    all_probs_file = "wsc_problems_file.json"
    f = open(all_probs_file,"r")
    all_probs = f.read()    
    probs = json.loads(all_probs)
#    prob = {}
#    prob["ws_sent"] = "The fish ate the worm because it was tasty."
#    prob["pronoun"] = "they"
#    prob["ans"] = "worm"
#    prob["choice1"] = "fish"
#    prob["choice2"] = "worm"
#    prob["know_sent"] = "We ate crabs because seafood is tasty."
    
    qasrl_output_dict = {}
    qasrl_ws_sent_file = "winograd_output.json"#"qa_srl_ws_sents_out.json"
    f = open(qasrl_ws_sent_file,"r")
    for line in f:
        json_obj = json.loads(line.rstrip())
#        print(json_obj)
        tokens = json_obj["words"]
        sentence = " ".join(tokens)
        qasrl_output_dict[sentence] = json_obj

#    qasrl_know_sent_file = "qa_srl_know_sents_out.json"
    qasrl_know_sent_file = "know_sents_and_qasrl_out.txt"
    f = open(qasrl_know_sent_file,"r")
    for line in f:
        sent_and_qasrl = line.rstrip().split("$$$$")
        json_obj = json.loads(sent_and_qasrl[1])
#        tokens = json_obj["words"]
#        sentence = " ".join(tokens)
        sentence = sent_and_qasrl[0]
        qasrl_output_dict[sentence] = json_obj
   
#    print("QASRL_DICT= ", qasrl_output_dict)
     
    know_not_parsed = 0
    wssent_not_parsed = 0
    for i in range(0,len(probs)):
        prob = probs[i]
        if prob["ws_sent"] in qasrl_output_dict:
            ws_sent_qasrl_pairs = qasrl_output_dict[prob["ws_sent"]]
            if "know_sent" in prob and prob["know_sent"] in qasrl_output_dict:
                know_sent_qasrl_pairs = qasrl_output_dict[prob["know_sent"]]
                pronoun = prob["pronoun"]
        
                #ws_sent_qa_pairs = process_qasrl_output(ws_sent_qasrl_pairs,pronoun)
                #know_sent_qa_pairs = process_qasrl_output(know_sent_qasrl_pairs,None)
                #print(ws_sent_qa_pairs)
                #print(know_sent_qa_pairs)

                #main(prob,ws_sent_qa_pairs,know_sent_qa_pairs)
            else:
                know_not_parsed+=1
        else:
            wssent_not_parsed+=1
    
    print(know_not_parsed)
    print(wssent_not_parsed)
