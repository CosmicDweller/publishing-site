from sys import flags
from unittest import result
from flask import Blueprint, url_for, render_template, redirect, request, flash, jsonify, Response
from . import db
import os
from .models import File
from website import allowed_file, UPLOAD_FOLDER, create_app
import json
from werkzeug.utils import secure_filename
import re

views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
@views.route('/home', methods=['POST', 'GET'])
def home():
    files = File.query.all()
    for file in files:
        print(file.filename)
    print(len(files))
    if request.method == 'POST' :
        title = request.form.get('title')
        date = request.form.get('date')
        author = request.form.get('author')
        if 'file' not in  request.files:
            flash('No file uploaded!', category='error')
            
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            path = url_for('static', filename=filename)
            print(path)
            print(filename)
            story = File( filename=path, title=title, date=date, author=author)
            db.session.add(story)
            db.session.commit()
            flash('File uploaded!', category='success')
        print(len(files))
        # print(path)
        return redirect(url_for('views.home'))
           
    return render_template("base.html", files=files)

@views.route('/sort', methods=['POST', 'GET'])
def sort():
    files = File.query.all()
    results = []
    if request.method == 'POST':
        search = request.form['search']
        
        for file in files:
            if re.search(f"{search}", str(file.author)):
                results.append(file)
            elif re.search(f"{search}", str(file.title)):
                results.append(file)
            elif re.search(f"{search}", str(file.date)):
                results.append(file)
            else: 
                continue
            
        if len(results) < 1:
            flash(f'No results found by the name of {search}', category='alert')
        files = results
    return render_template("base.html", files=results)