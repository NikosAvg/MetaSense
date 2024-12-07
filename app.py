from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0')

db = SQLAlchemy(app)

# Swagger
swagger = Swagger(app, template={
    "info": {
        "title": "Sensorium API",
        "description": "An API to manage sensors and projects.",
        "version": "1.0.0"
    }
})

# Import blueprints
from routes.api.projects_api import projects_api_bp
from routes.api.sensors_api import sensors_api_bp
from routes.api.sensor_data_api import sensor_data_api_bp
from routes.frontend.projects_frontend import projects_frontend_bp
from routes.frontend.sensors_frontend import sensors_frontend_bp
from routes.frontend.sensor_data_frontend import sensor_data_frontend_bp

# Register API routes
app.register_blueprint(projects_api_bp)
app.register_blueprint(sensors_api_bp)
app.register_blueprint(sensor_data_api_bp)

# Register frontend routes
app.register_blueprint(projects_frontend_bp)
app.register_blueprint(sensors_frontend_bp)
app.register_blueprint(sensor_data_frontend_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
