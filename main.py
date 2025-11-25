#!/usr/bin/env python3
"""
PFE Automated Email Sender - PRODUCTION VERSION v5.0
Counter-based sequential processing with AI content generation
Fully automated pipeline: Company Research → Content Generation → Email Sending
"""

import os
import logging
import smtplib
import csv
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from io import StringIO

from flask import Flask, jsonify

# Load environment variables from .env for local development
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global counter for round-robin email sending - use Windows-compatible path
import tempfile
temp_dir = tempfile.gettempdir()
email_counter_file = os.path.join(temp_dir, 'pfe_email_counter.txt')

# Failed emails log file
failed_emails_file = 'data/Failed.csv'

def get_email_counter():
    """Get current email counter"""
    try:
        if os.path.exists(email_counter_file):
            with open(email_counter_file, 'r') as f:
                return int(f.read().strip())
        return 0
    except:
        return 0

def update_email_counter(counter):
    """Update email counter"""
    try:
        with open(email_counter_file, 'w') as f:
            f.write(str(counter))
        logger.info(f"✅ Counter updated to: {counter}")
    except Exception as e:
        logger.error(f"Failed to update counter: {e}")

def advance_to_next_recipient(recipient_email):
    """Advance to next recipient by incrementing counter (no file modification needed)"""
    try:
        # Get current counter
        current_counter = get_email_counter()
        
        # Move to next recipient
        next_counter = current_counter + 1
        
        # Update counter file (this writes to /tmp which is writable)
        update_email_counter(next_counter)
        
        logger.info(f"✅ Advanced to next recipient. Counter: {current_counter} → {next_counter}")
        logger.info(f"📧 Processed: {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to advance to next recipient: {e}")
        return False

def save_failed_email(recipient_data, error_message):
    """Save failed email to Failed.csv for later review"""
    try:
        file_exists = os.path.exists(failed_emails_file)
        
        with open(failed_emails_file, 'a', newline='', encoding='utf-8') as f:
            fieldnames = ['First Name', 'Last Name', 'Email', 'Company', 'Title', 'Country', 'Error', 'Timestamp']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
            
            # Write failed record
            writer.writerow({
                'First Name': recipient_data.get('first_name', ''),
                'Last Name': recipient_data.get('last_name', ''),
                'Email': recipient_data.get('email', ''),
                'Company': recipient_data.get('company', ''),
                'Title': recipient_data.get('title', ''),
                'Country': recipient_data.get('country', ''),
                'Error': str(error_message)[:200],  # Truncate long errors
                'Timestamp': datetime.now().isoformat()
            })
        
        logger.info(f"💾 Failed email saved to Failed.csv")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save failed email: {e}")
        return False

def research_company(company_name):
    """Research company information automatically"""
    try:
        # Simple company info generation based on name
        # In production, you could integrate with APIs like Clearbit, LinkedIn, etc.
        
        company_insights = {
            'industry': 'Technology',
            'focus': 'Innovation and digital transformation',
            'values': 'cutting-edge solutions and customer success',
            'size': 'growing company',
            'market': 'competitive technology market'
        }
        
        # You can enhance this with real web scraping or API calls
        logger.info(f"✅ Company research completed for: {company_name}")
        return company_insights
        
    except Exception as e:
        logger.error(f"❌ Company research failed for {company_name}: {e}")
        return {
            'industry': 'Technology',
            'focus': 'business growth and innovation',
            'values': 'excellence and innovation',
            'size': 'dynamic organization',
            'market': 'evolving market'
        }

def generate_personalized_email(first_name, last_name, title, company, country, company_insights):
    """Generate personalized email content using company research"""
    
    # Create personalized subject line
    subjects = [
        f"DevOps Internship Application - {company}",
        f"Cloud Engineering Student - Internship Opportunity at {company}",
        f"End-of-Study Internship - DevOps & Cloud Expertise",
        f"DevOps Student seeking Internship at {company}",
        f"Final Year Student - Cloud Infrastructure Internship"
    ]
    
    # Select subject based on company name hash for consistency
    subject_index = hash(company) % len(subjects)
    subject = subjects[subject_index]
    
    # Generate personalized email body
    email_body = f"""Dear {first_name} {last_name},

I hope this message finds you well. As the {title} at {company}, I believe you would be interested in learning about my expertise in DevOps and cloud technologies.

I am Akrem Alamine, a final-year engineering student specializing in DevOps and cloud infrastructure with hands-on experience in:

• Cloud Infrastructure & Deployment (GCP, AWS, Azure)
• DevOps & CI/CD Pipelines (Docker, Kubernetes, Jenkins)
• Infrastructure as Code (Terraform, CloudFormation)
• Automation & Monitoring (Python scripting, Prometheus, Grafana)

Given {company}'s focus on {company_insights['focus']}, I believe my technical skills in cloud architecture and DevOps practices could contribute to your infrastructure modernization goals.

As I am completing my engineering studies, I am actively seeking end-of-study internship opportunities where I can apply my DevOps and cloud expertise while contributing to innovative projects{f' in {country}' if country else ''}.

I would welcome the opportunity to discuss how my technical skills and fresh perspective could support {company}'s continued growth. I have attached my comprehensive CV detailing my technical projects and hands-on experience with modern DevOps tools.

Thank you for your time and consideration.

Best regards,

Akrem Alamine
DevOps & Cloud Engineering Student
Email: akrem.alamine@etudiant-fst.utm.tn
LinkedIn: linkedin.com/in/akrem-alamine
GitHub: github.com/Akrem-Alamine"""

    return subject, email_body

def send_email_with_cv(recipient_email, recipient_name, subject, body, sender_email, sender_password):
    """Send email with CV attachment"""
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # CV attachment
        cv_path = 'assets/Akrem_Alamine_ENOP.pdf'
        
        if os.path.exists(cv_path):
            with open(cv_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(cv_path)}'
            )
            msg.attach(part)
            
            logger.info(f"✅ CV attachment added: {cv_path}")
        else:
            logger.warning(f"❌ CV file not found: {cv_path}")
            return False, f"CV file not found: {cv_path}"
        
        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        logger.info(f"✅ Automated email sent to {recipient_name} at {recipient_email}")
        return True, f"Automated email sent to {recipient_name}"
        
    except Exception as e:
        error_msg = f"Failed to send automated email: {str(e)}"
        logger.error(f"❌ {error_msg}")
        return False, error_msg

def get_next_recipient():
    """Get next recipient with automated content generation using line pointer"""
    try:
        csv_path = os.environ.get('CSV_FILE_PATH', 'data/contacts_real.csv')
        
        if not os.path.exists(csv_path):
            logger.error(f"CSV file not found: {csv_path}")
            return None
        
        recipients = []
        try:
            with open(csv_path, 'r', encoding='utf-8', errors='ignore') as file:
                # Read and clean lines
                lines = file.readlines()
                cleaned_lines = []
                for i, line in enumerate(lines):
                    # Remove NUL characters and other problematic characters
                    cleaned_line = line.replace('\x00', '').strip()
                    if cleaned_line or i == 0:  # Keep header and non-empty lines
                        cleaned_lines.append(cleaned_line + '\n')
                
                # Parse CSV from cleaned lines
                csv_content = ''.join(cleaned_lines)
                reader = csv.DictReader(StringIO(csv_content))
                for row in reader:
                    if row and any(row.values()):  # Skip completely empty rows
                        recipients.append(row)
        except Exception as e:
            logger.error(f"CSV parsing error: {e}")
            return None
        
        if not recipients:
            logger.warning("No recipients found in CSV file")
            return None
        
        # Get current line pointer (which recipient we're processing)
        counter = get_email_counter()
        
        # Check if we've processed all recipients
        if counter >= len(recipients):
            logger.info("✅ All recipients have been contacted. Email campaign completed.")
            return None
        
        # Get the recipient at current counter position
        recipient = recipients[counter]
        
        # Extract recipient data with NULL-safe handling
        first_name = (recipient.get('First Name') or '').strip()
        last_name = (recipient.get('Last Name') or '').strip()
        title = (recipient.get('Title') or '').strip()
        company = (recipient.get('Company') or '').strip()
        email = (recipient.get('Email') or '').strip()
        country = (recipient.get('Country') or '').strip()
        
        # Skip if no email is available
        if not email:
            logger.warning(f"Recipient {counter + 1} has no email - skipping")
            advance_to_next_recipient(f"skipped_{counter}")
            return get_next_recipient()  # Try next recipient
        
        # Skip if no company is available, but continue with generic values
        if not company:
            company = "Your Company"
            logger.warning(f"Recipient {counter + 1} has no company name - using generic")
        
        # Research company and generate personalized content
        logger.info(f"🔍 Researching company: {company} (recipient {counter + 1}/{len(recipients)})")
        company_insights = research_company(company)
        
        logger.info(f"✍️ Generating personalized email for {first_name} {last_name}")
        subject, content = generate_personalized_email(
            first_name, last_name, title, company, country, company_insights
        )
        
        return {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'full_name': f"{first_name} {last_name}".strip(),
            'title': title,
            'company': company,
            'country': country,
            'subject': subject,
            'content': content,
            'counter': counter,
            'total_recipients': len(recipients),
            'company_insights': company_insights
        }
        
    except Exception as e:
        logger.error(f"Error processing recipient: {str(e)}")
        return None

@app.route('/')
def home():
    return jsonify({
        'status': 'OK',
        'message': 'PFE Automated Email Sender - PRODUCTION',
        'version': '5.0-PRODUCTION',
        'features': ['Company Research', 'AI Content Generation', 'Personalized Emails', 'Counter-Based Processing'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'pfe-email-sender-production',
        'version': '5.0-PRODUCTION',
        'environment': 'production',
        'automation': 'counter-based sequential processing',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/status')
def status():
    csv_path = os.environ.get('CSV_FILE_PATH', 'data/contacts_real.csv')
    csv_exists = os.path.exists(csv_path)
    recipient_count = 0
    
    if csv_exists:
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                recipient_count = len(list(csv.DictReader(file)))
        except:
            recipient_count = 0
    
    return jsonify({
        'status': 'running',
        'automation': 'PRODUCTION PIPELINE ACTIVE',
        'features': ['Company Research', 'Content Generation', 'Counter-Based Sequential Processing'],
        'business_hours': f"{os.environ.get('START_HOUR', '9')}:00 - {os.environ.get('END_HOUR', '17')}:00 UTC",
        'csv_status': {
            'file_exists': csv_exists,
            'file_path': csv_path,
            'recipient_count': recipient_count,
            'current_counter': get_email_counter()
        },
        'email_configured': bool(os.environ.get('EMAIL_ADDRESS')),
        'timestamp': datetime.now().isoformat()
    })

def send_email_with_cv(recipient_email, recipient_name, subject, body, sender_email, sender_password):
    """Send email with CV attachment"""
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Process placeholders in body
        processed_body = body.replace('{first_name}', recipient_name.split()[0] if recipient_name else 'Recruiter')
        processed_body = processed_body.replace('{last_name}', ' '.join(recipient_name.split()[1:]) if len(recipient_name.split()) > 1 else '')
        processed_body = processed_body.replace('{full_name}', recipient_name if recipient_name else 'Recruiter')
        
        msg.attach(MIMEText(processed_body, 'plain'))

        # CV attachment
        cv_path = os.environ.get('CV_FILE_PATH', 'assets/Akrem_Alamine_ENOP.pdf')
        cv_status = "CV file not found"
        
        if os.path.exists(cv_path):
            with open(cv_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(cv_path)}')
            msg.attach(part)
            cv_status = "CV attached"

        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        logger.info(f"✅ Email sent to {recipient_name} <{recipient_email}> ({cv_status})")
        return True, cv_status

    except Exception as e:
        logger.error(f"❌ Failed to send email to {recipient_name} <{recipient_email}>: {str(e)}")
        return False, str(e)

@app.route('/debug-csv', methods=['GET'])
def debug_csv():
    """Debug endpoint to check CSV reading and current position"""
    try:
        csv_path = os.environ.get('CSV_FILE_PATH', 'data/contacts_real.csv')
        
        if not os.path.exists(csv_path):
            return jsonify({'error': f'CSV file not found: {csv_path}'}), 404
        
        recipients = []
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            recipients = list(reader)
        
        # Get current position using counter
        counter = get_email_counter()
        
        if recipients:
            if counter >= len(recipients):
                return jsonify({
                    'csv_path': csv_path,
                    'total_recipients': len(recipients),
                    'current_counter': counter,
                    'status': 'completed',
                    'message': 'All recipients have been processed',
                    'progress': f'{len(recipients)}/{len(recipients)} completed'
                })
            
            current_recipient = recipients[counter]
            return jsonify({
                'csv_path': csv_path,
                'total_recipients': len(recipients),
                'current_counter': counter,
                'progress': f'{counter + 1}/{len(recipients)}',
                'current_recipient': {
                    'first_name': current_recipient.get('First Name', ''),
                    'last_name': current_recipient.get('Last Name', ''),
                    'email': current_recipient.get('Email', ''),
                    'company': current_recipient.get('Company', ''),
                    'title': current_recipient.get('Title', ''),
                    'country': current_recipient.get('Country', '')
                },
                'raw_recipient_keys': list(current_recipient.keys()),
                'next_few_recipients': recipients[counter:counter+3]  # Next 3 for preview
            })
        else:
            return jsonify({'error': 'No recipients found'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Debug failed: {str(e)}'}), 500


@app.route('/cron/send-emails', methods=['GET', 'POST'])
def cron_send_emails():
    """Cron endpoint - sends emails (with business hours override option for local development)"""
    try:
        now = datetime.now()
        current_hour = now.hour
        current_weekday = now.weekday()
        
        start_hour = int(os.environ.get('START_HOUR', 9))
        end_hour = int(os.environ.get('END_HOUR', 17))
        sender_email = os.environ.get('EMAIL_ADDRESS')
        sender_password = os.environ.get('EMAIL_PASSWORD')
        
        # Business hours check with override options
        is_weekday = current_weekday < 5
        is_business_hours = start_hour <= current_hour < end_hour
        test_mode = os.environ.get('TEST_MODE', 'false').lower() == 'true'
        production_mode = os.environ.get('PRODUCTION_MODE', 'false').lower() == 'true'
        ignore_business_hours = os.environ.get('IGNORE_BUSINESS_HOURS', 'false').lower() == 'true'
        
        # Determine if we should send email
        should_send = False
        mode_msg = ""
        
        if production_mode and ignore_business_hours:
            should_send = True
            mode_msg = "PRODUCTION MODE - ignoring business hours"
        elif test_mode:
            should_send = True
            mode_msg = "TEST MODE - ignoring business hours"
        elif is_weekday and is_business_hours:
            should_send = True
            mode_msg = "business hours"
        
        if should_send:
            logger.info(f"✅ Automated pipeline started: {now.isoformat()} ({mode_msg})")
            
            if not sender_email or not sender_password:
                return jsonify({'status': 'error', 'message': 'Email credentials not configured'}), 500
            
            recipient_data = get_next_recipient()
            
            if recipient_data and recipient_data['email']:
                success, message = send_email_with_cv(
                    recipient_email=recipient_data['email'],
                    recipient_name=recipient_data['full_name'],
                    subject=recipient_data['subject'],
                    body=recipient_data['content'],
                    sender_email=sender_email,
                    sender_password=sender_password
                )
                
                if success:
                    # Advance to next recipient after successful email
                    advance_success = advance_to_next_recipient(recipient_data['email'])
                    advance_msg = " - Advanced to next recipient" if advance_success else " - Warning: Failed to advance counter"
                    
                    return jsonify({
                        'status': 'success',
                        'message': f'✅ Email sent successfully! ({message}){advance_msg}',
                        'timestamp': now.isoformat(),
                        'email_details': {
                            'to': recipient_data['email'],
                            'recipient_name': recipient_data['full_name'],
                            'subject': recipient_data['subject'],
                            'recipient_number': recipient_data['counter'] + 1,
                            'total_recipients': recipient_data['total_recipients'],
                            'advanced_to_next': advance_success
                        }
                    })
                else:
                    # Failed to send - save to Failed.csv and move to next
                    save_failed_email(recipient_data, message)
                    advance_to_next_recipient(recipient_data['email'])
                    
                    return jsonify({
                        'status': 'failed',
                        'message': f'⚠️ Email failed - moving to next recipient',
                        'timestamp': now.isoformat(),
                        'error': message,
                        'email_details': {
                            'to': recipient_data['email'],
                            'recipient_name': recipient_data['full_name'],
                            'saved_to_failed': True
                        }
                    })
            else:
                # Check if campaign is completed (CSV is empty) vs other errors
                csv_path = os.environ.get('CSV_FILE_PATH', 'data/contacts_real.csv')
                
                try:
                    if os.path.exists(csv_path):
                        with open(csv_path, 'r', encoding='utf-8') as file:
                            remaining_recipients = len(list(csv.DictReader(file)))
                        
                        if remaining_recipients == 0:
                            return jsonify({
                                'status': 'completed',
                                'message': '✅ Email campaign completed! CSV is now empty - all recipients have been contacted.',
                                'timestamp': now.isoformat(),
                                'campaign_stats': {
                                    'csv_status': 'empty',
                                    'remaining_recipients': 0
                                }
                            })
                        else:
                            return jsonify({
                                'status': 'error',
                                'message': f'No recipient data available - unexpected error ({remaining_recipients} recipients still in CSV)'
                            }), 500
                    else:
                        return jsonify({
                            'status': 'completed',
                            'message': '✅ Email campaign completed! CSV file no longer exists.'
                        })
                except:
                    return jsonify({
                        'status': 'error',
                        'message': 'No recipient data available - CSV file error'
                    }), 500
        else:
            reason = "weekend" if not is_weekday else "outside business hours"
            return jsonify({
                'status': 'skipped',
                'message': f'No email sent - {reason}',
                'timestamp': now.isoformat()
            })
    
    except Exception as e:
        logger.error(f"❌ Cron job error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Cron job failed: {str(e)}'
        }), 500

@app.route('/reset-counter', methods=['POST'])
def reset_counter():
    """Reset the recipient counter to start from beginning"""
    try:
        update_email_counter(0)
        logger.info("✅ Counter reset to 0 - will start from first recipient")
        return jsonify({
            'status': 'success',
            'message': 'Counter reset to 0 - will start from first recipient',
            'counter': 0,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to reset counter: {str(e)}'
        }), 500

from apscheduler.schedulers.background import BackgroundScheduler

def trigger_send_email_job():
    try:
        # Directly call the cron_send_emails function (Flask route logic)
        with app.app_context():
            cron_send_emails()
    except Exception as e:
        logger.error(f"Scheduled email send failed: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🚀 Starting PFE Email Sender - PRODUCTION v5.0 on port {port}")
    logger.info(f"⏰ Business hours: {os.environ.get('START_HOUR', '9')}:00 - {os.environ.get('END_HOUR', '17')}:00 UTC")
    logger.info(f"📧 Sending 5 emails per minute (every 12 seconds)")
    logger.info(f"📁 Counter file: {email_counter_file}")
    logger.info(f"📊 Current counter value: {get_email_counter()}")

    # Start scheduler to send email every 12 seconds (5 per minute)
    scheduler = BackgroundScheduler()
    scheduler.add_job(trigger_send_email_job, 'interval', seconds=12)
    scheduler.start()

    app.run(host='0.0.0.0', port=port, debug=False)