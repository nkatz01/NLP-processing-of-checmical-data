
#pip install nltk
# pip install nltk==3.5
# pip install numpy matplotlib
#from chempy import Substance
import re
from chemdataextractor import Document
from nltk.chunk.regexp import RegexpChunkRule
import nltk
import itertools
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
from chemdataextractor.nlp.pos import ChemCrfPosTagger
from chemdataextractor.doc import Paragraph 
from chemdataextractor.nlp.tokenize  import  ChemWordTokenizer
# with open("C:/Users/nuche/Downloads/exercise_experimentals.txt", 'r') as file:
#     data = file.read().replace('\n', '')
# tokens = word_tokenize(data)
# print(tokens)
f = open("C:/Users/nuche/Downloads/exercise_experimentals.txt", 'rb')
f1 = open("C:/Users/nuche/Downloads/exercise_experimentals.txt", 'r', encoding="utf-8")
#content_to_str = f.read(-1)
#content_to_str =content_to_str.replace(u"\u2013",u"\u002D")
#print(content_to_str)
#print(type(what))
#type(f)
doc = Document.from_file(f)
#doc = Document(content_to_str)

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
# for chem in doc.records.serialize() :
#     for part in chem["names"][0].split(' '):
#         if cpt.tag(cwt.tokenize(part))[0][1]!='JJ':#
#             copied_chem_records[part]='CHEM'
# copied_chem_records
# tokens = cwt.tokenize("The yellow complex, chloro(ƞ4–cycloocta–1,5–diene)(1,3-dimesitylimidazol-2-ylidene) iridium(I) (0.700 g, 1.093 mmol ) , 30 was dissolved in dry THF (15 mL)")
# print(tokens)
# print()
for line in f1:
    if line=="\n":
        continue
    content_to_str =line.replace(u"\u2013",u"\u002D")
    for chem in Document(content_to_str)[0].cems :
        for part in str(chem).split(' '):
            if cpt.tag(cwt.tokenize(part))[0][1]!='JJ':#
                copied_chem_records[part]='CHEM'
            #print(part)
    #print(copied_chem_records)
    para_tokens = Document(content_to_str)[0].raw_tokens
    #para_tokens = doc.elements[0].raw_tokens
    #print("\n")
    #print(para_tokens)
    #print("endOfPara")
    all_sentences_in_para_tagged = []
    copied_para_tagged_tokens = []
    for sente in para_tokens:
         all_sentences_in_para_tagged.append(cpt.tag(sente))
         para_tagged_tokens= list(itertools.chain(*all_sentences_in_para_tagged))
    needed_tokens = {"VB","VBG","VBN","NN","CHEM","TO","CC","-LRB-","-RRB-","CD",".","NNP","NNPS","NNS","IN","JJ","RB"}
    #print(para_tagged_tokens)
    #print("endOfPara")
    for tupe in range(len( para_tagged_tokens)):
        #tru = next((item for item in doc.records.serialize() if item["names"] == [tupe[0]]),None) 
        #if tru != None:
        if para_tagged_tokens[tupe][0] in copied_chem_records or (para_tagged_tokens[tupe-1][0] == "of" and para_tagged_tokens[tupe][1].startswith("NN")) :
                    # if any(tupe[0] in key for key in copied_chem_records) and tupe[1]=='NN':
          #tupe = (tupe[0],'CHEM')
          copied_para_tagged_tokens.append( (para_tagged_tokens[tupe][0],'CHEM'))
        elif para_tagged_tokens[tupe][1] not in needed_tokens :
          # tupe = (tupe[0],tupe[1])
          copied_para_tagged_tokens.append((para_tagged_tokens[tupe][0],'REMO'))
        else :
          copied_para_tagged_tokens.append(para_tagged_tokens[tupe])
    #print(copied_para_tagged_tokens)
    #print("endOfPara")
    copied_para_tagged_tokens[:] = [tupl for tupl in copied_para_tagged_tokens if tupl[1] !="REMO"]
    #print(copied_para_tagged_tokens)
    #print("endOfPara")#UNITS: {<-LRB-><.*>*?<-RRB->}
    units_grammer = """UNITS: {<-LRB-><CD|IN|JJ|NN|NNS|CHEM>*<-RRB->}
    {<CD><NN>}
    """#  {(<CD><NN>)*}
    units_parser = nltk.RegexpParser(units_grammer)
    para_units_condesed = units_parser.parse( copied_para_tagged_tokens)
    #print(para_units_condesed)
    # print(para_units_condesed)
    # print("endOfPara")
    #print(para_units_condesed.draw())
    
    
    
    for subtree in range(len(para_units_condesed)) :
        if type(para_units_condesed[subtree]) == nltk.tree.Tree and  type(para_units_condesed[subtree-1]) !=  nltk.tree.Tree : 
            
            #para_units_condesed[subtree-1][1]='CHEM'
            units_chunk_merged = ' '.join(c[0] for c in para_units_condesed[subtree])
            a = re.compile(r'\bmmol\b', re.IGNORECASE)
            b = re.compile(r'\bmol\b', re.IGNORECASE)
            c = re.compile(r'\bmg\b', re.IGNORECASE)
            d = re.compile(r'\bml\b', re.IGNORECASE)
            #NN_tag = re.compile(r'NN.?')
            #print(type(para_units_condesed[subtree-1]))
            if  (( a.search( units_chunk_merged) or b.search( units_chunk_merged) or c.search( units_chunk_merged) or d.search( units_chunk_merged))
             and (  para_units_condesed[subtree-1][1] == "NN" or para_units_condesed[subtree-1][1] == "JJ" )):
                copied_chem_records[para_units_condesed[subtree-1][0]]='CHEM'
                #print(para_units_condesed[subtree-1][0])
                #print(' '.join(c[0] for c in para_units_condesed[subtree]))
            #elif para_units_condesed[subtree+2][1] =="NNP"
    copied_para_tagged_tokens = []
    for tupe in range(len(para_units_condesed)):
        if type(para_units_condesed[tupe]) != nltk.tree.Tree :
            if para_units_condesed[tupe][0] in copied_chem_records :
                copied_para_tagged_tokens.append( (para_units_condesed[tupe][0],'CHEM'))
            elif ((para_units_condesed[tupe][0].lower().startswith("add") and not(para_units_condesed[tupe][0].lower().endswith("nal"))) or ('dissolved' in para_units_condesed[tupe][0] and para_units_condesed[tupe+1][1]=='IN' )) :
                copied_para_tagged_tokens.append((para_units_condesed[tupe][0],'ADD'))
            elif  ('dropwise' in para_units_condesed[tupe][0]) :
                copied_para_tagged_tokens.append((para_units_condesed[tupe][0],'PORTN'))
            elif (para_units_condesed[tupe][1].startswith("NN") and  not(para_units_condesed[tupe][1].endswith("NP"))) or para_units_condesed[tupe][1] == "IN" or para_units_condesed[tupe][1] == "."  or para_units_condesed[tupe][1] == "JJ" or para_units_condesed[tupe][1] == "-LRB-" or para_units_condesed[tupe][1] == "RB":
                continue
            else:
                copied_para_tagged_tokens.append(para_units_condesed[tupe])
        # elif tupe[1] not in needed_tokens :
        #   copied_para_tagged_tokens.append((tupe[0],'REMO'))
        else :
          copied_para_tagged_tokens.append(para_units_condesed[tupe])
    print(copied_para_tagged_tokens)
    # print("endOfPara")
    # units_grammer = """UNITS: {<-LRB-><CD|IN|NN|>*<-RRB->}
    # {<CD><NN>}"""
    # units_parser = nltk.RegexpParser(units_grammer)
    # para_units_condesed = units_parser.parse( copied_para_tagged_tokens)
    # para_units_condesed.draw()
    #print("endOfPara")
    #units_grammer = "ADDITION: {(<CHEM>+<UNITS>?<CC>?)+<ADD>(<CHEM>+<UNITS>?<CC>?)}<VBN>"
    whole_chem_grammer = """CH&UNT: {<CHEM>+<UNITS>|<UNITS><CHEM>+}
    NNP&UNT: {<NNP>+<UNITS>|<UNITS><NNP>+}"""
    #{(<UNITS><CHEM>+)?}
   
    # {<UNITS><NNP>+}

    chem_and_unit_parser = nltk.RegexpParser(whole_chem_grammer)
    para_units_condesed = chem_and_unit_parser.parse( copied_para_tagged_tokens)
    #para_units_condesed.draw()
    
    addition_grammer = """ADDITION: {(<CH&UNT|NNP&UNT>+<UNITS>?<CC>?)+<PORTN>?<ADD><PORTN>?(<CH&UNT|NNP&UNT>+<UNITS>?<CC>?)+(^<VB.*>)*}"""
    # {(<UNITS>*<CHEM|NNP>+<UNITS>*<CC>?)+<ADD><PORTN>?(^<VB.*>)*}
    # {(^<VB.*>)*<PORTN>?<ADD>(<UNITS>*<CHEM|NNP>+<UNITS>*<CC>?)+}
    addition_parser = nltk.RegexpParser(addition_grammer)
    para_units_condesed = addition_parser.parse(para_units_condesed)
    para_units_condesed.draw()
    
    addition_grammer = """ADDITION2SIDE: {(<CHEM|NNP>+<UNITS>*<CC>?)+<PORTN>?<ADD><PORTN>?(<UNITS>*<CHEM|NNP>+<UNITS>*<CC>?)+(^<VB.*>)*}
    ADDITIONLEFT: {(<CHEM|NNP>+<UNITS>*<CC>?)+<ADD><PORTN>?(^<VB.*>)*}
    ADDITIONRIGHT: {(^<VB.*>)*<PORTN>?<ADD>(<CHEM|NNP>+<UNITS>*<CC>?)+}
    """
    #LRB added to line two to deal with some tokinization issue
    addition_parser = nltk.RegexpParser(addition_grammer)
    para_units_condesed = addition_parser.parse( copied_para_tagged_tokens)
    #print(copied_para_tagged_tokens)
    #print("endOfPara")
    para_units_condesed.draw()
# p = Paragraph('methylbenzaldehyde')
# p.abbreviation_definitions    
    #print(para_tagged_tokens)
    # myList = iter( doc.records.serialize())
# for count in range(len(doc.records.serialize())):
#     x =next(myList)
#     print(x)
# t = "names"
# item == None
#grammar = "Addition: {<VBD><VBN><IN><DT><NN><IN><NN><-LRB-><CD><NN>}"
#grammar = "Addition: {<VBD><VBN><IN><DT><NN><IN><NN><-LRB-><CD><NN>}"

#chunk_parser = nltk.RegexpParser(grammar)
# tree = chunk_parser.parse(token_1st_para)
# tree
# tree.draw()
# #para=doc.elements[0]
# #para.tokens
# #doc[0].records.serialize()
# type(doc.records.serialize()[0])
