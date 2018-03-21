from app.handlers.auth_handler import AuthHandler
from app.handlers.question_handler import QuestionHandler
from app.handlers.polls_handler import PollsHandler
from app.handlers.response_handler import ResponseHandler
from app.handlers.results_handler import ResultsHandler
from app.handlers.favorites_handler import FavoritesHandler
from app.handlers.bookmark_handler import BookmarkHandler
from app.handlers.comments_handler import CommentsHandler
from app.handlers.ranking_handler import RankingHandler
from app.handlers.follows_handler import FollowsHandler
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
      r"/polls/(?P<user>\w+)/(?P<current_user>\d+)",),

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

    CommentsHandler: (
      r"/(?P<item>{})".format('|'.join(CommentsHandler.ITEMS)),
      r"/(?P<item>{})/(?P<the_id>\d+)".format('|'.join(CommentsHandler.ITEMS)),),

    RankingHandler: (
      r"/ranking/(?P<the_id>\w+)/(?P<item>{})".format('|'.join(RankingHandler.ITEMS)),),

    FollowsHandler: (
      r"/follows/(?P<user_id>\d+)",),

    AppHandler: (
      r"/",)
}