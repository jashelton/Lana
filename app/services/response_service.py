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
    current_poll = response['poll_id']

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

  def create_poll(self, poll):
    author = poll['author']
    questions = poll['questions']

    sql = text(' \
      insert into polls (created_at, creator_id, is_live) values(curdate(), :creator_id, 1) \
    ')
    self._db_session.execute(sql, dict(creator_id=author))
    sql_last_poll_id = text('SELECT LAST_INSERT_ID();')
    last_poll_id = self._db_session.execute(sql_last_poll_id).fetchone()[0]

    sql_create_poll_event = text(' \
      insert into poll_events(poll_id, user_id, action, timestamp) values(:poll_id, :user_id, "created", curdate()) \
    ')

    self._db_session.execute(sql_create_poll_event, dict(poll_id=last_poll_id, user_id=author))

    for index, q in enumerate(questions):
      question_type = 'primary' if index == 0 else 'secondary'
      sql_question = text(' \
        insert into questions(poll_id, type, question) values(:poll_id, :type, :name) \
      ')
      self._db_session.execute(sql_question, dict(poll_id=last_poll_id, type=question_type, name=q['name']))
      sql_last_question_id = text('select last_insert_id();')
      last_question_id = self._db_session.execute(sql_last_question_id).fetchone()[0]
      for a in q['answers']:
        sql_answer = text(' \
          insert into answers(poll_id, question_id, value, answer) values(:poll_id, :question_id, :value, :name) \
        ')
        self._db_session.execute(sql_answer, dict(poll_id=last_poll_id, question_id=last_question_id, value=a['name'], name=a['name']))
    self._db_session.commit()
    return last_poll_id