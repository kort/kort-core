#!/bin/bash
DIR="/docker-entrypoint-initdb.d/update"
DB_NAME="osm_bugs"
DB_OWNER="postgres"

while getopts "ok" arg; do
  case $arg in
    o)
        echo "skip overpass"
        SKIP_OVERPASS="true"
      ;;
    k)
        echo "skip keepright"
        SKIP_KEEPRIGHT="true"
      ;;
  esac
done

if [ -z $DB_NAME ] ; then
    DB_NAME="osm_bugs"
fi

if [ -z $DB_OWNER ] ; then
    DB_OWNER=`whoami`
fi

echo "do update"

####error sources###

###drop all error sources###
#echo "drop all error sources..."
#psql -d $DB_NAME -c "drop schema if exists keepright;"
#psql -d $DB_NAME -c "drop schema if exists osm_errors cascade;"
#psql -d $DB_NAME -c "drop schema if exists all_errors cascade;"

###Update error sources###
echo "update error sources..."


if [[ $SKIP_KEEPRIGHT ]] ; then
    echo "skip keepright update"
else
    ###Keepright reletaded###
    echo "start keepright related update"
    $DIR/../01_setup_keepright_db.sh -d -o $DB_OWNER
    # add geometry to table
    echo "Add geometry column to keepright.errors"
    psql -d $DB_NAME -c "select AddGeometryColumn ('keepright','errors','geom', 4326,'POINT',2);"

    # update table
    echo "Generate geometry objects based on lat/lng values"
    psql -d $DB_NAME -c "update keepright.errors set geom = ST_SetSRID(ST_Point(lon/10000000.0,lat/10000000.0),4326);"
    echo "keepright related update ended"
fi

if [[ $SKIP_OVERPASS ]] ; then
    echo "skip overpass update"
else
    ###osm_errors reletaded###
    echo "start osm_errors related update"
    $DIR/../03_setup_osm_errors_db.sh -d -o $DB_OWNER -n $DB_NAME -s osm_errors
    echo "osm_errors related update ended"
fi

### consolidate error sources and build indexes###
echo "consolidate error sources..."
echo "start consolidation"
$DIR/../04_setup_all_errors_db.sh -d -o $DB_OWNER -n $DB_NAME -s all_errors -c
echo "consolidation ended"

### rebuild kort views and update kort data - errors are possible and tolerated ###
echo "rebuild kort views and update kort data"
$DIR/update_kort_db.sh -o $DB_OWNER -n $DB_NAME -s kort
### reindex database ###
echo "reindex database"
psql -d $DB_NAME -c "REINDEX DATABASE osm_bugs;"




