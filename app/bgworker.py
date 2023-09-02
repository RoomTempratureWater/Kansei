from bs4 import BeautifulSoup, NavigableString, Tag
import markdown
from .hfapi import summarys, questions
import re
import json

class bgworker():
    
    def __init__(self, file) -> None:
        self.mdfile = file
        self.doc = {}
    
    async def get_doc_dict(self):
        # comment these 2 lines later
        # a = open("Data Structures and Algorithms.md", "r+")
        # a = a.read()

        a_html = markdown.markdown(self.mdfile)

        soup = BeautifulSoup(a_html, 'html.parser')
        for header in soup.find_all(re.compile('^h[1-6]$')):
            nextNode = header
            to_change = ""
            ht = header.decode_contents()
            self.doc[ht] = {}
            l = []
            quests = []
            total_text = ""
            while True:
                nextNode = nextNode.nextSibling
                if nextNode is None:
                    summary = summarys(total_text)
                    #print(type(summary))
                    self.doc[ht] = {"summary": summary, "indiv_text": l, "questions": quests}
                    break
                # if isinstance(nextNode, NavigableString):
                #     print(str(nextNode.string).strip())
                #     continue
                if isinstance(nextNode, Tag):
                    #print(nextNode.name)
                    if nextNode.name[0] == 'h':
                        summary = str(summarys(total_text))
                        self.doc[ht] = {"summary": summary, "indiv_text": l, "questions": quests}
                        break
                    if nextNode.name == "ul":
                        a = nextNode.find_all('li')
                        for i in a:
                            temp = i.get_text(strip=True)
                            l.append(temp)
                            quests.append(questions(temp))
                            total_text += " " + temp
                            #i.string = "changed this ahahaha" #chaning the AST
                    if nextNode.name == "p":
                        s = str(nextNode.string).strip()
                        #print("in:", s)
                        #nextNode.string = "changed this ahahaha" #chaning the AST
                        #print(s)
                        total_text += " " + s
                        l.append(s)
                        quests.append(questions(s))
        #return self.doc
        return self.doc
    

