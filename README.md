# Log Analysis Project

Reporting tool that prints out reports (in plain text) based on the data in a database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

The reporting tool needed to answer the following questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## 0. Prerequisites (Vagrant Virtualization of Linux and Required packages)

#### Open the git CLI on your host and Virtualize Linux OS (Vagrant & Vbox).

(The commands listed here are for CentOs. Consider it if you are using another distribution).

```bash
mkdir vm_folder
cd vm_folder
vagrant init centos/7
```

#### **Edit .Vagrant file for having the machine as another host in your network**

```bash
config.vm.network "public_network", ip: "192.168.1.200", gateway: "192.168.1.1", bootproto:"static", bridge: "adap_name"

config.vm.synced_folder "./share", "/vagrant", type: "virtualbox"
```

#### up & connect

```bash
vagrant up && vagrant ssh
```

#### Check the avability of your VM making a request.

```bash
sudo printf 'HTTP/1.1 302 Moved\r\nlocation: https://www.eff.org' | nc -l 2345
```

#### Enter in the browser

`192.168.1.200:2345`  should now redirect to `eff.org`

#### Install required packages

```bash
sudo yum install dnf -y
sudo dnf install make zip unzip nano vim net-tools nmap tcpdum traceroute mtr libpcap bind-utils -y
```

#### Install Python3.6, PostgreSQL and psycopg2

```bash
sudo yum install https://centos7.iuscommunity.org/ius-release.rmp -y
sudo dnf install python36u python36u-libs python36u-devel python36u-pip -y
sudo pip3.6 install --upgrade pip

postgresql.org/download → select SO and follow the steps

sudo pip3.6 install -U flask
sudo pip3.6 install oauth2client redis passlib flask-httpauth
sudo pip3.6 install sqlalchemy psycopg2-binary bleach requests
```

## 1. Create the database and connect with the sql file provided

#### Enter in the PostgreSQL cli by typing:

```sql
psql
```

#### Create the `news` database.

```sql
create database news;
```

#### Connect to it by typing

```sql
\c news
```

#### **Download the .sql file from this link provided by Udacity.

[**HERE**](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).

#### After downloaded, connect it with the postgresql database**

```bash
psql -d news -f /path_to_your/newsdata.sql
```

## 2. Enter in `psql` cli and submit the SQL views.

#### Make a view listing all the articles titles, ordered by views.

```sql
create view top_articles as
select articles.title, count(log.id) as total_views
from articles, log
where log.path = concat('/article/', articles.slug)
group by articles.title
order by total_views desc;
```

#### Make a view linking the author's name and their articles titles.

```sql
create view titles_by_author as
select title, name
from articles, authors
where articles.author = authors.id;
```

#### Count the total of status/requests ordered by day.

```sql
create view total as
select date(time) as day, cast(count(status) as float) as total
from log
group by day
order by day;
```

#### Count the total of status with errors.

```sql
create view errors as
select date(time) as day, cast(count(status) as float) as errors
from log
where not status='200 OK'
group by day
order by day;
```

## 3. With those views created, run the log_analysis.py file:

`python3.6 log_analysis.py`

#### Author

Alejandro Martinez