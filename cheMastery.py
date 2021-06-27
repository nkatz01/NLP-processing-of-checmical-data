
#pip install nltk
# pip install nltk==3.5
# pip install numpy matplotlib
from chemdataextractor import Document
import nltk
import itertools
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
from chemdataextractor.nlp.pos import ChemCrfPosTagger
# with open("C:/Users/nuche/Downloads/exercise_experimentals.txt", 'r') as file:
#     data = file.read().replace('\n', '')
# tokens = word_tokenize(data)
# print(tokens)
f = open("C:/Users/nuche/Downloads/exercise_experimentals.txt", 'rb')
doc = Document.from_file(f)
doc.elements
all_sentences_in_para_tagged = []
# for para in doc.elements:
#     for sente in para.sentences:
#       tokens = sente.pos_tagged_tokens
#       print(tokens)
#       print()

# for sente in doc.elements[0]:
#     sentencesList.append(sente.pos_tagged_tokens)

para = doc.elements[0]
token_1st_para = para.raw_tokens
#sentencesList = para
#print(sentencesList)
#token_1st_para= doc.elements[0][0].pos_tagged_tokens
#token_1st_para= sentencesList.pos_tagged_tokens
print(token_1st_para)
print(len(token_1st_para))
cpt = ChemCrfPosTagger()
for para in doc.elements:
    para_tokens = para.raw_tokens
    for sente in para_tokens:
         all_sentences_in_para_tagged.append(cpt.tag(sente))
    para_tagged_tokens= list(itertools.chain(*all_sentences_in_para_tagged))
    print(para_tagged_tokens)
    print("\n")
         

grammar = "Addition: {<VBD><VBN><IN><DT><NN><IN><NN><-LRB-><CD><NN>}"
chunk_parser = nltk.RegexpParser(grammar)
tree = chunk_parser.parse(token_1st_para)
tree
tree.draw()
#para=doc.elements[0]
#para.tokens
#doc[0].records.serialize()
#doc.records.serialize()
