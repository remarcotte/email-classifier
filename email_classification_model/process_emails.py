import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from text_cleaner import clean_text
from config import LABEL_MAP
import argparse

def load_emails(file_path):
    """Load emails from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: File {file_path} is not a valid JSON file.")
        return []

def save_emails(file_path, emails):
    """Save emails to a JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(emails, f, indent=4)
    except IOError:
        print(f"Error: Unable to write to file {file_path}.")

def process_emails(operation, emails_path, classifieds_path, model_path, output_path):
    """Process emails by training a model, predicting classifications, or both."""
    
    # Load new emails to classify
    new_emails = load_emails(emails_path)
    if not new_emails:
        print("No emails to process.")
        return

    # Prepare the new emails for classification
    combined_texts = []
    original_emails = []

    for email in new_emails:
        clean_subject = clean_text(email['subject'])
        clean_from = clean_text(email['from'])
        clean_mailbox = clean_text(email['mailbox'])
        # Keep the body as is, assuming it was already cleaned during extraction
        combined_text = f"{clean_subject} {clean_from} {email['body']} {clean_mailbox}"
        combined_texts.append({'unique_id': email['unique_id'], 'c_text': combined_text})

        # Keep original email fields
        original_emails.append({
            'unique_id': email['unique_id'],
            'subject': email['subject'],
            'from': email['from'],
            'body': email['body'],
            'mailbox': email['mailbox']
        })

    if operation != 'predict':
        # Load classified emails for training
        classified_emails = load_emails(classifieds_path)
        if not classified_emails:
            print("No classified emails found for training.")
            return

        X = []
        y = []
        # Extract features and labels from classified emails
        for classified in classified_emails:
            email = next((ct for ct in combined_texts if ct['unique_id'] == classified['unique_id']), None)
            if email:
                X.append(email['c_text'])
                y.append(LABEL_MAP[classified['label']])
            else:
                print(f"Warning: Email with unique_id {classified['unique_id']} not found in combined_texts.")

        # Vectorize the features
        vectorizer = TfidfVectorizer(max_features=5000)
        X = vectorizer.fit_transform(X).toarray()

        # Split the data for training and verification
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

        # Train the model
        model = MultinomialNB()
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_val)
        print(classification_report(y_val, y_pred))

        # Save the trained model and vectorizer
        try:
            joblib.dump(model, f"{model_path}/email_classification_model.pkl")
            joblib.dump(vectorizer, f"{model_path}/vectorizer.pkl")
        except IOError:
            print(f"Error: Unable to write models to {model_path}.")

    if operation != 'train':
        # Load the trained model and vectorizer from files if not just trained
        if operation == 'predict':
            try:
                model = joblib.load(f"{model_path}/email_classification_model.pkl")
                vectorizer = joblib.load(f"{model_path}/vectorizer.pkl")
            except:
                print("Error: Unable to load model and vectorizer.")
                return

        # Vectorize the combined text for prediction
        X_new = vectorizer.transform([email['c_text'] for email in combined_texts]).toarray()

        # Predict labels for the new emails
        predicted_labels = model.predict(X_new)

        # Map label indices back to label names
        label_map_inverse = {v: k for k, v in LABEL_MAP.items()}

        # Add predictions to original emails
        for email, label in zip(original_emails, predicted_labels):
            email['predicted_label'] = label_map_inverse[label]

        # Save the emails with predictions to a JSON file
        save_emails(output_path, original_emails)
        print(f"Predicted emails saved to '{output_path}'")

def main():
    """Main function to train model and/or batch classify emails."""
    parser = argparse.ArgumentParser(description='Train a model, predict classifications, or both.')
    parser.add_argument('operation', type=str, choices=['predict', 'train', 'both'], help='Operation to perform (predict, train, both)')
    parser.add_argument('source', type=str, help='Emails to classify (JSON file)')
    parser.add_argument('--classifieds', type=str, help='Classified emails (JSON file)')
    parser.add_argument('model_folder', type=str, help='Model folder')
    parser.add_argument('--output_path', type=str, help='Path to save output of predictions')
    args = parser.parse_args()

    process_emails(args.operation, args.source, args.classifieds, args.model_folder, args.output_path)

if __name__ == '__main__':
    main()
