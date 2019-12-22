import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import json
import datetime
from mysqlTool import connectMysql
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


class PaperSearch(tornado.web.RequestHandler):
    def post(self):

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


class PaperSearchSimple(tornado.web.RequestHandler):
    def post(self):
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

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

