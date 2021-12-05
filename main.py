import ast, json, ast2json
import getTemplate as gtl
import getComments as gcm

def main():
    file_name = "sampleCode.py"
    with open(file_name, 'r') as f:
        astTree = ast.parse(f.read())
        f.close
    jsonTree = ast2json.ast2json(astTree)
    dumped = json.dumps(jsonTree, indent=4)
    tree = json.loads(dumped)
    funcTree = tree['body'][1]
    funcStartLineNo = funcTree['lineno']
    funcEndLineNo = funcTree['end_lineno']
    prevComLines = 3#Number of lines before the function to extract comments from.
    comments = gcm.getComments(file_name, funcStartLineNo-prevComLines, funcEndLineNo)
    template = gtl.getTemplate(funcTree, comments)
    print(template)
    print("DONE")

if __name__ == '__main__':
    main()