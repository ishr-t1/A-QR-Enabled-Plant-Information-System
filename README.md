Botanical Garden Information System

Live Demo: https://ishratjahan.pythonanywhere.com
Developer: Ishrat Jahan

A web-based Botanical Information System built using Django, featuring plant records, QR code generation, reporting issues, and a clean admin interface powered by Jazzmin.

🚀 Features
🪴 Plant Management

Add, edit, delete plant entries
Rich text descriptions using TinyMCE
Upload multiple images
Display plant details publicly (frontend)

🔍 Search Functionality
Search plants by name, family, local names
Fast search results page

🔗 QR Code Integration
Automatic QR code generation for each plant
Inline QR preview in admin
QR code links directly to public plant detail page

⚠️ Issue Reporting
Users can report issues for a plant
Admin can review & update status (Pending, Reviewed, Resolved)

🛠 Modern Admin Panel (Jazzmin)
Clean, responsive dashboard
Colored badges (status, QR)
Admin filters, search, custom display fields

📁 Project Structure
botanical_system/
│
├── botanical_system/       # Core project settings
├── plants/                 # Main Django app
├── templates/              # HTML templates (public pages)
├── static/                 # Custom static files
├── media/                  # Uploaded plant images & QR codes
├── requirements.txt
└── manage.py

🔧 Installation Guide (Local Setup)
1️⃣ Clone the Repository
git clone https://github.com/your-username/botanical_system.git
cd botanical_system
2️⃣ Create & Activate Virtual Environment
python -m venv venv
venv\Scripts\activate     # Windows
# OR
source venv/bin/activate  # Mac/Linux
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Create .env File
Copy .env.example → .env:
cp .env.example .env

Fill real SECRET_KEY + other values.
5️⃣ Run Migrations
python manage.py migrate
6️⃣ Create Superuser
python manage.py createsuperuser
7️⃣ Start Server
python manage.py runserver
Visit:
🔗 http://127.0.0.1:8000

🌐 Production Deployment

The project is deployed on PythonAnywhere:
🔗 https://ishratjahan.pythonanywhere.com
Deployed using:
WSGI configuration
Collected static files
Environment variables stored securely in PythonAnywhere dashboard

📄 License
This project is created for academic purposes by Ishrat Jahan.
All rights reserved.
