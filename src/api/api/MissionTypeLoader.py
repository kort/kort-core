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

    def getInputType(self, lang, type_id, input_type_name, re_description, re, lower_bound, upper_bound):
        try:
            locale = I18n.I18n()
            input_type = {
                'constraints': {
                    'description': locale.translate(lang, re_description) or '',
                    're': re or '',
                    'lowerBound': lower_bound or '',
                    'upperBound': upper_bound or ''
                },
                'options': locale.translateList(lang, self.options.get(type_id, [])),
                'values': locale.translateList(lang, self.values.get(type_id, [])),
                'name': locale.translate(lang, input_type_name)
            }
        except Exception as e:
            print(traceback.format_exc())
        return input_type;
