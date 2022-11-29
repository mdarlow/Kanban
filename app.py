from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone
import pytz


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # 3 forward slashes = relative path; 4 slashes = absolute path. Rather not specify exact location
db = SQLAlchemy(app)

class Todo(db.Model):
    date = datetime.now(tz=pytz.utc) ###################################################################################################
    date = date.astimezone(timezone('US/Pacific')) #####################################################################################
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=date) # default=datetime.utcnow not accurate. Testing to see if updated line is more accurate.



    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST': # If the request set to this route is POST, 
        task_content = request.form['content'] # New task = user input
        new_task = Todo(content=task_content) # Grab a new task from input

        try:
            db.session.add(new_task)
            db.session.commit() # Commit to database
            return redirect('/') # Redirect to index page
        except:
            return 'There was an issue adding your task'

    else: # Otherwise,
        tasks = Todo.query.order_by(Todo.date_created).all() # Go through all database content by order of creation and return all of them
        return render_template('index.html', tasks=tasks) # Just display the page.
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content'] # Set the content of the task to what is in the form's input box

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
            
    else:
        return render_template('update.html', task=task)



if __name__ == "__main__":
    app.run(debug=True)
