# Web Automation Project - Complete Setup Guide

## 📋 Table of Contents
1. [PyCharm Setup (Windows)](#pycharm-setup)
2. [Running Tests Locally](#running-tests)
3. [Jenkins Installation](#jenkins-installation)
4. [Jenkins Pipeline Setup](#jenkins-pipeline)
5. [Email Notifications](#email-notifications)
6. [GitHub Repository Setup](#github-setup)
7. [Allure Reports](#allure-reports)
8. [Troubleshooting](#troubleshooting)

---

## 🖥️ PyCharm Setup (Windows)

### Step 1: Download and Extract Project
1. Download the `web-automation-saucedemo` folder
2. Extract to any location (e.g., `C:\Users\YourName\Projects\`)

### Step 2: Open in PyCharm
1. Open PyCharm IDE
2. Click **File → Open**
3. Navigate to the extracted folder
4. Click **OK**

### Step 3: Configure Python Interpreter
1. Go to **File → Settings** (or `Ctrl + Alt + S`)
2. Navigate to **Project → Python Interpreter**
3. Click gear icon ⚙️ → **Add**
4. Select **Virtualenv Environment** → **New**
5. Location: `<project_path>\venv`
6. Base interpreter: Select your Python 3.10 installation
7. Click **OK**

### Step 4: Install Dependencies
**Method 1: Using PyCharm**
1. Open `requirements.txt`
2. PyCharm will show a banner "Package requirements are not satisfied"
3. Click **Install requirements**
4. Wait for installation to complete

**Method 2: Using Terminal**
1. Open PyCharm Terminal (bottom panel)
2. Activate virtual environment (automatically activated in PyCharm)
3. Run:
```bash
pip install -r requirements.txt
```

### Step 5: Verify Installation
In PyCharm terminal, run:
```bash
pytest --version
selenium --version
```

✅ **Setup Complete!** You can now run tests.

---

## ▶️ Running Tests Locally

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test File
```bash
# Login tests only
pytest tests/test_login.py

# Product tests only
pytest tests/test_products.py

# Cart tests
pytest tests/test_cart.py

# Checkout tests
pytest tests/test_checkout.py
```

### Run with Specific Markers
```bash
# Smoke tests only
pytest -m smoke

# Regression tests
pytest -m regression

# Login related tests
pytest -m login
```

### Run with Different Browser
```bash
# Chrome (default)
pytest tests/ --browser=chrome

# Firefox
pytest tests/ --browser=firefox

# Edge
pytest tests/ --browser=edge
```

### Run in Headless Mode
```bash
pytest tests/ --headless=true
```

### Generate HTML Report
```bash
pytest tests/ --html=reports/report.html
```

### Generate Allure Report
```bash
# Step 1: Run tests with allure
pytest tests/ --alluredir=reports/allure-results

# Step 2: View allure report
allure serve reports/allure-results
```

### Run Parallel Tests (Faster)
```bash
# Install pytest-xdist first
pip install pytest-xdist

# Run with 4 parallel workers
pytest tests/ -n 4
```

---

## 🔧 Jenkins Installation (Windows)

### Step 1: Install Java
1. Download JDK from: https://www.oracle.com/java/technologies/downloads/
2. Install JDK 11 or 17
3. Verify installation:
```cmd
java --version
```

### Step 2: Download Jenkins
1. Go to: https://www.jenkins.io/download/
2. Download **Windows** installer (.msi)
3. Run the installer

### Step 3: Install Jenkins
1. During installation:
   - Port: **8080** (default)
   - Service account: **Local System**
   - Install as Windows Service: **Yes**
2. Complete installation

### Step 4: Initial Setup
1. Open browser: `http://localhost:8080`
2. Get initial admin password:
   - Location: `C:\Program Files\Jenkins\secrets\initialAdminPassword`
   - Or check installation window
3. Paste the password
4. Click **Install suggested plugins**
5. Create admin user
6. Click **Save and Continue**
7. Jenkins URL: `http://localhost:8080/` (keep default)
8. Click **Start using Jenkins**

### Step 5: Install Required Plugins
1. Go to **Manage Jenkins → Plugins**
2. Click **Available plugins**
3. Search and install:
   - **Allure**
   - **Email Extension Plugin** (if not installed)
   - **Pipeline** (should be pre-installed)
4. Click **Install without restart**

### Step 6: Configure Allure
1. Go to **Manage Jenkins → Tools**
2. Scroll to **Allure Commandline**
3. Click **Add Allure Commandline**
4. Name: `Allure`
5. Check **Install automatically**
6. Choose latest version
7. Click **Save**

✅ **Jenkins Installed!**

---

## 🔄 Jenkins Pipeline Setup

### Step 1: Create New Pipeline Job
1. Click **New Item**
2. Name: `Web-Automation-Tests`
3. Select **Pipeline**
4. Click **OK**

### Step 2: Configure Pipeline

#### General Settings
1. ✅ Check **This project is parameterized**
2. Add parameters:
   - **Choice Parameter**
     - Name: `BROWSER`
     - Choices: `chrome`, `firefox`, `edge`
   - **Choice Parameter**
     - Name: `HEADLESS`
     - Choices: `false`, `true`

#### Pipeline Definition
1. Definition: **Pipeline script from SCM**
2. SCM: **Git**
3. Repository URL: `<your-github-repo-url>` (we'll create this later)
4. Branch: `*/main`
5. Script Path: `Jenkinsfile`

**OR**

If NOT using GitHub:
1. Definition: **Pipeline script**
2. Copy-paste the entire Jenkinsfile content

### Step 3: Configure Build Triggers (Optional)

#### Daily Build
1. ✅ Check **Build periodically**
2. Schedule: `H 2 * * *` (Runs at 2 AM daily)

#### Build after every commit (requires GitHub webhook)
1. ✅ Check **GitHub hook trigger for GITScm polling**

### Step 4: Save Configuration
Click **Save**

### Step 5: Run Pipeline
1. Click **Build with Parameters**
2. Select browser: `chrome`
3. Headless: `false`
4. Click **Build**
5. Check **Console Output** for logs

---

## 📧 Email Notifications Setup

### Step 1: Configure Email in Jenkins
1. Go to **Manage Jenkins → System**
2. Scroll to **Extended E-mail Notification**

#### SMTP Settings (Gmail Example)
```
SMTP server: smtp.gmail.com
SMTP Port: 465
Use SSL: ✅ Checked

Credentials:
- Click **Add → Jenkins**
- Kind: Username with password
- Username: your.email@gmail.com
- Password: Your App Password (NOT Gmail password!)
- ID: gmail-credentials
- Click **Add**

Select: gmail-credentials
```

#### Generate Gmail App Password
1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification** (if not enabled)
3. Search for **App passwords**
4. Select app: **Mail**
5. Select device: **Other** → Name it "Jenkins"
6. Click **Generate**
7. Copy the 16-character password
8. Use this password in Jenkins credentials

### Step 2: Configure Default Recipients
1. In **Extended E-mail Notification** section:
2. Default Recipients: `your.email@example.com`
3. Default Subject: `$PROJECT_NAME - Build #$BUILD_NUMBER - $BUILD_STATUS`
4. Click **Save**

### Step 3: Test Email
1. Click **Test configuration by sending test e-mail**
2. Enter your email
3. Click **Test**
4. Check your inbox

### Step 4: Update Jenkinsfile Email
Open `Jenkinsfile` and update:
```groovy
to: 'your-email@example.com',  // Change this to your email
```

---

## 🐙 GitHub Repository Setup

### Step 1: Create GitHub Repository
1. Go to: https://github.com
2. Click **+** → **New repository**
3. Repository name: `web-automation-saucedemo`
4. Description: `Selenium Python automation framework`
5. Public or Private (your choice)
6. **Do NOT** initialize with README
7. Click **Create repository**

### Step 2: Push Code to GitHub
Open terminal in project folder:
```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Web automation framework"

# Add remote repository
git remote add origin https://github.com/<your-username>/web-automation-saucedemo.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Update Jenkins Pipeline
1. Go to Jenkins job → **Configure**
2. Update **Repository URL**:
   ```
   https://github.com/<your-username>/web-automation-saucedemo.git
   ```
3. Click **Save**

### Step 4: Setup Webhook (Optional - for auto-build on commit)
1. In GitHub repo, go to **Settings → Webhooks**
2. Click **Add webhook**
3. Payload URL: `http://<jenkins-url>:8080/github-webhook/`
4. Content type: `application/json`
5. Events: **Just the push event**
6. Click **Add webhook**

---

## 📊 Allure Reports Setup

### Step 1: Download Allure
1. Go to: https://github.com/allure-framework/allure2/releases
2. Download latest **allure-x.x.x.zip**
3. Extract to: `C:\allure`

### Step 2: Add to PATH
1. Open **Environment Variables**:
   - Press `Win + R`
   - Type `sysdm.cpl` → Enter
   - Click **Advanced** tab
   - Click **Environment Variables**
2. Under **System variables**, select **Path**
3. Click **Edit**
4. Click **New**
5. Add: `C:\allure\bin`
6. Click **OK** on all windows

### Step 3: Verify Installation
Open new command prompt:
```cmd
allure --version
```

### Step 4: Generate Allure Report Locally
```bash
# Run tests with allure
pytest tests/ --alluredir=reports/allure-results

# Serve allure report
allure serve reports/allure-results
```

Browser will open automatically with interactive report!

### Step 5: View Allure Report in Jenkins
1. After pipeline runs
2. Click on build number
3. Click **Allure Report** (left sidebar)
4. Interactive report opens

---

## 🐛 Troubleshooting

### Issue 1: ChromeDriver not found
**Solution:**
```bash
# Webdriver-manager will auto-download
# If still issues, manually download from:
# https://chromedriver.chromium.org/
```

### Issue 2: Tests running very slow
**Solution:**
```bash
# Use headless mode
pytest tests/ --headless=true

# Or run in parallel
pytest tests/ -n 4
```

### Issue 3: Import errors
**Solution:**
```bash
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 4: Jenkins cannot find Python
**Solution:**
1. In Jenkins, go to **Manage Jenkins → Tools**
2. Add Python installation
3. Or update Jenkinsfile with full Python path

### Issue 5: Email not sending
**Solution:**
1. Check SMTP credentials
2. Ensure App Password is used (for Gmail)
3. Check firewall/antivirus
4. Test configuration in Jenkins

### Issue 6: Allure report not generating
**Solution:**
1. Check Allure is installed in System PATH
2. In Jenkins: **Manage Jenkins → Tools** → Configure Allure
3. Ensure Allure plugin is installed

---

## 🎯 Quick Reference

### Run Tests
```bash
pytest tests/                          # All tests
pytest tests/test_login.py            # Specific file
pytest -m smoke                       # Smoke tests
pytest --browser=chrome --headless=true  # Chrome headless
```

### Reports
```bash
pytest --html=reports/report.html     # HTML report
pytest --alluredir=reports/allure-results  # Allure
allure serve reports/allure-results   # View Allure
```

### Jenkins
- URL: `http://localhost:8080`
- Build: Click **Build with Parameters**
- Console: Build → **Console Output**
- Reports: Build → **Allure Report**

---

## 📞 Support

**For Interview Questions:**
- Check `README.md` → Interview Tips section
- Review test code in `tests/` folder
- Understand Page Object Model in `pages/` folder

**Project Structure:**
- `config/` - Configurations
- `pages/` - Page Objects (POM)
- `tests/` - Test cases
- `utils/` - Utilities (driver, logger, helpers)
- `Jenkinsfile` - CI/CD pipeline

---

**🎉 Setup Complete! Happy Testing!** 🚀
