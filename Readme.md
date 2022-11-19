## CREATE DATABASE

```

create user portal_user with password '4#R1K4by4#Qv';
alter role portal_user set client_encoding to 'utf8';
alter role portal_user set default_transaction_isolation to 'read committed';
alter role portal_user set timezone to 'UTC';
create database portal owner portal_user;
\q
```


## INSTALL PACKAGES

1. create venv or miniconda env
2. install poetry
3. run poetry install

1. [x] [admin@OldoGeNtuDiC](http://168.119.13.25:8777/admin/)