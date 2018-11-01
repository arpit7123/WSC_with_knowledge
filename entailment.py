from allennlp.predictors.predictor import Predictor

predictor = Predictor.from_path("./esim-elmo-2018.05.17.tar.gz")



if __name__=="__main__":
    h = "Anna did a lot better than her good friend Lucy on the test because Anna had studied so hard ."
    p = "Anna succeeded because Anna studied hard ."
    score = predictor.predict(hypothesis=h,premise=p)["label_probs"]
    print("SCORE: ",score)
