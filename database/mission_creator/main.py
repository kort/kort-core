#!/usr/bin/env python
import os

import overpass
import time

from overpass import MultipleRequestsError
from overpass import ServerLoadError
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import insert

import models
from models import osm_error
import overpass_queries

def add_errors_from_query(mission_type, elements):
    for element in elements:
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


def retrieve_data_with_bbox(current_bbox):
    print('current bbox: ', current_bbox)
    for mission_type, queries in overpass_queries.all_requests.items():
        print('adding errors for type '+mission_type)
        for query in queries:
            no_of_tries = 3
            for i in range(no_of_tries):
                try:
                    print('request overpass with query ' + query + ' and bbox ' + current_bbox)
                    response = api.Get(query.replace('bbox', current_bbox), responseformat="json")
                    elements = response.get('elements')
                    print('adding errors to database, no of elements:', len(elements))
                    add_errors_from_query(mission_type, elements)
                    # sometimes a MultipleRequestsError (429) happens when too many queries are being sent
                    if len(elements) > 0:
                        time.sleep(1)
                except MultipleRequestsError as e:
                    if i < no_of_tries - 1:
                        print('MultipleRequestsError no.'+i+' -> sleep for'+str(10+10*i)+' seconds')
                        time.sleep(10+10*i)
                        continue
                except ServerLoadError as e:
                    if i < no_of_tries - 1:
                        print('ServerLoadError no.'+i+' -> sleep for 10 minutes')
                        time.sleep(600)
                        continue
                    else:
                        raise
                except TimeoutError as e:
                    if i < no_of_tries - 1:
                        print('TimeoutError no.'+i+' -> sleep for 10 minutes')
                        time.sleep(600)
                        continue
                break

if __name__ == '__main__':

    db_session = models.init_db()
    api = overpass.API(timeout=6000)

    bbox = (47.3, 8.5, 47.4, 8.6)
    if os.getenv('BBOX_OVERPASS'):
        bbox = tuple(map(float, os.getenv('BBOX_OVERPASS').split(',')))

    increment_lat = 0.1
    increment_lon = 0.1

    lat = bbox[0]
    lon = bbox[1]
    no_of_bboxes = round((bbox[3] - bbox[1])/increment_lon)*round((bbox[2] - bbox[0])/increment_lat)
    if no_of_bboxes != 0:
        progressChange = 1.0 / no_of_bboxes
    else:
        progressChange = 1.0
    progress = 0.0
    print('no of bboxes: ', no_of_bboxes)
    for x in range(0, round((bbox[3] - bbox[1])/increment_lon)):
        lon = bbox[1] + x * increment_lon
        for y in range(0, round((bbox[2] - bbox[0])/increment_lat)):
            lat = bbox[0] + y * increment_lat
            current_bbox = '(' + str(lat) + ',' + str(lon) + ',' + str(lat + increment_lat) + ',' + str(
                lon + increment_lon) + ')'
            retrieve_data_with_bbox(current_bbox)
            progress += progressChange
            print('progress: ', round(progress*100, 2), '%')











