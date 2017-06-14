FROM mdillon/postgis

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    git \
    libpq-dev \
    make \
    mercurial \
    pkg-config \
    python3.4 \
    python3.4-dev \
    ssh \
    && apt-get autoremove \
    && apt-get clean

# copy helper scripts
COPY keepright/* /docker-entrypoint-initdb.d/keepright/
COPY whitelist_errors.txt /docker-entrypoint-initdb.d/

COPY osm_errors/* /docker-entrypoint-initdb.d/osm_errors/

COPY all_errors/* /docker-entrypoint-initdb.d/all_errors/

COPY kort/* /docker-entrypoint-initdb.d/kort/

COPY update/* /docker-entrypoint-initdb.d/update/

COPY mission_creator/* /docker-entrypoint-initdb.d/mission_creator/

# install python dependencies for mission creator
ADD https://raw.githubusercontent.com/pypa/pip/701a80f451a62aadf4eeb21f371b45424821582b/contrib/get-pip.py /root/get-pip.py
RUN python3.4 /root/get-pip.py
RUN pip3.4 install -r /docker-entrypoint-initdb.d/mission_creator/requirements.txt

### copy and run initialization scripts
COPY 00_init_db.sql /docker-entrypoint-initdb.d/
COPY 02_setup_postgis.sh /docker-entrypoint-initdb.d/
COPY 01_setup_keepright_db.sh /docker-entrypoint-initdb.d/
COPY 03_setup_osm_errors_db.sh /docker-entrypoint-initdb.d/
COPY 04_setup_all_errors_db.sh /docker-entrypoint-initdb.d/
COPY 05_setup_kort_db.sh /docker-entrypoint-initdb.d/

