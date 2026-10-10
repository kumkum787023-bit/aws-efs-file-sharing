import os
from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'local-demo-change-me')
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
SHARED_DIR = Path(os.environ.get('SHARED_DIR', './shared_files')).resolve()
SHARED_DIR.mkdir(parents=True, exist_ok=True)

@app.get('/')
def index():
    files = sorted(({'name': p.name, 'size': p.stat().st_size} for p in SHARED_DIR.iterdir() if p.is_file()), key=lambda x: x['name'].lower())
    return render_template('index.html', files=files, host=__import__("socket").gethostname())

@app.post('/upload')
def upload():
    item = request.files.get('file')
    name = secure_filename(item.filename or '') if item else ''
    if not name:
        flash('Choose a file first.', 'error')
    elif (SHARED_DIR / name).exists():
        flash('That filename already exists. Rename it before uploading.', 'error')
    else:
        item.save(SHARED_DIR / name)
        flash(f'{name} uploaded to shared storage.', 'success')
    return redirect(url_for('index'))

@app.get('/files/<path:name>')
def download(name):
    if name != secure_filename(name):
        return 'Invalid filename', 400
    return send_from_directory(SHARED_DIR, name, as_attachment=True)

@app.post('/delete/<path:name>')
def delete(name):
    if name != secure_filename(name):
        return 'Invalid filename', 400
    target = SHARED_DIR / name
    if not target.is_file():
        return 'File not found', 404
    target.unlink()
    flash(f'{name} deleted.', 'success')
    return redirect(url_for('index'))

@app.get('/health')
def health():
    return {'status': 'ok', 'storage': str(SHARED_DIR)}

@app.errorhandler(413)
def too_large(_):
    return 'Maximum upload size is 20 MB.', 413

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)

