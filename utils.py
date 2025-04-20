import re
import joblib

# loading  model,vectorizer, and label_encoder
model = joblib.load("logreg_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# PII  masking and demmaksing
def mask_pii(text):
    pii_dict = {}

    patterns = [
    # credit card  or debit card- 16 digits grouped
    ("credit_debit_no", r"\b(?:\d{4}[-\s./_]?){3}\d{4}\b"),

    # phone number
    ("phone_number", r"(?:(?<=\s)|^)(?:\+91[\-\s]?|0)?[6-9]\d{9}\b"),

    # aadhar card number - specifically 12 digits
    ("aadhar_num", r"(?<!\+91)(?<!\d)(\d{4}[\s-]?\d{4}[\s-]?\d{4})(?!\d)"),
    # full name
    ("full_name", r"(?i)(?:my name is|this is|i am|i'm)\s+([a-zA-Z][a-zA-Z.]*\s+[a-zA-Z][a-zA-Z.]*\s+[a-zA-Z][a-zA-Z.]*)"), 

    
    # email
    ("email", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),

    # CVV - must follow keyword
    ("cvv_no", r"(?i)\bcvv(?:[\s\-]*code)?(?:\s*[:\-]?\s*|[\s]+is[\s]+)(\d{3})\b"),

    # DOB - multiple formats
    ("dob", r"\b\d{2}[\/\-]?\d{2}[\/\-]?\d{4}\b|\b\d{8}\b"),
    
    # Expiry - MMYY or MM/YYYY
   ("expiry_no", r"(?i)(?:exp(?:iry)?(?:\s*date)?s?\s*(?:is|are)?|expires?|expire\s*on|ends\s*(?:in|on)?)(?:\s*is|\s*on)?[:\-]?\s*((?:\b(0[1-9]|1[0-2])[/\-]?(?:\d{2}|\d{4})\b)(?:\s*(?:and|,)?\s*\b(0[1-9]|1[0-2])[/\-]?(?:\d{2}|\d{4})\b)*)")

]


    masked_text = text
    for key, pattern in patterns:
        for match in re.finditer(pattern, masked_text):
            value = match.group(0)
            tag = f"[{key}]"
            if key == "cvv_no":
                value = match.group(1)
            if key == "expiry_no":
                value = match.group(1)  
            if key == "full_name":
                value = match.group(1)
            if tag not in pii_dict:
                pii_dict[tag] = []

            pii_dict[tag].append(value)
            masked_text = masked_text.replace(value, tag, 1)


    return masked_text, pii_dict



def demask_email(masked_text, pii_dict):
    for tag, original in pii_dict.items():
        masked_text = masked_text.replace(tag, original)
    return masked_text


def classify_email(text: str) -> str:
    vector = vectorizer.transform([text])
    prediction = model.predict(vector)
    label = label_encoder.inverse_transform(prediction)[0]
    return label