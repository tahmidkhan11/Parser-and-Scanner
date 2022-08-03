from typing import List
import re

class Scanner:

    def __init__(self, a: List):
        #array of lines segmented into an array that is parsed
        self.a = a
        # variable to keep track of if you're in the middle of a comment or not
        self.commentOpen = False
        # array of tokens that will be returned when Scanner.scan() runs
        # that hold the list of tokens in a batch
        self.tokens = []
        self.batchList = []
        self.resetter = 0

    def scan(self):
        #for each line that is in a batch
        for k in range(len(self.a)):
            # print('loop: {0}'.format(k+1))
            #one liner comment
            if '/*' in self.a[k] and '*/' in self.a[k]:
                continue

            #beginning of a multi-line comment
            #if /* is contained in the line then declare it as the beginning of a comment
            if '/*' in self.a[k]:
                self.commentOpen = True

            #end of a multi-line comment
            #if */ is contained in the line then declare it as the end of a comment
            elif '*/' in self.a[k]:
                self.commentOpen = False

            #no white spaces EX's: "five" or "3.14159 54"
            elif (' ' not in self.a[k]) and self.commentOpen == False:
                if self.a[k] == 'read':
                    self.tokens.append('read')
                    self.batchList.append('read')
                elif self.a[k] == 'write':
                    self.tokens.append('write')
                    self.batchList.append('write')
                else:
                    try:

                        for i in range(len(self.a[k])):
                            # print(self.a[k])
                            if self.a[k][i] == '(':
                                self.tokens.append('lparen')
                                self.batchList.append('(')
                            elif self.a[k][i] == ')':
                                self.tokens.append('rparen')
                                self.batchList.append(')')
                            elif self.a[k][i] == '+':
                                self.tokens.append('plus')
                                self.batchList.append('+')
                            elif self.a[k][i] == '-':
                                try:
                                    check = float(self.a[k])
                                    if isinstance(check, float):
                                        if check * -1 > 0:
                                            continue
                                except:
                                    self.tokens.append('minus')
                                    self.batchList.append('-')
                                    # print(self.a[k][i])
                            elif self.a[k][i] == '/':
                                self.tokens.append('div')
                                self.batchList.append('/')
                            elif self.a[k][i] == '*':
                                self.tokens.append('mult')
                                self.batchList.append('*')
                            elif self.a[k][i] == ':' and self.a[k][i+1] == '=':
                                self.tokens.append('assign')
                                self.batchList.append(':-')
                            elif self.a[k][i].isnumeric():
                                try:
                                    check = float(self.a[k])
                                    # '123', '-10', '2.34', etc
                                    if isinstance(check, float):
                                        self.tokens.append('number')
                                        self.batchList.append(self.a[k])
                                        break
                                except:
                                    if self.a[k].isalnum():
                                        print('error')
                                        break
                                    #throw error for '1.2.3'
                                    elif self.a[k].count('.') > 1:
                                        raise ValueError('error')

                                    elif self.a[k].isnumeric():
                                        self.tokens.append('number')
                                        self.batchList.append(self.a[k])
                                        break
                                    #do something here if element is a number ex 3.13)
                                    elif len(self.tokens) == 0 or self.tokens[-1] != 'number':
                                        tokenValue = re.search(r'\((.*?)\)',self.a[k]).group(1)
                                        self.tokens.append('number')
                                        self.batchList.append(tokenValue)
                            # to identify if token is a valid id
                            elif self.a[k][i].isalpha():
                                #do something here if element is a letter (A-Z,a-z,1-9)
                                if self.a[k].isalnum():
                                    self.tokens.append('id')
                                    self.batchList.append(self.a[k])
                                    break
                                else:
                                    raise ValueError('error')
                    except:
                        print('error')
                # print('tokens for {0}: {1}'.format(self.a[k], self.tokens))
        # print('tokens: {0}'.format(self.tokens))
            #check to see if there are multiple possible tokens such as "five 5"
            #if the line has multiple possible tokens and is not a comment
            elif (' ' in self.a[k]) and (self.commentOpen == False):
                tokens = self.a[k].split()
                try:
                    for token in tokens:
                        if token == 'read':
                            self.tokens.append('read')
                            self.batchList.append('read')
                        elif token == 'write':
                            self.tokens.append('write')
                            self.batchList.append('write')
                        #identify what the a specific index in the token is
                        else:
                            for i in range(len(token)):
                                if token[i] == '(':
                                    self.tokens.append('lparen')
                                    self.batchList.append('(')
                                elif token[i] == ')':
                                    self.tokens.append('rparen')
                                    self.batchList.append(')')
                                elif token[i] == '+':
                                    self.tokens.append('plus')
                                    self.batchList.append('+')
                                elif token[i] == '-':
                                    check = float(token)
                                    if isinstance(check, float):
                                        if check * -1 > 0:
                                            continue
                                    else:
                                        self.tokens.append('minus')
                                        self.batchList.append('-')
                                elif token[i] == '/':
                                    self.tokens.append('div')
                                    self.batchList.append('/')
                                elif token[i] == '*':
                                    self.tokens.append('mult')
                                    self.batchList.append('*')
                                elif token[i] == ':' and token[i+1] == '=':
                                    self.tokens.append('assign')
                                    self.batchList.append(':-')
                                elif token[i].isnumeric():
                                    try:
                                        check = float(token)
                                        # '123', '-10', '2.34', etc
                                        if isinstance(check, float):
                                            self.tokens.append('number')
                                            self.batchList.append(token[i])
                                            break

                                    except:
                                        #throw error for '1.2.3'
                                        if token.count('.') > 1:
                                            raise ValueError('error')

                                        elif token.isnumeric():
                                            self.tokens.append('number')
                                            self.batchList.append(token)
                                            break
                                        #do something here if element is a number ex 3.13)
                                        elif len(self.tokens) == 0 or self.tokens[-1] != 'number':
                                            self.tokens.append('number')
                                            self.batchList.append(token)
                                # to identify if token is a valid id
                                elif token[i].isalpha():
                                    #do something here if element is a letter (A-Z,a-z,1-9)
                                    if token.isalnum():
                                        self.tokens.append('id')
                                        self.batchList.append(token)
                                        break
                                    else:
                                        raise ValueError('error')
                except:
                    print('error')

        return(self.tokens)

    def list(self):
        return self.batchList