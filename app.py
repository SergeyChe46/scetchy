import cv2
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "e232C4V#$vcq!vkctx$@imc U8$mp)^vc@<v"

if "static" not in os.listdir("."):
    os.mkdir("static")

if "uploads" not in os.listdir("static/"):
    os.mkdir("static/uploads")


def allowed_file(filename: str):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


def make_scetch(img):
    grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(grayed)
    blurred = cv2.GaussianBlur(inverted, (15, 15), sigmaX=0, sigmaY=0)
    result = cv2.divide(grayed, 255 - blurred, scale=256)
    return result


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/scetch", methods=["POST"])
def scetch():
    file = request.files["file"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        img = cv2.imread(UPLOAD_FOLDER + "/" + filename)
        scetch_image = make_scetch(img)
        scetch_image_name = filename.split(".")[0] + "_scetched.png"
        _ = cv2.imwrite(UPLOAD_FOLDER + "/" + scetch_image_name, scetch_image)
        return render_template(
            "home.html", org_img_name=filename, sketch_img_name=scetch_image_name
        )


if __name__ == "main":
    app.run(debug=True)
