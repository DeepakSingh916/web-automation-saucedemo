 # Web Automation Project - SauceDemo

## 🎯 Project Overview
This is a complete Selenium + Python + Pytest automation framework for testing the SauceDemo e-commerce website.
Built following industry-standard practices with Page Object Model design pattern.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Framework:** Pytest
- **Automation Tool:** Selenium WebDriver
- **Design Pattern:** Page Object Model (POM)
- **Reporting:** Allure Reports, HTML Reports
- **CI/CD:** Jenkins

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
│   ├── test_login.py      # Login test cases
│   ├── test_products.py   # Product test cases
│   ├── test_cart.py       # Cart test cases
│   └── test_checkout.py   # Checkout test cases
├── utils/                 # Utility functions
│   ├── driver_factory.py  # WebDriver management
│   ├── logger.py          # Logging configuration
│   └── helpers.py         # Helper functions
├── reports/               # Test reports (auto-generated)
├── screenshots/           # Screenshots (auto-generated)
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
├── Jenkinsfile           # Jenkins pipeline
└── README.md             # This file
```

## 🚀 Setup Instructions (Windows)

### Step 1: Clone/Download Project
```bash
# Clone from GitHub
git clone https://github.com/DeepakSingh916/web-automation-saucedemo.git
cd web-automation-saucedemo

# Or download ZIP from GitHub and extract
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Allure (For Reports)
```bash
# Download Allure from: https://github.com/allure-framework/allure2/releases
# Extract to C:\allure
# Add C:\allure\bin to PATH environment variable
```

## ▶️ Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test File
```bash
pytest tests/test_login.py
```

### Run with HTML Report
```bash
pytest tests/ --html=reports/report.html
```

### Run with Allure Report
```bash
# Run tests and generate allure results
pytest tests/ --alluredir=reports/allure-results

# Generate and open allure report
allure serve reports/allure-results
```

### Run Tests in Headless Mode
```bash
pytest tests/ --headless=true
```

### Run Tests on Different Browser
```bash
pytest tests/ --browser=chrome
pytest tests/ --browser=firefox
pytest tests/ --browser=edge
```

## 📊 Reports & Screenshots

### HTML Report
- Location: `reports/report.html`
- Open in browser to view detailed test results

### Allure Report
- Interactive HTML report with graphs and charts
- Screenshots attached to failed tests
- Execution timeline

### Screenshots
- Location: `screenshots/`
- Auto-captured on test failure
- Named with timestamp and test name

## 🔧 Configuration

### Environment Config (`config/config.py`)
```python
BASE_URL = "https://www.saucedemo.com"
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"
```

### Browser Config (`config/browser_config.py`)
- Default browser: Chrome
- Headless mode: False
- Window size: Maximized
- Implicit wait: 10 seconds

## 🧪 Test Cases Covered

### Login Tests (5 cases)
- ✅ Valid login
- ✅ Invalid username
- ✅ Invalid password
- ✅ Empty credentials
- ✅ Locked user

### Product Tests (4 cases)
- ✅ Product display
- ✅ Sort by price (low to high)
- ✅ Sort by name (A to Z)
- ✅ Add to cart from listing

### Cart Tests (3 cases)
- ✅ Add multiple items
- ✅ Remove item from cart
- ✅ Continue shopping

### Checkout Tests (3 cases)
- ✅ Complete checkout flow
- ✅ Form validation
- ✅ Order completion

**Total: 15 Automated Test Cases**

## 🏗️ Jenkins Integration

### Pipeline Features
- Automated test execution
- Scheduled runs (nightly)
- Email notifications
- Allure report publishing
- Screenshot archiving

### Setup Jenkins Pipeline
1. Install Jenkins
2. Create new Pipeline job
3. Point to Jenkinsfile in repo
4. Configure GitHub webhook (optional)
5. Set up email notifications

See `docs/JENKINS_SETUP.md` for detailed instructions.

## 📝 Interview Tips

When discussing this project in interviews, mention:

1. **Framework Design:**
   - "Used Page Object Model for maintainability"
   - "Separated test logic from page elements"
   - "Implemented reusable components"

2. **CI/CD Integration:**
   - "Integrated with Jenkins for automated execution"
   - "Configured scheduled nightly runs"
   - "Set up email notifications for test results"

3. **Reporting:**
   - "Used Allure for rich interactive reports"
   - "Captured screenshots on failures"
   - "Generated HTML reports for quick review"

4. **Best Practices:**
   - "Used pytest fixtures for setup/teardown"
   - "Implemented implicit/explicit waits"
   - "Added logging for debugging"
   - "Followed PEP8 coding standards"

## 🐛 Troubleshooting

### ChromeDriver Issues
```bash
# Webdriver-manager auto-downloads driver
# If issues persist, manually download from:
# https://chromedriver.chromium.org/
```

### Import Errors
```bash
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Tests Running Too Slow
```bash
# Use headless mode
pytest tests/ --headless=true

# Run in parallel (install pytest-xdist)
pip install pytest-xdist
pytest tests/ -n 4
```

## 📚 Additional Resources
- Pytest Documentation: https://docs.pytest.org/
- Selenium Documentation: https://www.selenium.dev/documentation/
- Allure Reports: https://docs.qameta.io/allure/

## 👤 Author
Created for automation interview preparation

## 📄 License
Free to use for learning and interview preparation
