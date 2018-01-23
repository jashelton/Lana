import json
from datetime import datetime
from app.services.base_service import BaseService
from sqlalchemy import select, desc, and_, text, update, func
from app.models.auth import Auth
from app.models.errors import InvalidParametersError, ResourceNotFoundError, HTTPError, \
  UserNotFoundError, UnauthorizedRequest, ArgumentError

class ResponseService(BaseService):
  def __init__(self):
    self._db_session = self.new_session()

  def create_response(self, response):

    print('--- response ---')
    print(response)
    current_poll = response['poll_id']
    print(response)

    insert_poll_event = text(' \
      insert into poll_events(poll_id, user_id, action, timestamp) values(:poll_id, :user_id, "completed", curdate()) \
    ')

    insert_response = text(' \
      insert into responses(value, question_id, poll_id, user_id) values(:value, :question_id, :poll_id, :user_id) \
    ')

    self._db_session.execute(insert_poll_event, dict(poll_id=current_poll, user_id=response['username']))
    for key, val in response['form'].items():
      self._db_session.execute(insert_response, dict(value=val, question_id=key, poll_id=current_poll, user_id=response['username']))
    self._db_session.commit()

    return response
