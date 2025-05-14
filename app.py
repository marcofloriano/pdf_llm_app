from flask import Flask, request, render_template
import fitz  # PyMuPDF
import pymupdf4llm
import pymupdf4llm_enhance  # <- ativa to_dict_for_llm()
import os

# This package converts the pages of a file to text in Markdown format using PyMuPDF.
#
# Standard text and tables are detected, brought in the right reading sequence and then together converted to GitHub-compatible Markdown text.
#
# Header lines are identified via the font size and appropriately prefixed with one or more # tags.
#
# Bold, italic, mono-spaced text and code blocks are detected and formatted accordingly. Similar applies to ordered and unordered lists.
#
# By default, all document pages are processed. If desired, a subset of pages can be specified by providing a list of 0-based page numbers.

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_html_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]  # apenas primeira página para teste
    data = page.to_dict_for_llm()
    html = ""
    for block in data["blocks"]:
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"]
                if span.get("bold"):
                    text = f"<strong>{text}</strong>"
                if span.get("italic"):
                    text = f"<em>{text}</em>"
                html += text + " "
            html += "<br>"
        html += "<br><br>"
    return html

@app.route('/', methods=['GET', 'POST'])
def index():
    content = None
    if request.method == 'POST':
        file = request.files['pdf']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            content = extract_html_from_pdf(filepath)
    return render_template('index.html', content=content)

if __name__ == '__main__':
    app.run(debug=True)
