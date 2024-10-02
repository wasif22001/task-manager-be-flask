
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost:3306/task_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()


@app.route('/health')
def health():
    return 'App is up and running!'

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add',methods=['POST'])
def add_task():
    task_content = request.form['content']
    new_task = Task(content=task_content)

    db.session.add(new_task)
    db.session.commit()

    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET','POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    print (request)
    print(request.method)

    if request.method=='POST':
        task.content = request.form['content']
        db.session.commit()
        return redirect('/')

    print(request.method)

    return render_template('edit.html',task=task)

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task=Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True, port=8080)
