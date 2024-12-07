from flask import Blueprint, jsonify, request
from models import SensorData
from app import db
import json
sensor_data_api_bp = Blueprint('sensor_data_api', __name__, url_prefix='/api/sensor_data')

@sensor_data_api_bp.route('/', methods=['GET'])
def get_sensor_data():
     # Get query parameters
    page = request.args.get('page', 1, type=int)  # Default to page 1
    per_page = request.args.get('per_page', 10, type=int)  # Default to 10 items per page

    # Query the database for sensor data with pagination
    sensor_data_paginated = SensorData.query.paginate(page=page, per_page=per_page, error_out=False)

    # Format the paginated response
    data = [{
        "id": d.id,
        "sensor_id": d.sensor_id,
        "timestamp": d.timestamp,
        "value": d.value,
        "unit": d.unit,
        "extra_data": d.extra_data
    } for d in sensor_data_paginated.items]

    return jsonify({
        "data": data,
        "page": sensor_data_paginated.page,
        "per_page": sensor_data_paginated.per_page,
        "total": sensor_data_paginated.total,
        "pages": sensor_data_paginated.pages
    })

@sensor_data_api_bp.route('/', methods=['POST'])
def create_sensor_data():
    data = request.json
    sensor_data = SensorData(
        sensor_id=data['sensor_id'],
        timestamp=data['timestamp'],
        value=data['value'],
        unit=data.get('unit'),
        extra_data=data.get('extra_data', {})
    )
    db.session.add(sensor_data)
    db.session.commit()
    return jsonify({"id": sensor_data.id, "message": "Sensor data created successfully!"}), 201

@sensor_data_api_bp.route('/<int:id>', methods=['GET'])
def get_single_sensor_data(id):
    data = SensorData.query.get_or_404(id)
    return jsonify({
        "id": data.id,
        "sensor_id": data.sensor_id,
        "timestamp": data.timestamp,
        "value": data.value,
        "unit": data.unit,
        "extra_data": data.extra_data
    })

@sensor_data_api_bp.route('/<int:id>', methods=['PUT'])
def update_sensor_data(id):
    data_entry = SensorData.query.get_or_404(id)
    data = request.json
    data_entry.sensor_id = data.get('sensor_id', data_entry.sensor_id)
    data_entry.timestamp = data.get('timestamp', data_entry.timestamp)
    data_entry.value = data.get('value', data_entry.value)
    data_entry.unit = data.get('unit', data_entry.unit)
    data_entry.extra_data = data.get('extra_data', data_entry.extra_data)
    if data_entry.extra_data:
        try:
            # Convert extra_data string to dictionary
            data_entry.extra_data = json.loads(data_entry.extra_data)
        except json.JSONDecodeError as e:
             return jsonify({"error": f"Invalid JSON for extra_data: {str(e)}"}), 400
    db.session.commit()
    return jsonify({"message": "Sensor data updated successfully!"})

@sensor_data_api_bp.route('/<int:id>', methods=['DELETE'])
def delete_sensor_data(id):
    data_entry = SensorData.query.get_or_404(id)
    db.session.delete(data_entry)
    db.session.commit()
    return jsonify({"message": "Sensor data deleted successfully!"})
