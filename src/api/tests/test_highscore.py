import pytest

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


from api import highscores

def test_highscore():
    scores = highscores.get_highscore('day', 10)
    assert scores is not None

