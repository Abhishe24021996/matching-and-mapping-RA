# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 00:33:48 2019

@author: Abhis
"""

import nltk 

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from string import punctuation
import re
ps = PorterStemmer()
remwords=['','»','’','O.lM','/mg','â€Ÿs','•','/mg-','/ml','-up','\'7gre','\'la.ter','-70°C','¢','F.','T.','','root',':250','°/o','stem','®','™','-1','lmM','i.e','U.K','lOOml','we~e','ng/ml','g/L','.A','P.','/m','Gujarat','Co.','Corp.','E.','St.','Dr.','Ltd.','Inc','U.S.A.','','°C','S.','M.','Prof.','-20°C','C.','U.S.A','·','-3','±','L.','A.','‘','-2','N-','J.','K.','Co.Usa','','~g/ml','O.D','D.','J.l','O.lM','B.']    

def product_dict_cleaner(id_pro_c):
    
    with open('stemmeshfinal.txt','r') as f:
        c = f.readlines()
    contents=[]
    for cont in c:
        contents.append(cont.replace('\n','').lower())       
    stop_words = stopwords.words('english') + list(punctuation) + list(contents)+list(remwords) + ['','C','','’','•','¢','F.','T.','root','stem','®','™','Dancers','elastase','factor','actitvity','death','beta','chicken','receptor','speede','transcription','ligand','lysates','convertase','iqe','custom','kit','total','analysis','lisa','elisa','iqelisa','human','mouse','rat','cell','based','related','assay','array','recombinant','Infusion','Sporulation','B.','Greenland','Centrifuge','Resuspend','custom','kit','total','analysis','lisa','elisa','iqelisa','human','mouse','rat','cell','based','related','assay','array','recombinant','procured','.A','P.','/m','Gujarat','Co.','E.','St.','Dr.','Ltd.','Inc','U.S.A.','','°C','S.','M.','Prof.','-20°C','C.','U.S.A','·','-3','±','L.','A.','‘','-2','N-','J.','K.','Co.Usa','Diagnostics','Sequencing','Sterilized','Signaling','','~g/ml','O.D','D.','J.l','O.lM','Staining','Upstate','B.']
    
    with open('productnamescleaner.txt','r') as fp:
        lines=fp.readlines()
    clean=[]
    for line in lines:
        clean.append(line.replace('\n','').lower())
    clean_n=[]
    for item in clean:
        if not item in clean_n:
            clean_n.append(item)
   
    for key, value in id_pro_c.items():
        words = value.split(' ')
        word = [w for w in words if not w.lower() in clean_n]
        final=[]
        for item in word:
            if '/' in item:
                woli = item.split('/')
                new=[]
                for it in woli:
                    if it.lower() in clean_n:
                        continue
                    else:
                        new.append(it)
                final.append('/'.join(new))
            else:
                final.append(item)
        wojoi = ' '.join(final)
        token = nltk.word_tokenize(wojoi)

        words=[]
        for word in token:
            word=re.sub('^[¢»®™•°/’!"#$%&\€Ÿ\'()*+,-./:;<=>?@[\]^_`{|}~\“\”]+','',word)
            word=re.sub('[¢»®™•°/’!"#$%&\€Ÿ\'()*+,-./:;<=>?@[\]^_`{|}~\“\”]+$','',word)
            word = re.sub('^[0-9]\/','',word)
            if re.search('^[¢»®™•°/’!"#$%&\\'()*+,-./:;<=>?@[\]^_`{|}~\“\”0-9]+$',word): #eliminate allpunctuation if only 
                continue
            elif word == '':
                continue
            elif re.search('m[mlin]{0,3}/[cmlin]+',word):
                continue
            elif re.search('^[μ]',word):
                continue
            elif re.search('[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~][A-Za-z0-9][!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~][A-Za-z0-9][!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]',word): #wliminates like #s#3$ #3#a@
                continue
            elif len(word)<=2:
                continue
            elif (len(word)>45):
                continue
            elif word:
                words.append(word) 
        words1 = [word for word in words if not ps.stem(word.lower()) in stop_words]
        words2 = [ word.lower() for word in words1 if not word in clean_n]
        id_pro_c[key] = words2
    return id_pro_c
    
        
# =============================================================================
#     remwords=['','»','’','O.lM','/mg','â€Ÿs','•','/mg-','/ml','-up','Concentrated','beta','dilution','conjugate','lmmunoresearch','assays','\'7gre','\'la.ter','-70°C','¢','F.','T.','','root',':250','°/o','stem','®','™','-1','lmM','i.e','U.K','electrodes','electrode','digestion','ice-cold','lOOml','we~e','centrifugation','dye','ng/ml','g/L','slants','routinely','w.r.t','stimulation','commercially','promoter','digestion','labeling','amplification','transfection','kindly','freshly','doses','absorbance','freshly','Prof','quantitation','in-house','Dancers','Infusion','Sporulation','B.','Greenland','Centrifuge','Resuspend','.A','P.','/m','Gujarat','Co.','Corp.','E.','St.','Dr.','Ltd.','Inc','U.S.A.','','°C','S.','M.','Prof.','-20°C','C.','U.S.A','·','-3','±','L.','A.','‘','-2','N-','J.','K.','Co.Usa','Diagnostics','Sequencing','Sterilized','Signaling','','~g/ml','O.D','D.','J.l','O.lM','Staining','Upstate','B.']    
#     
#     for key,value in id_pro_c.items():
#         item=id_pro_c[key]
#         words = [ word for word in item if not word in remwords]
#         id_pro_c[key] = words
#     
# =============================================================================
# =============================================================================
#         
#     for key,value in id_pro_c.items():
#         item=id_pro_c[key]
#         words = [ word for word in item if not word in clean_n]
#         id_pro_c[key] = words    
# =============================================================================
    
    
