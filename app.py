from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import os
import pickle

app = Flask(__name__)
CORS(app)

# Load model once
model = pickle.load(open("admission_lr_model.pickle", "rb"))

@app.route('/', methods=['GET'])
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
@cross_origin()
def index():
    try:
        gre_score = float(request.form['gre_score'])
        toefl_score = float(request.form['toefl_score'])
        university_rating = float(request.form['university_rating'])
        sop = float(request.form['sop'])
        lor = float(request.form['lor'])
        cgpa = float(request.form['cgpa'])
        research = 1 if request.form['research'] == 'yes' else 0

        prediction = model.predict([[gre_score,toefl_score,university_rating,sop,lor,cgpa,research]])

        return render_template('result.html', prediction=round(100 * prediction[0]))

    except Exception as e:
        return str(e)

if __name__ == "__main__":
     port = int(os.environ.get("PORT", 8080))
     app.run(host="0.0.0.0", port=port)
