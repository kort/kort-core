import pytest

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


from api import achievements

def test_highscore():
    rewards = achievements.get_achievements(-1, 'en')
    assert rewards is not None

