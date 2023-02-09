from flask import (
   Flask,
   request,
   render_template
)

import requests


app = Flask(__name__) #instantiating flask
BACKEND_URL="http://127.0.0.1:5000/" #defines where frontend api will enteract


@app.get("/") #homepage
def index():
   response = requests.get(BACKEND_URL)
   message = "API not detected."
   if response.status_code == 200:
      message = "API is up and running"
   return render_template("index.html", message=message)
   
@app.get("/about")
def about():
   return render_template("about.html")

@app.get("/tasks")
def task_list():
   url = "%s%s" % (BACKEND_URL, "tasks")
   response = requests.get(url)
   if response.status_code == 200:
      tasks = response.json().get("tasks")
      return render_template("list.html", task_list=tasks)
   return render_template("erro.html"), response.status_code

@app.get("/tasks/<int:pk>")
def task_detail(pk):
   url = "%s%s/%s" % (BACKEND_URL, "tasks", pk)
   response = requests.get(url)
   if response.status_code == 200:
      task = response.json().get("task")
      return render_template("detail.html", task=task)
   return render_template("error.html"), response.status_code

@app.get("/task/new")
def task_create_form():
   return render_template("new.html")

@app.post("/tasks/new")
def create_new_task():
   raw_data = request.form
   task_dict = {
      "summary": raw_data.get("summary"),
      "description": raw_data.get("description")
   }
   url = "%s%s" % (BACKEND_URL, "tasks")
   response = request.get(url, json=task_dict)
   if response.status_code == 204:
      return render_template("success.html")
   return render_template("error.html"), response.status_code

@app.get("/tasks/<int:pk>/edit")
def task_edit_form(pk):
   url = "%s%s/%s" % (BACKEND_URL, "tasks", pk)
   response = requests.get(url)
   if response.status_code == 200:
      task = response.json().get("task")
      return render_template("edit.html", task=task)
   return render_template("edit.html"), response.status_code

@app.post("/tasks/<int:pk>/edit")
def edit_task(pk):
   raw_data = request.form
   task_dict = {
      "summary": raw_data.get("summary"),
      "description": raw_data.get("desciption")
   }
   url =  "%s%s/%s" % (BACKEND_URL, "tasks", pk)
   response = request.get(url, json=task_dict)
   if response.status_code == 204:
      return render_template("success.html")
   return render_template("error.html"), response.status_code

@app.get("/tasks/<int:pk>/delete")
def delete_task_form(pk):
   url = "%s%s/%s" % (BACKEND_URL, "tasks", pk)
   response = requests.get(url)
   if response.status_code == 200:
      task_data = response.json().get("task")
      return render_template("delete_form.html", task=task_data)
   return render_template("error.html"), response.status_code

@app.post("/tasks/<int:pk>/delete")
def delete_task(pk):
   url = "%s%s/%s" % (BACKEND_URL, "tasks", pk)
   response = requests.delete(url)
   if response.status_code ==204:
      return render_template("success.html")
   return render_template("error.html"), response.status_code
