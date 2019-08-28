
import xml.etree.ElementTree as ET
import json


def parse():
    # create element tree object
    tree = ET.parse('COPA/copa-all.xml')

    # get root element
    root = tree.getroot()

    total_copa_ques = []
    # iterate news items
    for item in root:
        # empty obj dictionary
        obj = {}
        # iterate child elements of item
        for child in item:
            if child.tag == 'p':
                obj['question'] = child.text
            if child.tag == 'a1':
                obj['choice1'] = child.text
            if child.tag == 'a2':
                obj['choice2'] = child.text
        obj['asks-for'] = item.attrib['asks-for']
        obj['answer'] = item.attrib['most-plausible-alternative']
        obj['id'] = item.attrib['id']
        total_copa_ques.append(obj)

    for each in total_copa_ques:
        each['alternate1'] = each['question'] + ' ? ' + each['choice1']
        each['alternate2'] = each['question'] + ' ? ' + each['choice2']

    with open('COPA/copa-all.json', 'w') as outfile:
        json.dump(total_copa_ques, outfile)


def QASRL_Parse():
    with open('/Users/ash/Documents/Study/Research/COPA-resources/datasets/copa-all.json', 'r') as json_file:
        copa_data = json.loads(json_file.read(), strict=False)
        i = 1
        for each in copa_data:
            obj1 = {}
            obj1['sentence'] = each['question'] + ' ' + each['choice1']
            obj2 = {}
            obj2['sentence'] = each['question'] + ' ' + each['choice2']
            with open('/Users/ash/Documents/Study/Research/COPA-resources/datasets/qasrl/q'+str(i)+'.json', 'w') as outfile:
                json.dump(obj1, outfile)
            i = i + 1
            with open('/Users/ash/Documents/Study/Research/COPA-resources/datasets/qasrl/q'+str(i)+'.json', 'w') as outfile:
                json.dump(obj2, outfile)
            i = i + 1


parse()
