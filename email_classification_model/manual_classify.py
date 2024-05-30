import json
import random
import argparse
from config import CLASSIFY_BATCH_SIZE, LABEL_MAP2, LABEL_MAP2_STR

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

def classify_emails(source, destination):
    """Classify or review and fix classifications for emails."""
    # Load the emails
    all_emails = load_emails(source)

    # Shuffle the emails
    random.shuffle(all_emails)

    # Load progress if available
    classified_emails = load_emails(destination)
    if classified_emails:
        print(f"{len(classified_emails)} previously classified")

    # Get the set of classified email ids
    classified_ids = {email['unique_id'] for email in classified_emails}

    def classify_emails_batch(emails, batch_size=CLASSIFY_BATCH_SIZE):
        """Manually classify a batch of emails."""
        classifications = []
        current_index = 0
        while current_index < len(emails):
            email = emails[current_index]
            if email['unique_id'] not in classified_ids:
                print(f"Subject: {email['subject']}")
                print(f"From: {email['from']}")
                print(f"Body: {email['body'][:500]}")  # Show first 500 characters of the body
                if 'predicted_label' in email:
                    print(f"Predicted: {email['predicted_label']}")
                print(f"Enter classification ({LABEL_MAP2_STR}): ", end='')
                label = input().strip().lower()
                if label == '':
                    if 'predicted_label' in email:
                        classifications.append({'unique_id': email['unique_id'], 'label': email['predicted_label']})
                    else:
                        print("No predicted label available. Please enter a classification.")
                        continue
                    current_index += 1
                elif label == 'x':
                    print("Ending classification session.")
                    break
                elif label == '.':
                    if classifications:
                        classifications.pop()
                        current_index -= 1
                        print("Backing up to reclassify the previous email.")
                    else:
                        print("No previous email to back up to.")
                elif label in LABEL_MAP2:
                    classifications.append({'unique_id': email['unique_id'], 'label': LABEL_MAP2[label]})
                    current_index += 1
                else:
                    print("Invalid input. Please enter a valid classification.")
                print('-' * 50)

                if len(classifications) >= batch_size:
                    break
            else:
                current_index += 1
        return classifications

    # Classify a batch of emails
    new_classifications = classify_emails_batch(all_emails, batch_size=CLASSIFY_BATCH_SIZE)
    classified_emails.extend(new_classifications)

    # Save progress
    save_emails(destination, classified_emails)

def main():
    """Main function to parse arguments and start the classification process."""
    parser = argparse.ArgumentParser(description='Manually classify emails for use in training/verifying classification model.')
    parser.add_argument('source', type=str, help='Emails to classify (JSON file)')
    parser.add_argument('destination', type=str, help='Classified emails (JSON file)')
    args = parser.parse_args()
    classify_emails(args.source, args.destination)

if __name__ == '__main__':
    main()
