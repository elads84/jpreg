from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'blah blah'

db = SQLAlchemy(app)


class Participant(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    event = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    mobile_phone = db.Column(db.String(), nullable=False)
    morning_or_evening = db.Column(db.String(), nullable=False)
    guest = db.Column(db.Boolean(), nullable=False)
    partner = db.Column(db.Boolean(), nullable=False)
    invited_by = db.Column(db.String(), nullable=False)


@app.route('/')
def home():
    return render_template('reg.html')


@app.route("/thanks")
def thanks():
    return render_template("thanks.html")


@app.route('/registration/<type_of_guest>', methods=['GET', 'POST'])
def registration(type_of_guest):
    if request.method == "POST":
        print(request.form)
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone_number')
        morning_or_evening = request.form.get('morning_or_evening')
        if type_of_guest == 'guest':
            invited_by = request.form.get('invited_by')
            guest = True
            partner = False
        else:
            invited_by = 'None'
            guest = False
            partner = True

        participant = Participant(
            first_name=first_name,
            last_name=last_name,
            event='',
            mobile_phone=phone,
            morning_or_evening=morning_or_evening,
            guest=guest,
            partner=partner,
            invited_by=invited_by
        )
        db.session.add(participant)
        db.session.commit()

        return redirect(url_for("thanks"))

    return render_template('registration.html', type_of_guest=type_of_guest)


# if __name__ == '__main__':
#     app.run(debug=True)
