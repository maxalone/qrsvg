from flask import Flask, request, Response
import qrcode
import qrcode.image.svg

app = Flask(__name__)

@app.route("/qr")
def generate_qr():
    data = request.args.get("data", "")
    if not data:
        return "Missing 'data' parameter", 400

    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(data, image_factory=factory)
    svg_io = img.get_image()
    return Response(svg_io.to_string(), mimetype="image/svg+xml")
