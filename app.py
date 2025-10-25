from flask import Flask, request, Response, send_file
from flask_cors import CORS
import qrcode
import qrcode.image.svg
import io

app = Flask(__name__)
CORS(app)

@app.route("/qr")
def generate_qr():
    data = request.args.get("data", "")
    fmt = request.args.get("format", "svg").lower()  # default svg

    if not data:
        return "Missing 'data' parameter", 400

    if fmt == "png":
        # Genera QR in PNG
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Salva in buffer PNG
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        # Restituisce immagine come file PNG
        return send_file(
            buf,
            mimetype="image/png",
            as_attachment=True,
            download_name="qrcode.png"
        )

    elif fmt == "svg":
        # Genera QR in SVG
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

        # Salva in buffer SVG
        stream = io.BytesIO()
        img.save(stream)
        svg_data = stream.getvalue().decode('utf-8')

        return Response(svg_data, mimetype="image/svg+xml")

    else:
        return "Invalid format. Use 'svg' or 'png'.", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
