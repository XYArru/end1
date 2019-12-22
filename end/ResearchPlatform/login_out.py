import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import json
<<<<<<< HEAD
import datetime
from mysqlTool import connectMysql
=======
from mysqlTool import  connectMysql
>>>>>>> 2d5fc4b10d6fe8cd8a7209b87566e11cf311de9b
from emailConfirm import confirmEmail
from tornado.options import define, options
define("port", default=8445, help="run on the given port", type=int)

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")
    def get_current_password(self):
        return self.get_secure_cookie("password")


class LoginHandler(BaseHandler):
    def post(self):
        'self.set_secure_cookie("user", self.get_argument("username"))'
        jsonbyte = self.request.body
        jsonstr = jsonbyte.decode('utf8')
        jsonobj = json.loads(jsonstr)
        userName = jsonobj.get('username')
        password = jsonobj.get('password')
       # print('二进制json字符串', jsonbyte)

        #print(str(userName))
        sql = "select * from user where user_name ='%s' and user_passwd = '%s'" % (userName, password)
        if conn.resultNum(sql) == 1:
            print(True)
            result = {
                'code': 200
            }
            result_json = json.dumps(result, cls=DateEncoder)
            self.write(result_json)
        else:
            result = {
                'code': 400
            }
            result_json = json.dumps(result, cls=DateEncoder)
            self.write(result_json)


class RegistHandler(BaseHandler):


    def post(self):
        
        jsonbyte = self.request.body
        jsonstr = jsonbyte.decode('utf8')
        jsonobj = json.loads(jsonstr)
        userName = jsonobj.get('username')
        password = jsonobj.get('password')
        email = jsonobj.get('email')
        repassword = jsonobj.get('repassword')
        print('二进制json字符串', jsonbyte)
        if (self.get_argument("logout", None)):
            print("log out")

        sql = "select * from user where user_name ='%s'" % userName
        flag = 0
        if conn.resultNum(sql) != 0:
            print("Exist username")
            flag = 1
        if password != repassword:
            print("Unmatched password")
            flag = 1
        sql = "insert into user(user_id,user_name,user_passwd,user_mailadd) values(3,'%s','%s','%s')" %(userName, password, email)
        confirm = confirmEmail(email, userName)
        if flag == 0:
            conn.resultNum(sql)
            if (self.get_argument("/regist", None)):
                print('none')

            application.add_handlers('.*', [
                (r"/user", HomePageHandler),
            ])
            result = {
                'code':200
            }
            result_json = json.dumps(result, cls=DateEncoder)
            self.write(result_json)
            # application.add_handlers(r'/"%s"'%userName,HomePageHandler);


class HomePageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('homepage.html', user=self.current_user)


class LoginErrorHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('error.html', user=self.current_user)


class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', user=self.current_user)


class LogoutHandler(BaseHandler):
    def post(self):
        if (self.get_argument("logout", None)):
            self.clear_cookie("username")
        self.redirect("/")

class PaperShow(BaseHandler):
    def get(self):
        sql = "select * from paper limit 5"
        resultSet = conn.resultList(sql)
        self.render('showPaper.html', target=resultSet)

class PaperSearch(tornado.web.RequestHandler):
    def post(self):

<<<<<<< HEAD
        jsonbyte = self.request.body
        jsonstr = jsonbyte.decode('utf8')
        jsonobj = json.loads(jsonstr)

        sqlPaperName = " where summary "
        paperNameA = "'%" + jsonobj.get("paperNameA") + "%'"
        paperNameB = "'%" + jsonobj.get("paperNameB") + "%'"
        paperNameLogic = jsonobj.get("paperNameLogic")

        if paperNameLogic == "AND":
            sqlPaperName = sqlPaperName + " like " + paperNameB + " and like " + paperNameA
        elif paperNameLogic == "OR":
            sqlPaperName = sqlPaperName + " like " + paperNameB + " OR  summary like " + paperNameA
        elif paperNameLogic == "NOT":
            sqlPaperName = sqlPaperName + " like " + paperNameB + " not like " + paperNameA
        else:
            print("Error Logic")
            sqlPaperName = ""

        sql = "select * from complete" + sqlPaperName
        print(sql)
        resultSet = conn.resultList(sql)
        sss = []

        for temp in resultSet:
            ss = temp[2].split(';')
            temp = list(temp)
            temp[2] = ss
            sss.append(temp)

        result_json = json.dumps(sss, cls=DateEncoder)

        self.write(result_json)
=======
        sqlPaperName = " where Paper_head "
        paperNameA = "'%" + str(self.get_argument("paperNameA")) + "%'"
        paperNameB = "'%" + str(self.get_argument("paperNameB")) + "%'"
        paperNameLogic = str(self.get_argument("PaperNameLogic"))
        paperTage = str(self.get_argument("paperTag"))

        if paperNameLogic == "and":
            if paperNameA.__len__()==4 :
                if paperNameB.__len__()==4:
                    sqlPaperName = ""
                else:
                    sqlPaperName=sqlPaperName + " like "+paperNameB
            else:
                if paperNameB.__len__()==4:
                    sqlPaperName = sqlPaperName + " like " + paperNameA
                else:
                    sqlPaperName = sqlPaperName + " like " + paperNameA + " and Paper_head like " + paperNameB
        elif paperNameLogic == "or":
            if paperNameA.__len__()==4 :
                if paperNameB.__len__()==4:
                    sqlPaperName = ""
                else:
                    sqlPaperName=sqlPaperName + " like "+paperNameB
            else:
                if paperNameB.__len__()==4:
                    sqlPaperName = sqlPaperName + " like " + paperNameA
                else:
                    sqlPaperName = sqlPaperName + " like " + paperNameA + " or Paper_head like " + paperNameB
        elif paperNameLogic == "not":
            if paperNameA.__len__()==4 :
                if paperNameB.__len__()==4:
                    sqlPaperName = ""
                else:
                    sqlPaperName=sqlPaperName + " not like "+paperNameB
            else:
                if paperNameB.__len__()==4:
                    sqlPaperName = sqlPaperName + " like " + paperNameA
                else:
                    sqlPaperName = sqlPaperName + " like " + paperNameA + " and Paper_head not like " + paperNameB
        else:
            # self.write("Error Logic")
            sqlPaperName = ""

        sqlPaperKeyword = " where Paper_keywd "
        paperKeywordA = "'%" + str(self.get_argument("paperKeywordA")) + "%'"
        paperKeywordB = "'%" + str(self.get_argument("paperKeywordB")) + "%'"
        paperKeywordLogic = str(self.get_argument("PaperKeywordLogic"))
        print("paper-len"+paperKeywordA.__len__().__str__())
        if paperKeywordLogic == "and":
            if paperKeywordA.__len__() == 4:
                if paperKeywordB.__len__() == 4:
                    sqlPaperKeyword = ""
                else:
                    sqlPaperKeyword = sqlPaperKeyword + " like " + paperKeywordB
            else:
                if paperKeywordB.__len__() == 4:
                    sqlPaperKeyword =sqlPaperKeyword + " like " + paperKeywordA
                else:
                    sqlPaperKeyword = sqlPaperKeyword + " like " + paperKeywordA + " and Paper_keywd like " + paperKeywordB
        elif paperKeywordLogic == "or":
            if paperKeywordA.__len__() == 4:
                if paperKeywordB.__len__() == 4:
                    sqlPaperKeyword = ""
                else:
                    sqlPaperKeyword = sqlPaperKeyword + " like " + paperKeywordB
            else:
                if paperKeywordB.__len__() == 4:
                    sqlPaperKeyword = sqlPaperKeyword+ " like " + paperKeywordA
                else:
                    sqlPaperKeyword = sqlPaperKeyword + " like " + paperKeywordA + " or Paper_keywd like " + paperKeywordB
        elif paperKeywordLogic == "not":
            if paperKeywordA.__len__() == 4:
                if paperKeywordB.__len__() == 4:
                    sqlPaperKeyword = ""
                else:
                    sqlPaperKeyword = sqlPaperKeyword + " not like " + paperKeywordB
            else:
                if paperKeywordB.__len__() == 4:
                    sqlPaperKeyword = sqlPaperKeyword + " like " + paperKeywordA
                else:
                    sqlPaperKeyword = sqlPaperKeyword + " like " + paperKeywordA + " and Paper_keywd not like " + paperKeywordB
        else:
            # self.write("Error Logic")
            sqlPaperKeyword = ""

        sqlAuthorName = " where Author "
        authorNameA = "'%" + str(self.get_argument("authorNameA")) + "%'"
        authorNameB = "'%" + str(self.get_argument("authorNameB")) + "%'"
        authorNameLogic = str(self.get_argument("AuthorNameLogic"))
        if authorNameLogic == "and":
            if authorNameA.__len__() == 4:
                if authorNameB.__len__() == 4:
                    sqlAuthorName = ""
                else:
                    sqlAuthorName = sqlAuthorName + " like " + authorNameB
            else:
                if authorNameB.__len__() == 4:
                    sqlAuthorName = sqlAuthorName + " like " + authorNameA
                else:
                    sqlAuthorName = sqlAuthorName + " like " + authorNameA + " and Author like " + authorNameB
        elif authorNameLogic == "or":
            if authorNameA.__len__() == 4:
                if authorNameB.__len__() == 4:
                    sqlAuthorName = ""
                else:
                    sqlAuthorName = sqlAuthorName + " like " + authorNameB
            else:
                if authorNameB.__len__() == 4:
                    sqlAuthorName = sqlAuthorName + " like " + authorNameA
                else:
                    sqlAuthorName = sqlAuthorName + " like " + authorNameA + " or Author like " + authorNameB
        elif authorNameLogic == "not":
            if authorNameA.__len__() == 4:
                if authorNameB.__len__() == 4:
                    sqlAuthorName = ""
                else:
                    sqlAuthorName = sqlAuthorName + " not like " + authorNameB
            else:
                if authorNameB.__len__() == 4:
                    sqlAuthorName = sqlAuthorName + " like " + authorNameA
                else:
                    sqlAuthorName = sqlAuthorName + " like " + authorNameA + " and Author not like " + authorNameB
        else:
            # self.write("Error Logic")
            sqlAuthorName = ""


        if sqlPaperName.__len__()==0:
            if sqlAuthorName.__len__()==0:
                if sqlPaperKeyword.__len__()==0:
                    sql = "select * from paper "
                else:
                    sql = "select * from paper " + sqlPaperKeyword
            else:
                if sqlPaperKeyword.__len__()==0:
                    sql = "select * from paper " + sqlAuthorName
                else:
                    sql = "select * from paper " + sqlAuthorName + " and " + sqlPaperKeyword
        else:
            if sqlAuthorName.__len__()==0:
                if sqlPaperKeyword.__len__()==0:
                    sql = "select * from paper " + sqlPaperName
                else:
                    sql = "select * from paper " + sqlPaperName + " and " + sqlPaperKeyword
            else:
                if sqlPaperKeyword.__len__()==0:
                    sql = "select * from paper " + sqlPaperName + " and " + sqlAuthorName
                else:
                    sql = "select * from paper " + sqlPaperName + " and " + sqlAuthorName + " and " + sqlPaperKeyword

        if paperTage.__len__()!=0:
            if(sql == "select * from paper "):
                sql = sql + " where PaperTag = '%s'" %(paperTage)
            else:
                sql = sql + " and PaperTag = '%s'" %(paperTage)

        print(sql)
        resultSet = conn.resultList(sql)
        for i in range(resultSet.__len__()):
            print(resultSet[i])
            result_json = json.dumps(resultSet[i], ensure_ascii=False)
            self.write(result_json)
        # self.redirect("/")
>>>>>>> 2d5fc4b10d6fe8cd8a7209b87566e11cf311de9b


class PaperSearchSimple(tornado.web.RequestHandler):
    def post(self):
<<<<<<< HEAD
        jsonbyte = self.request.body
        jsonstr = jsonbyte.decode('utf8')
        jsonobj = json.loads(jsonstr)
        keyword = "'%" +jsonobj.get('title') + "%'"
        sql = "select * from complete where title like %s or summary like %s" % (keyword, keyword)
        resultSet = conn.resultList(sql)
        sss = []
        for temp in resultSet:
            ss = temp[2].split(';')
            temp = list(temp)
            temp[2] = ss
            sss.append(temp)

        result_json = json.dumps(sss, cls=DateEncoder)
        self.write(result_json)

class PaperSearchSimple_author(tornado.web.RequestHandler):
    def post(self):
        jsonbyte = self.request.body
        jsonstr = jsonbyte.decode('utf8')
        jsonobj = json.loads(jsonstr)
       # lsword = jsonobj.get('titile')
        keyword = jsonobj.get('title')
        sql = "select * from complete where author like %s " % (keyword)
        resultSet = conn.resultList(sql)

        sss = []
        for temp in resultSet:
            ss = temp[2].split(';')
            temp = list(temp)
            temp[2] = ss
            sss.append(temp)

        result_json = json.dumps(sss, cls=DateEncoder)
        self.write(result_json)

class PaperSearchSimple_keyword(tornado.web.RequestHandler):
    def post(self):
        jsonbyte = self.request.body
        jsonstr = jsonbyte.decode('utf8')
        jsonobj = json.loads(jsonstr)
        keyword = "'%" +jsonobj.get('title') + "%'"
        sql = "select * from complete where keyword like %s " % (keyword)
        resultSet = conn.resultList(sql)
        sss = []
        for temp in resultSet:
            ss = temp[2].split(';')
            temp = list(temp)
            temp[2] = ss
            sss.append(temp)

        result_json = json.dumps(sss, cls=DateEncoder)
        self.write(result_json)

class ReturnLatest50(tornado.web.RequestHandler):
    def get(self):
        sql = "select * from complete order by id desc limit 50"
        resultSet = conn.resultList(sql)
        sss = []
        for temp in resultSet:
            ss = temp[2].split(';')
            temp = list(temp)
            temp[2] = ss
            sss.append(temp)

        result_json = json.dumps(sss, cls=DateEncoder)
        self.write(result_json)

class findme(tornado.web.RequestHandler):
    def post(self):
        jsonbyte = self.request.body
        jsonstr = jsonbyte.decode('utf8')
        jsonobj = json.loads(jsonstr)
       # lsword = jsonobj.get('titile')
        keyword = "'%" +jsonobj.get('author') + "%'"
        sql = "select * from complete where author like %s limit 1" % (keyword)
        resultSet = conn.resultList(sql)
        sss = []
        for temp in resultSet:
            ss = temp[2].split(';')
            temp = list(temp)
            temp[2] = ss
            sss.append(temp)
=======
        keyword = "'%" + str(self.get_argument("keyword")) + "%'"

        sql = "select * from paper where Paper_head like %s or Author like %s or Paper_keywd like %s" %(keyword,keyword,keyword)
        print(conn.resultList(sql))
        resultSet = conn.resultList(sql)
        for i in range(resultSet.__len__()):
            print(resultSet[i])
            result_json = json.dumps(resultSet[i], ensure_ascii=False)
            self.write(result_json)
        # self.redirect("/")
>>>>>>> 2d5fc4b10d6fe8cd8a7209b87566e11cf311de9b

        result_json = json.dumps(sss, cls=DateEncoder)
        self.write(result_json)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings ={
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "login_url": "/login"
    }
    conn=connectMysql()
    conn.createConnection()
    application = tornado.web.Application([
        (r'/', WelcomeHandler),
<<<<<<< HEAD
        (r'/api/regist', RegistHandler),
        (r'/api/login', LoginHandler),
        (r'/api/login/error', LoginErrorHandler),
        (r'/api/logout', LogoutHandler),
        (r'/api/simpleSearch/author', PaperSearchSimple_author),
        (r'/api/simpleSearch/keyword', PaperSearchSimple_keyword),
        (r'/api/simpleSearch/abstract', PaperSearchSimple),
        (r'/api/last6', ReturnLatest50),
        (r'/api/findme', findme),
        (r'/api/search', PaperSearch)], debug=True, **settings)
=======
        (r'/regist',RegistHandler ),
        (r'/login', LoginHandler),
        (r'/login/error',LoginErrorHandler),
        (r'/logout', LogoutHandler),
        (r'/showPaper',PaperShow),
        (r'/simpleSearch', PaperSearchSimple),
        (r'/search', PaperSearch)],debug= True,**settings)
>>>>>>> 2d5fc4b10d6fe8cd8a7209b87566e11cf311de9b

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

