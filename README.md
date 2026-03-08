# 🚲 Sky Bicycle Rental System

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2.7-092E20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql)
![TensorFlow](https://img.shields.io/badge/TensorFlow.js-2.0-FF6F00?style=for-the-badge&logo=tensorflow)
![Razorpay](https://img.shields.io/badge/Razorpay-Payments-02042B?style=for-the-badge&logo=razorpay)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A complete, production-ready bicycle rental management system with AI-powered face verification and secure payment integration**

[Features](#✨-features) • [Demo](#🎯-live-demo) • [Installation](#📥-installation) • [Documentation](#📚-documentation) • [Contributing](#🤝-contributing)

</div>

---

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [✨ Features](#✨-features)
- [🏗️ System Architecture](#🏗️-system-architecture)
- [📥 Installation](#📥-installation)
- [⚙️ Configuration](#⚙️-configuration)
- [🚀 Usage Guide](#🚀-usage-guide)
- [👨‍💼 Admin Guide](#👨‍💼-admin-guide)
- [📚 API Documentation](#📚-api-documentation)
- [🧪 Testing](#🧪-testing)
- [📦 Deployment](#📦-deployment)
- [🛠️ Technology Stack](#🛠️-technology-stack)
- [📊 Project Structure](#📊-project-structure)
- [🤝 Contributing](#🤝-contributing)
- [📄 License](#📄-license)
- [📞 Contact](#📞-contact)

---

## 🎯 Project Overview

**Sky Bicycle Rental** is a comprehensive digital platform that revolutionizes the traditional bicycle rental business by providing an end-to-end online booking system with AI-powered identity verification, secure payments, and real-time management dashboard.

### 🎯 Vision
To create the most user-friendly, secure, and efficient bicycle rental platform that bridges the gap between traditional rental services and modern technology.

### 🎯 Mission
- ✅ Digitize the complete rental process
- ✅ Eliminate paperwork and manual verification
- ✅ Provide real-time booking management
- ✅ Ensure secure transactions
- ✅ Deliver exceptional user experience

---

## ✨ Features

### 👥 User Features

| Feature | Description | Technology |
|---------|-------------|------------|
| **5-Step Booking** | Intuitive guided booking flow | Django Sessions |
| **Face Verification** | AI-powered identity check | TensorFlow.js + BlazeFace |
| **Secure Payments** | Razorpay integration | Payment Gateway |
| **Digital Receipts** | Train ticket style PDF | Custom Generator |
| **Search Booking** | By ticket ID or mobile | Django ORM |
| **My Bookings** | Personal dashboard | Session Management |
| **24/7 Availability** | Always accessible | Cloud Hosting |

### 👨‍💼 Admin Features

| Feature | Description | Benefit |
|---------|-------------|---------|
| **Dashboard** | Real-time analytics | Data-driven decisions |
| **Booking Management** | CRUD operations | Complete control |
| **Status Updates** | Real-time status change | Quick updates |
| **Revenue Tracking** | Financial analytics | Profit monitoring |
| **Search & Filter** | Advanced booking search | Easy management |

---

## 🏗️ System Architecture
┌─────────────────────────────────────────────────────────────┐
│ CLIENT LAYER (Browser) │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ HTML5 │ │ CSS3 │ │ JS │ │TensorFlow│ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ APPLICATION LAYER (Django) │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │ │
│ │ │ Views │ │ Models │ │ Forms │ │ URLs │ │ │
│ │ └────────┘ └────────┘ └────────┘ └────────┘ │ │
│ │ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │ │
│ │ │ Utils │ │Decorator│ │Context │ │Middleware│ │ │
│ │ └────────┘ └────────┘ └────────┘ └────────┘ │ │
│ └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ DATA LAYER (MySQL) │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Bookings │ │ Settings │ │ Admin │ │
│ │ Table │ │ Table │ │ Table │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
└─────────────────────────────────────────────────────────────┘

text

---

## 📥 Installation

### Prerequisites
- Python 3.11+
- MySQL 8.0+
- Git
- Web Browser (Chrome/Firefox/Edge)

### Step-by-Step Installation

```bash
# 1. Clone Repository
git clone https://github.com/yourusername/sky-bicycle-rental.git
cd sky-bicycle-rental

# 2. Create Virtual Environment
python -m venv venv

# 3. Activate Virtual Environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install Dependencies
pip install -r requirements.txt

# 5. Create MySQL Database
mysql -u root -p < scripts/create_db.sql

# 6. Configure Environment Variables
cp .env.example .env
# Edit .env with your credentials

# 7. Run Migrations
python manage.py makemigrations
python manage.py migrate

# 8. Create Initial Settings
python manage.py shell
>>> from booking.models import SiteSettings
>>> SiteSettings.objects.create(
...     site_name="Sky Bicycle Rental",
...     contact_phone="+919876543210",
...     contact_email="ride@skybicycle.in",
...     address="Downtown Hub",
...     bikes_available=6,
...     rate_per_hour=200,
...     booking_amount=50
... )
>>> exit()

# 9. Collect Static Files
python manage.py collectstatic

# 10. Run Development Server
python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser.

⚙️ Configuration
Environment Variables (.env)
env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
SITE_URL=http://localhost:8000

# Database Configuration
DATABASE_NAME=sky_booking_db
DATABASE_USER=sky_booking_user
DATABASE_PASSWORD=Skyroot@07
DATABASE_HOST=localhost
DATABASE_PORT=3306

# Razorpay Keys (Test Mode)
RAZORPAY_KEY_ID=rzp_test_SLFHCozccwGp9N
RAZORPAY_KEY_SECRET=your-test-secret

# Admin Credentials
ADMIN_USERNAME=
ADMIN_PASSWORD=
Test Credentials
text
User Test:
- Mobile: 9876543210
- Aadhar: 1234 5678 9012

Admin:
- Username: skybikerentals
- Password: akashtakate@123

Razorpay Test Card:
- Card: 4111 1111 1111 1111
- Expiry: 12/25
- CVV: 123
- OTP: 123456
🚀 Usage Guide
User Flow
Step 1: Home Page
View rental rates and bike availability

Click "Book" to start booking

Search existing tickets

Step 2: Personal Details
text
├── Full Name (as per Aadhar)
├── Aadhar Number (auto-format)
├── Mobile Number (10 digits)
├── Age (18+ validation)
├── Hours (1-24)
├── Address
├── Location (GPS/Manual)
├── Date
└── Time
Step 3: Selfie Verification
Click "Start Camera"

Position face in frame

Auto-detection activates

Click "Capture" when ready

Step 4: Terms & Conditions
Read all policies

Accept both checkboxes

Proceed to payment

Step 5: Payment
Review booking summary

Pay ₹50 advance via Razorpay

Use test card for demo

Step 6: Receipt
View train ticket style receipt

Download as text file

Print receipt

Save ticket ID

👨‍💼 Admin Guide
Access Admin Panel
text
URL: http://127.0.0.1:8000/admin-panel/login/
Username: skybikerentals
Password: akashtakate@123
Dashboard Features
text
📊 Dashboard Overview
├── Total Bookings
├── Pending Bookings
├── Confirmed Bookings
├── Completed Bookings
├── Total Revenue
└── Today's Revenue

📋 Booking Management
├── View All Bookings
├── Filter by Status/Date
├── Search by Ticket/Mobile
├── Update Booking Status
└── Update Payment Status
Status Management
text
Booking Status Flow:
Pending → Confirmed → In Progress → Completed
                  ↘ Cancelled

Payment Status:
Pending → Completed → Refunded
       ↘ Failed
📚 API Documentation
Payment Callback
http
POST /payment-callback/
Content-Type: application/json

{
    "razorpay_payment_id": "pay_123456",
    "razorpay_order_id": "order_123456",
    "razorpay_signature": "signature_123456"
}
Response
json
{
    "status": "success",
    "booking_id": 1
}
Admin Statistics
http
GET /admin-panel/stats/
Authorization: Admin session required
🧪 Testing
Run Tests
bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test booking

# Run with coverage
coverage run manage.py test
coverage report
coverage html  # Generate HTML report
Manual Test Cases
Test Case	Steps	Expected Result
Home Page	Open URL	Page loads with all elements
Booking Form	Fill all fields	Validation passes
Face Detection	Start camera	Camera works, face detected
Payment	Use test card	Payment successful
Receipt	After payment	Receipt generated
Admin Login	Enter credentials	Login successful
Search	Enter ticket ID	Booking found
📦 Deployment
Deploy on Railway
bash
# Install Railway CLI
curl -fsSL https://railway.app/install.sh | sh

# Login
railway login

# Initialize project
railway init

# Add MySQL
railway add -p mysql

# Set environment variables
railway variables set DEBUG=False
railway variables set SECRET_KEY=your-production-key
railway variables set RAZORPAY_KEY_ID=live-key
railway variables set RAZORPAY_KEY_SECRET=live-secret

# Deploy
railway up

# Open app
railway open
Deploy on Heroku
bash
# Create Heroku app
heroku create sky-bicycle-rental

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main
heroku run python manage.py migrate
heroku open
🛠️ Technology Stack
Backend
text
├── Python 3.11          - Core programming language
├── Django 4.2.7         - Web framework
├── MySQL 8.0            - Database
├── Razorpay API         - Payment gateway
├── Gunicorn 21.2.0      - WSGI HTTP server
└── WhiteNoise 6.6.0     - Static file serving
Frontend
text
├── HTML5                - Structure
├── CSS3                 - Styling & animations
├── JavaScript (ES6)     - Client-side logic
├── TensorFlow.js 2.0    - Face detection AI
├── BlazeFace 0.0.5      - Face detection model
├── Font Awesome 6.0     - Icons
└── Razorpay SDK         - Payment integration
Development Tools
text
├── Git                  - Version control
├── Virtual Environment   - Python isolation
├── VS Code              - IDE
├── MySQL Workbench      - Database management
└── Postman              - API testing
📊 Project Structure
text
sky_bicycle_rental/
│
├── manage.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── sky_rental/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── booking/
│   ├── models.py
│   ├── views.py
│   ├── admin_views.py
│   ├── urls.py
│   ├── admin_urls.py
│   ├── forms.py
│   ├── utils.py
│   ├── decorators.py
│   ├── context_processors.py
│   └── migrations/
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   ├── face-detection.js
│   │   └── payment.js
│   └── images/
│
├── media/
│   └── selfies/
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── booking.html
│   ├── selfie.html
│   ├── terms.html
│   ├── payment.html
│   ├── receipt.html
│   ├── search_booking.html
│   ├── search_results.html
│   ├── my_bookings.html
│   └── admin/
│       ├── admin_login.html
│       ├── admin_dashboard.html
│       ├── bookings_list.html
│       └── booking_detail.html
│
└── scripts/
    └── create_db.sql
📊 Database Schema
Table: booking_booking
Column	Type	Description
id	BIGINT	Primary Key
ticket_id	VARCHAR(20)	Unique ticket ID (SKY-1234)
full_name	VARCHAR(100)	Customer name
aadhar_number	VARCHAR(20)	Aadhar with spaces
mobile	VARCHAR(10)	10-digit mobile
hours	INT	Rental hours
total_amount	INT	hours * 200
paid_amount	INT	50 (advance)
status	VARCHAR(20)	pending/confirmed/completed
created_at	DATETIME	Timestamp
🤝 Contributing
We welcome contributions! Please follow these steps:

Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add AmazingFeature')

Push to branch (git push origin feature/AmazingFeature)

Open a Pull Request

Coding Standards
Follow PEP 8 for Python code

Use meaningful variable names

Add comments for complex logic

Write unit tests for new features

Update documentation

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

text
MIT License

Copyright (c) 2026 Sky Bicycle Rental

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
📞 Contact
Project Maintainer: [Your Name]

📧 Email: your.email@example.com

💼 LinkedIn: Your LinkedIn

🐙 GitHub: Your GitHub

Project Links:

📦 Repository: https://github.com/yourusername/sky-bicycle-rental

🚀 Live Demo: https://sky-bicycle-rental.railway.app

📚 Documentation: https://github.com/yourusername/sky-bicycle-rental/wiki

🌟 Support
If you like this project, please give it a ⭐ on GitHub!

🏆 Project Status
Area	Status
Development	✅ Complete
Testing	✅ Complete
Documentation	✅ Complete
Deployment	✅ Ready
