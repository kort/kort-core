# kort-core [![Build Status](https://travis-ci.org/kort/kort-core.svg?branch=master)](https://travis-ci.org/kort/kort-core)
Kort Native - Kort Backend for kort-native


# Setup

1. edit .env file

2. setup database

```shell
docker-compose build && docker-compose up -d postgres
```

3. run API

```shell
docker-compose build && docker-compose up -d tokeninfo nginx api
```
