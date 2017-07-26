import pytest
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from api import models


def test_db():
    db_session = models.init_db()
    assert db_session is not None

