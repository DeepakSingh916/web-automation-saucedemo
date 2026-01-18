pipeline {
    agent any
    
    parameters {
        choice(
            name: 'BRANCH_NAME',
            choices: ['main', 'dev', 'feature/test-pr-workflow'],
            description: 'Select the branch to build'
        )
        booleanParam(
            name: 'HEADLESS_MODE',
            defaultValue: true,
            description: 'Run tests in headless mode'
        )
    }

    environment {
        PYTHON_VERSION = '3.10'
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo '=========================================='
                    echo 'BUILD CONFIGURATION'
                    echo '=========================================='
                    echo "Branch: ${params.BRANCH_NAME}"
                    echo "Headless Mode: ${params.HEADLESS_MODE}"
                    echo '=========================================='
                }
                echo "Checking out ${params.BRANCH_NAME} branch from repository..."
                git branch: "${params.BRANCH_NAME}",
                    url: 'https://github.com/DeepakSingh916/web-automation-saucedemo.git',
                    credentialsId: 'github-credentials'
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat """
                    python -m venv ${VENV_DIR}
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo "Executing tests with configuration:"
                    echo "  - Branch: ${params.BRANCH_NAME}"
                    echo "  - Browser: Chrome"
                    echo "  - Headless: ${params.HEADLESS_MODE}"
                    
                    // Build pytest command based on headless parameter
                    def headlessFlag = params.HEADLESS_MODE ? '--headless' : ''
                    
                    bat """
                        call ${VENV_DIR}\\Scripts\\activate.bat
                        pytest tests/test_login.py::TestLogin::test_valid_login -v ${headlessFlag} ^
                            --html=reports/report.html --self-contained-html ^
                            --alluredir=allure-results ^
                            --clean-alluredir
                    """
                }
            }
        }

        stage('Publish HTML Report') {
            steps {
                echo 'Publishing HTML report...'
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: "Test Report - ${params.BRANCH_NAME} - ${params.HEADLESS_MODE}",
                    reportTitles: 'SauceDemo Test Execution Report'
                ])
            }
        }

        stage('Publish Allure Report') {
            steps {
                echo 'Publishing Allure report...'
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'allure-results']]
                    ])
                }
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo 'Archiving test reports and screenshots...'
                archiveArtifacts artifacts: 'reports/**, allure-results/**, screenshots/**',
                                allowEmptyArchive: true,
                                fingerprint: true
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
        success {
            echo '=========================================='
            echo 'BUILD SUCCESSFUL!'
            echo '=========================================='
            echo "Branch: ${params.BRANCH_NAME}"
            echo "Headless: ${params.HEADLESS_MODE}"
            echo '=========================================='
        }
        failure {
            echo '=========================================='
            echo 'BUILD FAILED!'
            echo '=========================================='
            echo "Branch: ${params.BRANCH_NAME}"
            echo "Headless: ${params.HEADLESS_MODE}"
            echo '=========================================='
        }
    }
}