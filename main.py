
import json
from allennlp.predictors.predictor import Predictor

predictor = Predictor.from_path("./decomposable-attention-elmo-2018.02.19.tar.gz")

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

def is_similar(ws_qa_pair,know_qa_pair):
    ws_ques = ws_qa_pair["ques"]
    ws_verb = ws_qa_pair["verb"]
    know_ques = know_qa_pair["ques"]
    know_verb = know_qa_pair["verb"]
    
    if ws_ques==know_ques:
        return 1.0
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
        

def main():
    ws_sent = "The fish ate the worm because it was tasty."
    ws_pronoun = "it"
    ws_ans = "worm"
    ws_choice1 = "fish"
    ws_choice2 = "worm"
    know_sent = "We ate crabs because seafood is tasty."
    
    ws_qa_pairs_json = "[{\"ques\":\"What ate something\",\"ans\":\"fish\", \"verb\":\"eat\"},{\"ques\":\"What was eaten\",\"ans\":\"worm\", \"verb\":\"eat\"},{\"ques\":\"Why ate\",\"ans\":\"it was tasty\", \"verb\":\"eat\"}]"
    know_qa_pairs_json = "[{\"ques\":\"What ate something\",\"ans\":\"we\", \"verb\":\"eat\"},{\"ques\":\"What was eaten\",\"ans\":\"crabs\", \"verb\":\"eat\"},{\"ques\":\"Why ate\",\"ans\":\"seafood is tasty\", \"verb\":\"eat\"}]"
    
    ws_qa_pairs = json.loads(ws_qa_pairs_json)
    know_qa_pairs = json.loads(know_qa_pairs_json)
    
    dict_of_similar_ques,dict_of_sim_ans = get_similar_ques(ws_qa_pairs,know_qa_pairs)
    
    ws_qa_dict = generate_qa_dict(ws_qa_pairs)
    know_qa_dict = generate_qa_dict(know_qa_pairs)
    
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
        print(dict_of_sim_ans)
                
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


if __name__=="__main__":
    main()
