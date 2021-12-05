import tokenize

#Code adapted from https://stackoverflow.com/questions/34511673/extracting-comments-from-python-source-code
def getComments(fileName, startLineNo, endLineNo):
    with open(fileName, 'r') as f:
        comments = list()
        for toktype, tok, start, end, line in tokenize.generate_tokens(f.readline):
            if toktype == tokenize.COMMENT and startLineNo<=start[0] and endLineNo>=end[0]:
                comments.append(tok)
            
    return comments