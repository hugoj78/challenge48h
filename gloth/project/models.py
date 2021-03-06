from flask_sqlalchemy import SQLAlchemy
from .views import app

db = SQLAlchemy(app)

class Pathology(db.Model):
    __tablename__ = "pathology"
    __bind_key__ = "pathology"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    info = db.Column(db.String(), nullable=False)
    has = db.Column(db.String(), nullable=True)
    age_min = db.Column(db.Integer, nullable=False)
    age_max = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(), nullable=False)
    symptoms = db.Column(db.String(), nullable=False)
    other_name = db.Column(db.String(), nullable=True)
    norm_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    icd_10 = db.Column(db.String(), nullable=False)
    rec_tests_string = db.Column(db.String(), nullable=True)
    rec_tests = db.Column(db.PickleType, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now(tz=app.config['TIMEZONE']))
    updated_by = db.Column(db.Integer, nullable=True)
    updated_on = db.Column(db.DateTime, server_default=db.func.now(tz=app.config['TIMEZONE']))
    user_id = db.Column(db.Integer, nullable=False)
    treatment = db.Column(db.String(), nullable=True)
    specialty = db.relationship('Specialty', secondary='pathology_specialty')

    def __init__(self, name, info, symptoms, age_min, age_max, sex, user_id, rec_tests = [], has = None,
                other_name = None, rec_tests_string = "",updated_by = None, updated_on = None, treatment = None,
                description = None, icd_10 = None):
        self.name = name
        self.info = info
        self.age_min = age_min
        self.age_max = age_max
        self.sex = sex
        self.has = has
        self.description = description
        self.icd_10 = icd_10
        self.symptoms = symptoms
        self.other_name = other_name
        self.rec_tests = rec_tests
        self.rec_tests_string = rec_tests_string
        self.norm_name = pt.strip_accents(name.lower().strip())
        self.user_id = user_id
        self.updated_by = updated_by
        self.updated_on = updated_on
        self.treatment = treatment

    def __repr__(self):
        return "<Pathology(pathology=%s)>" %(self.name)

    def __str__(self):
        return self.name


class Specialty(db.Model):
    """
    Define pathology specialty
    """
    __tablename__ = "specialty"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return "<Specialty(name=%s)>" %(self.name)


class PathologySpecialty(db.Model):
    """
    Interface between pathology and specialty
    """
    __tablename__ = 'pathology_specialty'
    id = db.Column(db.Integer(), primary_key=True)
    pathology_id = db.Column(db.Integer(), db.ForeignKey('pathology.id', ondelete='CASCADE'))
    specialty_id = db.Column(db.Integer(), db.ForeignKey('specialty.id', ondelete='CASCADE'))

class Role(db.Model):
    """
    Define user roles
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Role(name=%s)>" %(self.name)


class UserRoles(db.Model):
    """
    Interface between user and roles
    """
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class User(db.Model):
    __tablename__="user"
    __bind__="user"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), unique=True)
    rpps =  db.Column(db.BigInteger, unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(50), nullable=False)
    forename = db.Column(db.String(50), nullable=False)
    registered_on = db.Column(db.DateTime, server_default=db.func.now(tz=app.config['TIMEZONE']))
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    entry_count_patient = db.Column(db.Integer, nullable=False, default=0)
    entry_count_pathology = db.Column(db.Integer, nullable=False, default=0)
    modify_count_patient = db.Column(db.Integer, nullable=False, default=0)
    modify_count_pathology = db.Column(db.Integer, nullable=False, default=0)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    zip_code = db.Column(db.String(20), nullable=False)
    # roles = db.relationship('Role', secondary='user_roles')

    def __init__(self, name, forename, rpps, email, password, confirmed=True, confirmed_on = None, entry_count_patient=0, entry_count_pathology=0, modify_count_patient=0, modify_count_pathology=0, phone=0, zip_code=0) :
        self.rpps = rpps
        self.password = password
        self.email = email
        self.forename = forename
        self.name = name
        self.confirmed_on = confirmed_on
        self.confirmed = confirmed
        self.entry_count_patient = entry_count_patient
        self.entry_count_pathology = entry_count_pathology
        self.modify_count_patient = modify_count_patient
        self.modify_count_pathology = modify_count_pathology
        self.phone = phone
        self.zip_code = zip_code

    def __repr__(self):
        return "<User(forename=%s, name=%s, rpps=%d, email=%s)>" %(self.forename, self.name, self.rpps,self.email)

class TraitementCIS(db.Model):
    __tablename__="treatement_cis"
    __bind__="treatement_cis"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    icd_10 = db.Column(db.Integer(), db.ForeignKey('pathology.icd_10', ondelete='CASCADE'), nullable=False)
    pathology_name = db.Column(db.String(50), nullable=False)
    cis = db.Column(db.Integer, nullable=False)

    def __init__(self, icd_10, pathology_name, cis):
        self.icd_10 = icd_10
        self.pathology_name = pathology_name
        self.cis = cis 
    
    def __repr__(self):
        return "<Treatement_cis(icd10=%d, pathology_name=%s, cis=%d)>" %(self.icd_10, self.pathology_name, self.cis)
    
    def __str__(self):
        return self.pathology_name

class TreatementClass(db.Model):
    __tablename__="treatement_class"
    __bind__="treatement_class"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    icd_10 = db.Column(db.Integer(), db.ForeignKey('pathology.icd_10', ondelete='CASCADE'), nullable=False)
    pathology_name = db.Column(db.String(50), nullable=False)
    class_id = db.Column(db.Integer, nullable=False)

    def __init__(self, icd_10, pathology_name, class_id):
        self.icd_10 = icd_10
        self.pathology_name = pathology_name
        self.class_id = class_id 
    
    def __repr__(self):
        return "<Treatement_Class(icd10=%d, pathology_name=%s, class_id=%d)>" %(self.icd_10, self.pathology_name, self.class_id)
    
    def __str__(self):
        return self.pathology_name

class TraitementMolecule(db.Model):
    __tablename__="treatement_molecule"
    __bind__="treatement_molecule"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    icd_10 = db.Column(db.Integer(), db.ForeignKey('pathology.icd_10', ondelete='CASCADE'), nullable=False)
    pathology_name = db.Column(db.String(50), nullable=False)
    molecule_id = db.Column(db.Integer, nullable=False)

    def __init__(self, icd_10, pathology_name, molecule_id):
        self.icd_10 = icd_10
        self.pathology_name = pathology_name
        self.molecule_id = molecule_id 
    
    def __repr__(self):
        return "<Treatement_molecule(icd10=%d, pathology_name=%s, molecule_id=%d)>" %(self.icd_10, self.pathology_name, self.molecule_id)
    
    def __str__(self):
        return self.pathology_name


class Classes(db.Model):
    __tablename__="classes"
    __bind__="classes"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "<Classes(name=%s)>" %(self.name)
    
    def __str__(self):
        return self.name

class Classes_families(db.Model):
    __tablename__="classes_families"
    __bind__="classes_families"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    molecule_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    family_name = db.Column(db.String(50))
    atc = db.Column(db.String(50))

    def __init__(self, molecule_id, class_id, family_name, atc):
        self.molecule_id = molecule_id
        self.class_id = class_id
        self.family_name = family_name 
        self.atc = atc

    
    def __repr__(self):
        return "<Classes_families(molecule_id=%d, class_id=%d, family_name=%s, atc=%s)>" %(self.molecule_id, self.class_id, self.family_name, self.atc)
    
    def __str__(self):
        return self.family_name

class Molecule(db.Model):
    __tablename__= "molecules"
    __bind__= "molecules"
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String)
    rcp = db.Column(db.String)
    rcp_sum = db.Column(db.String)
    
    def __init__(self, name, rcp, rcp_sum):
        self.name = name
        self.rcp = rcp
        self.rcp_sum = rcp_sum
        
    def __repr__(self):
        return "<Molecule(name=%s, rcp=%s, rcp_sum=%s)>" % (self.name, self.rcp, self.rcp_sum)
        
    def __str__(self):
        return self.name

class Dosage(db.Model):
    """
    """
    __tablename__ = "dosage"
    __bind__ = "dosage"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    cis = db.Column(db.Integer, nullable=False)
    icd_10 = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    form_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cadence = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    def __init__(self, cis, icd_10, user_id, form_id, quantity, cadence, duration):
        self.cis = cis
        self.icd_10 = icd_10
        self.user_id = user_id
        self.form_id = form_id
        self.quantity = quantity
        self.cadence = cadence
        self.duration = duration
