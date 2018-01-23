from app.handlers.base_handler import BaseHandler
from app.services.poll_service import PollService
# from app.models.errors import HTTPError

class PollsHandler(BaseHandler):
  ITEMS = ('polls')
  def get(self, item=None, user=None, **kwargs):
    if user:
      # polls/:user
      res = PollService().get_poll_by_user(user)
      response = {'data': res}
      self.finish(response)
    else:
      self.finish({'error': 'blah'})
      # /questions
      # res = QuestionService().all()
      # response = { 'data': res }
      # print(response)
      # self.finish(response)

  def post(self, data=None, **kwargs):
    if data:
      print(data)