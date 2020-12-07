#!/bin/bash

# This script should be run from inside the virtual machine

# build the jar
cd /vagrant/java-getting-started
mvn install

# start the postgres server which will listen to the default port 5432
sudo service postgresql start

# In the Heroku assignment, the DATABASE_URL environment variable was automatically
# created when the Heroku Postgres add-on was added to your Heroku application.
# See the `Config Vars` section in your Heroku application settings:
# https://dashboard.heroku.com/apps/<random-generated-app-name>/settings
#
# The Heroku DATABASE_URL environment variable is automatically converted into
# a JDBC_DATABASE_URL environment variable when the Heroku dyno starts up. See:
# https://devcenter.heroku.com/articles/connecting-to-relational-databases-on-heroku-with-java
#
# The JDBC_DATABASE_URL is needed to start the Java Spring web application:
# https://github.com/heroku/java-getting-started/blob/7894b41275e1bef0fa08c2b21f7835290f395099/src/main/resources/application.properties#L1
#
# To connect to a local database, the JDBC_DATABASE_URL needs to be configured as described below:
# === Example for PostgreSQL ===
# Heroku DATABASE_URL environment variable format:
# postgres://[username]:[password]@[host]:[port]/[databaseName]
#
# JDBC_DATABASE_URL format for connecting from a virtual machine to a local database:
# jdbc:postgresql://[host]:[port]/[databaseName]?user=[username]&password=[password]
#
# JDBC_DATABASE_URL format for connecting from a virtual machine to the remote Heroku Postgres database:
# jdbc:postgresql://[host]:[port]/[databaseName]?user=[username]&password=[password]&sslmode=require
#
#
# NOTE: because the Heroku CLI (https://devcenter.heroku.com/articles/heroku-cli) is not installed in the container,
# we cannot use the
# ```bash
# $ heroku local:start
# ```
# command which would load the contents of the `.env` looking for the JDBC_DATABASE_URL:
# https://github.com/heroku/java-getting-started/blob/7894b41275e1bef0fa08c2b21f7835290f395099/README.md#running-locally
#
# Therefore, we have to use the command below, and use the -D flag to set the JDBC_DATABASE_URL environment variable
# and pass it to the java web server to be able to connect to the database
java -DJDBC_DATABASE_URL="jdbc:postgresql://localhost:5432/postgresonvagrantdb?user=postgresonvagrantuser&password=postgresonvagrantpassword" -jar /vagrant/java-getting-started/target/java-getting-started-1.0.jar
