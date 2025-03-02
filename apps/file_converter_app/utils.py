import io
import base64
import hashlib
import pandas as pd
import markdown2  # alternative to markdown
import pdfkit
import yaml
import xmltodict
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pdf2image import convert_from_bytes
from moviepy.editor import VideoFileClip, VideoClip, AudioFileClip
from forex_python.converter import CurrencyRates
from pint import UnitRegistry

# ----- Text & Document Converters -----
def txt_to_pdf(text):
    """Convert plain text to PDF in-memory."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    textobject = c.beginText(40, 750)
    for line in text.splitlines():
        textobject.textLine(line)
    c.drawText(textobject)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def docx_to_pdf(docx_file):
    # Note: Converting DOCX to PDF in pure Python is challenging.
    # One common approach is to use external tools like LibreOffice headless mode.
    # Here, we assume you call an external command.
    import subprocess, tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_in, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_out:
        temp_in.write(docx_file.read())
        temp_in.flush()
        # Ensure LibreOffice is installed and added to PATH.
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', temp_in.name, '--outdir', tempfile.gettempdir()])
        with open(temp_out.name, 'rb') as f:
            pdf_data = f.read()
    return io.BytesIO(pdf_data)

def pdf_to_docx(pdf_file):
    # Converting PDF to DOCX typically requires tools like 'pdf2docx'.
    from pdf2docx import Converter
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
        temp_pdf.write(pdf_file.read())
        temp_pdf.flush()
        cv = Converter(temp_pdf.name)
        cv.convert(temp_docx.name, start=0, end=None)
        cv.close()
        with open(temp_docx.name, 'rb') as f:
            docx_data = f.read()
    return io.BytesIO(docx_data)

def md_to_html(md_text):
    """Convert Markdown text to HTML."""
    html = markdown2.markdown(md_text)
    return io.StringIO(html)

# def html_to_pdf(html_text):
#     """Convert HTML text to PDF using pdfkit."""
#     pdf_bytes = pdfkit.from_string(html_text, False)
#     return io.BytesIO(pdf_bytes)

def html_to_pdf(html_text):
    """Convert HTML text to PDF using pdfkit."""
    # wkhtmltopdf executable का path सेट करें
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        'no-stop-slow-scripts': '',
        'javascript-delay': '2000',  # Delay to allow JavaScript to execute, if needed
        'load-error-handling': 'ignore',
        'load-media-error-handling': 'ignore'
    }
    pdf_bytes = pdfkit.from_string(html_text, False,options=options,configuration=config)
    return io.BytesIO(pdf_bytes)


# ----- Spreadsheet & Data Converters -----
def excel_to_csv(excel_file):
    df = pd.read_excel(excel_file)
    csv_str = df.to_csv(index=False)
    return io.BytesIO(csv_str.encode('utf-8'))

def csv_to_json(csv_file):
    df = pd.read_csv(csv_file)
    json_str = df.to_json(orient='records')
    return io.StringIO(json_str)

def json_to_csv(json_file):
    import json
    data = json.load(json_file)
    df = pd.DataFrame(data)
    csv_str = df.to_csv(index=False)
    return io.BytesIO(csv_str.encode('utf-8'))

def xml_to_json(xml_file):
    xml_content = xml_file.read()
    data_dict = xmltodict.parse(xml_content)
    import json
    json_str = json.dumps(data_dict)
    return io.StringIO(json_str)

def json_to_xml(json_file):
    import json
    data = json.load(json_file)
    xml_str = xmltodict.unparse(data)
    return io.StringIO(xml_str)

def yaml_to_json(yaml_text):
    data = yaml.safe_load(yaml_text)
    import json
    json_str = json.dumps(data)
    return io.StringIO(json_str)

def json_to_yaml(json_text):
    import json
    data = json.loads(json_text)
    yaml_str = yaml.dump(data)
    return io.StringIO(yaml_str)

# ----- Image Converters -----
def png_to_jpg(image_file):
    image = Image.open(image_file)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer

def jpg_to_png(image_file):
    image = Image.open(image_file)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def webp_to_jpg(image_file):
    image = Image.open(image_file)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer

def svg_to_raster(svg_file, fmt="PNG"):
    # Requires cairosvg
    import cairosvg
    svg_data = svg_file.read()
    output = io.BytesIO()
    cairosvg.svg2png(bytestring=svg_data, write_to=output) if fmt.upper()=="PNG" else cairosvg.svg2pdf(bytestring=svg_data, write_to=output)
    output.seek(0)
    return output

def img_to_base64(image_file):
    data = image_file.read()
    encoded = base64.b64encode(data)
    return encoded.decode('utf-8')

def base64_to_img(b64_string):
    decoded = base64.b64decode(b64_string)
    return io.BytesIO(decoded)

# ----- Multimedia Converters -----
def video_to_gif(video_file_path, duration=5):
    # Extract first few seconds as GIF using moviepy.
    clip = VideoFileClip(video_file_path).subclip(0, duration)
    buffer = io.BytesIO()
    clip.write_gif("temp.gif")
    with open("temp.gif", "rb") as f:
        buffer.write(f.read())
    buffer.seek(0)
    return buffer

def gif_to_mp4(gif_file_path):
    clip = VideoFileClip(gif_file_path)
    buffer = io.BytesIO()
    clip.write_videofile("temp.mp4", codec="libx264")
    with open("temp.mp4", "rb") as f:
        buffer.write(f.read())
    buffer.seek(0)
    return buffer

def mp4_to_mp3(video_file_path):
    clip = VideoFileClip(video_file_path)
    audio = clip.audio
    buffer = io.BytesIO()
    audio.write_audiofile("temp.mp3")
    with open("temp.mp3", "rb") as f:
        buffer.write(f.read())
    buffer.seek(0)
    return buffer

def wav_to_mp3(wav_file):
    from pydub import AudioSegment
    audio = AudioSegment.from_wav(wav_file)
    buffer = io.BytesIO()
    audio.export("temp.mp3", format="mp3")
    with open("temp.mp3", "rb") as f:
        buffer.write(f.read())
    buffer.seek(0)
    return buffer

# ----- Compression & Optimization -----
def pdf_compress(pdf_file):
    # Using PyMuPDF (fitz) for PDF compression
    import fitz
    input_data = pdf_file.read()
    doc = fitz.open("pdf", input_data)
    output = io.BytesIO()
    doc.save("temp_compressed.pdf", garbage=4, deflate=True)
    with open("temp_compressed.pdf", "rb") as f:
        output.write(f.read())
    output.seek(0)
    return output

def img_compress(image_file, quality=50):
    image = Image.open(image_file)
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    return buffer

def video_compress(video_file_path, target_size_mb=10):
    # Video compression can be done using ffmpeg.
    # This is a placeholder calling ffmpeg via subprocess.
    import subprocess, os, tempfile
    temp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    subprocess.run(['ffmpeg', '-i', video_file_path, '-b:v', '1000k', temp_out.name])
    with open(temp_out.name, "rb") as f:
        data = f.read()
    os.remove(temp_out.name)
    return io.BytesIO(data)

# ----- Encoding & Decoding -----
def base64_encode(data_file):
    data = data_file.read()
    return base64.b64encode(data).decode('utf-8')

def base64_decode(b64_string):
    decoded = base64.b64decode(b64_string)
    return io.BytesIO(decoded)

def url_encode(text):
    from urllib.parse import quote
    return quote(text)

def url_decode(encoded_text):
    from urllib.parse import unquote
    return unquote(encoded_text)

def hash_generate(data_file, algo="md5"):
    data = data_file.read()
    if algo.lower() == "md5":
        h = hashlib.md5()
    else:
        h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()

# ----- Unit Converters -----
def temp_convert(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

def currency_convert(amount, from_currency, to_currency):
    c = CurrencyRates()
    rate = c.get_rate(from_currency, to_currency)
    return amount * rate

def unit_convert(value, from_unit, to_unit):
    ureg = UnitRegistry()
    try:
        result = (value * ureg(from_unit)).to(to_unit)
        return result.magnitude
    except Exception as e:
        return str(e)
