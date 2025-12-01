# LEMP Stack Deployment Example – Flask + Mariadb + Nginx

## Project Overview

This project demonstrates the deployment of a Python web application on a LEMP stack (Linux, Nginx, MariaDB, Python) hosted on CSC's cPouta cloud service. The application uses Flask as the backend framework, MariaDB as the database, and Nginx as a reverse proxy. The web page displays the current time retrieved from the SQL server and includes personalized content.

## Technology Stack
- Linux (Ubuntu)
- Nginx(web server,Reverse proxy,Static file server,HTTPS handler)
- MariaDB
- Python
- Flask(a Python web framework)
- Gunicorn(a Python WSGI server)
- systemd (a Linux service manager)

## Features

- Web page accessible via HTTP
- Version control using GitHub
- Current time displayed from SQL database
- Personalized HTML content
- Persistent service using systemd

## Installation & Deployment Steps

### 1. Update the System
```bash
sudo apt update && sudo apt upgrade -y
```
### 2. Install Nginx
```bash
sudo apt install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
```

### 3. Install MariaDB
```bash
sudo apt install mysql-server -y
sudo mysql_secure_installation
```
Create a database and user:
```bash
CREATE DATABASE exampledb;
CREATE USER 'exampleuser'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON exampledb.* TO 'exampleuser'@'localhost';
FLUSH PRIVILEGES;
```
### 4. Install Python and Dependencies
```bash
sudo apt install python3 python3-pip python3-venv -y
mkdir ~/lemp-app && cd ~/lemp-app
python3 -m venv venv
source venv/bin/activate
pip install flask gunicorn mysql-connector-python
```
### 5.Create the Flask App
Example [`app.py`](https://github.com/JuanYu0417/LinuxAdministation/blob/main/LEMP-app.py.txt)

### 6. Configure Nginx as a Reverse Proxy
Create /etc/nginx/sites-available/lemp-app:[nginx](https://github.com/JuanYu0417/LinuxAdministation/blob/main/Nginx-as-ReverseProxy.txt)

Enable the site and reload Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/lemp-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```
### 7.Run the App with Gunicorn and systemd
When I press Ctrl + C or close the terminal, the app stops, and my website becomes unreachable.I need it Runs continuously, restarts automatically, and doesn’t stop when you close the terminal.

Create /etc/systemd/system/lemp-app.service:[GunicornandSystemd](https://github.com/JuanYu0417/LinuxAdministation/blob/main/withGunicorn%2Bsystemd.txt)

Start and enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable lemp-app
sudo systemctl start lemp-app
```

### 8.Personlize the website page
```bash
cd templates
sudo nano index.html
```
Now  personalized webpage is ready:[newPage](https://github.com/JuanYu0417/LinuxAdministation/blob/main/Personalize%20HTML%20page.txt)

Restart systemd:
```bash
source venv/bin/activate
sudo systemctl restart lemp-app.service
sudo systemctl status lemp-app.service
```

## Access Information

Web page: http://86.50.20.134:8080/

## Notes(somethings need be improved)
1.Time zone(finished);

2.website page personalizes(finished)

# Adding Streamlit to LEMP Stack and Configuring Nginx Reverse Proxy

## What is Streamlit,plotly and pandas?
- Streamlit: an open-source Python framework for data scientists and AI/ML engineers to deliver interactive data apps – in only a few - lines of code.
- Pandas: Cleaning, transforming, and analyzing datasets efficiently.
- Plotly: Creating interactive charts and visualizations.

## I used "listen 80" in viikotehtävä 1. How can I deal with the port 80?
Nginx is a reverse proxy and web server that can handle multiple paths simultaneously. listen 80 means Nginx continues to listen on the standard HTTP port. As long as I keep the existing location / or root pointing to my  original web directory in the Nginx configuration, the original page will remain accessible.

At first of all, I should release :80 port from apache2.
1. Stop and Disable Apache Service
```bash
sudo systemctl stop apache2
sudo systemctl disable apache2
```
2. Verify Port Release
```bash
sudo lsof -i :80
```
3. Make sure Nginx is installed and start the service:
```bash
sudo systemctl start nginx
```
## Preparing the enviroment
1. log in to my CSC cPouta VPS and add new rules:Add 8501 port;
2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. create myapp
```bash
sudo nano myapp.py
```
Then add Streamlit-Nginx as ReverseProxy:[myapp](https://github.com/JuanYu0417/LinuxAdministation/blob/main/Streamlit_programme/Add-Streamlit-Nginx-as-ReverseProxy.txt)

4.Run the App with Gunicorn and systemdc
```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit
sudo systemctl status streamlit
```
## Set up and run Streamlit following guide
1.install required package
```bash
pip install streamlit pandas plotly mysqlclient
```
2.Run Streamlit As A Service:
```bash
sudo nano /etc/systemd/system/streamlit.service
```
[StramlitService](https://github.com/JuanYu0417/LinuxAdministation/blob/main/Streamlit_programme/RunStreamlitAsAServiceNew.txt)

3.Configure Streamlit for subpath by creating .streamlit/config.toml
```bash
[server]
port = 8501
address = "127.0.0.1"
baseUrlPath = "/data-analysis"
enableCORS = false
enableXsrfProtection = false
```
4.then 
```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit
sudo systemctl status streamlit
```
5.create Streamlit page:[Stramlitpage](https://github.com/JuanYu0417/LinuxAdministation/blob/main/Streamlit_programme/RunStreamlitAsAServiceNew.txt)

## create database and use it
1.create database stockdb
```bash
sudo mysql -u root -p
SHOW DATABASES;
CREATE DATABASE stockdb;
USE stockdb;
```

2.create table company_info 
```bash

CREATE TABLE company_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    industry VARCHAR(50) NOT NULL,
    country VARCHAR(50) DEFAULT 'Finland',
    ytd_gain DECIMAL(6,2),
    description TEXT
);

```   
create table stock_prices  
```bash


CREATE TABLE stock_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(10,2),
    high DECIMAL(10,2),
    low DECIMAL(10,2),
    close DECIMAL(10,2),
    volume BIGINT
);
``` 
3.CSV from windows to ubuntu and update database to mysql:

```bash
cd myapp
sudo nano omxh25_companies.csv
sudo mysql
use stockdb

LOAD DATA INFILE ' /home/ubuntu/myapp/omxh25_companies.csv'
INTO TABLE company_info
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(name, symbol, industry, country, ytd_gain, description);

```

4.fetch prices from yfinance using Python. I tried many times and used Copilot code:[Fetch:prices](https://github.com/JuanYu0417/LinuxAdministation/blob/main/Streamlit_programme/fetch_price.csv.txt)

## Access Information

Web page: http://86.50.20.134


# Cron + API + MySQL + Streamlit
## Modify database table:stock-prices.
```bash
sudo mysql
USE stockdb;
ALTER TABLE stock_prices MODIFY date DATETIME NOT NULL;
```  
The database is now able to precisely store timestamps (YYYY-MM-DD HH:MM:SS), and is ready for the upcoming 15-minute Cron updates.
## modify fetch_prices.py  
Modified the script to fetch the latest data snapshot using** period="1d" ** instead of a historical date range.   
Implemented ** datetime.now()  ** to insert the precise execution timestamp into the database.  
[Fetch:prices](https://github.com/JuanYu0417/LinuxAdministation/blob/main/Streamlit_programme/fetch_price.csv.txt)


## Cron every 15min
### What is Cron?
Cron is a time-based job scheduler in Unix-like operating systems that automates repetitive tasks by running commands at specified intervals. These automated tasks are called "cron jobs" and are defined in a file called a **crontab**.   
Cron jobs are used for tasks like system maintenance, running backups, and processing data, and are configured using a specific syntax with five fields for minute, hour, day of the month, month, and day of the week. 
A common format includes five fields for time, followed by the command to run:
* * * * * /path/to/command

### configure Cron:  
```bash
crontab -e
*/15 * * * * /home/ubuntu/myapp/venv/bin/python /home/ubuntu/myapp/fetch_prices.py >> /home/ubuntu/myapp/cron_log.txt 2>&1
crontab -l
```  
Then test:  
```bash
/home/ubuntu/myapp/venv/bin/python /home/ubuntu/myapp/fetch_prices.py >> /home/ubuntu/myapp/cron_log.txt 2>&1
cat /home/ubuntu/myapp/cron_log.txt
```  
### Add "Currect time" and "Update time"

```Python
import os
import time
import pytz
from datetime import datetime

tz = pytz.timezone('Europe/Helsinki')

st.write(f"Current Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
data_file = 'cron_log.txt' 
if os.path.exists(data_file):
    file_ts = os.path.getmtime(data_file)
    file_dt = datetime.fromtimestamp(file_ts, tz)
    st.write(f"Update: {file_dt.strftime('%Y-%m-%d %H:%M:%S')}")
else:
    st.write("Update: Never")
```

### Extra Api (Helsinki Weather)

```bash
nano /home/ubuntu/myapp/run_cron.sh
``` 
```bash

PROJECT_DIR="/home/ubuntu/myapp"
VENV_DIR="$PROJECT_DIR/venv"

cd $PROJECT_DIR

source $VENV_DIR/bin/activate

python fetch_prices.py

echo "Cron run finished at $(date)"
``` 
```bash
chmod +x /home/ubuntu/myapp/run_cron.sh
``` 
update app.py:[app.py](https://github.com/JuanYu0417/LinuxAdministation/blob/main/Streamlit_programme/createStreamlitPage.txt)

# Docker container+MQTT
## Docker VS virtual machine
Docker is a platform designed to help developers build, share, and run container applications.  
VMs run independent OS kernels; Docker shares the host's kernel.VMs are heavy and take minutes to start; Docker is lightweight and starts in seconds.
## What is MQTT?
MQTT (Message Queuing Telemetry Transport) is a very lightweight messaging protocol used to send data between devices.
## Prerequisites
### Add port 1883,9001(TCP)
### install docker
```bash
sudo apt update
sudo apt install docker.io docker-compose-plugin
sudo docker-compose up -d --build
sudo docker-compose ps
```  
### create Python-skripti
```bash
sudo apt install python3-paho-mqtt
 ```

### test
Problem 1:404 Not Found
```bash
sudo nginx -t
```
** 2025/12/01 17:28:37 [warn] 308754#308754: conflicting server name "_" on 0.0.0.0:80, ignored **
Modify  /etc/nginx/sites-available/default[default](https://github.com/JuanYu0417/LinuxAdministation/blob/main/docker%2BMQTT/default),let Nginx configuration act as a unified entry point, utilizing port 80 to distribute incoming client requests to various backend destinations based on the URL path

Problem 2:Not Found
The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
```bash
sudo ss -lptn 'sport = :5000'
ps -ef |grep python3
sudo pkill -f gunicorn
sudo ss -tlnp | grep 5000
```

