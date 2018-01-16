import json
from datetime import datetime
from app.services.base_service import BaseService
from sqlalchemy import select, desc, and_, text, update, func
from app.models.errors import InvalidParametersError, ResourceNotFoundError, HTTPError, \
  UserNotFoundError, UnauthorizedRequest, ArgumentError

class PollService(BaseService):
  def __init__(self):
    self._db_session = self.new_session()

  def get_poll_by_user(self, user):
    # +-----------------------------------------------+
    # | poll_id | created_at | question_id | question |
    # +-----------------------------------------------+
    sql_username = text(' \
      select id from users where username = :user; \
    ')

    username = self._db_session.execute(sql_username, dict(user=user)).fetchone()

    sql_polls = text(' \
      select PE.poll_id as poll_id, PE.timestamp as created_at, Q.id as question_id, Q.question, U.username \
      from poll_events PE \
      join questions Q on PE.poll_id = Q.poll_id \
      join users U on U.id = PE.user_id \
      where PE.user_id = :user_id and PE.action = "created" and Q.type = "primary"; \
    ')

    polls = self._db_session.execute(sql_polls, dict(user_id=username['id'])).fetchall()
    return [dict(zip(row.keys(), row)) for row in polls]
