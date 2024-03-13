# diff_db

This repository contains code to enable creation of csvs to view differences between different `sqlite` database. This repository effectively serves as a CDC pipeline for `sqlite` databases.

``` csv
Table Name, Primary Key Column Name, Primary Key, Column Name, Old Value, New Value, Type
Users, ID, 78, Name, Null, John, Insert
Users, ID, 78, Age, Null, 91, Insert
Users, ID, 78, Name, John, Null, Delete
Users, ID, 78, Name, Jack, John, Update
```

When there is a composite key in the table, to uniquely identify the name, we'll use a seperator to seperate between the different rows of the keys. This is defined as a constant ";".
