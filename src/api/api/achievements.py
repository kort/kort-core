import json
import api.models
import traceback
from sqlalchemy import or_

db_session = api.models.init_db()

def get_achievements(user_id, lang):

    try:
        all_badges = db_session.query(api.models.Badge, api.models.UserBadge)\
            .outerjoin(api.models.UserBadge)\
            .filter(or_(api.models.UserBadge.user_id == user_id, api.models.UserBadge.user_id == None))

        badges_achieved = []
        for badge, user_badge in all_badges:
            achievement_date = None
            achieved = False
            if user_badge:
                achievement_date = user_badge.create_date
                achieved = True
            badges_achieved.append(badge.dump(language=lang, achieved=achieved, achievementDate=achievement_date))

        return badges_achieved

    except Exception as e:
        print(traceback.format_exc())

    print('get achievements for language '+lang)
    with open('data/achievements.json') as json_data:
        d = json.load(json_data)
        return d
    return '{}'