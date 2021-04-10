"""Personal, Day Modules"""
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from typing import Dict
import json
import csv
from datetime import datetime, timedelta
import pandas
from send_email import email
import subprocess


class Days(FlaskForm):
    """ Day class
    """
    # Monday
    mon_hours = FloatField(
        'hours', render_kw={"placeholder": "Hours"}, default=0)
    mon_location = StringField(
        'location', render_kw={"placeholder": "Location"})
    mon_job_description = StringField(
        'job_description', render_kw={"placeholder": "Job Description"})

    # Tuesday
    tue_hours = FloatField(
        'hours', render_kw={"placeholder": "Hours"}, default=0)
    tue_location = StringField(
        'location', render_kw={"placeholder": "Location"})
    tue_job_description = StringField(
        'job_description', render_kw={"placeholder": "Job Description"})

    # Wednesday
    wed_hours = FloatField(
        'hours', render_kw={"placeholder": "Hours"}, default=0)
    wed_location = StringField(
        'location', render_kw={"placeholder": "Location"})
    wed_job_description = StringField(
        'job_description', render_kw={"placeholder": "Job Description"})

    # Thursday
    thu_hours = FloatField(
        'hours', render_kw={"placeholder": "Hours"}, default=0)
    thu_location = StringField(
        'location', render_kw={"placeholder": "Location"})
    thu_job_description = StringField(
        'job_description', render_kw={"placeholder": "Job Description"})

    # Friday
    fri_hours = FloatField(
        'hours', render_kw={"placeholder": "Hours"}, default=0)
    fri_location = StringField(
        'location', render_kw={"placeholder": "Location"})
    fri_job_description = StringField(
        'job_description', render_kw={"placeholder": "Job Description"})

    # Saturday
    sat_hours = FloatField(
        'hours', render_kw={"placeholder": "Hours"}, default=0)
    sat_location = StringField(
        'location', render_kw={"placeholder": "Location"})
    sat_job_description = StringField(
        'job_description', render_kw={"placeholder": "Job Description"})

    # Sunday
    sun_hours = FloatField(
        'hours', render_kw={"placeholder": "Hours"}, default=0)
    sun_location = StringField(
        'location', render_kw={"placeholder": "Location"})
    sun_job_description = StringField(
        'job_description', render_kw={"placeholder": "Job Description"})

    def total_hours(self):
        """ Sum total hours in calendar
        """
        return self.mon_hours.data + self.tue_hours.data +\
            self.wed_hours.data + self.thu_hours.data + self.fri_hours.data +\
            self.sat_hours.data + self.sun_hours.data

    def json(self):
        """ JSON epresentation of day class
        """
        week = current_week()
        days = {
            "total_hours": self.total_hours(),
            "monday": {
                "day": week[0],
                "hours": self.mon_hours.data,
                "location": self.mon_location.data,
                "job_description": self.mon_job_description.data
            },
            "tuesday": {
                "day": week[1],
                "hours": self.tue_hours.data,
                "location": self.tue_location.data,
                "job_description": self.tue_job_description.data
            },
            "wednesday": {
                "day": week[2],
                "hours": self.wed_hours.data,
                "location": self.wed_location.data,
                "job_description": self.wed_job_description.data
            },
            "thursday": {
                "day": week[3],
                "hours": self.thu_hours.data,
                "location": self.thu_location.data,
                "job_description": self.thu_job_description.data
            },
            "friday": {
                "day": week[4],
                "hours": self.fri_hours.data,
                "location": self.fri_location.data,
                "job_description": self.fri_job_description.data
            },
            "saturday": {
                "day": week[5],
                "hours": self.sat_hours.data,
                "location": self.sat_location.data,
                "job_description": self.sat_job_description.data
            },
            "sunday": {
                "day": week[6],
                "hours": self.sun_hours.data,
                "location": self.sun_location.data,
                "job_description": self.sun_job_description.data
            }
        }
        return days


class Personal(FlaskForm):
    """ Personal class
    """
    name = StringField('Name', validators=[DataRequired()])
    job_title = StringField('Job Title')
    employee_email = EmailField(
        "Employee's email", validators=[DataRequired()])
    manager_email = EmailField("Manager's email", validators=[DataRequired()])

    def json(self):
        """ JSON representation of Personal class
        """
        personal = {
            "name": self.name.data,
            "job_title": self.job_title.data,
            "employee_email": self.employee_email.data,
            "manager_email": self.manager_email.data
        }
        return personal


def current_week():
    """ Current Week
    """
    day_one = datetime.today() - timedelta(
        days=datetime.today().isoweekday() % 7)

    days = []

    for i in range(1, 8):
        day = day_one + timedelta(days=i)
        days.append(str(day.date()))

    return days


def schedule(personal_info: Dict, calendar: Dict, file_name: str) -> Dict:
    """ Weekly schedule
    """
    file_name = file_name.replace(" ", "")

    schedule = {
        "personal_info": personal_info,
        "calendar": calendar
    }

    schedule_csv = [
        [
            'Week Day', 'Day', 'Hours', 'Location', 'Job Description',
            'Total Hours', 'Full Name'
        ],
        [
            'Monday',
            calendar['monday']['day'], calendar['monday']['hours'],
            calendar['monday']['location'],
            calendar['monday']['job_description'], "", ""
        ],
        [
            'Tuesday',
            calendar['tuesday']['day'], calendar['tuesday']['hours'],
            calendar['tuesday']['location'],
            calendar['tuesday']['job_description'], "", ""
        ],
        [
            'Wednesday',
            calendar['wednesday']['day'], calendar['wednesday']['hours'],
            calendar['wednesday']['location'],
            calendar['wednesday']['job_description'], "", ""
        ],
        [
            'Thursday',
            calendar['thursday']['day'], calendar['thursday']['hours'],
            calendar['thursday']['location'],
            calendar['thursday']['job_description'], "", ""
        ],
        [
            'Friday',
            calendar['friday']['day'], calendar['friday']['hours'],
            calendar['friday']['location'],
            calendar['friday']['job_description'], "", ""
        ],
        [
            'Saturday',
            calendar['saturday']['day'], calendar['saturday']['hours'],
            calendar['saturday']['location'],
            calendar['saturday']['job_description'], "", ""
        ],
        [
            'Sunday',
            calendar['sunday']['day'], calendar['sunday']['hours'],
            calendar['sunday']['location'],
            calendar['sunday']['job_description'], "", ""
        ],
        [
            "", "", "", "", "", calendar['total_hours'], personal_info['name']
        ]
    ]

    FILE = file_name + "_" + str(datetime.today()) + "_"
    with open(
       f'FILE_DB/{FILE}.csv', 'w',) as csvfile:
        writer = csv.writer(csvfile)
        for row in schedule_csv:
            writer.writerow(row)

    file = pandas.read_csv(f'FILE_DB/{FILE}.csv')
    file.to_html(f'FILE_DB/{FILE}.html', na_rep="", justify="left")

    style = """<style>
        table {
            border: 1px solid black;
        }

        tr {
            border: 1px solid black;
        }

        th {
            background-color: #FF0000;
            color: white;
        }

        th, td {
            text-align: center;
            padding: 5px;
        }
    </style>
    """

    with open(f'FILE_DB/{FILE}.html', 'a') as html_file:
        html_file.writelines(style)

    with open(
       f'FILE_DB/{FILE}.json', 'w') as json_file:
        json.dump(schedule, json_file, indent=4)

    html_file = open(f'FILE_DB/{FILE}.html')
    json_file = open(f'FILE_DB/{FILE}.json')
    csvfile = open(f'FILE_DB/{FILE}.csv')

    date = calendar['monday']['day'] + " | " + calendar['sunday']['day']
    reciever = personal_info['employee_email'] +\
        ", " + personal_info['manager_email']

    email(
        personal_info['name'], date,
        [html_file, csvfile, json_file], reciever, calendar['total_hours'])

    html_file.close()
    json_file.close()
    csvfile.close()

    subprocess.call("./FILE_DB/clear_dir.sh")

    return schedule
