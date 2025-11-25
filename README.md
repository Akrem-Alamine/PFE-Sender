# 📧 PFE Automated Email Sender - Local Deployment

A Python Flask application that automatically sends personalized recruitment emails to multiple recipients from a CSV file. Runs locally on Windows with scheduled email sending every 12 seconds (5 emails per minute).

## ✨ Features

- ✅ **Local Deployment** - Runs on Windows without GCP dependency
- ✅ **Automatic Scheduling** - Sends 5 emails per minute (every 12 seconds)
- ✅ **CSV-based Recipients** - Read recipients from `data/contacts_real.csv`
- ✅ **CV Attachment** - Automatically attach PDF to every email
- ✅ **Personalized Content** - Generate personalized emails with recipient names
- ✅ **Error Handling** - Failed emails saved to `data/Failed.csv`, process continues
- ✅ **Windows Compatible** - Uses Windows temp directory for counter persistence
- ✅ **Production Mode** - Ignores business hours, sends 24/7
- ✅ **Email Template** - Professional recruitment email with dynamic content

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Windows 10/11
- Valid Gmail account with App Password

### 1. Installation

```powershell
# Clone the repository
git clone https://github.com/Akrem-Alamine/PFE-Sender.git
cd Akrem-Devops-PFE-Sender

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Update `.env` file with your credentials:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
CSV_FILE_PATH=data/contacts_real.csv
CV_FILE_PATH=assets/Akrem_Alamine_ENOP.pdf
START_HOUR=0
END_HOUR=23
PRODUCTION_MODE=true
IGNORE_BUSINESS_HOURS=true
```

**Gmail Setup:**
1. Enable 2-factor authentication on your Google Account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the 16-character app password in `EMAIL_PASSWORD`

### 3. Prepare CSV File

Your `data/contacts_real.csv` should have columns:
- `First Name` - Recipient's first name
- `Last Name` - Recipient's last name
- `Email` - Recipient's email address (must be valid)
- `Company` - Company name (optional)
- `Title` - Job title (optional)
- `Country` - Country (optional)

**Example:**
```csv
First Name,Last Name,Title,Company,Email,Country
Karl,Ai,Co-founder and CEO,Reliant AI,kmh@reliant.ai,Germany
Didier,Bourdenet,Product Manager AI,Inarix,didier@inarix.com,France
```

### 4. Run the Application

```powershell
python main.py
```

Expected output:
```
2025-11-24 17:21:00,813 - INFO - 🚀 Starting PFE Email Sender - PRODUCTION v5.0 on port 8080
2025-11-24 17:21:00,813 - INFO - 📧 Sending 5 emails per minute (every 12 seconds)
2025-11-24 17:21:00,813 - INFO - 📁 Counter file: C:\Users\akrem\AppData\Local\Temp\pfe_email_counter.txt
2025-11-24 17:21:00,813 - INFO - 📊 Current counter value: 0
2025-11-24 17:21:12,108 - INFO - ✅ Automated pipeline started: 2025-11-24T17:21:12.108516 (PRODUCTION MODE - ignoring business hours)
2025-11-24 17:21:12,165 - INFO - 🔍 Researching company: Reliant AI (recipient 1/16614)
2025-11-24 17:21:12,165 - INFO - ✍️ Generating personalized email for Karl Ai
2025-11-24 17:21:12,848 - INFO - ✅ Email sent to Karl Ai <kmh@reliant.ai> (CV attached)
```

## 📁 Project Structure

```
Akrem-Devops-PFE-Sender/
├── main.py                      # Main Flask application
├── requirements.txt             # Python dependencies
├── .env                         # Environment configuration
├── README.md                    # This file
├── data/
│   ├── contacts_real.csv        # Recipients list (17,000+ contacts)
│   └── Failed.csv               # Failed emails log (auto-generated)
├── assets/
│   └── Akrem_Alamine_ENOP.pdf   # CV attachment
├── deployment/
│   └── cron.yaml               # GCP cron config (optional)
└── app.yaml                    # GCP config (optional)
```

## 🔧 API Endpoints

### Health Check
```bash
curl http://127.0.0.1:8080/health
```

### Status
```bash
curl http://127.0.0.1:8080/status
```
Shows current progress and recipient count.

### Send Email (Manual)
```bash
curl -X POST http://127.0.0.1:8080/cron/send-emails
```

### Debug CSV
```bash
curl http://127.0.0.1:8080/debug-csv
```
Shows current recipient and next 3 in queue.

### Reset Counter
```bash
curl -X POST http://127.0.0.1:8080/reset-counter
```
Reset to first recipient (starts from 0).

## 📊 How It Works

1. **Scheduler** - APScheduler triggers job every 12 seconds
2. **CSV Reading** - Reads next recipient from `contacts_real.csv`
3. **NUL Handling** - Automatically removes NUL characters from corrupted CSV data
4. **Email Generation** - Creates personalized email with recipient's name
5. **SMTP Sending** - Sends via Gmail SMTP with CV attachment
6. **Counter Update** - Increments counter for next recipient
7. **Error Handling** - If email fails:
   - Saves to `Failed.csv` with error details
   - Moves to next recipient automatically
   - Continues processing

## ⚠️ Error Handling

Invalid emails are automatically:
1. Detected during sending
2. Logged to `data/Failed.csv` with error reason
3. Skipped (counter incremented)
4. Processing continues with next recipient

Example `Failed.csv`:
```csv
First Name,Last Name,Email,Company,Title,Country,Error,Timestamp
Patryk,Wlodarczyk,invalid-email@example,omniIT,CTO,Germany,Invalid email format,2025-11-24T17:21:00
```

## 🔄 Counter Persistence

- Counter file location: `C:\Users\{username}\AppData\Local\Temp\pfe_email_counter.txt`
- Tracks which recipient to send to next
- Survives application restarts
- Can be reset via `/reset-counter` endpoint

## 🛑 Stopping the Application

Press `CTRL+C` in the terminal to stop gracefully.

## 📈 Performance

- **Speed**: 5 emails per minute (12-second interval)
- **Rate**: At this rate, 16,615 recipients = ~56 hours
- **Reliability**: Failed emails logged, processing continues
- **Memory**: Minimal RAM usage, efficient CSV streaming

## 🐛 Troubleshooting

### Email Not Sending
1. Check `.env` credentials are correct
2. Verify Gmail App Password (not regular password)
3. Check `data/Failed.csv` for error details
4. Ensure CV file exists at `assets/Akrem_Alamine_ENOP.pdf`

### Counter Not Persisting
- Counter file is in Windows temp directory
- Don't manually delete `pfe_email_counter.txt`
- Use `/reset-counter` endpoint to reset if needed

### CSV Parsing Errors
- Script automatically handles NUL characters
- Invalid emails are skipped (moved to Failed.csv)
- Empty rows are ignored

### SMTP Errors
- "Invalid RFC 5321 address" → Email address in CSV is corrupted
- "5.7.8 Username and password not accepted" → Wrong Gmail credentials
- Check `Failed.csv` for detailed error messages

## 📝 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SMTP_SERVER` | smtp.gmail.com | Email server |
| `SMTP_PORT` | 587 | SMTP port |
| `EMAIL_ADDRESS` | - | Sender email |
| `EMAIL_PASSWORD` | - | Gmail App Password |
| `CSV_FILE_PATH` | data/contacts_real.csv | Recipients file |
| `CV_FILE_PATH` | assets/Akrem_Alamine_ENOP.pdf | CV attachment |
| `START_HOUR` | 0 | Business hours start (UTC) |
| `END_HOUR` | 23 | Business hours end (UTC) |
| `PRODUCTION_MODE` | true | Enable production mode |
| `IGNORE_BUSINESS_HOURS` | true | Send 24/7 |
| `TEST_MODE` | false | Override business hours |

## 🚢 Deployment Options

### Local Windows (Default)
```powershell
python main.py
```

### GCP App Engine (Optional)
```bash
gcloud app deploy app.yaml
gcloud app deploy deployment/cron.yaml
```

## 📦 Dependencies

- Flask 3.0.0 - Web framework
- APScheduler 3.10.4 - Job scheduling
- python-dotenv 1.0.1 - Environment variables
- requests 2.31.0 - HTTP requests
- gunicorn 21.2.0 - Production server

## 👨‍💻 Author

**Akrem Alamine**
- Email: akrem.alamine@etudiant-fst.utm.tn
- GitHub: https://github.com/Akrem-Alamine
- LinkedIn: linkedin.com/in/akrem-alamine

## 📄 License

This project is for personal recruitment purposes.

## 🎯 Recent Updates (v5.0)

✅ Converted to local Windows deployment (no GCP required)  
✅ Fixed NUL character handling in CSV  
✅ Implemented Windows-compatible counter persistence  
✅ Added Failed.csv error logging  
✅ Automatic retry with next recipient on failure  
✅ Production mode with 24/7 operation  
✅ 5 emails per minute scheduling (12-second intervals)

---

**Last Updated**: November 25, 2025  
**Repository**: https://github.com/Akrem-Alamine/Akrem-Devops-PFE-Sender
