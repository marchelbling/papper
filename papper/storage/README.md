# Setting up postgres

Need to create user/db manually:
* `sudo -u postgres createuser 'Config.database['user'] --pwprompt`
* `sudo -u postgres createdb --owner='Config.database['user']' --encoding=utf8 'Config.database['database']'`
