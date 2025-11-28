# WhiteKnight Security v1.0.0 - Administrator Guide

## Table of Contents
1. [System Administration](#system-administration)
2. [Service Operations](#service-operations)
3. [Security Operations](#security-operations)
4. [Incident Response](#incident-response)
5. [Performance Tuning](#performance-tuning)
6. [Backup & Recovery](#backup--recovery)
7. [Compliance & Auditing](#compliance--auditing)

---

## System Administration

### User Management

```bash
# Create WhiteKnight user
sudo useradd -m -s /usr/sbin/nologin whiteknight

# Add user to sudoers (for management)
sudo usermod -aG sudo username

# View sudoers
sudo visudo

# Grant specific sudo privileges
sudo tee -a /etc/sudoers.d/whiteknight << EOF
whiteknight ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart whiteknight
whiteknight ALL=(ALL) NOPASSWD: /usr/bin/journalctl
EOF
```

### System Logging

```bash
# Configure rsyslog
sudo nano /etc/rsyslog.d/30-whiteknight.conf

# Add:
# :programname, isequal, "whiteknight" /var/log/whiteknight/whiteknight.log
# :programname, isequal, "whiteknight" ~

# Restart rsyslog
sudo systemctl restart rsyslog

# View logs
sudo tail -f /var/log/whiteknight/whiteknight.log
```

### Log Rotation

```bash
# Create log rotation config
sudo tee /etc/logrotate.d/whiteknight << EOF
/var/log/whiteknight/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 root adm
    sharedscripts
    postrotate
        /usr/bin/systemctl reload whiteknight > /dev/null 2>&1 || true
    endscript
}
EOF
```

### Monitoring Disk Usage

```bash
# Check disk usage
du -sh /var/log/whiteknight/
du -sh /opt/whiteknight-security/

# Clean old logs
sudo journalctl --vacuum=30d

# Manage log size
sudo journalctl --vacuum=500M
```

---

## Service Operations

### Service Configuration

```bash
# View service file
sudo cat /etc/systemd/system/whiteknight.service

# Edit service
sudo systemctl edit whiteknight

# Reload configuration
sudo systemctl daemon-reload

# Verify changes
sudo systemctl show whiteknight
```

### Starting and Stopping

```bash
# Start service
sudo systemctl start whiteknight

# Stop service
sudo systemctl stop whiteknight

# Restart service
sudo systemctl restart whiteknight

# Graceful reload
sudo systemctl reload whiteknight
```

### Monitoring Service Health

```bash
# Real-time status
sudo systemctl status whiteknight

# Check if running
sudo systemctl is-active whiteknight

# Check if enabled on boot
sudo systemctl is-enabled whiteknight

# Detailed service info
sudo systemctl show whiteknight
```

### Resource Limits

```bash
# View current limits
sudo systemctl show -p MemoryLimit,CPUQuota whiteknight

# Set memory limit (512MB)
sudo systemctl set-property whiteknight MemoryLimit=512M

# Set CPU limit
sudo systemctl set-property whiteknight CPUQuota=50%

# Make permanent
sudo systemctl daemon-reload
```

---

## Security Operations

### Firewall Management

```bash
# View all rules
sudo ufw show added

# View raw rules
sudo iptables -L -n -v

# Add rule
sudo ufw allow from 192.168.1.0/24 to any port 22

# Remove rule
sudo ufw delete allow 22

# Block IP
sudo ufw deny from 192.168.1.100

# Enable connection tracking
sudo ufw enable

# Reload rules
sudo ufw reload
```

### Fail2ban Administration

```bash
# View all jails
sudo fail2ban-client status

# View specific jail
sudo fail2ban-client status sshd

# Ban IP
sudo fail2ban-client set sshd banip 192.168.1.100

# Unban IP
sudo fail2ban-client set sshd unbanip 192.168.1.100

# View banned IPs
sudo fail2ban-client status sshd | grep "Banned IP"

# Restart Fail2ban
sudo systemctl restart fail2ban
```

### SSH Hardening

```bash
# Backup SSH config
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.$(date +%Y%m%d)

# Edit SSH config
sudo nano /etc/ssh/sshd_config

# Key hardening settings:
# PermitRootLogin no
# PasswordAuthentication no
# PubkeyAuthentication yes
# X11Forwarding no
# MaxAuthTries 3
# MaxSessions 10
# AllowUsers user1 user2
# Port 2222

# Test config
sudo sshd -t

# Restart SSH
sudo systemctl restart ssh
```

### File Integrity Monitoring

```bash
# Install AIDE
sudo apt install -y aide aide-common

# Initialize database
sudo aideinit

# Check integrity
sudo aide --check

# Update database
sudo aide --update
sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db
```

### SELinux Management (if applicable)

```bash
# Check SELinux status
getenforce

# Get SELinux context
ls -lZ /opt/whiteknight-security/

# Set SELinux policy
sudo semanage fcontext -a -t admin_home_t "/opt/whiteknight-security(/.*)?"

# Restore context
sudo restorecon -R /opt/whiteknight-security/

# Put in enforcing mode
sudo setenforce 1
```

---

## Incident Response

### Immediate Response

```bash
# 1. Assess threat
sudo systemctl status whiteknight

# 2. Check active threats
curl http://localhost:8002/threats | python3 -m json.tool

# 3. Review firewall blocks
sudo iptables -L -n | grep DROP

# 4. Check failed logins
sudo grep "Failed password" /var/log/auth.log | tail -20

# 5. Preserve evidence
sudo tar -czf incident-evidence-$(date +%Y%m%d-%H%M%S).tar.gz /var/log/
```

### Threat Investigation

```bash
# Search for attack pattern
sudo grep "192.168.1.100" /var/log/auth.log

# Get whois info
whois 192.168.1.100

# Check IP reputation
curl "https://api.abuseipdb.com/api/v2/check" \
  -d "ip=192.168.1.100&maxAgeInDays=90" \
  -H "Key: YOUR_API_KEY"

# Block malicious IP
sudo ufw deny from 192.168.1.100
```

### Mitigation Steps

```bash
# 1. Block attacker
sudo ufw deny from 192.168.1.100

# 2. Harden SSH
sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart ssh

# 3. Update firewall
sudo ufw reload

# 4. Clear logs (optional)
sudo journalctl --vacuum=1d

# 5. Monitor
sudo journalctl -u whiteknight -f
```

### Evidence Preservation

```bash
# Create incident report
sudo cat > incident-$(date +%Y%m%d-%H%M%S).txt << EOF
Incident Report
Date: $(date)
Threat: SSH Attack
Source IP: 192.168.1.100
Action Taken: Blocked IP, Disabled Password Auth
EOF

# Archive logs
sudo tar -czf logs-$(date +%Y%m%d).tar.gz /var/log/auth.log /var/log/syslog

# Store securely
sudo mv *.tar.gz /secure/location/
```

### Law Enforcement Reporting

```bash
# Collect evidence
sudo journalctl -u whiteknight > whiteknight-logs.txt
sudo grep "192.168.1.100" /var/log/auth.log > attack-logs.txt
sudo iptables -L -n > firewall-rules.txt

# Create incident summary
sudo cat > incident-summary.txt << EOF
Incident Summary
================
Date: $(date)
Attack Type: SSH Brute Force
Source IP: 192.168.1.100
Target: Production Server
Impact: Blocked by IPS
Response: IP Banned, SSH Hardened
EOF

# Package for sharing
tar -czf incident-evidence.tar.gz *.txt
```

---

## Performance Tuning

### Memory Optimization

```bash
# Check memory usage
free -h

# View process memory
ps aux | grep api_server
sudo smem -s -k

# Limit memory usage
sudo systemctl set-property whiteknight MemoryMax=1G

# Clear cache
sudo sync && sudo echo 3 > /proc/sys/vm/drop_caches
```

### CPU Optimization

```bash
# Check CPU usage
top
htop
ps aux --sort=-%cpu | head

# View CPU cores
nproc
cat /proc/cpuinfo

# Limit CPU usage
sudo systemctl set-property whiteknight CPUQuota=75%
```

### Network Optimization

```bash
# Monitor network
nethogs
iftop

# Check connections
sudo netstat -tuln
sudo ss -tuln

# Optimize buffer
sudo sysctl -w net.core.rmem_default=134217728
sudo sysctl -w net.core.wmem_default=134217728
```

### Disk I/O Optimization

```bash
# Monitor I/O
iostat -x 1
iotop

# Check disk performance
dd if=/dev/zero of=test.bin bs=1M count=1024
rm test.bin

# Enable disk caching
sudo sysctl -w vm.page-cluster=3
```

---

## Backup & Recovery

### Backup Strategy

```bash
# Create backup directory
sudo mkdir -p /backup/whiteknight-$(date +%Y%m%d)

# Backup configuration
sudo cp -r /opt/whiteknight-security /backup/whiteknight-$(date +%Y%m%d)/
sudo cp -r /etc/systemd/system/whiteknight.service /backup/whiteknight-$(date +%Y%m%d)/

# Backup logs
sudo tar -czf /backup/whiteknight-logs-$(date +%Y%m%d).tar.gz /var/log/whiteknight/

# Backup firewall rules
sudo iptables-save > /backup/firewall-rules-$(date +%Y%m%d).txt
sudo ufw status > /backup/ufw-status-$(date +%Y%m%d).txt
```

### Automated Backups

```bash
# Create backup script
sudo tee /usr/local/bin/backup-whiteknight.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backup/whiteknight-$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup files
cp -r /opt/whiteknight-security $BACKUP_DIR/
cp /etc/systemd/system/whiteknight.service $BACKUP_DIR/

# Backup logs
tar -czf $BACKUP_DIR/logs.tar.gz /var/log/whiteknight/

# Backup firewall
iptables-save > $BACKUP_DIR/firewall.txt

# Remove old backups (keep 30 days)
find /backup -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;
EOF

sudo chmod +x /usr/local/bin/backup-whiteknight.sh

# Schedule daily backups
echo "0 2 * * * root /usr/local/bin/backup-whiteknight.sh" | sudo tee /etc/cron.d/whiteknight-backup
```

### Recovery Procedure

```bash
# Stop service
sudo systemctl stop whiteknight

# Restore configuration
sudo cp -r /backup/whiteknight-YYYYMMDD/* /opt/whiteknight-security/

# Restore systemd service
sudo cp /backup/whiteknight-YYYYMMDD/whiteknight.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start whiteknight

# Verify
sudo systemctl status whiteknight
```

---

## Compliance & Auditing

### Audit Logging

```bash
# Enable auditd
sudo apt install -y auditd audispd-plugins

# Start audit service
sudo systemctl enable auditd
sudo systemctl start auditd

# Add audit rules
sudo auditctl -w /opt/whiteknight-security/ -p wa -k whiteknight_changes
sudo auditctl -w /etc/ssh/sshd_config -p wa -k ssh_config_changes

# View audit logs
sudo ausearch -k whiteknight_changes
```

### Compliance Reporting

```bash
# Generate compliance report
sudo cat > compliance-report-$(date +%Y%m%d).txt << EOF
WhiteKnight Security Compliance Report
Generated: $(date)

System Information:
- Hostname: $(hostname)
- OS: $(lsb_release -ds)
- Kernel: $(uname -r)

Security Status:
- Firewall: $(sudo ufw status | head -1)
- Fail2ban: $(sudo systemctl is-active fail2ban)
- SSH Key Auth: $(grep "PasswordAuthentication" /etc/ssh/sshd_config)

Updates:
- Security Updates: $(sudo apt list --upgradable 2>/dev/null | wc -l)

Logs Monitored:
- Auth Logs: $(wc -l < /var/log/auth.log)
- System Logs: $(wc -l < /var/log/syslog)
EOF

cat compliance-report-$(date +%Y%m%d).txt
```

### Security Audit Checklist

```bash
#!/bin/bash

echo "WhiteKnight Security Audit Checklist"
echo "===================================="
echo ""

# 1. Service Status
echo "1. Service Status:"
sudo systemctl is-active whiteknight && echo "   ✓ Running" || echo "   ✗ Not Running"

# 2. Firewall
echo "2. Firewall Status:"
sudo ufw status | head -1

# 3. SSH Hardening
echo "3. SSH Password Auth:"
grep "PasswordAuthentication" /etc/ssh/sshd_config

# 4. Fail2ban
echo "4. Fail2ban Status:"
sudo fail2ban-client status sshd 2>/dev/null | head -1

# 5. System Updates
echo "5. Pending Security Updates:"
sudo apt list --upgradable 2>/dev/null | wc -l

# 6. Disk Space
echo "6. Disk Space Usage:"
df -h / | tail -1

# 7. Memory Usage
echo "7. Memory Usage:"
free -h | grep Mem

# 8. Open Ports
echo "8. Open Ports:"
sudo ss -tuln | grep LISTEN

# 9. Failed Logins (last 24h)
echo "9. Failed Logins:"
grep "Failed password" /var/log/auth.log | tail -5 | wc -l

# 10. Recent Changes
echo "10. Configuration Changes:"
sudo find /etc -mtime -7 -type f 2>/dev/null | wc -l

echo ""
echo "Audit Complete!"
```

---

## Troubleshooting

### Common Issues

**Issue**: Service crashes frequently
```bash
# Check logs
sudo journalctl -u whiteknight -n 200

# Check memory
ps aux | grep api_server

# Restart with debug
python3 -u /opt/whiteknight-security/api_server.py
```

**Issue**: High CPU usage
```bash
# Find process
top -b -n 1 | grep api_server

# Profile CPU
sudo python3 -m cProfile /opt/whiteknight-security/api_server.py
```

**Issue**: Port conflicts
```bash
# Find process on port
sudo lsof -i :8002

# Kill and restart
sudo fuser -k 8002/tcp
sudo systemctl restart whiteknight
```

---

## Support & Resources

**Documentation**: https://github.com/appdevwk/whiteknight-security
**Issues**: https://github.com/appdevwk/whiteknight-security/issues
**Contact**: appdevwk@proton.me

---

**WhiteKnight Security v1.0.0 - Enterprise Administration** 🛡️
