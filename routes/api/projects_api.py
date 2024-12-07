from flask import Blueprint, jsonify, request
from models import Project
from app import db

projects_api_bp = Blueprint('projects_api', __name__, url_prefix='/api/projects/')

@projects_api_bp.route('/', methods=['GET'])
def get_projects():
    """
    Get all projects
    ---
    tags:
      - Projects
    summary: Retrieve all projects
    description: Retrieve a list of all projects in the system with their IDs, names, and descriptions.
    responses:
      200:
        description: A list of projects
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: The unique ID of the project
                    example: 1
                  name:
                    type: string
                    description: The name of the project
                    example: "Network Monitoring"
                  description:
                    type: string
                    description: A brief description of the project
                    example: "Monitors network activity and logs statistics"
    """
    projects = Project.query.all()
    return jsonify([{"id": p.id, "name": p.name, "description": p.description} for p in projects])

@projects_api_bp.route('/', methods=['POST'])
def create_project():
    data = request.json
    project = Project(name=data['name'], description=data.get('description'))
    db.session.add(project)
    db.session.commit()
    return jsonify({"id": project.id, "message": "Project created successfully!"}), 201

@projects_api_bp.route('/<int:id>', methods=['GET'])
def get_project(id):
    project = Project.query.get_or_404(id)
    return jsonify({"id": project.id, "name": project.name, "description": project.description})

@projects_api_bp.route('/<int:id>', methods=['PUT'])
def update_project(id):
    project = Project.query.get_or_404(id)
    data = request.json
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)
    db.session.commit()
    return jsonify({"message": "Project updated successfully!"})

@projects_api_bp.route('/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted successfully!"})
