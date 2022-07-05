
# Project structure

**Notice:** Forked from [paalel/master](https://github.com/paalel/master).
This fork exists so that the package can be installed via `pip`. Some other very small changes were made.  

## Animation
The animation folder contains two subfolders: src and db.
src/ contains all things animation related, that is Skeleton and Animation objects,
methods for parsing .asf/.amc-files, methods for creating animations and some attempts at 
different frame interpolation.

db/ contains data and our database. To create the tables run:

```sqlite3 <Name_of_db>.db < create_tables_sqlite3.sql```


unzip the mocap data from mocap.cs.cmu.edu


create config-file: ```cp db_config_example.py db_config.py```

and add the paths to your database and subject folder.

run:

``` python insert_data_db_sqllite3.py```

to add data to database and download subject descriptions (which are scattered all over the site)
from mocap.cs.cmu.edu

```animation_manager.py``` is an interface for fetching animations in applications

## so3

The folder so3/ contains implementation our mathematical framework for SO3.

```convert.py``` : convert animation to curce in SO3

```transformations.py``` log, exp, interpolate, SRVT and other transformations applied to SO3 or curves in SO3

```curves.py```: operations that take a curve, or multiple curves as parameters. This includes distance, dynamic_distance,
close, move_origin and others. These are all written to be quite functional, note however that python has no way of actually enforcing this.

```dynamic_distance.py```: implementations off the the dynamic distance method proposed by Bauer.

```signature.py and log_signature.py```: proposed metrics using the iisignature
library.


experiments, test, and clustering all contain different applications of these method
