

def get_all_incorrects(file_name):
    with open(file_name) as f:
        content = f.readlines()

    all_incorrects = []
    prev_line = None
    curr_line = None
    for i in range(0,len(content)):
        curr_line = content[i].rstrip()
        if i>0:
            prev_line = content[i-1].rstrip()
        
        if curr_line == "************************************************************":
            an_incorrect = []
            an_incorrect.append(curr_line)
            i += 1
            if i < len(content):
                curr_line = content[i].rstrip()
                prev_line = content[i-1].rstrip()
                while curr_line != "************************************************************":
                    an_incorrect.append(curr_line)
                    i+=1
                    if i<len(content):
                        curr_line = content[i].rstrip()
                        prev_line = content[i-1].rstrip()
                an_incorrect.append(curr_line)
                if prev_line == "RESULT:  incorrect":
                    all_incorrects.append(an_incorrect)

        i+=1

    return all_incorrects

def into_tsv(file_name):
    with open(file_name) as f:
        content = f.readlines()

    all_incorrects = set()
    prev_line = None
    curr_line = None
    for i in range(0,len(content)):
        curr_line = content[i].rstrip()
        if i>0:
            prev_line = content[i-1].rstrip()

        if curr_line == "************************************************************":
            an_incorrect = []
            if curr_line.startswith('SENT:') or curr_line.startswith('KNOW SENT:'):
                an_incorrect.append(curr_line)
            i += 1
            if i < len(content):
                curr_line = content[i].rstrip()
                prev_line = content[i-1].rstrip()
                while curr_line != "************************************************************":
                    if curr_line.startswith('SENT:') or curr_line.startswith('KNOW SENT:'):
                        an_incorrect.append(curr_line)
                    i+=1
                    if i<len(content):
                        curr_line = content[i].rstrip()
                        prev_line = content[i-1].rstrip()
                if curr_line.startswith('SENT:') or curr_line.startswith('KNOW SENT:'):
                    an_incorrect.append(curr_line)

                #if prev_line == "RESULT:  incorrect":
                #    all_incorrects.append(an_incorrect)
        if len(an_incorrect)==2:
            #print(an_incorrect[0]+"\t"+an_incorrect[1])
            all_incorrects.add(an_incorrect[0]+"\t"+an_incorrect[1])
        i+=1

    return all_incorrects



if __name__=="__main__":
    incorrects = into_tsv("incorrects_nov10")
    for incorrect in incorrects:
        print(incorrect)
    #all_incorrects = get_all_incorrects("incorrects_nov10")#"output_nov10_2_ent_only")
    #for incorrect in all_incorrects:
    #    for line in incorrect:
    #        print(line)
