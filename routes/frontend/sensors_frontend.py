import requests
from flask import Blueprint, render_template, request, redirect, url_for
from models import Project

sensors_frontend_bp = Blueprint('sensors_frontend', __name__, url_prefix='/sensors')
API_URL = 'http://0.0.0.0:6969/api/sensors'

@sensors_frontend_bp.route('/', methods=['GET'])
def list_sensors():
    response = requests.get(API_URL)
    sensors = response.json()
    return render_template('sensors.html', sensors=sensors)

@sensors_frontend_bp.route('/add', methods=['GET', 'POST'])
def add_sensor():
    projects = Project.query.all()
    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "type": request.form['type'],
            "project_id": request.form['project_id'],
            "extra_data": request.form['extra_data']
        }
        requests.post(API_URL, json=data)
        return redirect(url_for('sensors_frontend.list_sensors'))
    return render_template('add_sensor.html', projects=projects)

@sensors_frontend_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_sensor(id):
    projects = Project.query.all()
    sensor = requests.get(f"{API_URL}/{id}").json()
    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "type": request.form['type'],
            "project_id": request.form['project_id'],
            "extra_data": request.form['extra_data']
        }
        requests.put(f"{API_URL}/{id}", json=data)
        return redirect(url_for('sensors_frontend.list_sensors'))
    return render_template('edit_sensor.html', sensor=sensor, projects=projects)

@sensors_frontend_bp.route('/<int:id>/delete', methods=['POST'])
def delete_sensor(id):
    requests.delete(f"{API_URL}/{id}")
    return redirect(url_for('sensors_frontend.list_sensors'))
