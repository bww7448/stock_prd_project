import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook

# dbconfig.py
# class MysqlController:
#     def __init__(self, host, id, pw, db_name):
#         self.conn = pymysql.connect(host=192.168.0.45, user= 12, password='minihs1207', db=db_name,charset='utf8')
#         self.curs = self.conn.cursor()

#     def insert_total(self,total):
#         sql = 'INSERT INTO entire_nodes (count_of_nodes) VALUES (%s)'
#         self.curs.execute(sql,(total,))
#         self.conn.commit()

juso_db = pymysql.connect(
    user='root', 
    passwd='minihs1207', 
    host='lionking.local',
    port=3306, 
    db='tese01', 
    charset='utf8mb4'
)