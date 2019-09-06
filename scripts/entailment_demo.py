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




if __name__=="__main__":
    model = PretrainedModel('../esim-elmo-2018.05.17.tar.gz','textual-entailment')
    predictor = model.predictor()
    
    problems = "../data_sets/winogrande/knowledge_queries.json"
    f = open(problems, "r")
    all_probs = f.read()
    knowledge = json.loads(all_probs)

    correct = 0
    incorrect = 0
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
