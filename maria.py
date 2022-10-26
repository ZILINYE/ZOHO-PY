from sqlalchemy import create_engine, false, true
import sys
import pandas as pd

import mysql.connector


class Maria:
    def __init__(self):
        try:
            sqlEngine = create_engine(
                "mysql+pymysql://it:Acumen321@192.168.5.238/Ace", pool_recycle=3600
            )
            self.mydb = mysql.connector.connect(
                host="192.168.5.238", user="it", password="Acumen321", database="Ace"
            )

        except:
            print("error on connecting to mysql")
            sys.exit(1)

        # Get Cursor
        self.mycursor = self.mydb.cursor()
        self.cursor = sqlEngine.connect()
        
    def GetStudentInfo(self,campemail) -> str:
        sql = "SELECT * FROM Student WHERE CampEmail='%s' LIMIT 1" % campemail
        stu = pd.read_sql(sql,self.cursor)

        if stu.empty:
            return None
        else:
            return stu.iloc[0]['ID']