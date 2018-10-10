
import json
from allennlp.predictors.predictor import Predictor

predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/decomposable-attention-elmo-2018.02.19.tar.gz")

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

    choice1_conf = 0
    choice2_conf = 0
    for (ques,ans) in ws_qas_with_pronoun_in_ans:
        k_ques_list = dict_of_similar_ques[ques]
        k_ans_list = dict_of_sim_ans[ans]
        
        new_ans1 = ""
        new_ans2 = ""
        ans_tokens = ans.split(" ")
        for ans_token in ans_tokens:
            if ans_token==ws_pronoun:
                new_ans1 += " " + ws_choice1
                new_ans2 += " " + ws_choice2
            else:
                new_ans1 += " " + ans_token
                new_ans2 += " " + ans_token
        
        new_ans1 = new_ans1.strip()
        new_ans2 = new_ans2.strip()
        
        for k_ans in k_ans_list:
            print("Compare 1: ",k_ans," with ",new_ans1) 
            comp1_score = predictor.predict(hypothesis=k_ans,premise=new_ans1)
            print("Compare 2: ",k_ans," with ",new_ans2)
            comp2_score = predictor.predict(hypothesis=k_ans,premise=new_ans2)
            
            if comp1_score > comp2_score:
                choice1_conf += 1
            else:
                choice2_conf += 1
   
    print("Choice 1: ",ws_choice1," Score: ",choice1_conf)
    print("Choice 2: ",ws_choice2," Score: ",choice2_conf)    
        
#    print(wsc_qa_pairs[0]["ques"])


if __name__=="__main__":
    main()
