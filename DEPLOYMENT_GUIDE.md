# WhiteKnight Security v1.0.0 - Deployment Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Initial Configuration](#initial-configuration)
4. [Service Management](#service-management)
5. [Security Hardening](#security-hardening)
6. [Verification & Testing](#verification--testing)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Hardware
- **CPU**: 1 GHz or faster
- **RAM**: 2 GB minimum, 4 GB recommended
- **Storage**: 500 MB free space minimum
- **Network**: Stable internet connection

### Software
- **OS**: Linux (Ubuntu 18.04+, Debian 10+, Fedora 30+, CentOS 7+, Arch Linux)
- **Python**: 3.8 or higher
- **Sudo**: Root or sudo access required

### Network
- Port 8002 available (dashboard/API)
- Port 22 available (SSH - for management)
- Firewall ports 3000, 3001, 5000, 8080 (optional - app ports)

---

## Installation Methods

### Method 1: Debian Package (Recommended)

**Prerequisites**:
```bash
sudo apt update
sudo apt install -y curl wget
```

**Installation**:
```bash
# Download package
wget https://github.com/appdevwk/whiteknight-security/releases/download/v1.0.0-fixed/whiteknight-security_1.0.0_amd64.deb

# Verify checksum
wget https://github.com/appdevwk/whiteknight-security/releases/download/v1.0.0-fixed/SHA256SUMS
sha256sum -c SHA256SUMS

# Install
sudo dpkg -i whiteknight-security_1.0.0_amd64.deb

# Install dependencies if needed
sudo apt --fix-broken install -y
```

**Verify Installation**:
```bash
sudo systemctl status whiteknight
curl http://localhost:8002
```

### Method 2: AppImage (Universal)

**Installation**:
```bash
# Download
wget https://github.com/appdevwk/whiteknight-security/releases/download/v1.0.0-fixed/WhiteKnight\ Security-1.0.0.AppImage

# Make executable
chmod +x WhiteKnight\ Security-1.0.0.AppImage

# Run
./WhiteKnight\ Security-1.0.0.AppImage &
```

### Method 3: Manual Installation

**Prerequisites**:
```bash
sudo apt update
sudo apt install -y python3 python3-pip clamav fail2ban ufw
pip3 install fastapi uvicorn python-dotenv requests
```

**Installation**:
```bash
# Clone repository
git clone https://github.com/appdevwk/whiteknight-security.git
cd whiteknight-security

# Run API
python3 api_server.py &

# Access dashboard
firefox http://localhost:8002
```

---

## Initial Configuration

### 1. Enable Firewall

```bash
# Enable UFW
sudo ufw enable

# Allow SSH (important!)
sudo ufw allow 22/tcp

# Allow WhiteKnight dashboard
sudo ufw allow 8002/tcp

# Allow app ports
sudo ufw allow 3000/tcp
sudo ufw allow 3001/tcp
sudo ufw allow 5000/tcp
sudo ufw allow 8080/tcp

# Check status
sudo ufw status
```

### 2. Configure Fail2ban

```bash
# Enable Fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Check status
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

### 3. Harden SSH

```bash
# Backup original config
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# Edit SSH config
sudo nano /etc/ssh/sshd_config

# Make these changes:
# PasswordAuthentication no
# PermitRootLogin no
# Port 2222 (optional - non-standard port)
# MaxAuthTries 3
# MaxSessions 10
# ClientAliveInterval 300
# ClientAliveCountMax 2

# Restart SSH
sudo systemctl restart ssh

# Verify
sudo sshd -t
```

### 4. Update ClamAV Signatures

```bash
# Update malware definitions
sudo freshclam

# Schedule automatic updates
sudo systemctl enable clamav-freshclam
sudo systemctl start clamav-freshclam
```

### 5. Configure WhiteKnight Service

```bash
# Service runs automatically on boot
sudo systemctl enable whiteknight

# Check configuration
sudo systemctl status whiteknight

# View logs
sudo journalctl -u whiteknight -f
```

---

## Service Management

### Start Service
```bash
sudo systemctl start whiteknight
```

### Stop Service
```bash
sudo systemctl stop whiteknight
```

### Restart Service
```bash
sudo systemctl restart whiteknight
```

### Check Status
```bash
sudo systemctl status whiteknight
```

### View Real-time Logs
```bash
sudo journalctl -u whiteknight -f
```

### View Historical Logs
```bash
sudo journalctl -u whiteknight --since "2 hours ago"
```

### Enable on Boot
```bash
sudo systemctl enable whiteknight
```

### Disable on Boot
```bash
sudo systemctl disable whiteknight
```

---

## Security Hardening

### 1. System Updates

```bash
# Update system packages
sudo apt update
sudo apt upgrade -y
sudo apt full-upgrade -y

# Install security updates
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 2. Firewall Advanced Rules

```bash
# Block specific IP
sudo ufw deny from 192.168.1.100

# Allow only from specific IP
sudo ufw allow from 203.0.113.0/24 to any port 22

# Rate limiting
sudo ufw limit 22/tcp
sudo ufw limit 8002/tcp

# Check rules
sudo ufw status numbered
```

### 3. IP Tables Rules

```bash
# View current rules
sudo iptables -L -n

# Save rules
sudo iptables-save > /etc/iptables/rules.v4

# Restore rules
sudo iptables-restore < /etc/iptables/rules.v4
```

### 4. SELinux (if available)

```bash
# Check status
getenforce

# Set to enforcing
sudo setenforce 1
```

### 5. File Permissions

```bash
# Restrict SSH config
sudo chmod 600 /etc/ssh/sshd_config

# Restrict sudoers
sudo chmod 440 /etc/sudoers

# Set proper log permissions
sudo chmod 640 /var/log/auth.log
```

---

## Verification & Testing

### 1. Dashboard Accessibility

```bash
# Test from local machine
curl http://localhost:8002

# Test API
curl http://localhost:8002/threats

# Test from remote (if applicable)
curl http://<SERVER_IP>:8002
```

### 2. Service Health Check

```bash
# Check service status
sudo systemctl is-active whiteknight

# Check if listening
sudo netstat -tuln | grep 8002
sudo ss -tuln | grep 8002

# Check process
ps aux | grep python3 | grep api_server
```

### 3. Security Verification

```bash
# Check firewall
sudo ufw status verbose

# Check Fail2ban
sudo fail2ban-client status

# Check SSH hardening
sudo grep -E "PasswordAuthentication|PermitRootLogin" /etc/ssh/sshd_config

# Check system updates
sudo apt list --upgradable
```

### 4. Threat Detection Test

```bash
# Test SSH detection
ssh invalid_user@localhost

# Test firewall detection
sudo iptables -A INPUT -s 192.168.1.100 -j DROP

# Check dashboard for threats
firefox http://localhost:8002
```

### 5. Log Review

```bash
# Check WhiteKnight logs
sudo journalctl -u whiteknight -n 50

# Check auth logs
sudo tail -50 /var/log/auth.log

# Check system logs
sudo tail -50 /var/log/syslog
```

---

## Troubleshooting

### Issue: Service Won't Start

**Error**: `Failed to start whiteknight.service`

**Solutions**:
```bash
# Check error
sudo systemctl status whiteknight -l

# View detailed logs
sudo journalctl -u whiteknight -n 100

# Check if port is in use
sudo lsof -i :8002

# Kill process on port
sudo fuser -k 8002/tcp

# Restart service
sudo systemctl restart whiteknight
```

### Issue: Dashboard Not Accessible

**Error**: `Connection refused` or `This site can't be reached`

**Solutions**:
```bash
# Check if service is running
sudo systemctl status whiteknight

# Test local connection
curl http://localhost:8002

# Check firewall
sudo ufw status | grep 8002

# Allow port if blocked
sudo ufw allow 8002/tcp

# Check logs for errors
sudo journalctl -u whiteknight -f
```

### Issue: Permission Denied

**Error**: `Permission denied` when executing commands

**Solutions**:
```bash
# Use sudo for sensitive operations
sudo iptables -L

# Check user permissions
id

# Add user to sudo group (if needed)
sudo usermod -aG sudo username

# Verify sudo works
sudo whoami
```

### Issue: High CPU Usage

**Error**: Service consuming excessive CPU

**Solutions**:
```bash
# Check process
top -p $(pgrep -f api_server)

# Check logs for errors
sudo journalctl -u whiteknight

# Restart service
sudo systemctl restart whiteknight

# Monitor
watch -n 1 'ps aux | grep api_server'
```

### Issue: Port Already in Use

**Error**: `Address already in use` on port 8002

**Solutions**:
```bash
# Find process using port
sudo lsof -i :8002

# Kill process
sudo kill -9 <PID>

# Or use fuser
sudo fuser -k 8002/tcp

# Verify port is free
sudo netstat -tuln | grep 8002

# Restart service
sudo systemctl restart whiteknight
```

### Issue: Database/Log Storage Full

**Error**: `No space left on device`

**Solutions**:
```bash
# Check disk usage
df -h

# Clean old logs
sudo journalctl --vacuum=30d

# Clean package cache
sudo apt clean
sudo apt autoclean

# Find large files
du -sh /* | sort -rh

# Clear old logs manually
sudo rm -rf /var/log/whiteknight/*.old
```

---

## Advanced Configuration

### Custom Port

```bash
# Edit systemd service
sudo nano /etc/systemd/system/whiteknight.service

# Change port in ExecStart:
# ExecStart=/usr/bin/python3 /opt/whiteknight-security/api_server.py --port 9000

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart whiteknight
```

### Environment Variables

```bash
# Create config file
sudo nano /etc/whiteknight/config.env

# Add settings:
# DEBUG=true
# LOG_LEVEL=debug
# API_PORT=8002

# Load in service
sudo nano /etc/systemd/system/whiteknight.service
# EnvironmentFile=/etc/whiteknight/config.env
```

### SSL/TLS Configuration

```bash
# Generate self-signed certificate
sudo openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Update api_server.py to use SSL
# (See documentation for SSL setup)
```

---

## Monitoring & Maintenance

### Daily Tasks
```bash
# Check service status
sudo systemctl status whiteknight

# Review threat logs
sudo journalctl -u whiteknight -n 100

# Check disk space
df -h
```

### Weekly Tasks
```bash
# Update firewall rules
sudo ufw status

# Check Fail2ban status
sudo fail2ban-client status

# Review security logs
sudo tail -200 /var/log/auth.log
```

### Monthly Tasks
```bash
# Full system update
sudo apt update && sudo apt upgrade -y

# Update ClamAV definitions
sudo freshclam

# Review and rotate logs
sudo logrotate -f /etc/logrotate.conf

# Security audit
sudo apt autoremove
sudo apt autoclean
```

---

## Support & Resources

**Documentation**: https://github.com/appdevwk/whiteknight-security
**Issues**: https://github.com/appdevwk/whiteknight-security/issues
**Contact**: appdevwk@proton.me

---

**WhiteKnight Security v1.0.0 - Enterprise Cybersecurity Platform** 🛡️
