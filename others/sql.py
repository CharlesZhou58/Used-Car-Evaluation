# coding=utf-8
# some script for preprocessing data, especially organize car model
import pymysql
import csv
import re

# read csv to list
with open('/Users/xianzheng/Downloads/P2/data/Result_model_count.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

# connect to DB
db = pymysql.connect(
    host='localhost',
    user='root',
    passwd='passpasspass',
    db='p2',
    port=3306,
)
cursor = db.cursor()

# do some query here, like pattern match, and update
for i in range(len(data)):
    #matchObj = re.search(" truck",data[i][0])
    if True:
        sql = ''
        #temp = data[i][0]
        #result = re.sub(" truck", "", temp)
        try:
            sql = "UPDATE vehicles SET model = '%s' WHERE manufacturer = 'ford' AND model = '%s'" % ("f-250 super duty", data[i][0])
            #sql = "delete from vehicles where manufacturer = 'chevrolet' and model = '%s'" % data[i][0]
            print(sql)
            cursor.execute(sql)
            db.commit()
        except:
            print('SQL Error on:' + sql)

db.close()

