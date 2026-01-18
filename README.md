# Web Automation Project - SauceDemo

## 🎯 Project Overview
Complete Selenium + Python + Pytest automation framework for SauceDemo e-commerce website with Jenkins CI/CD integration.
Built with Page Object Model design pattern following industry standards.

## ✨ Key Features
- ✅ 25 comprehensive test cases (Login, Products, Cart, Checkout)
- ✅ Page Object Model (POM) design pattern
- ✅ Jenkins CI/CD pipeline with parameterized builds
- ✅ Chrome browser with headless mode support
- ✅ HTML test reports with screenshots
- ✅ Incognito mode (no password popups)
- ✅ Logging framework for debugging

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Framework:** Pytest 7.4.3
- **Automation Tool:** Selenium WebDriver 4.15.2
- **Design Pattern:** Page Object Model (POM)
- **Reporting:** HTML Reports, pytest-html
- **CI/CD:** Jenkins with parameterized pipeline
- **Browser:** Chrome (with incognito + headless modes)

## 📁 Project Structure
```
web-automation-saucedemo/
├── config/                 # Configuration files
│   ├── config.py          # Environment configs (URLs, credentials)
│   └── browser_config.py  # Browser settings
├── pages/                 # Page Object Model classes
│   ├── base_page.py       # Base page with common methods
│   ├── login_page.py      # Login page objects
│   ├── products_page.py   # Products page objects
│   ├── cart_page.py       # Cart page objects
│   └── checkout_page.py   # Checkout page objects
├── tests/                 # Test cases
│   ├── conftest.py        # Pytest fixtures
│   ├── test_login.py      # Login test cases (5 tests)
│   ├── test_products.py   # Product test cases (6 tests)
│   ├── test_cart.py       # Cart test cases (6 tests)
│   └── test_checkout.py   # Checkout test cases (8 tests)
├── utils/                 # Utility functions
│   ├── driver_factory.py  # WebDriver management
│   └── helpers.py         # Helper functions (screenshots, etc)
├── drivers/               # Local ChromeDriver
├── reports/               # Test reports (auto-generated)
├── screenshots/           # Screenshots (auto-generated)
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
├── Jenkinsfile           # Jenkins pipeline (parameterized)
└── README.md             # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Chrome browser installed
- Git (for cloning repository)

### Step 1: Clone Repository
```bash
git clone https://github.com/DeepakSingh916/web-automation-saucedemo.git
cd web-automation-saucedemo
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## ▶️ Running Tests Locally

> **📖 For comprehensive command reference, see:**
> - **[PYTEST_COMMANDS.md](docs/PYTEST_COMMANDS.md)** - Complete command guide with all options
> - **[COMMAND_CHEATSHEET.txt](docs/COMMAND_CHEATSHEET.txt)** - Quick reference cheat sheet

### Understanding Test Modes

| Mode | Flag | Behavior |
|------|------|----------|
| **Normal Mode** | No flag | Browser visible (default) |
| **Headless Mode** | `--headless` | Browser hidden |

### Quick Start Commands

**All Tests:**
```bash
# Normal mode (browser visible)
pytest tests/ -v

# Headless mode (browser hidden)
pytest tests/ -v --headless
```

**Specific Test File:**
```bash
# Normal mode
pytest tests/test_login.py -v

# Headless mode
pytest tests/test_login.py -v --headless
```

**Specific Test Case:**
```bash
# Normal mode
pytest tests/test_login.py::TestLogin::test_valid_login -v

# Headless mode
pytest tests/test_login.py::TestLogin::test_valid_login -v --headless
```

### Report Generation

Reports are automatically generated (configured in `pytest.ini`):
- **HTML Report:** `reports/report.html`
- **Allure Results:** `reports/allure-results/`

**Custom report names:**
```bash
# Custom HTML report
pytest tests/ -v --html=reports/custom_name.html --self-contained-html

# Custom Allure location
pytest tests/ -v --alluredir=allure-results --clean-alluredir
```

**View Allure Report:**
```bash
allure serve reports/allure-results
# or
allure serve allure-results
```

### Common Scenarios

```bash
# Quick smoke test (login tests only, headless)
pytest tests/test_login.py -v --headless

# Debug specific test (normal mode, see output)
pytest tests/test_checkout.py::TestCheckout::test_complete_checkout_flow -v -s

# Full regression (parallel execution, headless)
pytest tests/ -v --headless -n 4

# Stop on first failure
pytest tests/ -v --headless -x
```

## 🔧 Jenkins CI/CD Integration

### Pipeline Features
- ✅ Parameterized builds (branch + headless mode selection)
- ✅ Automated test execution
- ✅ HTML report generation and publishing
- ✅ Screenshot archiving on failures
- ✅ Workspace cleanup after execution

### Jenkins Build Parameters

When you click **"Build with Parameters"** in Jenkins, you'll see:

**1. BRANCH** - Select which branch to test
- `main` - Production-ready code (stable)
- `dev` - Development code (latest features)

**2. HEADLESS_MODE** - Choose execution mode
- `false` - Chrome opens (visible execution, slower)
- `true` - Background execution (faster, no UI)

### Common Jenkins Build Scenarios

**Scenario 1: Quick Dev Testing**
- Branch: `dev`
- Headless Mode: `true`
- **Use case:** Fast feedback on dev branch changes

**Scenario 2: Main Branch Verification**
- Branch: `main`
- Headless Mode: `false`
- **Use case:** Visual verification of production code

**Scenario 3: Fast Regression (Main)**
- Branch: `main`
- Headless Mode: `true`
- **Use case:** Quick regression testing

**Scenario 4: Dev Branch with UI**
- Branch: `dev`
- Headless Mode: `false`
- **Use case:** Debugging dev branch issues

### Setting Up Jenkins Pipeline

1. **Install Jenkins** (if not already installed)
2. **Create New Pipeline Job:**
   - Dashboard → New Item → Pipeline
   - Name: `SauceDemo-WebAutomation-Pipeline`
3. **Configure Pipeline:**
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: `https://github.com/DeepakSingh916/web-automation-saucedemo.git`
   - Credentials: Add GitHub credentials
   - Branch Specifier: `*/main` (default)
   - Script Path: `Jenkinsfile`
4. **Save Configuration**
5. **First Build:**
   - Click "Build Now" (first time only)
   - After first build, button changes to "Build with Parameters"
6. **Subsequent Builds:**
   - Click "Build with Parameters"
   - Select branch and headless mode
   - Click "Build"

## 📊 Test Coverage

### Login Tests (5 cases)
- ✅ Valid login with standard_user
- ✅ Invalid username error handling
- ✅ Invalid password error handling
- ✅ Empty credentials validation
- ✅ Locked user account handling

### Products Tests (6 cases)
- ✅ Products page display verification
- ✅ Sort products by name (A to Z)
- ✅ Sort products by name (Z to A)
- ✅ Sort products by price (low to high)
- ✅ Sort products by price (high to low)
- ✅ Add single product to cart
- ✅ Add multiple products to cart

### Cart Tests (6 cases)
- ✅ Cart page loaded verification
- ✅ Cart items display correctly
- ✅ Remove single item from cart
- ✅ Remove all items from cart
- ✅ Continue shopping from cart
- ✅ Proceed to checkout from cart

### Checkout Tests (8 cases)
- ✅ Checkout information page display
- ✅ Complete checkout flow
- ✅ Empty first name validation
- ✅ Empty last name validation
- ✅ Empty postal code validation
- ✅ Cancel checkout functionality
- ✅ Back to home after completion
- ✅ Order confirmation display

**Total: 25 Automated Test Cases**
**Pass Rate: 100% ✅**

## 📈 Test Reports

### HTML Report
- **Location:** `reports/report.html`
- **Features:** 
  - Test execution summary
  - Pass/Fail status for each test
  - Execution time
  - Environment details
  - Screenshots for failed tests

### Screenshots
- **Location:** `screenshots/`
- **Auto-captured:** On test failure
- **Naming:** `FAILED_<test_name>_<timestamp>.png`

### View Reports in Jenkins
- Navigate to build → "Test Report - main/dev - true/false"
- View HTML report directly in Jenkins
- Download archived artifacts (reports + screenshots)

## 🔑 Key Framework Features

### 1. Incognito Mode
- Chrome opens in incognito mode
- No password manager popups
- Clean browser state for each test
- No cookies/cache interference

### 2. Test Isolation
- Each test gets fresh Chrome instance
- No side effects between tests
- Independent test execution

### 3. Intelligent Waits
- Added waits in cart fixture for page load
- Prevents flaky tests
- Ensures element availability

### 4. Screenshot on Failure
- Automatic screenshot capture
- Saved with test name + timestamp
- Archived in Jenkins artifacts

### 5. Comprehensive Logging
- INFO level logs for execution flow
- ERROR level logs for failures
- Logs saved in console output

## 🐛 Troubleshooting

### ChromeDriver Issues
```bash
# Framework uses local ChromeDriver in drivers/ folder
# If issues persist, download compatible version:
# https://chromedriver.chromium.org/downloads

# Place chromedriver.exe in:
web-automation-saucedemo/drivers/chromedriver.exe
```

### Tests Fail with "Password Popup"
```bash
# Already fixed! Framework uses incognito mode
# If you see popup, verify driver_factory.py has:
options.add_argument("--incognito")
```

### Import Errors
```bash
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Jenkins Build Fails
```bash
# Check Jenkins console output
# Common issues:
# 1. Python not in PATH
# 2. Git credentials not configured
# 3. Chrome browser not installed
```

## 💡 Interview Tips

### When Discussing This Project

**1. Framework Architecture:**
- "Implemented Page Object Model for better maintainability and reusability"
- "Separated test logic from page elements for easier updates"
- "Used pytest fixtures for efficient setup/teardown"

**2. CI/CD Integration:**
- "Integrated Jenkins pipeline with parameterized builds"
- "Can test different branches with different execution modes"
- "Automated report generation and artifact archiving"

**3. Problem Solving:**
- "Fixed Chrome password manager popup issue using incognito mode"
- "Resolved ChromeDriver compatibility with local driver management"
- "Added intelligent waits to prevent flaky tests"

**4. Best Practices:**
- "Used incognito mode for clean test environment"
- "Implemented logging for debugging"
- "Captured screenshots on failures"
- "Created isolated test execution (fresh browser per test)"

**5. Technical Skills Demonstrated:**
- Python programming
- Selenium WebDriver automation
- Pytest testing framework
- Page Object Model design pattern
- Jenkins CI/CD pipeline
- Git version control
- Problem-solving and debugging

## 📚 Technologies & Tools

- **Python 3.10** - Core programming language
- **Selenium 4.15.2** - Web automation
- **Pytest 7.4.3** - Testing framework
- **pytest-html 4.1.1** - HTML reporting
- **webdriver-manager 4.0.1** - Driver management
- **Jenkins** - CI/CD automation
- **Git/GitHub** - Version control
- **Chrome** - Test browser

## 👤 Author
**Deepak Singh**
- GitHub: [@DeepakSingh916](https://github.com/DeepakSingh916)
- Repository: [web-automation-saucedemo](https://github.com/DeepakSingh916/web-automation-saucedemo)

## 📄 License
Free to use for learning and interview preparation

---

## 🎯 Quick Start Summary

**Local Testing:**
```bash
# Clone → Setup → Run
git clone https://github.com/DeepakSingh916/web-automation-saucedemo.git
cd web-automation-saucedemo
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run tests
pytest tests/ -v                    # Normal mode
pytest tests/ -v --headless         # Headless mode
```

**Jenkins Testing:**
```
1. Click "Build with Parameters"
2. Select branch: main or dev
3. Select headless: false or true
4. Click "Build"
5. View reports and artifacts
```

**Perfect for interviews - demonstrates production-ready automation skills!** 🚀

## 📋 Command Reference Documentation

For complete command reference with all options and examples:
- **[PYTEST_COMMANDS.md](docs/PYTEST_COMMANDS.md)** - Detailed command guide
- **[COMMAND_CHEATSHEET.txt](docs/COMMAND_CHEATSHEET.txt)** - Quick reference cheat sheet

## 📊 Report Generation

### Automatic Reports (via pytest.ini)

Both HTML and Allure reports are automatically generated for every test run:

| Report Type | Location | Features |
|-------------|----------|----------|
| **HTML** | `reports/report.html` | Self-contained, no dependencies |
| **Allure** | `reports/allure-results/` | Rich UI, trends, history |

### Viewing Reports

**HTML Report:**
```bash
# Windows
start reports\report.html

# Mac
open reports/report.html

# Linux
xdg-open reports/report.html
```

**Allure Report:**
```bash
# Auto-opens in browser
allure serve reports/allure-results
```

### Installing Allure CLI (Optional)

```bash
# Using npm (recommended)
npm install -g allure-commandline

# Using scoop (Windows)
scoop install allure

# Verify installation
allure --version
```

### Jenkins Reports

When running in Jenkins:
- **HTML Report:** Available via "Test Report" link
- **Allure Report:** Available via "Allure Report" link (requires Allure Jenkins Plugin)

Both reports are published automatically after each builds.
=================================================================
