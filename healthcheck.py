import os
import datetime
import csv
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Open the CSV file and read the URLs and do health checks and log results in the same csv file in another column
def health_check_and_log(csv_file_path):
    temp_file_path = csv_file_path + '.tmp'

    results = []
    with open(csv_file_path, mode='r', newline='') as csvfile, open(temp_file_path, mode='w', newline='') as temp_csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ['Status', 'Response Time (ms)', 'Checked At']
        writer = csv.DictWriter(temp_csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            url = row['website']
            try:
                start_time = datetime.datetime.now()
                response = requests.get(url, timeout=5)
                response_time = (datetime.datetime.now() - start_time).total_seconds() * 1000  # in milliseconds
                status = 'Healthy' if response.status_code == 200 else f'Unhealthy (Status Code: {response.status_code})'
            except requests.RequestException as e:
                status = f'Unhealthy (Error: {str(e)})'
                response_time = 'N/A'

            row['Status'] = status
            row['Response Time (ms)'] = response_time
            row['Checked At'] = datetime.datetime.now().isoformat()
            writer.writerow(row)
            results.append({"website": url, "status": status, "response_time": response_time, "checked_at": row['Checked At']})
    os.replace(temp_file_path, csv_file_path)
    return results

# Generate a simple email report from results
def generate_email_report(results):
    report_lines = ["Website Health Check Report\n"]
    for r in results:
        report_lines.append(f"{r['website']}: {r['status']} | Response Time: {r['response_time']} ms | Checked At: {r['checked_at']}")
    return "\n".join(report_lines)

# Send email with placeholder SMTP details
def send_email_report(subject, body, sender, recipient, smtp_server, smtp_port, smtp_user, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender, recipient, msg.as_string())
        print("Email report sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
# Example usage
# ...existing code...
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run website health checks and log to CSV.")
    parser.add_argument(
        "csv_file",
        nargs="?",
        default=r"C:\Users\KranthiVodnala\websites_url.csv",
    )
    parser.add_argument(
        "--send-email",
        action="store_true",
        help="Send email report after health check"
    )
    args = parser.parse_args()
    results = health_check_and_log(args.csv_file)

    if args.send_email:
        # Placeholder email details
        sender = "sender@example.com"
        recipient = "recipient@example.com"
        smtp_server = "smtp.example.com"
        smtp_port = 587
        smtp_user = "smtp_user"
        smtp_password = "smtp_password"
        subject = "Website Health Check Report"
        body = generate_email_report(results)
        send_email_report(subject, body, sender, recipient, smtp_server, smtp_port, smtp_user, smtp_password)
    # ...existing code...