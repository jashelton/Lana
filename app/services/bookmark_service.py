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

    # sql_polls = text(' \
    #   select * from questions where poll_id in :polls_list and type="primary"; \
    # ')

    sql_polls = text(' \
      select \
        Q.id, \
        Q.poll_id, \
        Q.question, \
        P.created_at, \
          U.username, \
          count(R.id) as response_count, \
          (select count(Q1.id) from questions Q1 where Q1.poll_id = P.id) as question_count \
      from questions Q \
      join polls P on P.id = Q.poll_id \
      join users U on U.id = P.creator_id \
      left join responses R on R.poll_id = P.id and R.question_id = Q.id \
      where Q.poll_id in :polls_list and type="primary" \
      group by Q.id, Q.poll_id, Q.question, P.created_at, U.username; \
    ')

    response_sql_polls = self._db_session.execute(sql_polls, dict(polls_list=polls)).fetchall()
    return [dict(zip(row.keys(), row)) for row in response_sql_polls]
