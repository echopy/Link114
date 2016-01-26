# coding: utf-8
import tornado.ioloop
import tornado.web
import tornado.gen
from QueryAPI import API
import tornado.options
import os
import tornado.httpclient
from tornado.concurrent import run_on_executor
# 这个并发库在python3自带在python2需要安装sudo pip install futures
from concurrent.futures import ThreadPoolExecutor


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        domain = self.get_argument('domain')
        domain = domain.replace('\r\n', '\n')
        domain = domain.replace(' ', '\n')
        domain = domain.split('\n')
        self.render('query.htm', domain=domain)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class QueryHandler(tornado.web.RequestHandler):
    # 使用多少线程
    executor = ThreadPoolExecutor(10)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        url = self.get_argument('url')
        res = yield self.query(url)
        self.write(res)
        self.finish()

    @run_on_executor
    def query(self, url):
        return API(url).run()


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/index/", IndexHandler),
    (r"/query", QueryHandler),
],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
