FROM mdillon/postgis

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

COPY 00_init_db.sql /docker-entrypoint-initdb.d/
COPY 02_setup_postgis.sh /docker-entrypoint-initdb.d/

# Keepright init
COPY keepright/* /docker-entrypoint-initdb.d/keepright/
COPY whitelist_errors.txt /docker-entrypoint-initdb.d/
COPY 01_setup_keepright_db.sh /docker-entrypoint-initdb.d/

# Setup OSM errors
COPY osm_errors/* /docker-entrypoint-initdb.d/osm_errors/
COPY 03_setup_osm_errors_db.sh /docker-entrypoint-initdb.d/

# Setup all errors
COPY all_errors/* /docker-entrypoint-initdb.d/all_errors/
COPY 04_setup_all_errors_db.sh /docker-entrypoint-initdb.d/

# Kort init
COPY kort/* /docker-entrypoint-initdb.d/kort/
COPY 05_setup_kort_db.sh /docker-entrypoint-initdb.d/

# put update scripts
COPY update/* /docker-entrypoint-initdb.d/update/