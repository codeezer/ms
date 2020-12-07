# update available package lists for Ubuntu
sudo apt-get update

# install the Java OpenJDK 8 (not the Oracle Java JDK 8, which requires a license)
# the Java JDK includes the Java JRE as well
sudo apt install -y openjdk-8-jdk

# git is already installed
# sudo apt install -y git

# install maven to be able to build the heroku startup repository
sudo apt install -y maven


# ==============================
# === DATABASE SETUP - START ===
# ==============================

# install PostgreSQL to allow the web application to store data in the local database
# the DEBIAN_FRONTEND environment variable argument is needed to suppress the postgres prompts
# for manually selecting the region and time zone
DEBIAN_FRONTEND=noninteractive
sudo apt-get install -y postgresql

# start the PostgreSQL service
sudo /etc/init.d/postgresql start

# create a PostgreSQL role named 'postgresonvagrantuser' having the password 'postgresonvagrantpassword'
# and then create a database 'postgresonvagrantdb' owned by the 'postgresonvagrantuser' role.
# NOTE: these commands are ran as the 'postgres' bash user, which was created automatically when postgresql was installed using apt-get
sudo -u postgres psql --command "CREATE USER postgresonvagrantuser WITH SUPERUSER PASSWORD 'postgresonvagrantpassword';"
sudo -u postgres createdb --owner postgresonvagrantuser postgresonvagrantdb

# ============================
# === DATABASE SETUP - END ===
# ============================


# clone the heroku startup repository containing the Java Spring web application
# into the /vagrant/java-getting-started folder
#
# NOTE:
# the contents of the /vagrant folder in the guest VM will be automatically synched with
# the <folder of cloned CS573-Assignments-Vagrant> folder on the host machine
# Hence, the source code of the cloned repository can be edited in the host machine,
# and the changes will be instantly available on the guest VM to be compiled and run
git clone https://github.com/heroku/java-getting-started /vagrant/java-getting-started

# all future commands will be relative to the cloned repository
cd /vagrant/java-getting-started

# this steps illustrates that we can be very specific with the revision
# of the cloned repository we want to build, as it could be the case that
# the latest revision of the cloned repository may contain unstable changes or
# changes with unwanted side effects.
# Also, this practice promotes reproducibility of the development environment being built.
#
# Alternatively, we can specify a git tag instead of a sha, but for this example,
# since we do not have write access to the cloned repository to create tags, we use the sha of commit
# https://github.com/heroku/java-getting-started/commit/7894b41275e1bef0fa08c2b21f7835290f395099
git reset --hard 7894b41275e1bef0fa08c2b21f7835290f395099


# === HACK FOR DEBUG AND GRADING - START ===
# insert this print statement at the beginning of the `dataSource()` method of the `Main` class
# to see the database url that was passed to the web server as an environment variable
#
# NOTE: this hack for debugging would only make sense if we specify the git commit sha in the
# `git reset --hard` command, where we know that at line 79 we could insert the print statement
# in the correct location:
# https://github.com/heroku/java-getting-started/blob/7894b41275e1bef0fa08c2b21f7835290f395099/src/main/java/com/example/Main.java#L79
#
# Obviously, in real world projects (and not in this simple example) in which we will have write access
# to the cloned repository, we could setup proper logging and there will be no need for this hack
sed -i '79i    System.out.println("dbUrl = " + dbUrl);' src/main/java/com/example/Main.java
# === HACK FOR DEBUG AND GRADING - END ===

# NOTE: The file <folder of cloned CS573-Assignments-Vagrant>/start_server.sh on the host machine will automatically be
# available in the guest VM at: /vagrant/start_server.sh and in this way it
# can be run from inside the VM
chmod +x /vagrant/start_server.sh 
