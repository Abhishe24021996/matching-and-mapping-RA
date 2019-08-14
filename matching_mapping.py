# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 20:55:10 2019

@author: Abhis
"""


import pandas as pd
import pymysql.cursors
from product_cleaner import product_dict_cleaner
con = con = pymysql.connect(host='profeza1.cmiovtxwqa3q.ap-south-1.rds.amazonaws.com',
                     user='root',            
                     passwd='profeza123',  
                     db='smart_sales_app',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor,
                     autocommit=True)

###################################################################################
#ADD NEW PRODUCT OR PRODUCT INTIALISATION

#step1 - get the product table ----  getting all the products from product table
id_product={}
with con.cursor() as cur:
    cur.execute("Select product_id, product_name from product")
    for row in cur.fetchall():
        id_product[row["product_id"]] = row["product_name"]
        
#cleaning the id_product dictinary for keywords
#eg - product p1 ---- list of k1, k2, k3 or single k1 if one
id_product = product_dict_cleaner(id_product)

#checking keyword present in keyword table or not 
#if present CASE 1 :::: if found, then getting the products mapped to keyword from k_p_m table
#then get all the thesis_id's against all the product found,
#finally append the product p1 with all thesis id found against the previous present product_id's in p_t_m table,  , eg. P1, T1 ,K1
#at last, update the keyword against the product in keyword table.

#CASE 2 :::: if not found, then search the keyword in unmatched_thesis_keyword table.This will also have two cases.
    #case 2.1 :::: if present, getting all the thesis_id's against the keyword from unmatched_thesis_table
            #and then mapped the product with the thesis_id's found
    #case 2.2 :::: if not present, so update the keyword in keyword table
            #update the k_p_m table with this new keyword and product mapping
with con.cursor() as cur:
    for key, value in id_product.items():
        for item in value:
            if item == '':
                continue
            ###obtaining product_id's against the keyword in item
            db_rows = cur.execute("Select keyword_keyword_id, GROUP_CONCAT(product_product_id) as all_p_ids FROM keyword_product_map WHERE keyword_keyword_id IN (SELECT keyword_id FROM keyword WHERE keyword_name = %s) GROUP BY keyword_keyword_id",(str(item)))
            if db_rows != 0:
                product_already_present = cur.fetchall()
                #CASE 1 :::: if products are there           
                #then if contains then getting all thesis_id's against the product or from number of products from p_t_m.
                for row in product_already_present:
                    product_already_ids = row["all_p_ids"].split(',')
                    keyword_already_id = row["keyword_keyword_id"]
                db_rows1 = cur.execute("Select product_product_id, GROUP_CONCAT(thesis_thesis_id) as all_t_ids FROM product_thesis_map WHERE product_product_id IN ("+','.join((str(i) for i in product_already_ids))+") GROUP BY product_product_id")
                if db_rows1 != 0:
                    thesis_present = cur.fetchall()
                    thesis_already_ids=[]
                    
                    for row in thesis_present:
                        thesis_already_ids.append(row["all_t_ids"])
                        #thesis_already_ids_l.extend(row["all_t_ids"].split(','))
                    thesis_already_ids_c = ','.join(thesis_already_ids)
                    thesis_already_ids_l = thesis_already_ids_c.split(',')
                    #updating the p_t_m table with ------ product(key) to all thesis
                    for tkey in thesis_already_ids_l:
                        cur.execute("INSERT INTO product_thesis_map (product_product_id, thesis_thesis_id, keyword) VALUES (%s,%s,%s)",(key,tkey,item))
                    #now also mapping keyword to the product
                    cur.execute("INSERT INTO keyword_product_map (keyword_keyword_id, product_product_id) VALUES (%s,%s)",(keyword_already_id,key))
                else:
                    continue
                
            #CASE 2 :: if keyword is not present in keyword table hence no product id from k_p_m and no thesis_id's from p_t_m
            else:
                #search the keyword in thesis_unmatched_keyword (is thesis present? against the keyword)
                #hence, getting all the thesis_id's against keyword if present
                db_rows2 = cur.execute("SELECT thesis_thesis_keyword, GROUP_CONCAT(thesis_thesis_id) as all_tu_ids FROM thesis_unmatched_keyword WHERE thesis_thesis_keyword = %s GROUP BY thesis_thesis_keyword",(item))
                if db_rows2!=0:
                    keyword_in_t_unmatch = cur.fetchall()
                    #case 2.1 :::: if keyword in unmatched keywords
                    thesis_already_id_l=[]
                    #extarct all thesis_id's in a keyword
                    for row in cur.fetchall():
                        thesis_already_ids_l.extend(row["all_t_ids"].split(','))
                    #mapping product to thesis_id's in p_t_m table
                    for tkey in thesis_already_id_l:
                        cur.execute("INSERT INTO product_thesis_map (product_product_id, thesis_thesis_id, keyword) VALUES (%s,%s,%s)",(key,tkey,item))
                    print('insert in p_t_m')
                    cur.execute("DELETE FROM `thesis_unmatched_keyword` WHERE thesis_thesis_keyword = %s;",(item))
                     #updating the keyword table with new keyword
                    cur.execute("INSERT INTO keyword (keyword_name) VALUES(%s)",(item))
                    cur.execute("SELECT keyword_id FROM keyword WHERE keyword_name = %s LIMIT 1",(item))
                    keyword_id = cur.fetchone()["keyword_id"]
                    #inserting into k_p_m , the keyword to corresponding product
                    cur.execute("INSERT INTO keyword_product_map (keyword_keyword_id, product_product_id) VALUES (%s,%s)",(keyword_id,key))
                    print('insert in k_p_m')
                
                #case 2.2 :::: if keyword is not in unmatched keywords also
                #update keyword in keyword table
                #mapped the keyword(item)_id with the product_id  in k_p_m table
                else:
                    #updating the keyword table with new keyword
                    cur.execute("INSERT INTO keyword (keyword_name) VALUES(%s)",(item))
                    print('insert in keyword_table')
                    #getting the id if new keyword entered in keyword table
                    cur.execute("SELECT keyword_id FROM keyword WHERE keyword_name = %s LIMIT 1",(item))
                    keyword_id = cur.fetchone()["keyword_id"]
                    #inserting into k_p_m , the keyword to corresponding product
                    cur.execute("INSERT INTO keyword_product_map (keyword_keyword_id, product_product_id) VALUES (%s,%s)",(keyword_id,key))
                    print('insert in k_p_m ...............')

                        

    
