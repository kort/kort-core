# kort-core [![Build Status](https://travis-ci.org/kort/kort-core.svg?branch=master)](https://travis-ci.org/kort/kort-core)
Kort Native - Kort Backend for kort-native

# Mission Types

| Mission Description               | Source    | OSM Tag         |
|-----------------------------------|-----------|-----------------|
| Motorway without reference        | Keepright | ref             |
| Object without a name             | Keepright | name            |
| Missing speed limit               | Keepright | maxspeed        |
| Type of track unknown             | Keepright | tracktype       |
| Place of worship without religion | Keepright | religion        |
| Language of the name unknown      | Keepright | name:XX         |
| Street without a name             | Keepright | name            |
| Restaurant without a cuisine      | Overpass  | cuisine         |
| Place without opening hours       | Overpass  | opening_hours   |
| Missing Levels                    | Overpass  | building:levels |

# Setup

1. edit .env file

2. setup database

```shell
docker-compose build && docker-compose up -d postgres
```

3. run API

```shell
docker-compose build && docker-compose up -d tokeninfo api nginx
```

update
```shell
 docker exec -d kortcore_postgres_1 su -c "docker-entrypoint-initdb.d/update/update_db.sh -k" -s /bin/sh postgres
 # -k skip keepright update
 # -o skip overpass update
 # or via cron
 docker exec -d kortcore_postgres_1 cron
 #log file for overpass update
 docker exec kortcore_postgres_1 su -c "tail -f docker-entrypoint-initdb.d/mission_creator/overpass.log" -s /bin/sh postgres
```

# Adding New Missions

* Add a new entry to the table `kort.error_type` with a new `error\_type\_id` (kort_data.sql).
* If additional achievement badges should be available, create the appropriate entries in this file as well.
* Create an appropriate QL Overpass query. Add also the `error_type_id` chosen in the step before (overpass_queries.py)
* In the next import run these new missions should be added to the database and available to the client
* Do not forget to add the appropriate language translations to the localization files
