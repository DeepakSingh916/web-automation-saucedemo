# Pytest Command Reference Guide

Complete guide for running tests with different configurations.

## Quick Start

```bash
# Activate virtual environment
venv\Scripts\activate

# Run all tests (normal mode, both reports)
pytest tests/ -v
```

---

## Understanding Test Execution Modes

| Mode | Flag | Behavior |
|------|------|----------|
| **Normal Mode** | No flag | Browser visible (default) |
| **Headless Mode** | `--headless` | Browser hidden |

---

## Report Generation

Your framework automatically generates reports based on `pytest.ini` configuration:

- **HTML Report**: Always generated at `reports/report.html`
- **Allure Results**: Always generated at `reports/allure-results/`

### Custom Report Names

```bash
# Custom HTML report name
pytest tests/ -v --html=reports/custom_name.html --self-contained-html

# Custom Allure results location
pytest tests/ -v --alluredir=allure-results --clean-alluredir
```

---

## 1. Run All Tests

### Normal Mode (Browser Visible)

```bash
# Default reports (from pytest.ini)
pytest tests/ -v

# Custom HTML report name
pytest tests/ -v --html=reports/all_tests.html --self-contained-html

# With both custom reports
pytest tests/ -v --html=reports/all_tests.html --self-contained-html --alluredir=allure-results --clean-alluredir
```

### Headless Mode (Browser Hidden)

```bash
# Default reports
pytest tests/ -v --headless

# Custom HTML report name
pytest tests/ -v --headless --html=reports/all_tests.html --self-contained-html

# With both custom reports
pytest tests/ -v --headless --html=reports/all_tests.html --self-contained-html --alluredir=allure-results --clean-alluredir
```

---

## 2. Run Specific Test File

### Syntax
```bash
pytest tests/<filename>.py [options]
```

### Examples - Normal Mode

```bash
# Login tests - default reports
pytest tests/test_login.py -v

# Login tests - custom HTML report
pytest tests/test_login.py -v --html=reports/login.html --self-contained-html

# Products tests - both custom reports
pytest tests/test_products.py -v --html=reports/products.html --self-contained-html --alluredir=allure-results --clean-alluredir

# Cart tests
pytest tests/test_cart.py -v --html=reports/cart.html --self-contained-html

# Checkout tests
pytest tests/test_checkout.py -v --html=reports/checkout.html --self-contained-html
```

### Examples - Headless Mode

```bash
# Login tests - default reports
pytest tests/test_login.py -v --headless

# Login tests - custom HTML report
pytest tests/test_login.py -v --headless --html=reports/login.html --self-contained-html

# Products tests - both custom reports
pytest tests/test_products.py -v --headless --html=reports/products.html --self-contained-html --alluredir=allure-results --clean-alluredir
```

---

## 3. Run Specific Test Class

### Syntax
```bash
pytest tests/<filename>.py::<ClassName> [options]
```

### Examples

```bash
# Normal mode
pytest tests/test_login.py::TestLogin -v

# Headless mode with custom report
pytest tests/test_login.py::TestLogin -v --headless --html=reports/login_class.html --self-contained-html

# Other classes
pytest tests/test_products.py::TestProducts -v
pytest tests/test_cart.py::TestCart -v --headless
pytest tests/test_checkout.py::TestCheckout -v
```

---

## 4. Run Specific Test Case

### Syntax
```bash
pytest tests/<filename>.py::<ClassName>::<test_method_name> [options]
```

### Examples - Normal Mode

```bash
# Valid login test
pytest tests/test_login.py::TestLogin::test_valid_login -v

# Invalid username test with custom report
pytest tests/test_login.py::TestLogin::test_invalid_username -v --html=reports/invalid_username.html --self-contained-html

# Locked user test
pytest tests/test_login.py::TestLogin::test_locked_user -v

# Add to cart test
pytest tests/test_products.py::TestProducts::test_add_product_to_cart -v

# Complete checkout flow
pytest tests/test_checkout.py::TestCheckout::test_complete_checkout_flow -v
```

### Examples - Headless Mode

```bash
# Valid login test
pytest tests/test_login.py::TestLogin::test_valid_login -v --headless

# Invalid username test with custom report
pytest tests/test_login.py::TestLogin::test_invalid_username -v --headless --html=reports/invalid_username.html --self-contained-html

# Complete checkout flow with both reports
pytest tests/test_checkout.py::TestCheckout::test_complete_checkout_flow -v --headless --html=reports/checkout_flow.html --self-contained-html --alluredir=allure-results --clean-alluredir
```

---

## 5. Run Multiple Specific Tests

```bash
# Multiple tests from different files (normal mode)
pytest tests/test_login.py::TestLogin::test_valid_login tests/test_products.py::TestProducts::test_add_product_to_cart -v

# Multiple tests from different files (headless mode)
pytest tests/test_login.py::TestLogin::test_valid_login tests/test_products.py::TestProducts::test_add_product_to_cart -v --headless

# Multiple tests with custom report
pytest tests/test_login.py::TestLogin::test_valid_login tests/test_login.py::TestLogin::test_invalid_username -v --html=reports/login_scenarios.html --self-contained-html
```

---

## 6. Advanced Options

### Parallel Execution

```bash
# Run with 4 parallel workers (normal mode)
pytest tests/ -v -n 4

# Run with 4 parallel workers (headless mode)
pytest tests/ -v --headless -n 4

# Parallel with custom reports
pytest tests/ -v -n 4 --html=reports/parallel.html --self-contained-html --alluredir=allure-results --clean-alluredir
```

### Debugging

```bash
# Stop on first failure (normal mode)
pytest tests/ -v -x

# Show print statements (normal mode)
pytest tests/ -v -s

# Show local variables on failure
pytest tests/ -v -l

# Combination: stop on failure + show output
pytest tests/ -v -x -s
```

### Re-run Failed Tests

```bash
# Run only last failed tests
pytest tests/ -v --lf

# Run failed tests first, then others
pytest tests/ -v --ff

# With headless mode
pytest tests/ -v --headless --lf
```

### Filter by Keyword

```bash
# Run tests with 'login' in name (normal mode)
pytest tests/ -v -k "login"

# Run tests with 'cart' in name (headless mode)
pytest tests/ -v --headless -k "cart"

# Run tests matching multiple keywords
pytest tests/ -v -k "login or checkout"
```

---

## 7. Viewing Reports

### HTML Report

```bash
# Windows
start reports/report.html

# Or custom report
start reports/login.html

# Mac
open reports/report.html

# Linux
xdg-open reports/report.html
```

### Allure Report

```bash
# Generate and serve (auto-opens in browser)
allure serve allure-results

# Or from custom location
allure serve reports/allure-results

# Generate static report
allure generate allure-results -o allure-report --clean

# Open static report
start allure-report/index.html  # Windows
```

---

## Test Files Reference

| File | Class | Test Count | Tests |
|------|-------|------------|-------|
| `test_login.py` | `TestLogin` | 5 | Valid login, Invalid username, Invalid password, Empty credentials, Locked user |
| `test_products.py` | `TestProducts` | 7 | Display, Sort by name (asc/desc), Sort by price (low/high), Add single/multiple to cart |
| `test_cart.py` | `TestCart` | 6 | Page loaded, Items display, Remove item, Remove all, Continue shopping, Checkout |
| `test_checkout.py` | `TestCheckout` | 7 | Info page, Complete flow, Empty validations (3), Cancel, Back home |

**Total: 25 test cases**

---

## Command Options Reference

| Option | Description |
|--------|-------------|
| `-v` | Verbose output |
| `-vv` | Extra verbose output |
| `-s` | Show print statements |
| `-x` | Stop on first failure |
| `-n 4` | Run with 4 parallel workers |
| `--lf` | Run last failed tests only |
| `--ff` | Run failed tests first |
| `-k "keyword"` | Run tests matching keyword |
| `-l` | Show local variables on failure |
| `--headless` | Run in headless mode (browser hidden) |
| `--html=path` | Custom HTML report path |
| `--self-contained-html` | Make HTML report self-contained |
| `--alluredir=path` | Custom Allure results path |
| `--clean-alluredir` | Clean previous Allure results |

---

## Common Scenarios

### Development & Debugging
```bash
# Run specific failing test with browser visible and see output
pytest tests/test_checkout.py::TestCheckout::test_complete_checkout_flow -v -s
```

### Quick Smoke Test
```bash
# Run login tests only (headless mode)
pytest tests/test_login.py -v --headless
```

### Full Regression Suite
```bash
# Run all tests in parallel (headless mode)
pytest tests/ -v --headless -n 4
```

### CI/CD Pipeline
```bash
# Run all tests, headless, stop on first failure
pytest tests/ -v --headless -x
```

---

## Important Notes

1. **Default Behavior**: Tests run in normal mode (browser visible) unless `--headless` flag is used
2. **Reports**: HTML and Allure reports are configured in `pytest.ini` and generate automatically
3. **Custom Names**: Use `--html` and `--alluredir` flags to override default report locations
4. **Parallel Execution**: Use `-n` flag but may not work well with non-headless mode
5. **Allure CLI**: Required for viewing Allure reports - install via `npm install -g allure-commandline`

---

## Quick Command Templates

```bash
# Template for all tests
pytest tests/ -v [--headless] [--html=reports/NAME.html --self-contained-html] [--alluredir=allure-results --clean-alluredir]

# Template for specific file
pytest tests/FILE.py -v [--headless] [--html=reports/NAME.html --self-contained-html]

# Template for specific test
pytest tests/FILE.py::CLASS::METHOD -v [--headless] [--html=reports/NAME.html --self-contained-html]
```

**Note**: Options in `[square brackets]` are optional and can be mixed and matched based on needs.

---

## Support

For issues or questions:
- Check [README.md](README.md) for framework overview
- Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for setup instructions
- Report issues on GitHub
