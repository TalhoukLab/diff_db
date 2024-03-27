# diff_db

This repository contains code to enable creation of csvs to view differences between different `sqlite` database. This repository effectively serves as a CDC pipeline for `sqlite` databases.

``` csv
Table Name, Primary Key, Value, Column Name, Old Value, New Value, Type
Users, ID, 78, Name, Null, John, Insert
Users, ID, 78, Age, Null, 25, Insert
Users, ID, 78, Name, John, Null, Delete
Users, ID, 78, Age, 25, Null, Delete
Users, ID, 78, Name, Jack, John, Update
Users, ID, 78, Age, 25, 26, Update
```
