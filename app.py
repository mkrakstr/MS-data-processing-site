from flask import Flask, send_file, session, jsonify, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField
from webforms import FileUploadForm
import pandas as pd
from data_processing import manual_input
#import flask_excel as excel
from werkzeug.utils import secure_filename
import json
import os



app = Flask(__name__)

app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS= {'txt', 'csv', 'xls', 'xlsx'}
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template("500.html"), 500

@app.route('/')
def index():
	return render_template("index.html")


@app.route('/custom_data', methods = ["GET", "POST"])
def custom_data():
	form =FileUploadForm()
	if request.method == "POST":
		Internal_standard = request.form['Internal_standard']
		Internal_standard = int(Internal_standard)
		Sample_metadata = request.files['Sample_metadata']
		Feature_metadata = request.files['Feature_metadata']
		file = request.files['upload_file']
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		flash("test")
		df_norm = manual_input(file, Internal_standard, Sample_metadata, Feature_metadata)
		df_norm = 2
		session['df_norm'] = df_norm  #.to_html
		#return redirect(url_for('data'))
		return render_template('Custom_data.html', form=form)
	return render_template('Custom_data.html', form=form)



@app.route('/data',  methods = ["GET", "POST"])
def data():
	file_name = os.path.join(app.static_folder, 'files', 'df_norm.json')
	with open(file_name) as json_file:
		data = json.load(json_file)
	return data

@app.route('/data_table')
def data_table():
	return render_template('data_table.html')

@app.route('/results')
def results():
	return render_template('results.html')

@app.route('/download_norm')
def download_norm():
    root_path = r"C:\Users\mavikr\Documents\Python\data_site\static\files"
    norm_data = "df_norm.xlsx"
    file_path_norm = os.path.join(root_path, norm_data)
    return send_file(file_path_norm)

@app.route('/download_results')
def download_results():
	root_path = r"C:\Users\mavikr\Documents\Python\data_site\static\files"
	results = "final_results.xlsx"
	file_path_results = os.path.join(root_path, results)
	return send_file(file_path_results)


if __name__ == "__main__":
    excel.init_excel(app)
    app.run()
		