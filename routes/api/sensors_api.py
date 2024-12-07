from flask import Blueprint, jsonify, request
from models import Sensor, Project
from app import db
import json
sensors_api_bp = Blueprint('sensors_api', __name__, url_prefix='/api/sensors')

@sensors_api_bp.route('/', methods=['GET'])
def get_sensors():
    sensors = Sensor.query.all()
    return jsonify([{
        "id": s.id,
        "name": s.name,
        "type": s.type,
        "project_id": s.project_id,
        "extra_data": s.extra_data
    } for s in sensors])

@sensors_api_bp.route('/', methods=['POST'])
def create_sensor():
    data = request.json
    sensor = Sensor(
        name=data['name'],
        type=data['type'],
        project_id=data['project_id'],
        extra_data=data.get('extra_data', {})
    )
    db.session.add(sensor)
    db.session.commit()
    return jsonify({"id": sensor.id, "message": "Sensor created successfully!"}), 201

@sensors_api_bp.route('/<int:id>', methods=['GET'])
def get_sensor(id):
    sensor = Sensor.query.get_or_404(id)
    return jsonify({
        "id": sensor.id,
        "name": sensor.name,
        "type": sensor.type,
        "project_id": sensor.project_id,
        "extra_data": sensor.extra_data
    })

@sensors_api_bp.route('/<int:id>', methods=['PUT'])
def update_sensor(id):
    sensor = Sensor.query.get_or_404(id)
    data = request.json
    sensor.name = data.get('name', sensor.name)
    sensor.type = data.get('type', sensor.type)
    sensor.project_id = data.get('project_id', sensor.project_id)
    sensor.extra_data = data.get('extra_data', sensor.extra_data)
    if sensor.extra_data:
        try:
            # Convert extra_data string to dictionary
            sensor.extra_data = json.loads(sensor.extra_data)
        except json.JSONDecodeError as e:
            return jsonify({"error": f"Invalid JSON for extra_data: {str(e)}"}), 400
    db.session.commit()
    return jsonify({"message": "Sensor updated successfully!"})

@sensors_api_bp.route('/<int:id>', methods=['DELETE'])
def delete_sensor(id):
    sensor = Sensor.query.get_or_404(id)
    db.session.delete(sensor)
    db.session.commit()
    return jsonify({"message": "Sensor deleted successfully!"})
