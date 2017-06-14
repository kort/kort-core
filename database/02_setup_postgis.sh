#!/bin/bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
while getopts ":d:s:t:" opt; do
    case $opt in
        d)
            DB_NAME="$OPTARG"
            ;;
        s)
            SCHEMA_NAME="$OPTARG"
            ;;
        t)  
            TABLE_NAME="$OPTARG"
            ;;
        \?) # fall-through
            ;&
        :)  
            echo "USAGE: `basename $0` [-d <database name>] [-s <schema name>] [-t <table name>]" >&2
            echo "Example: `basename $0` -d osm_bugs -s keepright -t errors" >&2
            exit 1
            ;;
    esac
done

if [ -z $DB_NAME ] ; then
    DB_NAME="osm_bugs"
fi

if [ -z $SCHEMA_NAME ] ; then
    SCHEMA_NAME="keepright"
fi

if [ -z $TABLE_NAME ] ; then
    TABLE_NAME="errors"
fi


# add geometry to table
echo "Add geometry column to $SCHEMA_NAME.$TABLE_NAME"
echo "select AddGeometryColumn ('$SCHEMA_NAME','$TABLE_NAME','geom', 4326,'POINT',2)"
psql -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS postgis;"
psql -d $DB_NAME -c "select AddGeometryColumn ('$SCHEMA_NAME','$TABLE_NAME','geom', 4326,'POINT',2);"

# update table
echo "Generate geometry objects based on lat/lng values"
psql -d $DB_NAME -c "update $SCHEMA_NAME.$TABLE_NAME set geom = ST_SetSRID(ST_Point(lon/10000000.0,lat/10000000.0),4326);"

# create spatial index
#echo "Create spatial index"
#psql -d $DB_NAME -c "create index geom_idx on $SCHEMA_NAME.$TABLE_NAME using gist(geom);"
