emailread
=========

Fetch your emails from gmail's "UNSEEN" box and read them off the admin!

Setup:
Add environmental variables 'EMAIL_ACCOUNT' and 'EMAIL_PASSWORD', 
e.g. deploying to heroku 
$ heroku config.set EMAIL_ACCOUNT=your_gmail_account
$ heroku config.set EMAIL_PASSWORD=your_gmail_password

Run:
python manage.py get_email

You can run 'python manage.py get_email' in a fab.py file and have it pull
emails whenever you want!
