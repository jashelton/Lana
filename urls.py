from app.handlers.auth_handler import AuthHandler
from app.handlers.question_handler import QuestionHandler
from app.handlers.polls_handler import PollsHandler
from app.handlers.app_handler import AppHandler

URL_HANDLERS = {
    AuthHandler: (
      r"/(?P<item>{})".format(
        '|'.join(AuthHandler.ITEMS)),
      r"/(?P<item>{})/(?P<token>\d+)"),

    QuestionHandler: (
      r"/questions",
      r"/questions/(?P<the_id>\d+)",
      r"/questions/(?P<the_id>\d+)/(?P<item>{})".format(
        '|'.join(QuestionHandler.ITEMS))),

    PollsHandler: (
      r"/polls",
      r"/polls/(?P<user>\w+)",
      r"/polls/(?P<user>\w+)/(?P<item>{})".format(
        '|'.join(QuestionHandler.ITEMS))),

    AppHandler: (
      r"/",)
}