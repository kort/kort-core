import api.models

from src.api.i18n import I18n
import traceback

class MissionTypeLoader:

    options = {}
    values = {}

    class __MissionTypeLoader:
        def __init__(self):
            print('create')
            db_session = api.models.init_db()
            q = db_session.query(api.models.Answer).order_by(api.models.Answer.sorting)
            for p in q:
                MissionTypeLoader.options[p.type] = []
                MissionTypeLoader.values[p.type] = []
            for row in q:
                MissionTypeLoader.options[row.type].append(row.title)
                MissionTypeLoader.values[row.type].append(row.value)

        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not MissionTypeLoader.instance:
            MissionTypeLoader.instance = MissionTypeLoader.__MissionTypeLoader()
    def __getattr__(self, name):
        return getattr(self.instance, name)



    constraints = {

        'motorway_ref':
            {
                'description': '',
                're': '',
                'lowerBound': '',
                'upperBound': ''
            },
        'poi_name':
            {
                'description': '',
                're': '',
                'lowerBound': '',
                'upperBound': ''
            }
    }


    image = {
        'way_wo_tags':     'mission_road',
        'motorway_ref':     'mission_road',
        'religion':    'mission_religion',
        'poi_name':    'mission_poi',
        'missing_maxspeed':    'mission_speed',
        'language_unknown':    'mission_language',
        'missing_track_type':    'mission_road',
        'missing_cuisine':   'mission_cuisine',
        'religion2':   'mission_floors',
        'religion3':   'mission_opening_hours'
    }




    def getInputType(self, lang, type_id,  name):
        try:
            locale = I18n.I18n()
            inputType = {
                'constraints': self.constraints.get(type_id, None),
                'options': locale.translateList(lang, self.options.get(type_id, [])),
                'values': locale.translateList(lang, self.values.get(type_id, [])),
                'name': locale.translate(lang, name)
            }
        except Exception as e:
            print(traceback.format_exc())
        return inputType;

    def getImage(self, type_id):
        return self.image.get(type_id, '')