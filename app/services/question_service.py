import json
from datetime import datetime
from app.services.base_service import BaseService
from sqlalchemy import select, desc, and_, text, update, func
from app.models.errors import InvalidParametersError, ResourceNotFoundError, HTTPError, \
  UserNotFoundError, UnauthorizedRequest, ArgumentError

class QuestionService(BaseService):
  def __init__(self):
    self._db_session = self.new_session()

  def all(self):
    # +----------------------------------------------------------+
    # | id | created_at | question_id | question_type | question |
    # +----------------------------------------------------------+
    sql = text(' \
      select \
        P.id, \
        created_at, \
        Q.id as question_id, \
        Q.type as question_type, \
        Q.question \
      from polls P \
      join questions Q on Q.poll_id = P.id \
      where Q.type = "primary"; \
    ')

    all_questions = self._db_session.execute(sql).fetchall()
    return [dict(zip(row.keys(), row)) for row in all_questions]

  def one(self, id):
    # +----------------------------------------------------------+
    # | id | created_at | question_id | question_type | question |
    # +----------------------------------------------------------+
    sql = text(' \
      select \
        P.id, \
        created_at, \
        Q.id as question_id, \
        Q.type as question_type, \
        Q.question \
      from polls P \
      join questions Q on Q.poll_id = P.id \
      where P.id = :id; \
    ')

    question = self._db_session.execute(sql, dict(id=id))
    question_dict = [dict(zip(row.keys(), row)) for row in question]

    return dict(
      poll_id=question_dict[0]['id'],
      created_at=question_dict[0]['created_at'],
      primary_question=next((item for item in question_dict if item['question_type'] == "primary"), None),
      secondary_questions=[x for x in question_dict if x['question_type'] == "secondary"]
    )
    # return [dict(zip(row.keys(), row)) for row in question]