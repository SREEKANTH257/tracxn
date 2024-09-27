 **Simple Flask App**
To signup as a user, sending verify the email using AWS SES, after verfying profile gets activated.

Project file structure:
tracxn/                                 # root folder
├── instance/                           # folder gets created while DB create
│     ├── users.db                      # User's database
├── myenv/                              # python -m venv myenv(this command creates the virtual env)
├── templates/                          # UI templates
│     ├── signup.html                   # User's signup page(basic UI)
├── app.py                              # Main file
├── requirements.txt                    # Python dependencies
└── README.md

Installation:
Python
SQLite
python3 -m venv yourenv
yourenv\Scripts\activate
pip install -r requirements.txt
Amazon Simple Email 
