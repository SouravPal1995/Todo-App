from flask import Flask, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, secrets

app=Flask(__name__)

app.config['SECRET_KEY']=secrets.token_hex()
app.config['SQLALCHEMY_DATABASE_URI']=("sqlite:///"
                                       +os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                     'database.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
migrate=Migrate(app,db)

class TasksTable(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String,nullable=False)
    description=db.Column(db.Text, nullable=False, default="Some text")
    
    def __repr__(self):
        return f'{self.id}: {self.title}'

class TaskForm(FlaskForm):
    title=StringField("Enter the title", 
                      validators=[
                          DataRequired("This field is necessary")
                      ])
    description=TextAreaField("What is your Task?: ", 
                          validators=[
                              DataRequired("This Field is necessary")
                          ])
    submit=SubmitField("Submit")
    

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    form = TaskForm()
    if form.validate_on_submit():
        title=form.title.data
        description=form.description.data
        task=TasksTable(title=title, 
                        description=description)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))
    tasks=TasksTable.query.all()
    return render_template('home.html', form=form, tasks=tasks)

@app.route('/delete/<int:index>')
def remove(index):
    query=TasksTable.query.get(index)
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for('home'))

