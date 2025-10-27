from flask import Flask, request, Response, send_file
from flask_cors import CORS
import qrcode
import qrcode.image.svg
import io

app = Flask(__name__)
CORS(app, origins=["https://qrcoder.spaziogenesi.org"])

ALLOWED_ORIGIN = "https://qrcoder.spaziogenesi.org"

@app.before_request
def restrict_origin():
    origin = request.headers.get("Origin") or request.headers.get("Referer", "")
    if not origin.startswith(ALLOWED_ORIGIN):
        return "Forbidden", 403

@app.route("/qr")
def generate_qr():
    data = request.args.get("data", "")
    fmt = request.args.get("format", "svg").lower()

    if not data:
        return "Missing 'data' parameter", 400

    if fmt == "png":
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        return send_file(
            buf,
            mimetype="image/png",
            as_attachment=True,
            download_name="qrcode.png"
        )

    elif fmt == "svg":
        factory = qrcode.image.svg.SvgPathImage
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            image_factory=factory
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        stream = io.BytesIO()
        img.save(stream)
        svg_data = stream.getvalue().decode('utf-8')

        return Response(svg_data, mimetype="image/svg+xml")

    return "Invalid format. Use 'svg' or 'png'.", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
