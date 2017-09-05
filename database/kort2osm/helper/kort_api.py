import requests
import logging
import models
from models import error_type, kort_errors, Solution, User

log = logging.getLogger(__name__)


class KortApi(object):
    def __init__(self):
        self.db_session = models.init_db()
        pass

    def mark_fix(self, fix_id):
        solution = self.db_session.query(Solution).filter(Solution.complete == True) \
            .filter(Solution.id == fix_id).one_or_none()
        solution.in_osm = True
        self.db_session.commit()

    def read_fix(self):
        """
        Returns an array of dicts containing fixes from kort
        """
        solutions = self.db_session.query(Solution).filter(Solution.complete == True) \
            .filter(Solution.valid == True) \
            .filter(Solution.in_osm == False)

        kort_fixes = []
        for s in solutions:
            error = self.db_session.query(kort_errors).filter(kort_errors.errorId == s.error_id) \
                .filter(kort_errors.osmId == s.osmId).one_or_none()
            osm_type = self.db_session.query(error_type).filter(error_type.type == s.error_type).one_or_none()
            if error and osm_type:
                u = self.db_session.query(User).filter(User.id == s.user_id).one_or_none()
                entry = {
                    'osm_id': s.osmId,
                    'osm_type': error.osmType,
                    'osm_tag': osm_type.osm_tag,
                    'answer': s.solution,
                    'error_type': s.error_type,
                    'username': u.username if u else '',
                    'user_id': s.user_id,
                    'fix_id': s.id,
                    'source': error.source
                }
                kort_fixes.append(entry)
        return kort_fixes


class MarkFixError(Exception):
    pass


class ReadFixError(Exception):
    pass
