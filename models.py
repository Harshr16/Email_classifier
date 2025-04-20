import pandas as pd
import re
import joblib
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# download stopwords if they  are not
nltk.download("punkt")
nltk.download("stopwords")

df = pd.read_csv("combined_emails_with_natural_pii.csv")
df = df[["email", "type"]].dropna()

stop_words = set(stopwords.words("english"))

def preprocess(text):
    # convert to lowercase
    text = text.lower()
    # remove subject from email 
    text = re.sub(r"subject:\s*", "", text)
    # remove special character
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = word_tokenize(text)
    # remove stopwords
    tokens = [word for word in tokens if word not in stop_words]
    # assembeling  all the  token again
    return " ".join(tokens)

df["clean_email"] = df["email"].apply(preprocess)

le = LabelEncoder()
df["label_encoded"] = le.fit_transform(df["type"])

vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
X = vectorizer.fit_transform(df["clean_email"])
y = df["label_encoded"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# model training
model = LogisticRegression(C=5.0, penalty='l2', solver='liblinear')
model.fit(X_train, y_train)
# model testing
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
# training result
print(f"Accuracy: {acc:.4f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_))


# saviing models
joblib.dump(model, "logreg_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
joblib.dump(le, "label_encoder.pkl")
