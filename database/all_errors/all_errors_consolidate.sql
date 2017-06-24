INSERT INTO all_errors.errors (source,error_id,schema,error_type_id,osm_id,osm_type,description,latitude,longitude,geom,txt1,txt2,txt3,txt4,txt5)
SELECT DISTINCT 'keepright' AS source, error_id, schema, error_type_id,object_id AS osm_id, object_type AS osm_type, msgid AS description, lat AS latitude, lon AS longitude, geom, txt1, txt2, txt3, txt4, txt5
FROM keepright.errors o1
WHERE ((state = ANY (ARRAY['new'::keepright.state, 'reopened'::keepright.state])) AND (object_id <> ALL (ARRAY[(1611867263)::bigint, (1723313154)::bigint, (111841602)::bigint]))) AND NOT EXISTS (SELECT 1 FROM all_errors.errors e WHERE e.schema=o1.schema AND e.error_id=o1.error_id AND e.osm_id=o1.object_id)
UNION ALL
SELECT 'osm_errors' AS source, error_id, schema, error_type_id,object_id AS osm_id, object_type AS osm_type, msgid AS description, lat AS latitude, lon AS longitude, geom, txt1, txt2, txt3, txt4, txt5
FROM osm_errors.errors o2 WHERE NOT EXISTS (SELECT 1 FROM all_errors.errors e WHERE e.schema=o2.schema AND e.osm_id=o2.object_id);