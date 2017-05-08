import json

def get_mission(mission_id):
    return 'the mission'

def get_missions(lat, lon, radius, limit, lang):
    print('get missions for language '+lang)
    with open('data/missions.json') as json_data:
        d = json.load(json_data)
        return d
    return '{}'