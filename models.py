from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class MacroVariable(db.Model):
    __tablename__ = 'macro_variables'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    regression_results = db.relationship('RegressionResult', backref='macro_variable', lazy=True, cascade='all, delete-orphan')

class MacroMaster(db.Model):
    __tablename__ = 'macro_master'
    periode = db.Column(db.Numeric, primary_key=True)
    macro_variable_id = db.Column(db.Integer, primary_key=True)
    macro_variable_name = db.Column(db.String(255), nullable=False)
    
    # Relationship with MacroVariable
    macro_variable = db.relationship('MacroVariable', 
        foreign_keys=[macro_variable_id],
        primaryjoin="and_(MacroMaster.macro_variable_id==MacroVariable.id)"
    )
    
    # Relationship with MacroValue
    values = db.relationship('MacroValue',
        primaryjoin="and_(MacroMaster.periode==MacroValue.periode, "
                   "MacroMaster.macro_variable_id==MacroValue.macro_variable_id)",
        backref='macro_master'
    )

    def __repr__(self):
        return f'<MacroMaster {self.periode}-{self.macro_variable_name}>'

class MacroValue(db.Model):
    __tablename__ = 'macro_values'
    periode = db.Column(db.Numeric, primary_key=True)
    macro_variable_id = db.Column(db.Integer, primary_key=True)
    macro_variable_name = db.Column(db.String(255), nullable=False)
    date_regresi = db.Column(db.Numeric, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key constraint to macro_master
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['periode', 'macro_variable_id'], 
            ['macro_master.periode', 'macro_master.macro_variable_id']
        ),
    )

class RegressionResult(db.Model):
    __tablename__ = 'regression_results'
    id = db.Column(db.Integer, primary_key=True)
    macro_variable_id = db.Column(db.Integer, db.ForeignKey('macro_variables.id'))
    r2_score = db.Column(db.Float)
    mse = db.Column(db.Float)
    mae = db.Column(db.Float)
    rmse = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    coefficients = db.Column(db.JSON)

class CfgParm(db.Model):
    __tablename__ = 'cfg_parm'
    parmid = db.Column(db.String(10), primary_key=True)
    parmnm = db.Column(db.String(100), nullable=False)
    parmgrp = db.Column(db.String(10), nullable=False)

class RefPdLtTemp(db.Model):
    __tablename__ = 'REF_PD_LT_TEMP'
    
    id = db.Column(db.Integer, primary_key=True)
    periode = db.Column(db.Numeric)
    version = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    prodid = db.Column(db.String(10))
    pd_seq = db.Column(db.String(10))
    pd_pct = db.Column(db.Float)
