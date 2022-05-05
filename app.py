from crypt import methods
import flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from requests import request
import requests

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if flask.request.method == 'POST':
        task_content = flask.request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return flask.redirect('/')
        except:
            return "There was an issue adding your task."

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return flask.render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return flask.redirect('/')
    except:
        return 'There was a problem deleting that task.'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if flask.request.method == 'POST':
        task.content = flask.request.form['content']

        try:
            db.session.commit()
            return flask.redirect('/')
        except:
            return 'There was an issue updating your task.'
    else:
        return flask.render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)
