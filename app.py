from itertools import takewhile
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self) -> str:
        return "task.{}".format(self.id)
@app.route("/",methods=['GET','POST'])
def index():
    if request.method=='POST':
        content=request.form['content']
        new_task=Todo()
        new_task.content=content
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There is an issue on the code"
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html",tasks=tasks)
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete= Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There is some issue in delete logic"

@app.route("/update/<int:id>",methods=['GET','POST'])
def update(id):
    task_to_update=Todo.query.get_or_404(id)
    if request.method=='POST':
        task_to_update.content=request.form['content']
        db.session.commit()
        return redirect("/")
    else:
        return render_template('update.html',task=task_to_update)
    
if __name__=="__main__":
    app.run(debug=True)