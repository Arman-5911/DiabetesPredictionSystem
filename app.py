from flask import Flask, render_template, request
import joblib
import numpy as np
from models import db, Prediction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diabetes.db'
db.init_app(app)

# Load model & feature order
model = joblib.load("models/diabetes_model.joblib")
feature_order = joblib.load("models/feature_order.joblib")

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = [float(request.form[f]) for f in feature_order]
    input_data = np.array([data])
    prediction = model.predict(input_data)[0]

    result = "Diabetic" if prediction == 1 else "Not Diabetic"

    new_pred = Prediction(
        pregnancies=data[0],
        glucose=data[1],
        bloodpressure=data[2],
        skinthickness=data[3],
        insulin=data[4],
        bmi=data[5],
        dpf=data[6],
        age=data[7],
        result=result
    )
    db.session.add(new_pred)
    db.session.commit()

    return render_template("result.html", result=result)

@app.route("/history")
def history():
    all_preds = Prediction.query.all()
    diabetic_count = Prediction.query.filter_by(result="Diabetic").count()
    non_diabetic_count = Prediction.query.filter_by(result="Not Diabetic").count()

    chart_data = [diabetic_count, non_diabetic_count]

    return render_template("history.html",
                           predictions=all_preds,
                           chart_data=chart_data)

if __name__ == "__main__":
    app.run(debug=True)
