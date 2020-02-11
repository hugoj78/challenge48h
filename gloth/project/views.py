import os
from werkzeug import secure_filename
from flask import Flask, request, redirect, url_for, render_template, flash
import pdfkit

app = Flask(__name__)
app.config.from_object("project.config.Config")

from .forms import PatientForm, MedicForm
from .utils import *

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    form = PatientForm()

    if request.method == "POST":
        if form.validate() == False:
            flash("All fields are required.")
            return render_template("index.html", title="Gloth", subtitle="test", patient_form=form, name="Ynov")
        else:
            data = request.args.get(form)
            return redirect(url_for('medic'), data=data)

    return render_template("index.html", title="Gloth", subtitle="subtitle", patient_form=form, name="Ynov")


@app.route('/medic', methods=["GET","POST"])
def medic():

    form = MedicForm(request.form)
    patho_id = (request.form.get("pathology"))
    user_id = (request.form.get("user"))
    return render_template("medic.html", name="Ynov", pathology=patho_id, user=user_id)

@app.route('/select', methods=["GET", "POST"])
def select():

    return render_template("select.html", name="Ynov")

@app.route('/ordonnance', methods=["GET"])
def posology():
    Classe = allClasses()
    id_classe = allClassesId()
    #Molecule_id = allMoleculeFilterByClass(id_classe[0])
    Molecule_name = []

    for x in id_classe:
        dict_class = {}
        dict_class[x] = allMoleculeFilterByClass(x)
        Molecule_name.append(dict_class)
    
    for w in Molecule_name:
        for key, value in w.items():
            print(key, value)
            names = []
            for v in value:
                names.append(allMoleculeFilterByClassName(v))
            w[key] = names
    
    return render_template("ordonnance.html", classes = Classe, dataMolecules = Molecule_name, name="Ynov")

@app.route('/medicaments', methods=["GET"])
def medicaments():
    return render_template("medic.html", name="Ynov")

@app.route('/leib', methods=["GET"])
def ordonnance():
    htmlstr = '<h2>Heading 2</h2><p>Sample paragraph.</p>'
    pdfkit.from_string(htmlstr, 'sample.pdf')
    return render_template("base.html", name='Ynov')


@app.route('/posology', methods=["GET"])
def adrien():
    return render_template("posology.html", name='Ynov')


@app.route('/traitement_cis', methods=["GET"])
def adrien3():
    return render_template("traitement_cis.html", name='Ynov')