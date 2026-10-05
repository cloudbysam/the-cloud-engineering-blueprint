# Project 05: Linux Systemd Service & Scheduled Uptime Timer

A native Linux service and timer deployment using Systemd unit files (`.service` and `.timer`) and Bash health check scripts to monitor and manage web server process lifetimes.

---

## Project Overview

Production web applications are managed as Linux background daemons using init systems like `systemd`. 

This project configures systemd to run our custom Python HTTP web server as a system service with automatic process recovery (`Restart=on-failure`), alongside a systemd timer that periodically executes an HTTP health check script to maintain high availability.

---

## Objectives

- Create custom systemd service units (`.service`) for process supervision.
- Implement scheduled systemd timer units (`.timer`) for automated health checks.
- Handle process recovery and service logging using `systemctl` and `journalctl`.

---

## Repository Structure

```text
05-server-uptime-tests/
├── http-server.service    # Systemd service definition for Python web server
├── uptime-check.service   # Oneshot execution service for health check script
├── uptime-check.timer     # Systemd scheduled timer (30-second interval)
├── health-check.sh        # Bash script to test port 8080 availability
└── README.md              # Project documentation
```
## How to Deploy & Test
```bash
# 1. Copy Unit Files to Systemd
sudo cp http-server.service /etc/systemd/system/
sudo cp uptime-check.service /etc/systemd/system/
sudo cp uptime-check.timer /etc/systemd/system/
sudo systemctl daemon-reload

# 2. Enable and Start Services
sudo systemctl enable --now http-server.service
sudo systemctl enable --now uptime-check.timer

# 3. Verify Active Timers and Logs
sudo systemctl list-timers | grep uptime-check
sudo journalctl -u uptime-check.service -n 20
```

## How to Disable the Service
To stop the server and prevent it from automatically restarting, you need to stop both the timer (which runs the health check) and the service itself.

```bash
# 1. Stop and Disable the Timer First
# If you don't stop the timer first, it will trigger health-check.sh on the next interval, detect that the server is down, and automatically start it again!

# Stop the active timer
sudo systemctl stop uptime-check.timer

# (Optional) Prevent it from starting automatically on system reboot
sudo systemctl disable uptime-check.timer

# 2. Stop the Web Server Service
Now you can cleanly shut down the web server:

# Stop the web server daemon
sudo systemctl stop http-server.service

# (Optional) Prevent it from starting automatically on system reboot
sudo systemctl disable http-server.service

# 3. Verify They Are Stopped
Check the status of both units to confirm they are inactive (dead):

sudo systemctl status uptime-check.timer http-server.service

# When you are ready to turn everything back on later, just run:
sudo systemctl start http-server.service uptime-check.timer.
```
