# AWS File Sharing System using Amazon EFS

A college demonstration of shared storage: two EC2 instances mount one Amazon EFS file system and serve the same file list. Upload on instance A, refresh instance B, and download the file there.

## Run locally in VS Code (Windows PowerShell)

```powershell
cd aws-efs-file-sharing
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:8000 . Local mode saves files in `shared_files`; it demonstrates the interface, but it does not use AWS EFS.

## AWS setup (Amazon Linux 2023)

1. Use one AWS Region and VPC. Create an EFS file system in that VPC, with mount targets in the Availability Zones of both EC2 instances. Wait for mount targets to be available.
2. Create an **EFS security group** allowing inbound **TCP 2049** only from the **EC2 security group**. Attach it to all EFS mount targets.
3. Create an **EC2 security group** allowing inbound **TCP 8000** only from your own IP for the demo. Allow SSH TCP 22 only from your IP if you use SSH. Its outbound rules must permit EFS TCP 2049. Never expose the demo broadly: it has no login.
4. Launch two Amazon Linux 2023 EC2 instances in the same VPC, preferably different Availability Zones that have EFS mount targets. Choose a compatible instance type and key pair or use Systems Manager Session Manager. Note both public IPs if direct browser access is configured.
5. Put this project folder at `/home/ec2-user/aws-efs-file-sharing` on **each** EC2 instance (for example, clone your own GitHub repository containing these files). Run on each instance:

```bash
cd /home/ec2-user/aws-efs-file-sharing
sudo bash scripts/setup-ec2.sh fs-REPLACE_WITH_YOUR_EFS_ID
```

6. Verify both with `http://INSTANCE_PUBLIC_IP:8000`. Upload a small file on the first. Refresh the second: it should appear. The displayed hostnames should differ. Download on the second. If the instances do not have public IPs, use a secure connection method instead of opening the service to the internet.

### Troubleshooting

- Mount hangs: confirm EFS mount target exists in the instance's AZ, VPC routing, and TCP 2049 security group rule.
- Permission denied: `sudo chown ec2-user:ec2-user /mnt/efs/shared_files` once, then check `ls -ld /mnt/efs/shared_files`.
- Service error: `sudo journalctl -u efs-share -n 50 --no-pager`.
- Browser unavailable: confirm service active, TCP 8000 inbound from your IP, and public reachability.
- Verify EFS: `findmnt /mnt/efs`; if absent, do not start the app with an unmounted storage path.

## Architecture and viva points

`Browser → EC2 instance A / EC2 instance B → same mounted EFS → shared files`

EFS is a managed network file system; EC2 instances read the same directory through NFS. The VPC provides network connectivity. Security groups control TCP 2049 to EFS and TCP 8000 to the demo app. The app stores files under `SHARED_DIR`; on EC2 it is `/mnt/efs/shared_files`. The service will not start unless `/mnt/efs` is mounted.

## Cost and cleanup

EFS storage and EC2 can consume credits or generate charges. After your demo, terminate both EC2 instances and delete the EFS file system if you do not need the uploaded data. Delete any leftover EFS access points and check other charged resources separately. Deleting EFS permanently deletes the demo files. Check AWS Billing for actual charges.

## Scope

This is an educational demo with no authentication or antivirus scanning. It limits uploads to 20 MB and rejects duplicate sanitized filenames. Use only non-sensitive demonstration files. For a public deployment, add authentication, HTTPS, access control, scanning, and a controlled reverse proxy.
