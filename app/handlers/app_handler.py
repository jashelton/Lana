from app.handlers.base_handler import BaseHandler

class AppHandler(BaseHandler):
  def get(self):
    self.redirect('/login')