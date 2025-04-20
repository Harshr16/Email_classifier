**Email Classification and PII Masking API**  

This project is a FastAPI-based application that classifies emails into categories and masks personally identifiable information (PII) such as full names, phone numbers, credit card numbers, Aadhaar numbers, CVVs, expiry dates, and more.  


**i) Features**  

- Classifies emails into predefined categories  
- Masks PII entities in the email text using regex  
- Returns original email, masked email, list of masked entities, and predicted category  
- Built with Logistic Regression and TF-IDF for fast, efficient inference  

**ii) Model**  

The model is a `LogisticRegression` classifier trained using `TF-IDF` features. It's saved as:  

- `logreg_model.pkl`  
- `label_encoder.pkl`  
- `tfidf_vectorizer.pkl`  


**iii) Requirements**  

Make sure you have Python 3.7+ and install the required libraries:  


**iv) Accepted PII Formats**  

The system detects and masks the following types of personally identifiable information (PII):

**1. Full Name** 

Detected using phrases like:  
- "my name is", "this is", "i am", "i'm"

Example matches:  
- My name is Frank A. Decosta  
- I'm Priya R. Sharmma  
- This is Raj Kumar 

**2. Phone Number**  

Formats accepted:  
- 9876543210  
- +91 9876543210  
- 09876543210  

**3. Aadhaar Number**  

Must be exactly 12 digits (not part of a longer sequence)  

Formats accepted:
- 1234 5678 9012
- 1234-5678-9012
- 123456789012

**4. Credit/Debit Card Number**

Must be 16 digits 

Formats accepted:  
- 1234 5678 1234 5678  
- 1234-5678-1234-5678  
- 1234.5678.1234.5678  
- 1234_5678_1234_5678 

**5. Email**

Standard email pattern:  
- example@email.com  
- test@gmail.com  

**6. CVV**

Must be 3 digits and follow keywords like:  
- "cvv", "cvv code", "cvv is", "cvv: 123" 

Examples:  
- CVV: 123  
- CVV code is 456  

**7. Date of Birth (DOB)**  

Accepted formats:  
- DD/MM/YYYY, DD-MM-YYYY  
- DDMMYYYY (no separators)
  
Examples:  
- 23/10/1998  
- 23101998  
- 23-10-1998  

**8. Expiry Date**  

Keyword triggers like:  
- "expiry date is", "expiry dates are", "expires on", "expire on", "ends on"  

Accepted formats:  
- MM/YY, MM/YYYY, MM-YY, MM-YYYY
  
Example matches:  
- Expiry date is 05/25  
- Expires on 06-2024  
- Expiry dates are 05/25 and 06-30


**v)  How to Run the Application**  

Follow these steps to set up and run the application locally:  

**Step 1: Install Dependencies**  

pip install -r requirements.txt  

 **Step 2: Train the Model**  
 
 python train_model.py

This will generate:  

- logreg_model.pkl
- tfidf_vectorizer.pkl
- label_encoder.pkl


**Step 3: Start the FastAPI Server**  

python -m uvicorn app:app --reload    

The API will be running at:   
- http://127.0.0.1:8000/docs#/default/classify_email_route_classify_post


**vi) API Endpoint Usage**  

**Click on POST /classify_email.**  

**Click the "Try it out" button.**  

**Input JSON**   

{
  "email_text": "My name is Rahul Singh and my CVV is 123. Card number is 1234 5678 9012 3456."
}  

**Output JSON**  

{
  "input_email_body": "...",
  "list_of_masked_entities": [...],
  "masked_email": "...",
  "category_of_the_email": "..."
}  

**vii) API Deployment & Usage**  

Deployed API (Hugging Face Spaces): 

https://harshr16-email-classifier-api.hf.space/classify  

**viii)How to Use the API via POST Request (e.g., Postman):**  

To use the API, send a POST request to:  

https://harshr16-email-classifier-api.hf.space/classify  

Request Body (JSON): 

{
  "email_text": "Hi my name is Harsh Rudani. My phone is 9876543210 and CVV is 123."
}  

Response (JSON):  

{
  "input_email_body": "...",
  "list_of_masked_entities": [...],
  "masked_email": "...",
  "category_of_the_email": "..."
}  




