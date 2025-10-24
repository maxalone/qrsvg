from flask import Flask, request, Response
from flask_cors import CORS
import qrcode
import qrcode.image.svg
import io

app = Flask(__name__)
CORS(app)

@app.route("/qr")
def generate_qr():
    data = request.args.get("data", "")
    if not data:
        return "Missing 'data' parameter", 400

    # Usa SvgPathImage invece di SvgImage (più compatibile)
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
    
    # Salva in un buffer
    stream = io.BytesIO()
    img.save(stream)
    svg_data = stream.getvalue().decode('utf-8')
    
    return Response(svg_data, mimetype="image/svg+xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
