import pytest

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


from api import missions

def test_missions():
    result = missions.get_missions(47.2, 8.2, 5000, 1, 'en', -1)
    assert '' is not None

def test_add_mission_solution():
    solution = {
        'solution': {
            "koins": 0,
            "lang": "en",
            "option": "string",
            "osm_id": 0,
            "solved": True,
            "userId": 0,
            "value": "string"
        }
    }
    missions.put_mission_solution('40', 123, solution)


def test_create_new_achievements():
    missions.create_new_achievements(-1, 'en', '1000')

def test_get_not_achieved_badges_no_of_missions():
    list_of_achievements = [0]
    achievements = missions.get_not_achieved_badges_no_of_missions(list_of_achievements, 1)
    assert len(achievements) is 1
    assert achievements[0].name in 'total_fix_count_1'

def test_get_not_achieved_badges_type_of_mission():
    list_of_achievements = [0]
    achievements = missions.get_not_achieved_badges_type_of_mission(list_of_achievements, 5, 'religion')
    assert len(achievements) is 1
    assert achievements[0].name in 'fix_count_religion_5'

def test_get_not_achieved_badges_highscore():
    list_of_achievements = [0]
    achievements = missions.get_not_achieved_badges_highscore(list_of_achievements, 1)
    assert len(achievements) is 1
    assert achievements[0].name in 'highscore_place_1'

def test_get_osm_geom():
    osm_id = 2810732510
    osm_type = 'node'
    geom = missions.get_osm_geom(osm_type, osm_id)
    assert geom is not None