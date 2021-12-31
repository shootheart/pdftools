# coding=utf-8

from flask import Flask, render_template
from pdfmerge.merge import pdfmerge
from pdfsplit.split import pdfsplit
from pdfconvert.convert import pdfconvert

app = Flask(__name__)

app.register_blueprint(pdfsplit, url_prefix = '/pdfsplit')
app.register_blueprint(pdfmerge, url_prefix = '/pdfmerge')
app.register_blueprint(pdfconvert, url_prefix = '/pdfconvert')

app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['ALLOWED_EXTENSIONS_IMG'] = {'jpg', 'jpeg', 'png'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MB
app.config['UPLOAD_FOLDER'] = 'tmp/'

@app.route('/family', strict_slashes=False)
def choice():
    return render_template('choice.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8800, debug=True)
