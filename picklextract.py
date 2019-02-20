import pickle
import json
if __name__=="__main__":                                                        
	file = open("wsc273_probs.pkl",'rb')                                        
	object_file = pickle.load(file)                                             
	file.close()

with open('scr_wsc273_prob.json', 'w') as outfile:
        json.dump(object_file, outfile)
