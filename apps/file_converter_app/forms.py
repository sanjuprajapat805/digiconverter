from django import forms

CONVERSION_CHOICES = (
    # Text & Document Converters
    ('', '---Select Value---'),
    ('txt_to_pdf', 'TXT to PDF'),
    ('docx_to_pdf', 'Word (DOCX) to PDF'),
    ('pdf_to_docx', 'PDF to Word (DOCX)'),
    ('md_to_html', 'Markdown to HTML'),
    ('html_to_pdf', 'HTML to PDF'),
    
    # Spreadsheet & Data Converters
    ('excel_to_csv', 'Excel to CSV'),
    ('csv_to_json', 'CSV to JSON'),
    ('json_to_csv', 'JSON to CSV'),
    ('xml_to_json', 'XML to JSON'),
    ('json_to_xml', 'JSON to XML'),
    ('yaml_to_json', 'YAML to JSON'),
    ('json_to_yaml', 'JSON to YAML'),
    
    # Image Converters
    ('png_to_jpg', 'PNG to JPG'),
    ('jpg_to_png', 'JPG to PNG'),
    ('webp_to_jpg', 'WebP to JPG/PNG'),  # A single option for simplicity
    ('svg_to_raster', 'SVG to PNG/JPG'),
    ('img_to_base64', 'Image to Base64'),
    ('base64_to_img', 'Base64 to Image'),
    
    # Multimedia Converters
    ('video_to_gif', 'Video to GIF'),
    ('gif_to_mp4', 'GIF to MP4'),
    ('mp4_to_mp3', 'MP4 to MP3 (Extract Audio)'),
    ('wav_to_mp3', 'WAV to MP3'),
    
    # Compression & Optimization
    ('pdf_compress', 'PDF Compressor'),
    ('img_compress', 'Image Compressor'),
    ('video_compress', 'Video Compressor'),
    
    # Encoding & Decoding
    ('base64_encode', 'Base64 Encode/Decode'),
    ('url_encode', 'URL Encode/Decode'),
    ('hash_generate', 'Hash Generator (MD5/SHA256)'),
    
    # Unit Converters
    ('temp_convert', 'Temperature (Celsius to Fahrenheit)'),
    ('currency_convert', 'Currency Converter'),
    ('length_convert', 'Length/Weight/Time Converter'),
)

class ConversionForm(forms.Form):
    conversion_type = forms.ChoiceField(choices=CONVERSION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    file = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control, file-field'}))
    text_input = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control, text-field', 'rows': 4}))
