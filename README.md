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
