import json

def get_achievements():
    with open('data/achievements.json') as json_data:
        d = json.load(json_data)
        return d
    return '{}'