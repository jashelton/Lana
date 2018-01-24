from app.services.base_service import BaseService
from sqlalchemy import text
# from app.models.errors import InvalidParametersError, ResourceNotFoundError, HTTPError, \
#   UserNotFoundError, UnauthorizedRequest, ArgumentError

class ResultsService(BaseService):
  def __init__(self):
    self._db_session = self.new_session()

  def get_results_by_poll_id(self, poll_id):
    sql_response_count = text(' \
      select count(*) as count \
      from poll_events \
      where poll_id = :poll_id and action = "completed"; \
    ')

    num_responses = self._db_session.execute(sql_response_count, dict(poll_id=poll_id)).fetchone()
    print(num_responses)
    return dict(responses=num_responses['count'])

    # What I want to return
    # results: {
    #   responses: number,
    #   questions: [{
    #     id: number,
    #     question: string,
    #     response_count: number,
    #     type?: 'primary' | 'secondary'
    #   }
    #   ...
    #   ]
    # }