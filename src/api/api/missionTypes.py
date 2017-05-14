class MissionTypes:

    # constraints = {
    #
    #     90:
    #         {
    #             'description': '',
    #             're': '',
    #             'lowerBound': '',
    #             'upperBound': ''
    #         },
    #     110:
    #         {
    #             'description': '',
    #             're': '',
    #             'lowerBound': '',
    #             'upperBound': ''
    #         }
    # }
    #
    # name = {
    #     71: 'text',
    #     90: 'text',
    #     100: 'select',
    #     110: 'text',
    #     300: 'number',
    #     360: 'select',
    #     390: 'select',
    #     1001: 'select',
    #     1002: 'number',
    #     1003: ''
    # }
    #
    # options = {
    #     100:
    #         [
    #             'Hindu',
    #             'Christian',
    #             'Spaghetti Monster'
    #         ],
    #     110:
    #     [
    #         'some option'
    #     ],
    #     360:
    #         [
    #             'English',
    #             'German',
    #             'Italian'
    #         ],
    #     390:
    #         [
    #             'Solid',
    #             'Mostly solid',
    #             'Even mixture of hard and soft materials',
    #             'Mostly soft',
    #             'Soft'
    #         ],
    #     1001:
    #         [
    #             'Italian',
    #             'Chinese',
    #             'Regional'
    #         ]
    # }
    #
    # values = {
    #
    # }
    #
    # question = {
    #     71: 'Is this the correct reference of this motorway?',
    #     90: 'Motorway without reference',
    #     100: 'Is this place of worship of this religion?',
    #     110: 'What is this place called?',
    #     300: 'What is the speed limit of this road?',
    #     360: 'Language of the name unknown',
    #     390: 'This track doesn\'t have a tracktype',
    #     1001: 'mission_cuisine',
    #     1002: 'mission_floors',
    #     1003: 'mission_opening_hours'
    # }
    #
    # image = {
    #     71:     'mission_road',
    #     90:     'mission_road',
    #     100:    'mission_religion',
    #     110:    'mission_poi',
    #     300:    'mission_speed',
    #     360:    'mission_language',
    #     390:    'mission_road',
    #     1001:   'mission_cuisine',
    #     1002:   'mission_floors',
    #     1003:   'mission_opening_hours'
    # }
    #
    # type = {
    #     71:     'mission_road',
    #     90:     'mission_road',
    #     100:    'mission_religion',
    #     110:    'mission_poi',
    #     300:    'mission_speed',
    #     360:    'mission_language',
    #     390:    'mission_road',
    #     1001:   'mission_cuisine',
    #     1002:   'mission_floors',
    #     1003:   'mission_opening_hours'
    # }
    #
    # title = {
    #     71: 'Missing Road Name',
    #     90: 'Missing Road',
    #     100: 'Missing Religion',
    #     110: 'Object without a name',
    #     300: 'Missing Speed Limit',
    #     360: 'Missing Language',
    #     390: 'Missing Tracktype',
    #     1001: 'mission_cuisine',
    #     1002: 'mission_floors',
    #     1003: 'mission_opening_hours'
    # }

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

    name = {
        'way_wo_tags': 'text',
        'motorway_ref': 'text',
        'religion': 'select',
        'poi_name': 'text',
        'missing_maxspeed': 'number',
        'language_unknown': 'select',
        'missing_track_type': 'select',
        'missing_cuisine': 'select',
        'religion2': 'number',
        'religion3': ''
    }

    options = {
        'religion':
            [
                'Hindu',
                'Christian',
                'Spaghetti Monster'
            ],
        'poi_name':
        [
            'some option'
        ],
        'language_unknown':
            [
                'English',
                'German',
                'Italian'
            ],
        'missing_track_type':
            [
                'Solid',
                'Mostly solid',
                'Even mixture of hard and soft materials',
                'Mostly soft',
                'Soft'
            ],
        'missing_cuisine':
            [
                'Italian',
                'Chinese',
                'Regional'
            ]
    }

    values = {

    }

    question = {
        'way_wo_tags': 'Is this the correct reference of this motorway?',
        'motorway_ref': 'Motorway without reference',
        'religion': 'Is this place of worship of this religion?',
        'poi_name': 'What is this place called?',
        'missing_maxspeed': 'What is the speed limit of this road?',
        'language_unknown': 'Language of the name unknown',
        'missing_track_type': 'This track doesn\'t have a tracktype',
        'missing_cuisine': 'mission_cuisine',
        'religion2': 'mission_floors',
        'religion3': 'mission_opening_hours'
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

    type = {
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

    title = {
        'way_wo_tags': 'Missing Road Name',
        'motorway_ref': 'Missing Road',
        'religion': 'Missing Religion',
        'poi_name': 'Object without a name',
        'missing_maxspeed': 'Missing Speed Limit',
        'language_unknown': 'Missing Language',
        'missing_track_type': 'Missing Tracktype',
        'missing_cuisine': 'mission_cuisine',
        'religion2': 'mission_floors',
        'religion3': 'mission_opening_hours'
    }


    def getInputType(self, type_id):
        inputType = {
            'constraints': self.constraints.get(type_id, None),
            'options': self.options.get(type_id, []),
            'values': self.values.get(type_id, []),
            'name': self.name.get(type_id, None)
        }
        return inputType;

    def getQuestion(self, type_id):
        return self.question.get(type_id, '')

    def getImage(self, type_id):
        return self.image.get(type_id, '')

    def getType(self, type_id):
        return self.type.get(type_id, '')

    def getTitle(self, type_id):
        return self.title.get(type_id, '')
