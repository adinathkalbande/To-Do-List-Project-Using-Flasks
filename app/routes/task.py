# from flask import Flask, Blueprint, redirect, render_template, request,flash, session, url_for
# from app import db
# from app.models import Tasks

# tasks_bp = Blueprint("tasks", __name__)

# @tasks_bp.route("/")
# def view_tasks():
#     if 'user' not in session:
#         return redirect(url_for('auth.login'))

#     tasks = Tasks.query.all()
#     return render_template('tasks.html', tasks=tasks)

# @tasks_bp.route('/add', methods=["POST"])
# def add_task():
#     if 'user' not in session:
#         return redirect(url_for('auth.login'))
    
#     title = request.form.get('title')
#     if title:
#         new_task = Tasks(title=title, status="pending")
#         db.session.add(new_task)
#         db.session.commit()
#         flash("Task added Successfully", 'success')

#     return redirect(url_for('tasks.view_tasks'))


# @tasks_bp.route("/toggle/<int:task_id>", methods=["POST"])
# def toggle_status(task_id):

#     print("TOGGLE HIT", task_id)

#     task = Tasks.query.get_or_404(task_id)

#     if task.status == "Pending":
#         task.status = "Working"

#     elif task.status == "Working":
#         task.status = "Done"

#     else:
#         task.status = "Pending"

#     db.session.commit()

#     return redirect(url_for("tasks.view_tasks"))


# @tasks_bp.route('/cleared', methods=["POST"])
# def clear_tasks():
#     Tasks.query.delete()
#     db.session.commit()
#     flash("All Task Cleared", "info")
#     return redirect(url_for('tasks.view_tasks'))


# @tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
# def delete_task(task_id):

#     task = Tasks.query.get_or_404(task_id)

#     db.session.delete(task)
#     db.session.commit()

#     return redirect(url_for("tasks.view_tasks"))





from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from app import db
from app.models import Tasks

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/")
def view_tasks():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    tasks = Tasks.query.filter_by(user_id=session['user_id']).all()

    return render_template('tasks.html', tasks=tasks)


@tasks_bp.route('/add', methods=["POST"])
def add_task():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get('title')

    if title:
        new_task = Tasks(
            title=title,
            status="Pending",
            user_id=session['user_id']
        )

        db.session.add(new_task)
        db.session.commit()

        flash("Task added Successfully", 'success')

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_status(task_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    task = Tasks.query.filter_by(
        id=task_id,
        user_id=session['user_id']
    ).first_or_404()

    if task.status == "Pending":
        task.status = "Working"

    elif task.status == "Working":
        task.status = "Done"

    else:
        task.status = "Pending"

    db.session.commit()

    return redirect(url_for("tasks.view_tasks"))

@tasks_bp.route('/cleared', methods=["POST"])
def clear_tasks():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    Tasks.query.filter_by(user_id=session['user_id']).delete()

    db.session.commit()

    flash("All Task Cleared", "info")

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    task = Tasks.query.filter_by(
        id=task_id,
        user_id=session['user_id']
    ).first_or_404()

    db.session.delete(task)
    db.session.commit()

    flash("Task Deleted", "danger")

    return redirect(url_for("tasks.view_tasks"))

