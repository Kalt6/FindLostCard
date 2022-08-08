import base64
from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug.utils import secure_filename

import uuid
import os

app = Flask(__name__)
app.secret_key = '[{(!@#$%^&*_+)}]'
DB_NAME = 'database'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String, nullable=False)
    telephone = db.Column(db.Unicode, nullable=False)
    filename = db.Column(db.String(100))
    file = db.Column(db.LargeBinary)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        student_id = request.form['student_id']
        username = request.form['username']
        telephone = request.form['telephone']
        photo = request.files['photo']

        save_data = Data(student_id=student_id, username=username, telephone=telephone,
                         filename=str(uuid.uuid1()) + '_' + secure_filename(photo.filename), file=photo.read())

        db.session.add(save_data)
        db.session.commit()
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    q = request.args.get('q')
    detail_display = Data.query.filter_by(student_id=q).first_or_404(description='ID {} is not yet uploaded'.format(q))

    if detail_display:
        image = base64.b64encode(detail_display.file).decode('ascii')
        return render_template('index.html', detail_display=detail_display, data=list, image=image, q=q)


if __name__ == '__main__':
    if not os.path.exists('Basics/' + DB_NAME):
        db.create_all()
    app.run(debug=True)
    # serve(app, listen="localhost:8080")



