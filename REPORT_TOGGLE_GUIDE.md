# Quick Guide: Toggle Between Report Modes

## Current Setup (Allure Only)

HTML report is commented out in pytest.ini, so only Allure report generates.

---

## Switch to Both Reports

Edit `pytest.ini` and uncomment HTML lines:

```ini
addopts =
    -v
    --tb=short
    --strict-markers
    --html=reports/report.html          # Uncommented
    --self-contained-html               # Uncommented
    --alluredir=reports/allure-results
```

---

## Switch to Allure Only

Edit `pytest.ini` and comment HTML lines:

```ini
addopts =
    -v
    --tb=short
    --strict-markers
    # --html=reports/report.html        # Commented
    # --self-contained-html             # Commented
    --alluredir=reports/allure-results
```

---

## One-Time Overrides

### Generate HTML even if disabled in pytest.ini:
```bash
pytest tests/ -v --html=reports/custom.html --self-contained-html
```

### Generate only Allure even if HTML enabled in pytest.ini:
```bash
pytest tests/ -v -o addopts="" --alluredir=allure-results --clean-alluredir
```

---

## Current Status

✅ **Allure Only Mode** - HTML report disabled in pytest.ini
