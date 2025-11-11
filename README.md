# LEMP Stack Deployment Example – Flask + MySQL + Nginx

## Project Overview

This project demonstrates the deployment of a Python web application on a LEMP stack (Linux, Nginx, MariaDB, Python) hosted on CSC's cPouta cloud service. The application uses Flask as the backend framework, MySQL as the database, and Nginx as a reverse proxy. The web page displays the current time retrieved from the SQL server and includes personalized content.

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