from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

from sqlalchemy.orm import relationship


app = Flask("__name__")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', "sqlite:///todo.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




class TodoList(db.Model):
    __tablename__ = "List_todo"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)


db.create_all()


@app.context_processor
def inject_date_day():
    return {"sas": datetime.today().strftime('%A %B, %d')}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form
        print(data)
        new_list = TodoList(
            text=data["newItem"]
        )
        db.session.add(new_list)
        db.session.commit()
        to_do = TodoList.query.all()
        return render_template("index.html", newListItems=to_do)
    else:
        to_do = TodoList.query.all()
        return render_template("index.html", newListItems=to_do)


@app.route("/delete",methods=["POST"])
def delete():
    data = request.form
    ID = data["checkbox"]
    item_to_delete = TodoList.query.get(ID)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)