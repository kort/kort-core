bbox = '(47.36347853810964,8.523116111755371,47.383415757118115,8.557062149047852)'
centroid = 'out meta center qt;'

all_requests = {
    'missing_cuisine': ['node["name"~".*"]["amenity"~"restaurant|fast_food"]["cuisine"!~".*"]'+bbox+';',
                        'way["name"~".*"]["amenity"~"restaurant|fast_food"]["cuisine"!~".*"]' + bbox + ';'+centroid],
    'opening_hours': [  'node[~"^(amenity)$"~"(bar|cafe|biergarten|pub|car_rental|car_sharing|car_wash|dentist|dentist|pharmacy|doctors|bank|atm|fuel|ice_cream|restaurant|fast_food|brothel|stripclub|swingerclub|casino|theatre|nightclub|planetarium|gym|post_office|register_office|sauna)"]["opening_hours"!~".*"]'+bbox+';',
                        'node[~"^(tourism)$"~"(aquarium|attraction|information|theme_park|museum|gallery|zoo)"]["opening_hours"!~".*"]'+bbox+';',
                        'node[~"^(shop)$"~".*"]["opening_hours"!~".*"]'+bbox+';',
                        'way[~"^(amenity)$"~"(bar|cafe|biergarten|pub|car_rental|car_sharing|car_wash|dentist|dentist|pharmacy|doctors|bank|atm|fuel|ice_cream|restaurant|fast_food|brothel|stripclub|swingerclub|casino|theatre|nightclub|planetarium|gym|post_office|register_office|sauna)"]["opening_hours"!~".*"]'+bbox+';'+centroid,
                        'way[~"^(tourism)$"~"(aquarium|attraction|information|theme_park|museum|gallery|zoo)"]["opening_hours"!~".*"]'+bbox+';'+centroid,
                        'way[~"^(shop)$"~".*"]["opening_hours"!~".*"]'+bbox+';'+centroid,
                        ],

    'missing_level': ['node["building"~".*"]["building:levels"!~".*"]'+bbox+';',
                       'way["building"~".*"]["building:levels"!~".*"]'+ bbox + ';'+centroid,
                       'relation["building"~".*"]["building:levels"!~".*"]' + bbox + ';' + centroid]
}

mission_type_ids = {
    'missing_cuisine': 1001,
    'opening_hours': 1002,
    'missing_level': 1003,
}