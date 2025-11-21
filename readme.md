## StudyBuddy

**StudyBuddy** is a collaborative learning platform built with **Django**.  
It lets users create topic-based rooms, join discussions, and connect with others in an interactive way.  

------------------------------------------------------------------------

## ✨ Features

- 🔐 **User Accounts**
  - Secure login & registration
  - Add or update a profile image in settings

- 🏠 **Rooms**
  - Create rooms on educational topics
  - Join existing rooms to debate and share knowledge
  - Hosts can edit or delete their rooms
  - View all rooms created by a host via their profile

- 📰 **Home Page**
  - Recent Activity feed shows ongoing discussions and debates

- 🚫 **Access Control**
  - Non-logged-in users are redirected to login/registration if they try to create rooms

- 🗄️ **Database**
  - Powered by SQLite (Django’s default database)

-------------------------------------------------------------------------------

## ⚙️ Installation & Setup

 **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/studybuddy.git
   cd studybuddy

---- Create a virtual environment

python -m venv venv
source venv/bin/activate   

---- Install dependencies

pip install -r requirements.txt

---- Run migrations

python manage.py migrate

---- Start the server

python manage.py runserver

--- Open your browser at 👉 http://127.0.0.1:8000/

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript (Dennis Ivy’s theme)
- **Backend:** Django, Django REST Framework
- **Packages:** django-cors-headers, Pillow
- **Database:** SQLite
- **Environment:** Local development with venv

🔌 API
- Built with Django REST Framework
- CORS handled via django-cors-headers

🤝 Contributing
Contributions are welcome!
Please open an issue before submitting major changes.


