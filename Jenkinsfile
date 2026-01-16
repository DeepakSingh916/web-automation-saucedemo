pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'firefox', 'edge'], description: 'Select browser for test execution')
        choice(name: 'HEADLESS', choices: ['false', 'true'], description: 'Run tests in headless mode?')
    }

    environment {
        PYTHON_VERSION = '3.10'
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "🔄 Checking out ${env.BRANCH_NAME} branch from repository..."
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up Python virtual environment...'
                bat '''
                    python -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests - Dev Branch') {
            when {
                branch 'dev'
            }
            steps {
                echo "🧪 Running tests on DEV branch with ${params.BROWSER} browser"
                bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat
                    pytest tests/ --browser=%BROWSER% --headless=%HEADLESS% -v --html=reports/report.html --self-contained-html
                '''
            }
        }

        stage('Run Tests - Main Branch') {
            when {
                branch 'main'
            }
            steps {
                echo "🚀 Running FULL test suite on MAIN branch with ${params.BROWSER} browser"
                bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat
                    pytest tests/ --browser=%BROWSER% --headless=%HEADLESS% -v --html=reports/report.html --self-contained-html
                '''
            }
        }

        stage('Publish HTML Report') {
            steps {
                echo '📄 Publishing HTML report...'
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Pytest HTML Report',
                    reportTitles: 'Test Execution Report'
                ])
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo 'Archiving test reports and screenshots...'
                archiveArtifacts artifacts: 'reports/**/*.html, screenshots/**/*.png', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }

        success {
            echo '✅ Test execution completed successfully!'
        }

        failure {
            echo '❌ Test execution failed!'
        }

        unstable {
            echo '⚠️ Test execution unstable (some tests failed)'
        }
    }
}
