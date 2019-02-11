import os
from flask import render_template
from flask import request
from flaskexample import app
import processes as prc
import pandas as pd
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = '/home/ubuntu/INSIGHT2/application/flaskexample/static/uploads'
ALLOWED_EXTENSIONS = set(['txt'])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#@app.route('/')
#@app.route('/index')
#def index():
#   user = { 'nickname': 'Babak' } # fake user
#   return render_template("index.html",
#       title = 'Babak',
#       user = user)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file',
                                    #filename=filename))
            #fullname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return render_template("input.html")


@app.route('/output', methods = ['GET', 'POST'])
def TC_output():
  if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))

  pd.set_option('display.max_colwidth',100)
  #open the text file containing the terms and services
  #file_name = request.args.get('birth_month')
  file_name = f.filename
  ff = open(file_name)
  txt = ff.read()

  # Here the model works on this document and distinguishes risky parts
  a = prc.doc2sent(file_name)
  a['cleaned'] = prc.preprocess(a['quote'])
  result = prc.model_1(a['cleaned'])
  nu_sentence = len(result)
  riskies = result[result['point']==0]
  riskies = riskies['quote'].to_frame()
  riskies.set_index('quote', inplace=True)
  riskies = riskies.to_html(float_format='%.0f').replace('<th>','<th style="color:#B22222">')


  return render_template("output.html", nu_sentence = nu_sentence, txt = txt, riskies=riskies)

@app.route('/output_text')
def output():
  #open the text file containing the terms and services
  file_name = request.args.get('file')
  ff = open(file_name)
  txt = ff.read()

  # Here the model works on this document and distinguishes risky parts
  a = prc.doc2sent(file_name)
  a['cleaned'] = prc.preprocess(a['quote'])
  result = prc.model_1(a['cleaned'])
  nu_sentence = len(result)
  riskies = result[result['point']==0]
  riskies = riskies['quote'].to_frame()
  riskies.set_index('quote', inplace=True)
  riskies = riskies.to_html(float_format='%.0f').replace('<th>','<th style="color:#B22222">')


  return render_template("output.html", nu_sentence = nu_sentence, txt = txt, riskies=riskies)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
