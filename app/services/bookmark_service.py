import json
from datetime import datetime
from app.services.base_service import BaseService
from sqlalchemy import select, desc, and_, text, update, func
from app.models.errors import InvalidParametersError, ResourceNotFoundError, HTTPError, \
  UserNotFoundError, UnauthorizedRequest, ArgumentError

class BookmarkService(BaseService):
  def __init__(self):
    self._db_session = self.new_session()

  def bookmarks(self, user):
    sql_polls_list = text(' \
      select poll_id from favorites where user_id = :user_id \
    ')

    response_sql_polls = self._db_session.execute(sql_polls_list, dict(user_id=user))
    polls = [ p.poll_id for p in response_sql_polls ]

    sql_polls = text(' \
      select * from questions where poll_id in :polls_list and type="primary"; \
    ')

    response_sql_polls = self._db_session.execute(sql_polls, dict(polls_list=polls)).fetchall()
    return [dict(zip(row.keys(), row)) for row in response_sql_polls]
