import pandas as pd
import pymysql.cursors

con = con = pymysql.connect(host='profeza1.cmiovtxwqa3q.ap-south-1.rds.amazonaws.com',
                     user='root',            
                     passwd='profeza123',  
                     db='smart_sales_app',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor,
                     autocommit=True)


###updating prct brnd and category inn p_t_m table
pro_brand={}
pro_category={}

with con.cursor() as cur:
    cur.execute("select product_id, brand_brand_id, category_category_id from product where product_id IN (Select distinct product_product_id from product_thesis_map);")
    for row in cur.fetchall():
        pro_brand[row['product_id']] = row['brand_brand_id']
        pro_category[row['product_id']] = row['category_category_id']
        

#####updating product_thesis_map table

#UPDATE `smart_sales_app`.`product_has_thesis` SET `product_brand_brand_id` = %s, `product_category_category_id` = %s WHERE product_product_id=%s;        

with con.cursor() as cur:
    for key, value in pro_brand.items():
        cur.execute("UPDATE `smart_sales_app`.`product_thesis_map` SET `product_brand_brand_id` = %s, `product_category_category_id` = %s WHERE product_product_id=%s;",(value,pro_category[key],key))
        print('pass')
        #con.commit()
        
############same for thesis_lab_lab_id, institute_isntitue_id
        

th_lab={}
th_inst={}

with con.cursor() as cur:
    cur.execute("select thesis_id, lab_lab_id, lab_institute_institute_id from thesis where thesis_id IN (Select distinct thesis_thesis_id from product_thesis_map);")
    for row in cur.fetchall():
        th_lab[row['thesis_id']] = row['lab_lab_id']
        th_inst[row['thesis_id']] = row['lab_institute_institute_id']
        

#####updating product_thesis_map table

#UPDATE `smart_sales_app`.`product_has_thesis` SET `product_brand_brand_id` = %s, `product_category_category_id` = %s WHERE product_product_id=%s;        

with con.cursor() as cur:
    for key, value in th_lab.items():
        cur.execute("UPDATE `smart_sales_app`.`product_thesis_map` SET `thesis_lab_lab_id` = %s, `thesis_lab_institute_institute_id` = %s WHERE thesis_thesis_id=%s;",(value,th_inst[key],key))
        print('pass')
        