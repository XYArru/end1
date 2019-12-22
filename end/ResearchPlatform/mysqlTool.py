import pymysql


class connectMysql:

    def createConnection(self):
       # conn = pymysql.connect(host='129.211.44.19', port=3306, user='root', password='root', db='project', charset='utf8')
        conn = pymysql.connect(host='129.211.44.19', port=3306, user='root', password='123456', db='project', charset='utf8')
        return conn

    def resultNum(self, sql):
        con = self.createConnection()
        cursor = con.cursor()
        result = cursor.execute(sql)
        con.commit()
        return result

    def resultList(self, sql):
        con = self.createConnection()
        cursor = con.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        con.commit()
        return result
