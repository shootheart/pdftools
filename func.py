# coding=utf-8

import os
import sys
from flask import request
from flask import current_app as app

path = os.path.abspath('.')

#reload(sys)
#sys.setdefaultencoding('utf-8') # 默认以ascii处理，如果文件不以ascii编码，就会抛出异常

def savefile(path):
	if request.blueprint == 'pdfmerge': # 获取当前处理请求的蓝图 str
		os.mkdir(path)
		filenames = []
		for i in range(len(request.files)):
			file = request.files['file'+str(i + 1)]
			filename = file.filename
			if file and filename != '' and check_file(filename):
				file.save(path + filename)
				filenames.append(filename)
			else:
				return
		return filenames
	file = request.files['file']
	filename = file.filename
	if file and filename != '' and check_file(filename):
		os.mkdir(path)
		file.save(path + filename) # 绝对路径
	else:
		filename = ''
	return filename

# 判断上传的文件类型
def check_file(filename):
	file_ext = filename.split('.')[-1].lower()
	if request.blueprint == 'pdfconvert':
		return True if file_ext in app.config['ALLOWED_EXTENSIONS_IMG'] else False
	return True if file_ext in app.config['ALLOWED_EXTENSIONS'] else False

#def downloadfile(filename):
#	bp = request.blueprint # 获取当前处理请求的蓝图 str
#	return send_from_directory(os.path.join(path, bp, app.config['UPLOAD_FOLDER']), filename, as_attachment=True)
