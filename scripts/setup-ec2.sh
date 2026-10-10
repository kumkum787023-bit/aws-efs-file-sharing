#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 ]]; then echo 'Usage: sudo bash setup-ec2.sh fs-xxxxxxxxxxxxxxxxx'; exit 1; fi
EFS_ID="$1"
dnf install -y python3 python3-pip amazon-efs-utils
mkdir -p /mnt/efs
if ! mountpoint -q /mnt/efs; then mount -t efs -o tls "$EFS_ID":/ /mnt/efs; fi
mkdir -p /mnt/efs/shared_files
chown ec2-user:ec2-user /mnt/efs/shared_files
if ! grep -q "^$EFS_ID:/ /mnt/efs " /etc/fstab; then echo "$EFS_ID:/ /mnt/efs efs _netdev,tls 0 0" >> /etc/fstab; fi
python3 -m venv /home/ec2-user/efs-venv
/home/ec2-user/efs-venv/bin/pip install 'Flask>=3.1,<4' gunicorn
cat > /etc/systemd/system/efs-share.service <<'UNIT'
[Unit]
Description=EFS File Sharing Demo
After=network-online.target remote-fs.target
Wants=network-online.target
RequiresMountsFor=/mnt/efs
[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/aws-efs-file-sharing
Environment=SHARED_DIR=/mnt/efs/shared_files
Environment=SECRET_KEY=replace-this-with-a-long-random-string
ExecStart=/home/ec2-user/efs-venv/bin/gunicorn --bind 0.0.0.0:8000 app:app
Restart=always
[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable --now efs-share
systemctl status efs-share --no-pager
