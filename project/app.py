from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from tasks.celery_conf import make_celery
from utils.email import send_email

from datetime import datetime, timedelta
from models.models import Book, User
from settings.db_config import db

from celery.schedules import crontab


app = Flask(__name__)

app.config.from_object('settings.config.DevelopmentConfig')

db.init_app(app)
app.app_context().push()
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


app.config.update(CELERY_CONFIG={
    'broker_url': 'redis://localhost:6379',
    'result_backend': 'redis://localhost:6379',
})


celery = make_celery(app)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Executes every one hour interval
    sender.add_periodic_task(
        timedelta(seconds=10),
        #crontab(minute=10, hour=14),
        check_return_date.s(),
    )

    sender.add_periodic_task(
        timedelta(seconds=10),
        #crontab(minute=10, hour=14),
        check_user_login.s(),
    )


@celery.task()
def check_return_date():


    cmp = str(datetime.today().date())
    cmp_date = datetime.strptime(cmp, '%Y-%m-%d')


    books = Book.query.all()
    for book in books:
        
        if book.return_date:
            if book.return_date < cmp_date:
                book.user_id = None
                book.return_date = None

                # Committing to database
                db.session.add(book)
                db.session.commit()

    return True


@celery.task()
def check_user_login():

    subject = 'login'
    message = 'You havent visited our website today'
    
    users = User.query.all()
    today = datetime.today().date()

    for user in users:
        last_seen = datetime.strptime(str(user.last_seen), '%Y-%m-%d').date()
        date_difference = last_seen - today

        if user.role == 'admin': continue

        if date_difference.days < 0:

            try:
                send_email(user.email, subject, message)
            except Exception as e:
                print(e)

    return True


CORS(app)


from controllers.authController import auth
from controllers.bookController import book_bp
from controllers.sectionController import section_bp
from controllers.searchController import search_bp
from controllers.librarianController import librarian_bp


app.register_blueprint(search_bp, url_prefix="/api/search")
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(book_bp, url_prefix="/api/books")
app.register_blueprint(section_bp, url_prefix="/api/sections")
app.register_blueprint(librarian_bp, url_prefix='/api/admin')

if __name__ == "main":
    app.run()