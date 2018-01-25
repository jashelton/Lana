from app.services.base_service import BaseService
from sqlalchemy import text
# from app.models.errors import InvalidParametersError, ResourceNotFoundError, HTTPError, \
#   UserNotFoundError, UnauthorizedRequest, ArgumentError

class ResultsService(BaseService):
  def __init__(self):
    self._db_session = self.new_session()

  def get_results_by_poll_id(self, poll_id):
    # +-------+
    # | count |
    # +-------+
    sql_response_count = text(' \
      select count(*) as count \
      from poll_events \
      where poll_id = :poll_id and action = "completed"; \
    ')

    # +----------------------+
    # | id | type | question |
    # +----------------------+
    sql_questions = text(' \
      select id, type, question from questions where poll_id = :poll_id; \
    ')

    # +--------------------------------------------+
    # | id | question_id | answer | response_count |
    # +--------------------------------------------+
    sql_answers_responses = text(' \
      select A.id, A.question_id, A.answer, count(R.id) as response_count from answers A \
      left join responses R on R.poll_id = A.poll_id and R.value = A.value \
      where A.poll_id = :poll_id \
      group by A.id, A.answer, A.question_id; \
    ')

    questions = self._db_session.execute(sql_questions, dict(poll_id=poll_id)).fetchall()
    questions_dict = [dict(zip(row.keys(), row)) for row in questions]

    answers_responses = self._db_session.execute(sql_answers_responses, dict(poll_id=poll_id))
    answers_responses_dict = [dict(zip(row.keys(), row)) for row in answers_responses]

    num_responses = self._db_session.execute(sql_response_count, dict(poll_id=poll_id)).fetchone()

    for q in questions_dict:
      q['answers'] = [a for a in answers_responses_dict if a['question_id'] == q['id']]

    
    return dict(responses=num_responses['count'], questions=questions_dict)
