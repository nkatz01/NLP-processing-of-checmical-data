
#pip install nltk
# pip install nltk==3.5
# pip install numpy matplotlib
from chemdataextractor import Document
import nltk
import itertools
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
from chemdataextractor.nlp.pos import ChemCrfPosTagger 
from chemdataextractor.nlp.tokenize  import  ChemWordTokenizer
# with open("C:/Users/nuche/Downloads/exercise_experimentals.txt", 'r') as file:
#     data = file.read().replace('\n', '')
# tokens = word_tokenize(data)
# print(tokens)
f = open("C:/Users/nuche/Downloads/exercise_experimentals.txt", 'r', encoding="utf-8")
content_to_str = f.read(-1)
content_to_str =content_to_str.replace(u"\u2013",u"\u002D")
#print(content_to_str)
#print(type(what))
#type(f)
#doc = Document.from_file(f)
doc = Document(content_to_str)

#print(type(doc))
all_sentences_in_para_tagged = []
# for para in doc.elements:
#     for sente in para.sentences:
#       tokens = sente.pos_tagged_tokens
#       print(tokens)
#       print()

# for sente in doc.elements[0]:
#     sentencesList.append(sente.pos_tagged_tokens)

#para = doc.elements[0]
#token_1st_para = para.raw_tokens
#sentencesList = para
#print(sentencesList)
#token_1st_para= doc.elements[0][0].pos_tagged_tokens
#token_1st_para= sentencesList.pos_tagged_tokens
#print(token_1st_para)
#print(len(token_1st_para))
#print(doc.records.serialize())
cwt = ChemWordTokenizer()
cpt = ChemCrfPosTagger()
copied_chem_records = {}
copied_para_tagged_tokens = []
for chem in doc.records.serialize() :
    for part in chem["names"][0].split(' '):
        if cpt.tag(cwt.tokenize(part))[0][1]!='JJ':#
            copied_chem_records[part]='CHEM'
copied_chem_records

para_tokens = doc.elements[0].raw_tokens
#print("\n")
#print(para_tokens)
all_sentences_in_para_tagged = []
copied_para_tagged_tokens = []
for sente in para_tokens:
     all_sentences_in_para_tagged.append(cpt.tag(sente))
     para_tagged_tokens= list(itertools.chain(*all_sentences_in_para_tagged))
for tupe in para_tagged_tokens:
     #tru = next((item for item in doc.records.serialize() if item["names"] == [tupe[0]]),None) 
     #if tru != None:
     if tupe[0] in copied_chem_records:
                 # if any(tupe[0] in key for key in copied_chem_records) and tupe[1]=='NN':
       #tupe = (tupe[0],'CHEM')
       copied_para_tagged_tokens.append( (tupe[0],'CHEM'))
     else:
       # tupe = (tupe[0],tupe[1])
       copied_para_tagged_tokens.append(tupe)
         # as_list = list(tupe)
         # as_list[1] = 'CHEM'
         # tupe = tupe(as_list)
print(copied_para_tagged_tokens)
print("nuchem")
    
    #print(para_tagged_tokens)
    # myList = iter( doc.records.serialize())
# for count in range(len(doc.records.serialize())):
#     x =next(myList)
#     print(x)
# t = "names"
# item == None
#grammar = "Addition: {<VBD><VBN><IN><DT><NN><IN><NN><-LRB-><CD><NN>}"
grammar = "Addition: {<VBD><VBN><IN><DT><NN><IN><NN><-LRB-><CD><NN>}"

chunk_parser = nltk.RegexpParser(grammar)
tree = chunk_parser.parse(token_1st_para)
tree
tree.draw()
#para=doc.elements[0]
#para.tokens
#doc[0].records.serialize()
type(doc.records.serialize()[0])
