from allennlp.predictors.predictor import Predictor
from allennlp.predictors import Predictor
from allennlp.models.archival import load_archive
import json

#model = PretrainedModel('./esim-elmo-2018.05.17.tar.gz','textual-entailment')
#predictor = model.predictor()


class PretrainedModel:
    """
    A pretrained model is determined by both an archive file
    (representing the trained model)
    and a choice of predictor.
    """
    def __init__(self, archive_file: str, predictor_name: str) -> None:
        self.archive_file = archive_file
        self.predictor_name = predictor_name

    def predictor(self) -> Predictor:
        archive = load_archive(self.archive_file)
        return Predictor.from_archive(archive, self.predictor_name)


def rank_knowledge():
    model = PretrainedModel('../esim-elmo-2018.05.17.tar.gz','textual-entailment')
    predictor = model.predictor()
    
    problems = "../data_sets/winogrande/knowledge_queries.json"
    f = open(problems, "r")
    all_probs = f.read()
    knowledge = json.loads(all_probs)
    for i in range(290, len(knowledge)):
        each = knowledge[i][0]
        q = each['question']
        obj = []
        for k in each['knowledge']:
            if len(k)== 0:
                continue
            score = predictor.predict(hypothesis=k,premise=q)["label_probs"]
            o = {}
            o['k'] =  k
            o['score'] = score[0]
            obj.append(o)
        obj.sort(key=lambda x: x['score'], reverse=True)
        each['knowledge'] = obj
        length = 10
        if(len(obj) > 10):
            new_obj = obj[0:10]
        else:
            new_obj = obj
        for e in new_obj:
            out = {}
            out['sentence'] = e['k']
            with open('../data_sets/winogrande/QASRL/winogrande_knowledge_score.txt', 'a') as outfile:
                json.dump(out, outfile)
                outfile.write('\n')
        print(str(i+1)+'/2863')
        
    with open('../data_sets/winogrande/knowledge_queries.json', 'w') as outfile:
        json.dump(knowledge, outfile)


if __name__=="__main__":
    problems = "../data_sets/winogrande/knowledge_queries.json"
    f = open(problems, "r")
    all_probs = f.read()
    knowledge = json.loads(all_probs)
    
    knowledge_qasrl = "../data_sets/winogrande/QASRL/winogrande_knowledge_score_290.txt"
    f1 = open(knowledge_qasrl, "r")
    knowledge_qasrl_txt = f1.read()
    knowledge_qasrl_out = knowledge_qasrl_txt.split('\n')
    start = 0
    for i in range(0, len(knowledge)):
        if(i == 290):
            break
        each = knowledge[i][0]
        length = 10
        if(len(each['knowledge']) < 10):
            length = len(each['knowledge'])
            
        knowledge_objects = []
        for j in range(start, len(knowledge_qasrl_out)):
            if(j >= (start + length)):
                start = start + length
                break
            json_obj = json.loads(knowledge_qasrl_out[j])
            new_obj = {}
            new_obj['k'] = json_obj['sentence']
            knowledge_objects.append(new_obj)
        each['knowledge'] = knowledge_objects
    
    with open('../data_sets/winogrande/knowledge_queries.json', 'w') as outfile:
        json.dump(knowledge, outfile)
            
            
        
        
        
  