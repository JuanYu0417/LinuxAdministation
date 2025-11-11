# LEMP Stack Deployment Example – Flask + MySQL + Nginx

## Project Overview

This project demonstrates the deployment of a Python web application on a LEMP stack (Linux, Nginx, MySQL/MariaDB, Python) hosted on CSC's cPouta cloud service. The application uses Flask as the backend framework, MySQL as the database, and Nginx as a reverse proxy. The web page displays the current time retrieved from the SQL server and includes personalized content.

## Technology Stack

- Linux (Ubuntu)
- Nginx
- MariaDB
- Python + Flask
- Gunicorn
- systemd (for service management)

## Features

- ✅ Web page accessible via HTTP
- ✅ Version control using GitHub
- ✅ Current time displayed from SQL database
- ✅ Personalized HTML content
- ✅ Persistent service using systemd

## Installation & Deployment Steps

### 1. Update the System

```bash
sudo apt update && sudo apt upgrade -y

### 2. Install Nginx
```bash
sudo apt install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx

### 3. Install MariaDB
```bash
sudo apt install mysql-server -y
sudo mysql_secure_installation

Create a database and user:
CREATE DATABASE exampledb;
CREATE USER 'exampleuser'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON exampledb.* TO 'exampleuser'@'localhost';
FLUSH PRIVILEGES;

### 4. Install Python and Dependencies

sudo apt install python3 python3-pip python3-venv -y
mkdir ~/lemp-app && cd ~/lemp-app
python3 -m venv venv
source venv/bin/activate
pip install flask gunicorn mysql-connector-python

### 5.Create the Flask App
Example app.py:.txt

### 6. Configure Nginx as a Reverse Proxy
Create /etc/nginx/sites-available/lemp-app:.txt

Enable the site and reload Nginx:
sudo ln -s /etc/nginx/sites-available/lemp-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

### 7.Run the App with Gunicorn and systemd
Create /etc/systemd/system/lemp-app.service:.txt

Start and enable the service:

sudo systemctl daemon-reload
sudo systemctl enable lemp-app
sudo systemctl start lemp-app

## Access Information

Web page: http://86.50.20.134:8080/

Notes