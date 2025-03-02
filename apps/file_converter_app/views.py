import os

from django.shortcuts import render
from django.http import HttpResponse

from apps.file_converter_app.forms import ConversionForm
from apps.file_converter_app import utils

def convert_file(request):
    conversion_success = 0
    if request.method == "POST":
        form = ConversionForm(request.POST, request.FILES)
        if form.is_valid():
            conv_type = form.cleaned_data.get("conversion_type")
            uploaded_file = request.FILES.get("file")
            text_input = form.cleaned_data.get("text_input")
            output = None
            filename = "output"
            content_type = "text/plain"  # default

            try:
                # Text & Document Converters
                if conv_type == "txt_to_pdf":
                    ext = os.path.splitext(uploaded_file.name)[1].lower()
                    if ext != ".txt":
                        return HttpResponse("Error: TXT to PDF conversion requires a .txt file.", status=400)
                    if text_input:
                        output = utils.txt_to_pdf(text_input)
                        filename += ".pdf"
                        content_type = "application/pdf"
                        conversion_success = 1
                    else:
                        return HttpResponse("Text input required.", status=400)

                elif conv_type == "docx_to_pdf":
                    if uploaded_file:
                        output = utils.docx_to_pdf(uploaded_file)
                        filename += ".pdf"
                        content_type = "application/pdf"
                        conversion_success = 1
                    else:
                        return HttpResponse("DOCX file required.", status=400)

                elif conv_type == "pdf_to_docx":
                    if uploaded_file:
                        output = utils.pdf_to_docx(uploaded_file)
                        filename += ".docx"
                        content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        conversion_success = 1
                    else:
                        return HttpResponse("PDF file required.", status=400)

                elif conv_type == "md_to_html":
                    if text_input:
                        output = utils.md_to_html(text_input)
                        filename += ".html"
                        content_type = "text/html"
                        conversion_success = 1
                    else:
                        return HttpResponse("Markdown text required.", status=400)

                elif conv_type == "html_to_pdf":
                    if text_input:
                        output = utils.html_to_pdf(text_input)
                        filename += ".pdf"
                        content_type = "application/pdf"
                        conversion_success = 1
                    else:
                        return HttpResponse("HTML text required.", status=400)

                # Spreadsheet & Data Converters
                elif conv_type == "excel_to_csv":
                    if uploaded_file:
                        output = utils.excel_to_csv(uploaded_file)
                        filename += ".csv"
                        content_type = "text/csv"
                        conversion_success = 1
                    else:
                        return HttpResponse("Excel file required.", status=400)

                elif conv_type == "csv_to_json":
                    if uploaded_file:
                        output = utils.csv_to_json(uploaded_file)
                        filename += ".json"
                        content_type = "application/json"
                        conversion_success = 1
                    else:
                        return HttpResponse("CSV file required.", status=400)

                elif conv_type == "json_to_csv":
                    if uploaded_file:
                        output = utils.json_to_csv(uploaded_file)
                        filename += ".csv"
                        content_type = "text/csv"
                        conversion_success = 1
                    else:
                        return HttpResponse("JSON file required.", status=400)

                elif conv_type == "xml_to_json":
                    if uploaded_file:
                        output = utils.xml_to_json(uploaded_file)
                        filename += ".json"
                        content_type = "application/json"
                        conversion_success = 1
                    else:
                        return HttpResponse("XML file required.", status=400)

                elif conv_type == "json_to_xml":
                    if uploaded_file:
                        output = utils.json_to_xml(uploaded_file)
                        filename += ".xml"
                        content_type = "application/xml"
                        conversion_success = 1
                    else:
                        return HttpResponse("JSON file required.", status=400)

                elif conv_type == "yaml_to_json":
                    if text_input:
                        output = utils.yaml_to_json(text_input)
                        filename += ".json"
                        content_type = "application/json"
                        conversion_success = 1
                    else:
                        return HttpResponse("YAML text required.", status=400)

                elif conv_type == "json_to_yaml":
                    if text_input:
                        output = utils.json_to_yaml(text_input)
                        filename += ".yaml"
                        content_type = "text/yaml"
                        conversion_success = 1
                    else:
                        return HttpResponse("JSON text required.", status=400)

                # Image Converters
                elif conv_type == "png_to_jpg":
                    if uploaded_file:
                        output = utils.png_to_jpg(uploaded_file)
                        filename += ".jpg"
                        content_type = "image/jpeg"
                        conversion_success = 1
                    else:
                        return HttpResponse("PNG file required.", status=400)

                elif conv_type == "jpg_to_png":
                    if uploaded_file:
                        output = utils.jpg_to_png(uploaded_file)
                        filename += ".png"
                        content_type = "image/png"
                        conversion_success = 1
                    else:
                        return HttpResponse("JPG file required.", status=400)

                elif conv_type == "webp_to_jpg":
                    if uploaded_file:
                        output = utils.webp_to_jpg(uploaded_file)
                        filename += ".jpg"
                        content_type = "image/jpeg"
                        conversion_success = 1
                    else:
                        return HttpResponse("WebP file required.", status=400)

                elif conv_type == "svg_to_raster":
                    if uploaded_file:
                        output = utils.svg_to_raster(uploaded_file, fmt="PNG")
                        filename += ".png"
                        content_type = "image/png"
                        conversion_success = 1
                    else:
                        return HttpResponse("SVG file required.", status=400)

                elif conv_type == "img_to_base64":
                    if uploaded_file:
                        b64_str = utils.img_to_base64(uploaded_file)
                        conversion_success = 1
                        return HttpResponse(b64_str, content_type="text/plain")
                    else:
                        return HttpResponse("Image file required.", status=400)

                elif conv_type == "base64_to_img":
                    if text_input:
                        output = utils.base64_to_img(text_input)
                        filename += ".png"  # Assuming PNG output
                        content_type = "image/png"
                        conversion_success = 1
                    else:
                        return HttpResponse("Base64 string required.", status=400)

                # Multimedia Converters
                elif conv_type == "video_to_gif":
                    if uploaded_file:
                        # For video, we assume file path usage (requires saving temporarily)
                        # Here, save uploaded file temporarily:
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                            tmp.write(uploaded_file.read())
                            tmp.flush()
                            output = utils.video_to_gif(tmp.name)
                        filename += ".gif"
                        content_type = "image/gif"
                        conversion_success = 1
                    else:
                        return HttpResponse("Video file required.", status=400)

                elif conv_type == "gif_to_mp4":
                    if uploaded_file:
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as tmp:
                            tmp.write(uploaded_file.read())
                            tmp.flush()
                            output = utils.gif_to_mp4(tmp.name)
                        filename += ".mp4"
                        content_type = "video/mp4"
                        conversion_success = 1
                    else:
                        return HttpResponse("GIF file required.", status=400)

                elif conv_type == "mp4_to_mp3":
                    if uploaded_file:
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                            tmp.write(uploaded_file.read())
                            tmp.flush()
                            output = utils.mp4_to_mp3(tmp.name)
                        filename += ".mp3"
                        content_type = "audio/mpeg"
                        conversion_success = 1
                    else:
                        return HttpResponse("MP4 file required.", status=400)

                elif conv_type == "wav_to_mp3":
                    if uploaded_file:
                        output = utils.wav_to_mp3(uploaded_file)
                        filename += ".mp3"
                        content_type = "audio/mpeg"
                        conversion_success = 1
                    else:
                        return HttpResponse("WAV file required.", status=400)

                # Compression & Optimization
                elif conv_type == "pdf_compress":
                    if uploaded_file:
                        output = utils.pdf_compress(uploaded_file)
                        filename += ".pdf"
                        content_type = "application/pdf"
                        conversion_success = 1
                    else:
                        return HttpResponse("PDF file required.", status=400)

                elif conv_type == "img_compress":
                    if uploaded_file:
                        output = utils.img_compress(uploaded_file)
                        filename += ".jpg"
                        content_type = "image/jpeg"
                        conversion_success = 1
                    else:
                        return HttpResponse("Image file required.", status=400)

                elif conv_type == "video_compress":
                    if uploaded_file:
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                            tmp.write(uploaded_file.read())
                            tmp.flush()
                            output = utils.video_compress(tmp.name)
                        filename += ".mp4"
                        content_type = "video/mp4"
                        conversion_success = 1
                    else:
                        return HttpResponse("Video file required.", status=400)

                # Encoding & Decoding
                elif conv_type == "base64_encode":
                    if uploaded_file:
                        encoded = utils.base64_encode(uploaded_file)
                        return HttpResponse(encoded, content_type="text/plain")
                    else:
                        return HttpResponse("File required for encoding.", status=400)

                elif conv_type == "url_encode":
                    if text_input:
                        encoded = utils.url_encode(text_input)
                        return HttpResponse(encoded, content_type="text/plain")
                    else:
                        return HttpResponse("Text required.", status=400)

                elif conv_type == "hash_generate":
                    if uploaded_file:
                        hash_value = utils.hash_generate(uploaded_file, algo="md5")
                        return HttpResponse(hash_value, content_type="text/plain")
                    else:
                        return HttpResponse("File required.", status=400)

                # Unit Converters
                elif conv_type == "temp_convert":
                    if text_input:
                        try:
                            celsius = float(text_input.strip())
                            fahrenheit = utils.temp_convert(celsius)
                            return HttpResponse(f"{fahrenheit} °F", content_type="text/plain")
                        except ValueError:
                            return HttpResponse("Invalid temperature value.", status=400)
                    else:
                        return HttpResponse("Temperature value required.", status=400)

                elif conv_type == "currency_convert":
                    # Expecting input as "amount,from_currency,to_currency" e.g., "100,USD,INR"
                    if text_input:
                        try:
                            parts = text_input.strip().split(',')
                            amount = float(parts[0])
                            result = utils.currency_convert(amount, parts[1].strip(), parts[2].strip())
                            return HttpResponse(str(result), content_type="text/plain")
                        except Exception as e:
                            return HttpResponse(f"Error: {e}", status=400)
                    else:
                        return HttpResponse("Currency conversion input required.", status=400)

                elif conv_type == "length_convert":
                    # Expecting input as "value,from_unit,to_unit" e.g., "10,meter,feet"
                    if text_input:
                        try:
                            parts = text_input.strip().split(',')
                            value = float(parts[0])
                            result = utils.unit_convert(value, parts[1].strip(), parts[2].strip())
                            return HttpResponse(str(result), content_type="text/plain")
                        except Exception as e:
                            return HttpResponse(f"Error: {e}", status=400)
                    else:
                        return HttpResponse("Unit conversion input required.", status=400)

                else:
                    return HttpResponse("Invalid conversion type.", status=400)

            except Exception as e:
                return HttpResponse(f"Conversion error: {str(e)}", status=500)

            # Return file download if output is available
            if output:
                response = HttpResponse(output, content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
    else:
        form = ConversionForm()
    context = {
        'form': form,
        'conversion_success': conversion_success,
    }
    return render(request, "file_converter/convert.html", context)
    # return render(request, "base.html")
