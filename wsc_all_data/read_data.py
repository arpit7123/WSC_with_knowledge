#import nltk
import xml.etree.ElementTree as ET 
import re
from pprint import pprint
import ast
import json

#[{"ws_sent": "The city councilmen refused the demonstrators a permit because they feared violence .", "pronoun": "they", "ans": "The city councilmen", "choice1": "The city councilmen", "choice2": "The demonstrators", "know_sent": "He also refused to give his full name because he feared for his safety .", "search_query": "Bing:[refused]&&[because]&&[feared]", "know_url": "http://www.calvaryroadbaptist.church/sermons/00-05/sermon__fear_god.htm"}]


#valid_pos_tags_list = ["JJ","JJR","JJS","NN","NNS","NNPS","RB","RBR","RBS","VB","VBD","VBG","VBN","VBP","VBZ"] 

def process(text):
    if text[-1]!=".":
        text += "."
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
    text = text.replace("won't","will not")
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
    re.sub( '\s+', ' ', text ).strip()
    return text


def main(xml_file_path):
    list_of_wsc_probs = []
    
    all_comparisons = set()
    # create element tree object 
    tree = ET.parse(xml_file_path) 
    # get root element 
    root = tree.getroot() 
    # create empty list for news items 
#    data_points = [] 
    # iterate news items 
    for item in root.findall('./schema'):
        sent = ""
        pronoun = ""
        answers = []
        corr_ans = ""
        for child in item:
            if child.tag=="text":
                for sent_child in child:
                    sent += sent_child.text.strip().rstrip().replace("\n"," ") + " "
                for child1 in child:
                    if child1.tag=="pron":
                        pronoun = child1.text.replace("\n"," ")
            if child.tag=="answers":
                for ans_child in child:
                    answers.append(ans_child.text.replace("\n"," "))
            if child.tag=="correctAnswer":
                ans = child.text
                if ans.strip()=="A":
                    corr_ans = answers[0]
                elif ans.strip()=="B":
                    corr_ans = answers[1]
                
        prob = {}
        sent = re.sub(' +',' ',sent).strip()
        pronoun = re.sub(' +',' ',pronoun).strip()
        ans = re.sub(' +',' ',corr_ans).strip()
        choice1 = re.sub(' +',' ',answers[0]).strip()
        choice2 = re.sub(' +',' ',answers[1]).strip()
        prob["ws_sent"] = sent
        prob["pronoun"] = pronoun
        prob["ans"] = ans
        prob["choice1"] = choice1
        prob["choice2"] = choice2
        prob["know_sent"] = "NA"
        prob["search_query"] = "NA"
        prob["know_url"] = "NA"

        list_of_wsc_probs.append(prob)

    return list_of_wsc_probs            
            


if __name__=="__main__":
    #xml_data_file_path = "./WSCollection.xml"
    #wsc_data = main(xml_data_file_path)
    #with open('wsc_problems.json', 'wt') as out:
    #    pprint(wsc_data, stream=out)

#    all_sents_old = set()
    #count = 0
    #total = 0
    sent_prob_dict = {}
    with open('../inputs/wsc_problems_final.json','r') as f1:
        wsc_probs = f1.read()
        wsc_probs_list = ast.literal_eval(wsc_probs)#json.loads(wsc_probs)
        for item in wsc_probs_list:
            #total+=1
            know_sent = item["know_sent"]
            if know_sent == "NA":
                print(item["ws_sent"])
                #count+=1
            #sent = item["ws_sent"]
            #sent_prob_dict[sent] = item
    
    #print("COUNT: ",count)
    #print("TOTAL: ",total)
    '''
    all_probs =[]
    with open('wsc_problems_processed.json','r') as f:
        data = f.read()
        data_list = ast.literal_eval(data)
        for item in data_list:
            if item["ws_sent"] in sent_prob_dict.keys():
                new_item = sent_prob_dict[item["ws_sent"]]
                if "know_sent" not in new_item.keys():
                    new_item["know_sent"] = "NA"
                if "know_url" not in new_item.keys():
                    new_item["know_url"] = "NA"
                if "search_query" not in new_item.keys():
                    new_item["search_query"] = "NA"

                all_probs.append(new_item)
            else:
                item["know_sent"] = "NA"
                item["know_url"] = "NA"
                item["search_query"] = "NA"
                all_probs.append(item)
        with open('wsc_problems_final.json', 'wt') as out:
            pprint(all_probs, stream=out)

            
    #for sent in all_sents_new:
    #    if sent not in all_sents_old:
    #        print(sent)
    
    '''


