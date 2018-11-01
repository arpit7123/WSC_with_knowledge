

import json

if __name__=="__main__":
    sent_file_path = "know_sents_to_parse"
    qasrl_file_path = "know_sents_parsed.json"
    
    f1 = open(sent_file_path,"r")
    sents_list = []
    for line in f1:
        #print("LINE is: :::",line,":::")
        sent_dict = json.loads(line.rstrip())
        sents_list.append(sent_dict["sentence"])

    f2 = open(qasrl_file_path,"r")
    qasrl_list = []
    for line in f2:
        qasrl_list.append(line.rstrip())

    for i in range(0,len(sents_list)):
        print(sents_list[i]+"$$$$"+qasrl_list[i])


    
    
