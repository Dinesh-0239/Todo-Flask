import os
from datetime import datetime
from flask import Flask, render_template,redirect,request
from models import db, Todo

app = Flask(__name__)

# Absolute path for SQLite DB file
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'todos.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create the database 
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    year = datetime.now().year
    return render_template('home.html',year=year)

@app.route('/add_todo', methods=['GET','POST'])
def add_todo():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_todo = Todo(title=title, description=description)
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/list_todos_pending')
    return render_template('add_todo.html')

@app.route('/list_todos_pending')
def list_todos_pending():
    todos = Todo.query.filter_by(status='pending').all()
    return render_template('pending_todo.html', todos=todos)

@app.route('/list_todos_completed')
def list_todos_completed():
    todos = Todo.query.filter_by(status='completed').all()
    return render_template('completed_todo.html', todos=todos)

@app.route('/edit_todo/<int:todo_id>',methods=["GET","POST"])
def edit_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.description = request.form['description']
        db.session.commit()
        return redirect('/list_todos_pending')
    return render_template('edit_todo.html', todo=todo)
    
@app.route('/complete_todo/<int:todo_id>',methods=["POST"])
def complete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.status = 'completed'
    db.session.commit()
    return redirect('/list_todos_completed')

@app.route('/delete_todo/<int:todo_id>',methods=["GET","POST"])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
    


if __name__ == '__main__':
    app.run(debug=True)
