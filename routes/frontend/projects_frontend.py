from flask import Blueprint, render_template, request, redirect, url_for
from models import Project
from app import db
from models import Project, Sensor
import json

projects_frontend_bp = Blueprint('projects_frontend', __name__, url_prefix='/projects')

@projects_frontend_bp.route('/', methods=['GET'])
def list_projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@projects_frontend_bp.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        project = Project(name=name, description=description)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projects_frontend.list_projects'))
    return render_template('add_project.html')

@projects_frontend_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form['description']
        db.session.commit()
        return redirect(url_for('projects_frontend.list_projects'))
    return render_template('edit_project.html', project=project)

@projects_frontend_bp.route('/<int:id>/delete', methods=['POST'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('projects_frontend.list_projects'))

@projects_frontend_bp.route('/<int:project_id>/map', methods=['GET'])
def project_map(project_id):
    # Fetch the project by ID
    project = Project.query.get_or_404(project_id)
    
    
    # Fetch sensors for the project
    sensors = Sensor.query.filter_by(project_id=project_id).all()
    
    # Extract coordinates from sensors
    sensor_locations = []
    
    for sensor in sensors:
        extra_data = sensor.extra_data or {}
        lat = extra_data.get('latitude') or extra_data.get('lat') or extra_data.get('lan') or extra_data.get('Latitude')
        lon = extra_data.get('longitude') or extra_data.get('lon') or extra_data.get('log') or extra_data.get('Longitude')
        if lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
                sensor_locations.append({
                    'name': sensor.name,
                    'latitude': lat,
                    'longitude': lon
                })
            except ValueError:
                pass

    return render_template('project_map.html', project=project, sensors=sensor_locations)
