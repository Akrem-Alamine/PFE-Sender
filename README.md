# Data Engineering Automated Email Sender - Mayez Ghouma

## 📅 Overview
Automated email sender for MLOps and Data Engineering internship applications. Sends personalized recruitment emails during business hours (Monday-Friday, 9 AM - 5 PM UTC) using CSV recipient data. Designed for Mayez Ghouma, Data Engineering student seeking internships in Data Science, AI, and MLOps.

## ✅ Features
- **Business Hours Only**: Emails sent Monday-Friday, 9 AM - 5 PM UTC
- **Round-Robin Recipients**: Cycles through CSV recipients automatically  
- **CV Attachment**: Includes Mayez Ghouma's CV in every email
- **MLOps Personalization**: Tailored content for Data Engineering, AI, and MLOps positions
- **GCP Deployment**: Ready for Google Cloud Platform
- **Cron Automation**: Sends 1 email per minute during business hours
- **AI Content Generation**: Automated personalization for data science roles

## 🚀 Quick Deployment

### 1. Upload to GitHub
```bash
git clone https://github.com/Akrem-Alamine/PFE-Sender.git
cd PFE-Sender
```

### 2. Deploy to GCP
```bash
# Deploy application
gcloud app deploy app.yaml --quiet

# Deploy cron jobs  
gcloud app deploy deployment/cron.yaml --quiet
```

### 3. Test System
```bash
# Test health
curl https://your-project.uc.r.appspot.com/health

# Test manual email
curl -X POST https://your-project.uc.r.appspot.com/test-email

# Check status
curl https://your-project.uc.r.appspot.com/status
```

## 📁 File Structure
```
PFE-Sender/
├── main.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── app.yaml               # GCP configuration
├── data/
│   └── contacts_real.csv   # Email recipients data
├── assets/
│   └── cv_Mayez-Ghouma.pdf  # Mayez Ghouma's CV attachment
└── deployment/
    └── cron.yaml         # Cron job configuration
```

## 📧 CSV Format
The `data/recipients.csv` file should have these columns:
- `first_name`: Recipient's first name
- `last_name`: Recipient's last name
- `email`: Recipient's email address (all set to akrem.alamine@etudiant-fst.utm.tn for testing)
- `subject`: Email subject line
- `content`: Email body with placeholders ({first_name}, {last_name}, {full_name})

## 🎯 Expected Behavior
- **Data Engineering Focus**: System targets MLOps, Data Science, and AI positions
- **Personalized Content**: Emails tailored for data engineering internships
- **Business Hours Only**: No emails sent on weekends or outside 9 AM - 5 PM UTC
- **1 Email/Minute**: During business hours, sends 1 personalized email per minute
- **CV Attached**: Every email includes Mayez Ghouma's CV PDF attachment
- **MLOps Expertise**: Content emphasizes data pipelines, ML operations, and big data

## 🔧 Configuration
Environment variables are set in `app.yaml`:
- `EMAIL_ADDRESS`: mayez.ghouma@etudiant-fst.utm.tn
- `EMAIL_PASSWORD`: [App-specific password]
- `START_HOUR`: 0 (Testing mode - 24/7)
- `END_HOUR`: 23 (Testing mode - 24/7)
- `CSV_FILE_PATH`: data/contacts_real.csv
- `CV_FILE_PATH`: assets/cv_Mayez-Ghouma.pdf

## 🎉 Success Indicators
1. ✅ Health check returns status "healthy"
2. ✅ Status shows correct recipient count (10)
3. ✅ Test email sends successfully with CV attached
4. ✅ Cron jobs skip during off-hours and weekends
5. ✅ During business hours, emails are sent every minute