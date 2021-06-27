
#pip install nltk
# pip install nltk==3.5
# pip install numpy matplotlib
from chemdataextractor import Document
import nltk
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
# with open("C:/Users/nuche/Downloads/exercise_experimentals.txt", 'r') as file:
#     data = file.read().replace('\n', '')
# tokens = word_tokenize(data)
# print(tokens)
f = open("C:/Users/nuche/Downloads/exercise_experimentals.txt", 'rb')
doc = Document.from_file(f)
doc.elements
# for para in doc.elements:
#     for sente in para.sentences:
#       tokens = sente.pos_tagged_tokens
#       print(tokens)
#       print()
token_1st_para= doc.elements[0][0].pos_tagged_tokens
print(token_1st_para)
grammar = "Addition: {<VBN><IN><DT><NN>}"
chunk_parser = nltk.RegexpParser(grammar)
tree = chunk_parser.parse(token_1st_para)
tree
tree.draw()
#para=doc.elements[0]
#para.tokens
#doc[0].records.serialize()
#doc.records.serialize()
