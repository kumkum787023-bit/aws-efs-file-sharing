# ☁️ AWS EFS File Sharing System

A cloud-based file-sharing application built using **Python Flask, Amazon EC2, and Amazon Elastic File System (EFS)**.

This project demonstrates how multiple EC2 instances can access the same shared file storage using Amazon EFS. A user can upload a file through the web interface on one instance and access that file from another instance connected to the same EFS file system.

## 📌 Project Overview

Traditional storage on a single server can make sharing files across multiple servers difficult. Amazon EFS provides shared network storage that multiple EC2 instances can access.

This project combines a simple Flask web application with AWS infrastructure to demonstrate shared file storage.

## ✨ Features

* 📤 Upload files through a web interface.
* 📥 Download shared files.
* ☁️ Store files in a shared Amazon EFS directory when deployed on AWS.
* 🖥️ Access shared files from multiple EC2 instances.
* 🔄 Demonstrate file sharing across instances.
* 🎨 Simple web interface built with HTML and CSS.
* 🧪 Run locally for development and demonstration.

## 🛠️ Technologies Used

| Technology | Purpose                     |
| ---------- | --------------------------- |
| Python     | Application programming     |
| Flask      | Web framework               |
| HTML       | Web page structure          |
| CSS        | Web page styling            |
| Amazon EC2 | Virtual servers             |
| Amazon EFS | Shared network file storage |
| Amazon VPC | Network infrastructure      |
| Git        | Version control             |
| GitHub     | Source code hosting         |

## 🏗️ Architecture

```text
                 User's Web Browser
                         |
                  Python Flask App
                    /          \
                   /            \
             EC2 Instance A   EC2 Instance B
                   \            /
                    \          /
                   Amazon EFS
                 Shared Storage
```

Both EC2 instances mount the same EFS file system. Files saved to the shared directory can then be accessed by either instance.

## 📂 Project Structure

```text
aws-efs-file-sharing/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── scripts/
│   └── setup-ec2.sh
│
├── static/
│   └── style.css
│
└── templates/
    └── index.html
```

The `shared_files/` directory is used for local file storage and is excluded from Git tracking.

## 💻 Run Locally

### Prerequisites

* Python 3
* Git
* Visual Studio Code (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/kumkum787023-bit/aws-efs-file-sharing.git
```

### 2. Open the project directory

```bash
cd aws-efs-file-sharing
```

### 3. Create a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
```

### 4. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```powershell
pip install -r requirements.txt
```

### 6. Start the application

```powershell
python app.py
```

Open the local address configured by the application in your browser. For the current project configuration, this is:

```text
http://127.0.0.1:8000
```

**Note:** Local mode demonstrates the application interface and stores files locally. It does not automatically connect to Amazon EFS.

## ☁️ AWS Deployment Overview

To demonstrate actual shared storage on AWS:

1. Create a VPC and appropriate networking configuration.
2. Create an Amazon EFS file system.
3. Configure EFS mount targets in the required Availability Zones.
4. Configure security groups to permit NFS traffic on TCP port 2049 from the EC2 security group.
5. Launch two EC2 instances with the required permissions and network access.
6. Mount the same EFS file system on both instances.
7. Configure the Flask application to use the EFS-mounted directory.
8. Start the application on each instance.
9. Upload a test file through one instance and verify that it is accessible through the other.

The EC2 instances must be configured correctly, and EFS must be mounted successfully for this demonstration to work.

## 🧪 Testing

The following tests can be performed:

* Open the application in a browser.
* Upload a sample file.
* Download the uploaded file.
* Verify that both EC2 instances access the same EFS-backed directory.
* Confirm that a file uploaded through one instance appears when accessing the other instance.

## 🔐 Security Considerations

* Never upload AWS private keys, passwords, access keys, or other secrets to GitHub.
* Keep private key files excluded using `.gitignore`.
* Restrict SSH access to trusted IP addresses.
* Restrict EFS access to authorized EC2 security groups.
* Use HTTPS and authentication before making the application available to the public.
* Use non-sensitive files for demonstrations.

## 💰 Cost Management

Amazon EC2 and Amazon EFS may incur charges.

After testing:

* Stop or terminate EC2 instances that are no longer required.
* Delete EFS resources that are no longer needed.
* Check for leftover resources that may incur charges.
* Review AWS Billing and Cost Management.

Deleting an EFS file system permanently removes its stored data. Back up anything important before deletion.

## 🎓 Learning Outcomes

This project demonstrates:

* Cloud storage using Amazon EFS.
* Virtual server deployment using Amazon EC2.
* Shared file access across multiple servers.
* Basic cloud networking and security groups.
* Flask application development.
* Git and GitHub version control.

## 👨‍💻 Author

**Kumkum Kumari**

GitHub: [kumkum787023-bit](https://github.com/kumkum787023-bit)

## 📄 Disclaimer

This project is intended for educational and demonstration purposes. The application should be reviewed and secured before production use.
