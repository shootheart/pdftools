# encoding=utf-8

from flask import Blueprint, render_template, send_from_directory, url_for
from flask import current_app as app
import datetime
import fitz, glob
from PilLite import Image

import sys, os
sys.path.append("..") 
from func import savefile

pdfconvert = Blueprint('pdfconvert', __name__, template_folder='templates')
a4width = 595 # A4纸常规宽度

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
        img_in = Image.open(filename)
        img_wid, img_hei = img_in.size
        if img_wid > a4width:
            img_out = img_in.resize((a4width, int(img_hei * (a4width / img_wid)))) # 按A4纸大小缩图
            img_out.save(filename)
    except Exception as e:
        print("resize %s failed: " %(filename, e))
        outname = ''

    try:
        outname = filename.split('.')[0] + '.pdf'
        with fitz.open() as doc:
            img_open = fitz.open(filename)
            to_pdf = img_open.convert_to_pdf()
            pdf_file = fitz.open('pdf', to_pdf)
            doc.insert_pdf(pdf_file)
            doc.save(outname)
    except Exception as e:
        print("jpg convert to pdf failed: %s" & e)
        outname = ''
    return render_template('convert_download.html', url=url_for('pdfconvert.download', file=outname), filename=outname)

@pdfconvert.route('/download/<file>')
def download(file):
    return send_from_directory(filepath, file, as_attachment=True)
