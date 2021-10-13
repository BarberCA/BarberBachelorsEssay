import ast, json, ast2json
import getTemplate as gtl

def main():#C:/Users/Carson Barber/Documents/Work/School/Bachelor's Essay/test.py
    with open("sampleCode.py", 'r') as f:
        astTree = ast.parse(f.read())
        f.close
    jsonTree = ast2json.ast2json(astTree)
    with open("data.json", 'w') as f:
        f.write(json.dumps(jsonTree, indent=4))
        f.close
    with open("data.json", 'r') as f:
        tree = json.load(f)
        f.close
    #argument = tree['body'][1]['args']['args'][0]['arg']
    #argType = tree['body'][1]['args']['args'][0]['_type']
    funcTree = tree['body'][1]
    template = gtl.getTemplate(funcTree)
    print(template)
    print("DONE")

if __name__ == '__main__':
    main()