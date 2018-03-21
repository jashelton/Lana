import json
from datetime import datetime
from app.services.base_service import BaseService
from sqlalchemy import select, desc, and_, text, update, func
from app.models.errors import InvalidParametersError, ResourceNotFoundError, HTTPError, \
  UserNotFoundError, UnauthorizedRequest, ArgumentError

class QuestionService(BaseService):
  def __init__(self):
    self._db_session = self.new_session()

  def all(self, user):
    # +----------------------------------------------------------+
    # | id | created_at | question_id | question_type | question |
    # +----------------------------------------------------------+
    # sql = text(' \
    #   select \
    #     P.id, \
    #     P.creator_id, \
    #     U.username as created_by, \
    #     P.created_at, \
    #     Q.id as question_id, \
    #     Q.type as question_type, \
    #     Q.question, \
    #     count(PE.id) as responses, \
    #     (select count(Q1.id) from questions Q1 where Q1.poll_id = P.id) as question_count, \
    #     exists (select 1 from favorites F where F.poll_id = P.id and F.user_id = :user_id ) as favorite \
    #   from polls P \
    #   join questions Q on Q.poll_id = P.id \
    #   join users U on U.id = P.creator_id \
    #   left join poll_events PE on PE.poll_id = P.id and PE.action = "completed" \
    #   where Q.type = "primary" \
    #   group by P.id, P.creator_id, U.username, P.created_at, Q.id, Q.type, Q.question; \
    # ')

    sql = text(' \
      select \
        P.id, \
        P.creator_id, \
        U.username as created_by, \
        P.created_at, \
        Q.id as question_id, \
        Q.type as question_type, \
        Q.question, \
        count(PE.id) as responses, \
        (select count(Q1.id) from questions Q1 where Q1.poll_id = P.id) as question_count, \
        exists (select 1 from favorites F where F.poll_id = P.id and F.user_id = :user_id ) as favorite, \
        (select cast(sum(PR.value) as signed) from poll_ranking PR where P.id = PR.poll_id) as total_rank, \
        (select PR.value from poll_ranking PR where PR.user_id = :user_id and P.id = PR.poll_id) as user_rank \
      from polls P \
      join questions Q on Q.poll_id = P.id \
      join users U on U.id = P.creator_id \
      left join poll_events PE on PE.poll_id = P.id and PE.action = "completed" \
      where Q.type = "primary" \
      group by P.id, P.creator_id, U.username, P.created_at, Q.id, Q.type, Q.question \
      order by total_rank desc; \
    ')

    all_questions = self._db_session.execute(sql, dict(user_id=user)).fetchall()
    return [dict(zip(row.keys(), row)) for row in all_questions]

  def one(self, id, user_id):

    sql_has_taken_poll = text(' \
      select exists( \
	      select * from poll_events \
        where action = "completed" and user_id = :user_id and poll_id = :poll_id) as has_taken_poll; \
    ')

    is_taken = self._db_session.execute(sql_has_taken_poll, dict(user_id=user_id, poll_id=id)).fetchone()
    if is_taken['has_taken_poll']:
      return dict(has_taken=True)

    # +----------------------------------------------------------+
    # | id | created_at | question_id | question_type | question |
    # +----------------------------------------------------------+
    sql_questions = text(' \
      select \
        P.id, \
        P.created_at, \
        Q.id as question_id, \
        Q.type as question_type, \
        Q.question \
      from polls P \
      join questions Q on Q.poll_id = P.id \
      where P.id = :id \
      order by Q.type; \
    ')

    sql_answers = text(' \
      select \
        id, \
        question_id, \
        answer \
      from answers \
      where poll_id = :id \
    ')

    questions = self._db_session.execute(sql_questions, dict(id=id)).fetchall()
    answers = self._db_session.execute(sql_answers, dict(id=id)).fetchall()
    question_dict = [dict(zip(row.keys(), row)) for row in questions]
    answers_dict = [dict(zip(row.keys(), row)) for row in answers]

    poll = dict(
      poll_id=question_dict[0]['id'],
      created_at=question_dict[0]['created_at'],
      questions=[x for x in question_dict],
      # primary_question=next((item for item in question_dict if item['question_type'] == "primary"), None),
      # secondary_questions=[x for x in question_dict if x['question_type'] == "secondary"]
    )

    for q in poll['questions']:
      q['answers'] = [a for a in answers_dict if a['question_id'] == q['question_id']]

    # poll['primary_question']['answers']=[a for a in answers_dict if a['question_id'] == poll['primary_question']['question_id']]

    # for sq in poll['secondary_questions']:
    #   sq['answers'] = [a for a in answers_dict if a['question_id'] == sq['question_id']]

    return dict(poll)
