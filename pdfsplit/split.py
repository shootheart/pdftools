# coding=utf-8

from flask import Blueprint, render_template, send_from_directory, url_for
from flask import current_app as app
import datetime
import PyPDF2
import zipfile

import sys, os
sys.path.append("..") 
from func import savefile

pdfsplit = Blueprint('pdfsplit', __name__, template_folder='templates')

@pdfsplit.route('/')
def upload():
    return render_template('split_upload.html')

@pdfsplit.route('/uploadapi', methods=['POST'], strict_slashes=False)
def pdf_save():
	global filepath
	filepath = os.path.join(pdfsplit.root_path, app.config['UPLOAD_FOLDER'], datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '/')
	filename = savefile(filepath)
	return render_template('split_start.html', filename=filename)

@pdfsplit.route('/split/<filename>')
def pdf_split(filename):
	splited_files = []
	os.chdir(filepath)
	file = open(filename, 'rb')
	repdf = PyPDF2.PdfFileReader(file, strict=False)
	outname = file.name.split('.pdf')[0]
	zipname = outname + '.zip'

	for i in range(repdf.getNumPages()):
		page = repdf.getPage(i)
		writer = PyPDF2.PdfFileWriter()
		writer.addPage(page)
		with open(outname+'-'+str(i + 1)+'.pdf', 'wb') as output:
			writer.write(output)
			splited_files.append(output.name)

	with zipfile.ZipFile(zipname, 'w') as outzip:
		for filename in splited_files:
			outzip.write(filename)
			os.remove(filename)

	return render_template('split_download.html', url=url_for('pdfsplit.download', file=zipname), filename=zipname)

@pdfsplit.route('/download/<file>')
def download(file):
	return send_from_directory(filepath, file, as_attachment=True)

