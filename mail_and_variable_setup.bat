set FLASK_APP=microblog.py
set FLASK_DEBUG=1

flask db init
flask db migrate -m "initial migration pt"
flask db upgrade

set MAIL_SERVER=smtp.googlemail.com
set MAIL_PORT=587

set MAIL_USE_TLS=1
set MAIL_USERNAME=sunykorea.cbbat@gmail.com
set MAIL_PASSWORD=O9br59Rauu0R

pause