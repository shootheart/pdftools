# coding=utf-8

from flask import Blueprint, render_template, send_from_directory, url_for
from flask import current_app as app

from PyPDF2 import PdfFileMerger

import sys, os, datetime
sys.path.append("..") 
from func import savefile

#imp.reload(sys)
#sys.setdefaultencoding('utf-8') # 默认以ascii处理，如果文件不以ascii编码，就会抛出异常

pdfmerge = Blueprint('pdfmerge', __name__, template_folder='templates')
out = u'合并的文件'

@pdfmerge.route('/')
def upload():
    return render_template('merge_upload.html')

@pdfmerge.route('/uploadapi', methods=['POST'], strict_slashes=False)
def pdf_save():
    global filepath, filenames
    filepath = os.path.join(pdfmerge.root_path, app.config['UPLOAD_FOLDER'], datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '/')
    filenames = savefile(filepath)
    return render_template('merge_start.html', filenames=filenames)

@pdfmerge.route('/merge')
def merge():
    os.chdir(filepath)
    merger = PdfFileMerger()
    outname = out + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
    for pdffile in filenames:
        try:
            merger.append(open(pdffile, 'rb'))
        except:
            print('error while file %s merge' % pdffile)
    with open(outname, 'wb') as pdfout:
        merger.write(pdfout)

    return render_template('merge_download.html', url=url_for('pdfmerge.download', file=outname), filename=outname)

@pdfmerge.route('/download/<file>')
def download(file):
    return send_from_directory(filepath, file, as_attachment=True)
