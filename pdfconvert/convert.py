# encoding=utf-8

from flask import Blueprint, render_template, send_from_directory, url_for
from flask import current_app as app
import datetime
from PilLite import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape

import sys, os
sys.path.append("..") 
from func import savefile

pdfconvert = Blueprint('pdfconvert', __name__, template_folder='templates')

@pdfconvert.route('/')
def upload():
    return render_template('convert_upload.html')

@pdfconvert.route('/uploadapi', methods=['POST'], strict_slashes=False)
def jpg_convert():
    global filepath
    filepath = os.path.join(pdfconvert.root_path, app.config['UPLOAD_FOLDER'], datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '/')
    filename = savefile(filepath)
    if not filename:
        return render_template('convert_download.html', url='', filename='')
    
    os.chdir(filepath)
    try:
        outname = filename.split('.')[0] + '.pdf'
        img_in = Image.open(filename)
        img_hei, img_wid = img_in.size
        a4_wid, a4_hei = landscape(A4)
        page = canvas.Canvas(outname)
        if img_wid > a4_wid:
            ratio = a4_wid / img_wid
        page.drawImage(filename, 3, 3, img_hei * ratio, img_wid * ratio)
        page.save()

    except Exception as e:
        print("jpg convert to pdf failed: %s" & e)
        outname = ''
    return render_template('convert_download.html', url=url_for('pdfconvert.download', file=outname), filename=outname)

@pdfconvert.route('/download/<file>')
def download(file):
    return send_from_directory(filepath, file, as_attachment=True)
