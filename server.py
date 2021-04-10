from flask import Flask, render_template, request, jsonify, redirect, flash
"""FLask App Module SERVER"""
from models import Personal, Days, schedule, current_week
from typing import Dict
import json


app = Flask(__name__)
app.config["SECRET_KEY"] = '12345gberwdf4356754refsw'


@app.route('/', strict_slashes=False, methods=['GET', 'POST'])
def contime_lite():
    """Home page of ConTimeLite"""
    form = Personal()
    days = Days()

    if request.method == "POST":
        if form.validate() and days.validate():
            SCHEDULE = schedule(
                form.json(),
                days.json(),
                form.json()['name']
            )
            flash("Schedule sent successfully :)", category='flash-success')
            return redirect('/')
        flash("Something went wrong :(", category='flash-error')
        return redirect('/')

    return render_template(
        'app.html', form=form, days=days, week=current_week()), 200


if __name__ == '__main__':
    app.run()
