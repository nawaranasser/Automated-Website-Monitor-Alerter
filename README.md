# Automated Website Monitor & Alerter

A DevOps project that automatically monitors website health and sends email alerts when issues are detected.

## Features
- ✅ Monitors website uptime every 5 minutes
- ✅ Detects slow response times
- ✅ Sends real-time email alerts via Gmail
- ✅ Comprehensive logging system
- ✅ Fully automated via cron jobs

## Technologies Used
- Python
- Gmail SMTP
- Linux Cron Jobs
- Requests library

## Setup
1. Configure Gmail app password in `config.py`
2. Set monitoring parameters
3. Add cron job:
   
       crontab -e
       */5 * * * * cd /path/to/project && /path/to/venv/bin/python monitor.py
     
