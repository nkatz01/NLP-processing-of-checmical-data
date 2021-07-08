# The solution to the problem is based on the following idea:

# Each hyponym of 'Addition' (or synonym of 'adding') found in the document, that may imply adding chemical/s to chemical/s will have on one or both sides.
    #P.S. The phrase 'dissolve in' was assumed to also be a type of 'adding'.
# one or more chemicals listed; in the same way that the + operation has operands on either side or like 'Polish notation' or 'back to front' Polish notation.
# The boundary for an 'addition' (the terminal that stops the parsing of chemicals to be added to a specific 'addition' operation) on either side are either
# the beginning or end of the paragraph, or a new and non-adding 'verb'; indicating that a new and different operation/action is starting/ending.

# The results:
# The results of run on a single paragraph/experimental is a tree with subtrees for each 'addition' operation found within it. 
# The subtrees are labelled, ADDITION2SIDE, ADDITIONRIGHT and ADDTIONLEFT depending on which sides the operands are found, as explained above.
# Each subtree/addition contains its own chemical/s as well as the units (how much of each) for each chemical. 

# What's left out from this solution are the following: 
# The program doesn't cycle through each 'addition' subtree to extract and get all its chemicals. However, the solution to the remainder of the task is trivial due to the realization 
# that although the first ‘addition’ in a paragraph may have only just one operand (e.g. in the case where a chemical is added to a flask) later 'additions', 
# even if they have only one operand, are always described in relation the previous addition/s and therefore can be viewed as an 'addition' 
# consisting (in terms of what chemicals are added) of the chemical/s described with it "as well as" the previous chemical/s described 
# in that paragraph (along with the previous 'addition' operations). In the case of the first 'addition' in a paragraph, having only one operand, it will have to be deemed 
# as part\operand of the second 'addition' (or to previous chemicals that were already mentioned in the paragraph but not with an explicit 'addition' operator - as in experimental 11)
# 
# The above can be achieved by the following:
#     for the first subtree in a paragraph:
#         if the first one:
#             check if it only has 1 operand and if so, deem it as an operand of the second subtree.
#         for all remaining subtrees:
#             unless they are a 2-sided "addition" (which is never the case here) deem them as consisting of their own chemicals together with all the chemicals listed previously (non-recursively).
# 
# Another issue which remains is that due to chemicals' units sometimes appearing before and sometimes after the chemical itself as well as sometimes pertaining to non-chemicals, 
# within subtrees, parsing is still needed in order to make sure that units are properly aligned and are listed together with the chemical they belong to. (This is still not a problem to
# checking if an 'addition' has two or one operand because even if they're not aligned, their label will be just a lone 'UNIT' (or 'CHEM', for chemical/s without units), and we consider an operand (or subtree branch) being a pair
# of chemical/s and 'UNIT' (termed: CH&UNT) or just CHEM (without a unit). 

 





import re
from chemdataextractor import Document
import nltk
import itertools
from chemdataextractor.nlp.pos import ChemCrfPosTagger
from chemdataextractor.nlp.tokenize  import  ChemWordTokenizer
f = open("C:/Users/nuche/Downloads/exercise_experimentals.txt", 'r', encoding="utf-8")

all_sentences_in_para_tagged = []
cwt = ChemWordTokenizer()
cpt = ChemCrfPosTagger()
copied_chem_records = {}
copied_para_tagged_tokens = []
for line in f:
    if line=="\n":
        continue
    content_to_str =line.replace(u"\u2013",u"\u002D")#The first chemical in the first line of experimental 8 has some funny dashes - rather long ones.
    #This loop cleans the chemicals that we can extract from a paragraph with the help of .cems provided by Chemdataextractor
    for chem in Document(content_to_str)[0].cems :
        for part in str(chem).split(' '):#To enable look up later from the token list to the chemical records. Chemdataextractor's chemical records parses
                                         #a chemical better - not based on whitespace, whereas its tagger not so good. However Chemdataextractor also takes the non-chemical words (JJs) in between
            if cpt.tag(cwt.tokenize(part))[0][1]!='JJ':#
                copied_chem_records[part]='CHEM'
    para_tokens = Document(content_to_str)[0].raw_tokens
    #print(copied_chem_records)
    all_sentences_in_para_tagged = []
    copied_para_tagged_tokens = []
    #This loop tags each sentence separately, appending them to obtain the entire paragraph, tagged.
    for sente in para_tokens:
         all_sentences_in_para_tagged.append(cpt.tag(sente))
         para_tagged_tokens= list(itertools.chain(*all_sentences_in_para_tagged))
    needed_tokens = {"VB","VBG","VBN","NN","CHEM","TO","CC","-LRB-","-RRB-","CD",".","NNP","NNPS","NNS","IN","JJ","RB"}
   #Chemdataextractor's tokenizer doesn't mark chemicals as such. Instead, it marks them as 'NN'. This loop does that and by doing a lookup
   #in the set of chemicals previously saved. It also marks additional tokens that may have not been picked up by .cems by assuming that 'of' followed by a noun
   #is also a chemical or some kind of substance that can serve as an operand for 'addition'. 
   #It also flags those tokens whose tags do not appear in needed_tokens for removal, which happens subsequently.
    for tupe in range(len( para_tagged_tokens)):
        if para_tagged_tokens[tupe][0] in copied_chem_records or (para_tagged_tokens[tupe-1][0] == "of" and para_tagged_tokens[tupe][1].startswith("NN")) :
          copied_para_tagged_tokens.append( (para_tagged_tokens[tupe][0],'CHEM'))
          if para_tagged_tokens[tupe-1][0] == "of" and para_tagged_tokens[tupe][1].startswith("NN"):
                copied_chem_records[para_tagged_tokens[tupe][0]]='CHEM'
        elif para_tagged_tokens[tupe][1] not in needed_tokens :
          copied_para_tagged_tokens.append((para_tagged_tokens[tupe][0],'REMO'))
        else :
          copied_para_tagged_tokens.append(para_tagged_tokens[tupe])
    copied_para_tagged_tokens[:] = [tupl for tupl in copied_para_tagged_tokens if tupl[1] !="REMO"]
    #The assumption is that all parenthesis "probably" contains amounts/units but still care has been taken to also include those that are not within parenthesis to account for
    #instances like in experimental 2.
    units_grammer = r"""UNITS: {<-LRB-><CD|IN|JJ|NN|NNS|CHEM>*<-RRB->}
    {<CD><NN>}
    """
    units_parser = nltk.RegexpParser(units_grammer)
    para_units_condesed = units_parser.parse( copied_para_tagged_tokens)

    #This loop seeks to further improve on the poor chemical tagging by .cems and the lack of septicity of the general tagger by assuming that each NN (or sometimes even JJ for some
    #odd reason - like 2-methylbenzaldehyde) preceding a unit that contains either of the following 4 measures are probably chemicals. 
    for subtree in range(len(para_units_condesed)) :
        if type(para_units_condesed[subtree]) == nltk.tree.Tree and  type(para_units_condesed[subtree-1]) !=  nltk.tree.Tree : 
            units_chunk_merged = ' '.join(c[0] for c in para_units_condesed[subtree])
            a = re.compile(r'\bmmol\b', re.IGNORECASE)
            b = re.compile(r'\bmol\b', re.IGNORECASE)
            c = re.compile(r'\bmg\b', re.IGNORECASE)
            d = re.compile(r'\bml\b', re.IGNORECASE)
            if  (( a.search( units_chunk_merged) or b.search( units_chunk_merged) or c.search( units_chunk_merged) or d.search( units_chunk_merged))
             and (  para_units_condesed[subtree-1][1] == "NN" or para_units_condesed[subtree-1][1] == "JJ" )):
                copied_chem_records[para_units_condesed[subtree-1][0]]='CHEM'
  
    copied_para_tagged_tokens = []
    needless_tokens = {"JJ","-LRB-","RB"}#We can now get rid of the few tokens we kept until now for certain clues.
    number_of_additions=0
    #This loop looks for the 'addition' and 'portional' words and tags them as such. It also assumes that 'dissolve in' when relating to two chemicals, or a chemical 
    #and e.g. a flask, is a type of 'addition'.
    #print(copied_chem_records)
    for tupe in range(len(para_units_condesed)):
        if type(para_units_condesed[tupe]) != nltk.tree.Tree :
            if para_units_condesed[tupe][0] in copied_chem_records :
                copied_para_tagged_tokens.append( (para_units_condesed[tupe][0],'CHEM'))
            elif ((para_units_condesed[tupe][0].lower().startswith("add") and not(para_units_condesed[tupe][0].lower().endswith("nal"))) or ('dissolved' in para_units_condesed[tupe][0] and para_units_condesed[tupe+1][1]=='IN' )) :
                copied_para_tagged_tokens.append((para_units_condesed[tupe][0],'ADD'))
                number_of_additions+=1
            elif  ('dropwise' in para_units_condesed[tupe][0]) :
                copied_para_tagged_tokens.append((para_units_condesed[tupe][0],'PORTN'))
            elif para_units_condesed[tupe][1] in needless_tokens :
                continue
            else:
                copied_para_tagged_tokens.append(para_units_condesed[tupe])
        else :
          copied_para_tagged_tokens.append(para_units_condesed[tupe])
    
    
    #The reason this is done is so that the first 'addition' of each paragraph can be checked to see how many subtrees\operands it has 
    #and so decide whether to consider it as part of the second 'addition' in the paragraph, or not. I.e. non-chemicals noun/unit pairs or orphans units are not mistaken as an operand.
    whole_chem_grammer = r"""CH&UNT: {<CHEM>+<UNITS>|<UNITS><IN>?<CHEM>+}
    NN*&UNT: {<NN.*>+<IN>?<UNITS>|<UNITS><IN>?<NN.*>+}"""
    chem_and_unit_parser = nltk.RegexpParser(whole_chem_grammer)
    para_units_condesed = chem_and_unit_parser.parse( copied_para_tagged_tokens)


    #Remove all NN*&UNTs as well as all standalone UNITS (except for those following a NN*&UNT - as they might have fallen out due to incorrect tagging )
    copied_para_tagged_tokens = []
    for subtree in range(len(para_units_condesed)) :
        if type(para_units_condesed[subtree]) == nltk.tree.Tree :
            if (para_units_condesed[subtree].label() == "NN*&UNT" or (para_units_condesed[subtree].label() == "UNITS" and ((type(para_units_condesed[subtree-1]) == nltk.tree.Tree and para_units_condesed[subtree-1].label() != "CH&UNT")
            or type(para_units_condesed[subtree-1]) != nltk.tree.Tree) )):
                continue
            else:
                copied_para_tagged_tokens.append(para_units_condesed[subtree])
        else:
            copied_para_tagged_tokens.append((para_units_condesed[subtree][0],para_units_condesed[subtree][1]))
    
    e = re.compile(r'NN.*')
    final_para_tagged_tokens = []
    #Clearing NN.* and IN tokens.
    for tupe in copied_para_tagged_tokens:
        if type(tupe) != nltk.tree.Tree:
            if not( e.fullmatch(tupe[1]) or tupe[1] == "IN"):
                final_para_tagged_tokens.append(tupe)
        else:
              final_para_tagged_tokens.append(tupe)
    #For safety the '.' was added as a terminal in case the VBN is just adjunct to a NN or JJ of to make a JJ; as for example with 'flame-dried' in experimental 9 or round-bottomed
    #in experimental 4. It also makes sense that an 'addition' would not span over two sentences.
    addition_grammer = """ADDITION2SIDE: {(<CH&UNT|CHEM>+<UNITS>?<CC>?)+<PORTN>?<ADD><PORTN>?(<CH&UNT|CHEM>+<UNITS>?<CC>?)+(^<VB.*|.>)*}
    ADDITIONLEFT: {(<CH&UNT|CHEM>+<UNITS>?<CC>?)+<ADD><PORTN>?(^<VB.*|.>)*}
    ADDITIONRIGHT: {(^<VB.*|.>)*<PORTN>?<ADD>(<CH&UNT|CHEM>+<UNITS>?<CC>?)+}"""
    addition_parser = nltk.RegexpParser(addition_grammer)
    para_additions_chunk = addition_parser.parse(final_para_tagged_tokens)
    para_additions_chunk.draw()
    
    #Test: For each paragraph, checks that number of 'addition' subtrees is equal to number of ADD tags found in the paragraph.
    number_of_add_subtrees=0
    for subtree in para_additions_chunk :
        if type(subtree) == nltk.tree.Tree and  subtree.label().startswith("ADDITION"):
            number_of_add_subtrees+=1
    assert number_of_add_subtrees == number_of_additions    


