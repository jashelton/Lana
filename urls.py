from app.handlers.auth_handler import AuthHandler
from app.handlers.question_handler import QuestionHandler
from app.handlers.polls_handler import PollsHandler
from app.handlers.response_handler import ResponseHandler
from app.handlers.results_handler import ResultsHandler
from app.handlers.favorites_handler import FavoritesHandler
from app.handlers.bookmark_handler import BookmarkHandler
from app.handlers.app_handler import AppHandler

URL_HANDLERS = {
    AuthHandler: (
      r"/(?P<item>{})".format(
        '|'.join(AuthHandler.ITEMS)),
      r"/(?P<item>{})/(?P<token>\d+)"),

    QuestionHandler: (
      r"/questions",
      r"/questions/(?P<the_id>\d+)",),

    PollsHandler: (
      r"/polls",
      r"/polls/(?P<user>\w+)",),

    ResponseHandler: (
      r"/(?P<item>{})".format(
        '|'.join(ResponseHandler.ITEMS)),
    ),

    ResultsHandler: (
      r"/results/(?P<the_id>\d+)",
      r"/test"),

    FavoritesHandler: ( # This could/should be merged into BookmarkHandler
      r"/favorites",),

    BookmarkHandler: (
      r"/bookmarks/(?P<user_id>\d+)",),

    AppHandler: (
      r"/",)
}