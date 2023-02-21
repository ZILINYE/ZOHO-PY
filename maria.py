from sqlalchemy import create_engine, false, true
import sys
import pandas as pd

import mysql.connector


class Maria:
    def __init__(self):
        try:
            sqlEngine = create_engine(
                "", pool_recycle=3600
            )
            # Database Connection mysql+pymysql://<Username>:<password>@<Ip Address>/<Databse Name>
            self.mydb = mysql.connector.connect(
                host="192.168.5.238", user="it", password="Acumen321", database="Ace"
            )

        except Exception as e:
            print(e)
            print("error on connecting to mysql")
            sys.exit(1)

        # Get Cursor
        self.mycursor = self.mydb.cursor()
        self.cursor = sqlEngine.connect()

    def GetStudentInfo(self, year, term, campemail):
        sql = "SELECT * FROM Student WHERE CampEmail='%s' LIMIT 1" % campemail
        stu = pd.read_sql(sql, self.cursor)

        if stu.empty:
            return None, None
        else:
            studentId = stu.iloc[0]["ID"]
            sql = (
                "SELECT * FROM Enrollment WHERE StudentID='%s' AND TermYear = '%s' AND Term = '%s'"
                % (studentId, str(year), term)
            )
            pro = pd.read_sql(sql, self.cursor)
            Program = "Unknown"
            if not pro.empty:
                Program = pro.iloc[0]["Program_code"]

            return studentId, Program
