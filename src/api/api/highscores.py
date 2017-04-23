import json

def get_highscore(type, limit):
    with open('data/highscore_'+type+'.json') as json_data:
        d = json.load(json_data)
        return d
    return '{}'