# 🚀 Data Engineering Email Sender - Mayez Ghouma Deployment Guide

## 📁 Repository Successfully Updated - MAYEZ GHOUMA PROFILE

### ✅ GitHub Repository Updated
Repository: `https://github.com/Akrem-Alamine/PFE-Sender`
Status: **Updated with Mayez Ghouma's Data Engineering Profile**

### 🗂️ Essential Files Only:
- ✅ `main.py` - Data Engineering Flask application (Mayez Ghouma profile)
- ✅ `app.yaml` - GCP App Engine configuration (Mayez Ghouma email & CV)
- ✅ `requirements.txt` - Minimal dependencies (Flask + gunicorn + requests)
- ✅ `data/contacts_real.csv` - Real recipient data for data engineering positions
- ✅ `assets/cv_Mayez-Ghouma.pdf` - Mayez Ghouma's CV attachment
- ✅ `deployment/cron.yaml` - Cron job configuration
- ✅ `README.md` - Updated documentation for data engineering focus
- ✅ `.gitignore` - Git ignore file

### ❌ Profile Changes Made:
- 🔄 Updated from Akrem Alamine (DevOps) to **Mayez Ghouma (Data Engineering)**
- 🔄 Email content focused on **MLOps, Data Engineering, and AI positions**
- 🔄 Skills updated to **data pipelines, big data, ML operations**
- 🔄 CV changed from `Akrem_Alamine_ENOP.pdf` to `cv_Mayez-Ghouma.pdf`
- 🔄 Email address updated to `mayez.ghouma@etudiant-fst.utm.tn`
- 🔄 All content personalized for data engineering internship applications

---

## 🎯 Deployment Strategy - Parallel GCP Services

### 🚀 DEPLOY AS SEPARATE SERVICE IN SAME GCP PROJECT

**This version will run alongside the existing PFE-Sender with these key differences:**
- 📧 **Different email profile**: Mayez Ghouma (Data Engineering)
- 🔄 **Reverse CSV processing**: Starts from BOTTOM → TOP, stops when reaching top
- 🎯 **Different service name**: Will be deployed as separate service
- ⚡ **Same GCP project**: Runs in parallel with existing system

### Step 1: ✅ Commit Current Changes
```bash
# Add all updated files
git add .

# Commit with clear message
git commit -m "Update profile: Mayez Ghouma - Data Engineering & MLOps

- Changed from Akrem Alamine (DevOps) to Mayez Ghouma (Data Engineering)
- Updated email content for MLOps and data engineering positions
- CV updated to cv_Mayez-Ghouma.pdf
- Email address: mayez.ghouma@etudiant-fst.utm.tn
- Skills focused on data pipelines, big data, ML operations
- CSV processing: BOTTOM to TOP (reverse order)
- Ready for parallel deployment alongside existing PFE-Sender"

# Push to GitHub
git push origin main
```

### Step 2: Deploy as Parallel Service in Same GCP Project
```bash
# Create new directory for parallel deployment
mkdir ~/PFE-Sender-DataEngineering
cd ~/PFE-Sender-DataEngineering

# Clone the updated repository with Mayez Ghouma's profile
git clone https://github.com/Akrem-Alamine/PFE-Sender.git .

# Verify the updated files are present
ls -la
cat app.yaml | grep EMAIL_ADDRESS  # Should show mayez.ghouma@etudiant-fst.utm.tn

# Update app.yaml for parallel deployment (different service name)
sed -i 's/service: default/service: mayez-data-engineering/g' app.yaml

# OR manually edit app.yaml to add:
# service: mayez-data-engineering

# Deploy as separate service in same project
gcloud app deploy app.yaml --quiet

# Deploy cron jobs for this service
gcloud app deploy deployment/cron.yaml --quiet
```

### 🔄 CSV Processing - BOTTOM to TOP (Reverse Order)
**Special Feature**: This version processes CSV from **last record to first record** and **stops when reaching the top**.

The system will:
1. 📊 **Start from bottom row** of contacts_real.csv
2. 🔄 **Work backwards** through recipients  
3. 🛑 **Stop when reaching the first row** (top of CSV)
4. ✅ **No looping** - one complete reverse pass through data

### Step 3: Verify Parallel Services
```bash
# Test Mayez's Data Engineering service
curl https://mayez-data-engineering-dot-pfe-sender.uc.r.appspot.com/health
curl https://mayez-data-engineering-dot-pfe-sender.uc.r.appspot.com/status

# Test original Akrem's service  
curl https://pfe-sender.uc.r.appspot.com/health
curl https://pfe-sender.uc.r.appspot.com/status

# Send manual test emails from both services
curl -X POST https://mayez-data-engineering-dot-pfe-sender.uc.r.appspot.com/test-email
curl -X POST https://pfe-sender.uc.r.appspot.com/test-email

# Monitor both service logs
gcloud app logs tail --service=mayez-data-engineering
gcloud app logs tail --service=default
```

## 📋 Verification Steps for Parallel Deployment

### Check Both Services Status
```bash
# List all services in the project
gcloud app services list

# Verify both services are running
gcloud app versions list

# Check service URLs
gcloud app browse --service=default  # Original Akrem's service
gcloud app browse --service=mayez-data-engineering  # New Mayez's service
```

### Monitor Email Sending from Both Services
1. **Original Service (Akrem)**: Processes CSV TOP to BOTTOM (normal order)
2. **New Service (Mayez)**: Processes CSV BOTTOM to TOP (reverse order)
3. Both services send **1 email per minute** during **work hours only**
4. Check logs: `gcloud app logs tail --service=mayez-data-engineering`

### 🎯 Key Differences Between Services
| Feature | Akrem (DevOps) | Mayez (Data Engineering) |
|---------|---------------|-------------------------|
| Email Address | akrem.alamine@etudiant-fst.utm.tn | mayez.ghouma@etudiant-fst.utm.tn |
| CV File | Akrem_Alamine_ENOP.pdf | cv_Mayez-Ghouma.pdf |
| Processing Order | TOP → BOTTOM | BOTTOM → TOP |
| Subject Focus | DevOps/Cloud | Data Engineering/MLOps |
| Service Name | default | mayez-data-engineering |
| URL | pfe-sender.uc.r.appspot.com | mayez-data-engineering-dot-pfe-sender.uc.r.appspot.com |

### 🚨 Troubleshooting 502 Errors
If you get 502 Bad Gateway errors:

```bash
# 1. Pull latest fixes and redeploy
git pull
gcloud app deploy app_test.yaml --quiet

# 2. Check application logs for errors
gcloud app logs read --limit 50

# 3. Test the debug endpoint (if available)
curl https://pfe-sender.uc.r.appspot.com/debug

# 4. Try deploying production version instead
gcloud app deploy app.yaml --quiet
```

---

## 📊 Mock CSV Data Details

### 10 Test Recipients:
1. **Michiel Backker** (CTO, Twintag)
2. **Charly Hamy** (CTO, Rtone)  
3. **Mehdy Salimi** (CTO, Log'in Line)
4. **Francois Beuvens** (CTO, Sagacify)
5. **Yunus Ozturk** (CTO, Eachstapp)
6. **Clement Pellegrini** (CTO, Qarnot)
7. **Mehdi Abaakouk** (Co-founder, Mergify)
8. **Nicola Moresi** (CEO, Moresi.Com SA)
9. **Chris Zurbruegg** (Co-Founder, aumico)
10. **Damien Hontang** (Co-Founder, thinkeo)

### ✅ All emails redirect to: `akrem.alamine@etudiant-fst.utm.tn`

---

## 🎯 Expected Test Results

### ✅ During Business Hours (Mon-Fri, 9 AM - 5 PM UTC):
- **Every minute**: System sends 1 personalized email
- **Round-robin**: Cycles through all 10 recipients
- **CV attached**: Every email includes the PDF
- **Personalization**: Uses real names from CSV in email content

### ⏸️ Outside Business Hours:
- **Cron runs**: But skips email sending
- **Status**: Returns "skipped - weekend" or "skipped - outside business hours"

### 📧 Email Content:
- **Subject**: Personalized for each recipient's company
- **Body**: Professional job application with name placeholders filled
- **Attachment**: Akrem_Alamine_ENOP.pdf
- **From**: akrem.alamine@gmail.com
- **To**: akrem.alamine@etudiant-fst.utm.tn (for all 10 recipients)

---

## 🔍 Success Verification Checklist

### ✅ Deployment Success:
- [ ] Repository uploaded to GitHub successfully
- [ ] GCP deployment completes without errors
- [ ] Health endpoint returns status "healthy"
- [ ] Status endpoint shows 10 recipients in CSV

### ✅ Email Functionality:
- [ ] Manual test email sends successfully
- [ ] CV attachment is included in emails
- [ ] Email content is properly personalized
- [ ] Cron endpoint works during business hours
- [ ] System skips email sending during off-hours

### ✅ Business Logic:
- [ ] Round-robin cycling through recipients works
- [ ] Counter resets after reaching recipient #10
- [ ] Business hours constraint is enforced
- [ ] Weekend emails are properly skipped

---

## 🎉 Final Result - Parallel Email Services

Once both services are deployed, you will have:

### 🏢 **Two Independent Email Services Running Simultaneously:**

#### **Service 1: Akrem Alamine (DevOps/Cloud)**
- 📧 **Sends emails every minute** during business hours  
- 🔄 **Processes CSV TOP to BOTTOM** (normal order)
- 🎯 **DevOps/Cloud-focused** email content
- 📎 **CV**: Akrem_Alamine_ENOP.pdf
- 📨 **From**: akrem.alamine@etudiant-fst.utm.tn

#### **Service 2: Mayez Ghouma (Data Engineering)**  
- 📧 **Sends emails every minute** during business hours
- 🔄 **Processes CSV BOTTOM to TOP** (reverse order)
- 🎯 **Data Engineering/MLOps-focused** email content  
- 📎 **CV**: cv_Mayez-Ghouma.pdf
- 📨 **From**: mayez.ghouma@etudiant-fst.utm.tn

### 🔄 **Combined Coverage Strategy:**
- **Maximum reach**: Same companies receive applications from both profiles
- **Different expertise**: DevOps AND Data Engineering applications  
- **No conflicts**: Reverse processing ensures different timing
- **Professional diversity**: Two distinct skillsets presented

**Your automated recruitment system now sends TWO types of applications simultaneously!** 🚀

---

## 🛠️ Next Steps (Optional)

To use with real recipients:
1. Replace mock data in `data/recipients.csv` with real recipient information
2. Update email addresses to real target addresses
3. Redeploy to GCP
4. Monitor via GCP logs and status endpoints

The system is designed to handle hundreds of recipients and will automatically cycle through them during business hours.