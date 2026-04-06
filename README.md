# 🏥 Psychological Counseling System

   This application was developed as an internship assignment to provide a
   structured platform for managing student counselling records. It enables
   administrators to delegate cases and allows Junior Psychologists (JPs) to
   track student history, psychological issues, and individual counselling sessions.
---
## 👥 User Roles & Access Control
The system implements a role-based access control (RBAC) model as specified in the project requirements:

Admin: Responsible for the initial intake and assigning students to specific Junior Psychologists (JPs).

Junior Psychologist (JP): Manages the complete lifecycle of the student's counselling, including background details, history, and session logs.

## 🚀 Key Modules

**Student Background:** Captures parent/guardian info, occupation, financial status, and sibling count.

**Clinical History:** Tracks medical records, daily habits (sleep/screen time), and JP clinical observations.

**Issue Management:** Generates unique Case IDs to track multiple specific psychological issues per student.

**Session Logging:** Hierarchically links multiple counselling sessions (with analysis and remarks) directly to their respective issues.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask
- **Database**: SQLAlchemy (SQLite)
- **Authentication**: Flask-Login
- **Security**: CSRF Protection via Flask-WTF
- **Frontend**: Custom CSS3, Jinja2 Templates, JavaScript

---
## Screenshots
<img width="1810" height="830" alt="image" src="https://github.com/user-attachments/assets/fe13556d-eb9e-45bb-9a92-72426f0a925b" />


<img width="1717" height="698" alt="image" src="https://github.com/user-attachments/assets/6d23474b-5ec3-4a60-a07c-c5186999dd62" />


<img width="1299" height="853" alt="image" src="https://github.com/user-attachments/assets/a2656974-bef9-4897-be5f-e282167bad49" />


<img width="807" height="694" alt="image" src="https://github.com/user-attachments/assets/5e5c42e6-3534-4f91-a203-610b50efa6eb" />


## 🚀 Quick Start Guide
1. Clone the repository
First, download the code from GitHub to your local machine.

Bash

  git clone https://github.com/swethanissankara-boop/Psychological-Counseling-System.git
  cd Psychological-Counseling-System

2. Create a Virtual Environment
It is a best practice to create a dedicated environment so your app's libraries don't mess with your computer's global Python settings.

Bash

#Create the virtual environment
### python -m venv venv

#Activate it (Windows)
### venv\Scripts\activate

#Activate it (Mac/Linux)
### source venv/bin/activate

3. Install Dependencies
### Install Flask, SQLAlchemy, WTForms, and all other required packages.

Bash

### pip install -r requirements.txt

4. Run the Application
Start the Flask server. Because of the way we set up app.py, this command will automatically build your psych.db database and create the necessary tables on the very first run!

Bash
 ### python app.py

5. Access the Portals
Open your web browser and navigate to:

👉 http://127.0.0.1:5000



⭐ Star this repo if you liked it and want to support the project!
