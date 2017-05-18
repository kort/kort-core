import json
import api.models
import traceback

db_session = api.models.init_db()

def get_achievements(user_id, lang):

    try:
        all_badges = db_session.query(api.models.Badge)
        user_badges = db_session.query(api.models.UserBadge).filter(api.models.UserBadge.user_id == user_id).all()

        user_badges_dict = {b.badge_id: b for b in user_badges}
        badges_achieved = []
        for badge in all_badges:
            badges_achieved.append(badge.dump(lang, badge.id in user_badges_dict, user_badges_dict.get('create_date', '')))

        return badges_achieved

    except Exception as e:
        print(traceback.format_exc())

    print('get achievements for language '+lang)
    with open('data/achievements.json') as json_data:
        d = json.load(json_data)
        return d
    return '{}'