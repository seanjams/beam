import enum
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Integer, DateTime, Enum, JSON
from sqlalchemy.sql import func

db = SQLAlchemy()

class JobStatus(enum.Enum):
    error = 0
    success = 1

class JobRun(db.Model):
    __tablename__ = "job_runs"

    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    name = Column(String, nullable=False)
    status = Column(Enum(JobStatus), nullable=False)
    data = Column(JSON)

    def json(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "name": self.name,
            "status": self.status.name,
        }
    
    def save(self):
        with app.app_context():
            db.session.add(self)
            db.session.commit()
