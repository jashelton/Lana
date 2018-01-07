import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from tornado.log import enable_pretty_logging
import logging
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from lana_app import LanaApp

define("debug", default=False, help="run in debug mode", type=bool)
define("env", default="test", help="The environment to use (test, development, staging, production)")
define("port", default="8080", help="The port to listen on")

def main():
  handler = logging.FileHandler('./log/lana.log')
  access_log = logging.getLogger("tornado.access")
  app_log = logging.getLogger("tornado.application")
  gen_log = logging.getLogger("tornado.general")
  enable_pretty_logging()
  access_log.addHandler(handler)
  app_log.addHandler(handler)
  gen_log.addHandler(handler)

  options.parse_command_line()
  app_log.setLevel(logging.DEBUG) if options.debug else app_log.setLevel(logging.INFO)
  gen_log.setLevel(logging.DEBUG) if options.debug else gen_log.setLevel(logging.INFO)
  access_log.setLevel(logging.DEBUG) if options.debug else access_log.setLevel(logging.INFO)
  http_server = tornado.httpserver.HTTPServer(LanaApp(), xheaders=True)
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
  main()