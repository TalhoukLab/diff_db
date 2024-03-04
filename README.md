# diff_db

This repository contains code to enable creation of csvs to view differences between different `sqlite` database. This repository effectively serves as a CDC pipeline for `sqlite` databases.

``` csv
Table Name, Primary Key, Column Name, Old Value, New Value, Type
Users, 78, Name, Null, John, Insert
Users, 78, Name, John, Null, Delete
Users, 78, Name, Jack, John, Update
```
