#!/usr/bin/env python
import overpass
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import insert

import models
from models import osm_error
import overpass_queries

def add_errors_from_query(mission_type, results):
    for element in results.get('elements'):
        if element.get('type') == 'node':
            lon = element.get('lon')
            lat = element.get('lat')
        if element.get('type') == 'way' or element.get('type') == 'relation':
            center = element.get('center')
            if center:
                lon = center.get('lon')
                lat = center.get('lat')
            else:
                continue
        geom = 'SRID=4326;POINT(' + str(lon) + ' ' + str(lat) + ')'
        lon *= 10000000
        lat *= 10000000
        osmId = element.get('id')
        stmt = insert(osm_error).values(
            error_type_id=overpass_queries.mission_type_ids.get(mission_type), object_id=osmId,
            object_type=element.get('type'), error_name=mission_type,
            lat=lat, lon=lon, geom=geom, txt1=element.get('tags').get('name')
        )
        stmt = stmt.on_conflict_do_update(
            constraint=UniqueConstraint(osm_error.error_type_id, osm_error.object_type, osm_error.object_id),
            set_=dict(
                error_type_id=overpass_queries.mission_type_ids.get(mission_type), object_id=osmId,
                object_type=element.get('type'), error_name=mission_type,
                lat=lat, lon=lon, geom=geom, txt1=element.get('tags').get('name')
            )
        )

        db_session.execute(stmt)
    db_session.commit()


if __name__ == '__main__':

    db_session = models.init_db()
    api = overpass.API(timeout=600)

    for mission_type, queries in overpass_queries.all_requests.items():
        print('adding errors for type '+mission_type)
        for query in queries:
            print('request overpass with query '+query)
            response = api.Get(query, responseformat="json")
            add_errors_from_query(mission_type, response)







