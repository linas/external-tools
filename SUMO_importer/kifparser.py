# S-expression parser adapted for SUO-kif expressions. In particular
# it skips things like documentation, comments, termFormat and such.

def removeExtra(orgString, index):
    #removes the parenthesis at the given index
    newSymbolString = orgString[:index]  + orgString[index+1:]
    return newSymbolString

def match_parenthesis(symbolString):
    ## close any and all open parenthesises & return a "file" to be processed further... 
    from pythonds.basic.stack import Stack
    s = Stack()
    balanced = True
    index = 0
    while index < len(symbolString) and balanced:
        symbol = symbolString[index]
        if symbol == "(":
            s.push(symbol+ str(index))
        elif symbol == ")":
            if s.isEmpty():
                balanced = False
            else:
                s.pop()

        index = index + 1

    if balanced and s.isEmpty():
        return symbolString
    elif balanced and not s.isEmpty():
        idx = int (s.pop().strip("("))
        return (match_parenthesis(removeExtra(symbolString,idx)))
    else:   #couldn't pop from stack
        return (match_parenthesis(removeExtra(symbolString,index-1)))

def skip_comments(myfile):

    '''You can't use this function directly because it would break parsing of multiline expressions'''
    copying = True

    for line in myfile:

        '''' skip documentation and such'''
        if copying:
            if line.startswith('(documentation ') \
               or line.startswith('(comment ') \
               or line.startswith('(termFormat ') \
               or line.startswith('(format ') \
               or line.startswith('(utterance ') \
               or line.startswith('(externalImage '):
                if '")' in line:
                    line = ""
                    copying = True
                else:
                    copying = False
        elif '")' in line and copying == False:
            line = ""
            copying = True

        if copying == False:
            line = ""

        '''' skip comments'''
        if not ';' in line:
            line = line.rstrip()
            yield line

def read_kif_file(filename):
    with open(filename, 'rt') as myfile:
        return '\n'.join(skip_comments(myfile))

def remove_blank_lines(text):
    return "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])

def parse_kif_string(inputdata):
    '''Returns a list containing the ()-expressions in the file.
    Each list expression is converted into a Python list of strings. Nested expressions become nested lists''' 
    # Very simple one which can't handle quotes properly for example

    #*** Check that parenthisis is matched on input data
    matched = match_parenthesis(inputdata)

    matched = remove_blank_lines(matched)

    if not matched:
        return []

    from pyparsing import OneOrMore, nestedExpr
    return OneOrMore(nestedExpr()).parseString(matched)

def parse_kif_file(filename):
    return parse_kif_string(read_kif_file(filename))
