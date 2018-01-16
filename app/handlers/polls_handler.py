from app.handlers.base_handler import BaseHandler
from app.services.poll_service import PollService
# from app.models.errors import HTTPError

class PollsHandler(BaseHandler):
  ITEMS = ('polls')
  def get(self, user=None, **kwargs):
    print(user)
    if user:
      print('--user--')
      print(user)
      # polls/:user
      res = PollService().get_poll_by_user(user)
      response = {'data': res}
      print(response)
      self.finish(response)
    else:
      self.finish({'error': 'blah'})
      # /questions
      # res = QuestionService().all()
      # response = { 'data': res }
      # print(response)
      # self.finish(response)
