from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def train_sentiment_model(df):
    data = df[df["Review"].str.strip().ne("")].copy()
    X_train, X_test, y_train, y_test = train_test_split(
        data["Review"], data["Sentiment"], test_size=0.20,
        random_state=42, stratify=data["Sentiment"]
    )
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1,2), max_features=3000)),
        ("nb", MultinomialNB())
    ])
    pipeline.fit(X_train, y_train)
    pred = pipeline.predict(X_test)
    metrics = {
        "Accuracy": round(float(accuracy_score(y_test, pred)), 3),
        "Precision": round(float(precision_score(y_test, pred, average="weighted", zero_division=0)), 3),
        "Recall": round(float(recall_score(y_test, pred, average="weighted", zero_division=0)), 3),
        "F1": round(float(f1_score(y_test, pred, average="weighted", zero_division=0)), 3),
    }
    return {"model": pipeline, "metrics": metrics}

def predict_sentiment(bundle, text):
    model = bundle["model"]
    label = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]
    confidence = float(max(probabilities))
    return label, confidence
