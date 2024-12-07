from app import db

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    extra_data = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    project = db.relationship('Project', backref=db.backref('sensors', lazy=True))

class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=True)
    extra_data = db.Column(db.JSON, nullable=True)

    sensor = db.relationship('Sensor', backref=db.backref('data', lazy=True))
