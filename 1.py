from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на секретный ключ для безопасности

# Настройки базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    priority = db.Column(db.String(10), nullable=False, default='Low')
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        task = Task(title=title, description=description, priority=priority, due_date=due_date)
        db.session.add(task)
        db.session.commit()
        flash('Задача добавлена успешно!', 'success')
        return redirect('/')
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/complete/<int:id>')
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.completed = True
    db.session.commit()
    flash('Задача выполнена!', 'success')
    return redirect('/')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
