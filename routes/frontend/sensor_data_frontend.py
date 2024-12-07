import requests
from flask import Blueprint, render_template, request, redirect, url_for
from models import Sensor

sensor_data_frontend_bp = Blueprint('sensor_data_frontend', __name__, url_prefix='/sensor_data')
API_URL = 'http://0.0.0.0:6969/api/sensor_data'

@sensor_data_frontend_bp.route('/', methods=['GET'])
def list_sensor_data():
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Call the API to get paginated data
    response = requests.get(f'{API_URL}?page={page}&per_page={per_page}')
    if response.status_code == 200:
        data = response.json()
        return render_template(
            'sensor_data.html',
            sensors=data['data'],
            page=data['page'],
            per_page=data['per_page'],
            total_pages=data['pages']
        )
    else:
        return render_template('error.html', message="Failed to fetch sensor data.")

@sensor_data_frontend_bp.route('/add', methods=['GET', 'POST'])
def add_sensor_data():
    sensors = Sensor.query.all()
    if request.method == 'POST':
        data = {
            "sensor_id": request.form['sensor_id'],
            "timestamp": request.form['timestamp'],
            "value": request.form['value'],
            "unit": request.form['unit'],
            "extra_data": request.form['extra_data']
        }
        requests.post(API_URL, json=data)
        return redirect(url_for('sensor_data_frontend.list_sensor_data'))
    return render_template('add_sensor_data.html', sensors=sensors)

@sensor_data_frontend_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_sensor_data(id):
    sensors = Sensor.query.all()
    data_entry = requests.get(f"{API_URL}/{id}").json()
    if request.method == 'POST':
        data = {
            "sensor_id": request.form['sensor_id'],
            "timestamp": request.form['timestamp'],
            "value": request.form['value'],
            "unit": request.form['unit'],
            "extra_data": request.form['extra_data']
        }
        requests.put(f"{API_URL}/{id}", json=data)
        return redirect(url_for('sensor_data_frontend.list_sensor_data'))
    return render_template('edit_sensor_data.html', data_entry=data_entry, sensors=sensors)

@sensor_data_frontend_bp.route('/<int:id>/delete', methods=['POST'])
def delete_sensor_data(id):
    requests.delete(f"{API_URL}/{id}")
    return redirect(url_for('sensor_data_frontend.list_sensor_data'))
