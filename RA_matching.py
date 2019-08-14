# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 23:16:36 2019

@author: Abhis
"""

import pandas as pd
import pymysql.cursors

con = con = pymysql.connect(host='profeza1.cmiovtxwqa3q.ap-south-1.rds.amazonaws.com',
                     user='root',            
                     passwd='profeza123',  
                     db='smart_sales_app',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor,
                     autocommit=True)


def batch_index(query,batch_size=100,index=0):
    control = True
    #index = 0
    query1 = query + " LIMIT "+str(batch_size)+" OFFSET "+str(1*index)
    with con:
        print("aggain")
        cur = con.cursor()
        cur.execute(query1)
        rows = cur.fetchall()
        if len(rows)== 0:
            control=False
        index1 = index + batch_size
    return rows, index1, control

#THSEIS MATCHING 
#First, we will get the thesis_id, thesis_keyword from theis_table
#search for each keyword from thesis T1 lets suppose.(T1 --- k1, k2, k3 .....) and then for T2 so on
#case -- if keyword present in keyword_table and then CASES will be
#CASE 1::::  if present,then get the keyword_id from keyword table
        #use that keyword_id to extract all the product that has been mapped to that keyword. (o/p:: k1---p1,p2,p3 or p1)
        #then map those products with the thesis_id and keyword in t_p_m table
#CASE 2:::: if not present, update that keyword against the thesis_id in thesis_unmatched_keyword
        #e.g keyword(text) ----- thesis_id and so for all


#getting thesis in the batch of 100 for processing
tindex = 0
control = True
with con.cursor() as cur:
    while control == True:
        trows, tindex, control = batch_index(query="SELECT research_article_id, research_article_keywords FROM research_article", index = tindex)
        #trows contains 100 thesis_id with thesis_keywords
        thesis_id_keywords={}
        for row in trows:
            thesis_id_keywords[row["research_article_id"]] = row["research_article_keywords"].lower().split() #making list of keyword in thesis_id as key
        for key, value in thesis_id_keywords.items():
            print(key)
            #Checking first if keyword present in keyword table or not
            duplicacy=[]
            for item in value:
                #print(item)
                if not item in duplicacy:
                    duplicacy.append(item)
                    #now get all the products mapped against the keyword if present 
                    dbrows = cur.execute("SELECT keyword_keyword_id, GROUP_CONCAT(product_product_id) AS all_p_ids FROM keyword_product_map WHERE keyword_keyword_id IN (SELECT keyword_id FROM keyword WHERE keyword_name = %s) GROUP BY keyword_keyword_id",(str(item)))
                    if dbrows != 0:
                        product_ids = cur.fetchone()["all_p_ids"].split(',')
                        #CASE 1:::: if present
                        #if product_ids:
                        #now map all products with each thesis_ids in t_p_m table
                        #print('in')
                        for pkey in product_ids:
                            print('a')
                            cur.execute("INSERT INTO product_research_article_map (product_product_id, research_article_research_article_id, keyword) VALUES (%s,%s,%s)",(pkey,key,item,))
                        print('insert in p_ra_m')
                    #CASE 2:::: If not present keyword in keyword table, 
                        #then update that keyword against the thesis_id in thesis_unmatched_keywords
                    else:
                        cur.execute("INSERT INTO research_article_unmatched_keyword (research_article_research_article_keyword, research_article_research_article_id) VALUES (%s,%s)",(item,key))
                        print("insert in research_article_unmatched")                  
            