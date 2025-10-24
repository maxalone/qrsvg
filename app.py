from flask import Flask, request, Response
import qrcode
import qrcode.image.svg
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route("/qr")
def generate_qr():
    data = request.args.get("data", "")
    if not data:
        return "Missing 'data' parameter", 400

    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(data, image_factory=factory)
    svg_element = img.get_image()

    svg_data = ET.tostring(svg_element, encoding="unicode")
    return Response(svg_data, mimetype="image/svg+xml")
