from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(300),nullable=True)
    status = db.Column(db.Enum('pending','completed',name='status_enum'),default='pending',nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.now)

    def __repr__(self):
        return f"<Todo {self.title} - {self.status}>"