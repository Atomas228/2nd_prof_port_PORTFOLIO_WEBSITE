from flask import Flask, render_template, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import smtplib
import os

OWN_EMAIL = 'MY_OWN_ENCRYPTED_EMAIL'
OWN_PASSWORD = 'MY_OWN_ENCRYPTED_PASSWORD'

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.secret_key = "secret"
basedir = os.path.abspath(os.path.dirname(__file__))

#place where db is stored
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'instance', 'about-me.db')
# initialize the app with the extension
db.init_app(app)

#text class where long texts are stored
class Text(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    context: Mapped[str] = mapped_column(unique=True)
    text: Mapped[str]

with app.app_context():
    db.create_all()

#main page
@app.route('/', methods = ['GET', 'POST'])
def main():
    text1 = db.session.execute(db.select(Text).filter_by(context = "main-page-intro")).scalar()
    text2 = db.session.execute(db.select(Text).filter_by(context = "main-page-more")).scalar()
    return render_template("index.html", text1 = text1, text2 = text2)

#about me page
@app.route('/about', methods=['GET', 'POST'])
def about_me():
    text1 = db.session.execute(db.select(Text).filter_by(context = "University")).scalar()
    text2 = db.session.execute(db.select(Text).filter_by(context = "Football")).scalar()
    text3 = db.session.execute(db.select(Text).filter_by(context = "Guitar")).scalar()
    return render_template("about.html", text1 = text1, text2 = text2, text3 = text3)

#album with stored photos
@app.route('/album', methods=['GET', 'POST'])
def album():
    return render_template("album.html", images=os.listdir("PORTFOLIO_WEBSITE/static/assets/photos"))


#contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        data = request.form
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

#send emails from my created new email to myself if 
def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nFrom: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)

#check the cv added
@app.route('/download')
def download():
    return send_from_directory('static', path="files/NEW_CV.pdf")

if __name__ == "__main__":
    app.run(debug=True)