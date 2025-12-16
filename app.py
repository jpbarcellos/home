from flask import Flask, render_template, request, send_file
import os
from gerar_qrcode import gerar_qrcode

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    title = request.form.get('title')
    url = request.form.get('url')
    
    if not title or not url:
        return "Por favor, preencha todos os campos.", 400
    
    # Create a safe filename from the title
    safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    filename = f"{safe_title.replace(' ', '_')}_qrcode.png"
    filepath = os.path.join('static', filename)
    
    # Generate the QR code
    gerar_qrcode(url, title, filepath)
    
    return render_template('index.html', generated_image=filename, title=title)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
