from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PASSWORD = 'mysecretpassword'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    photos = os.listdir(UPLOAD_FOLDER)
    logged_in = session.get('logged_in', False)
    return render_template('index.html', photos=photos, logged_in=logged_in)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('密语错误！')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))  # 确保注销后重定向到登录页面

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有选择文件！')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('没有选择文件！')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('照片上传成功！')
            return redirect(url_for('index'))
    
    return render_template('upload.html')

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('照片删除成功！')
    except FileNotFoundError:
        flash('照片未找到！')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
