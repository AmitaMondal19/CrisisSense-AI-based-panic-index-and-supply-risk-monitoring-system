import joblib

# Load model
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def ml_predict(text):
    vec = vectorizer.transform([text])
    return model.predict_proba(vec)[0][1]