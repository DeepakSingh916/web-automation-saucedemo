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
                echo 'Checking out code from repository...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat """
                    python -m venv ${VENV_DIR}
                    ${VENV_DIR}\\Scripts\\activate && pip install --upgrade pip
                    ${VENV_DIR}\\Scripts\\activate && pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running tests with ${params.BROWSER} browser (headless: ${params.HEADLESS})"
                bat """
                    ${VENV_DIR}\\Scripts\\activate && pytest tests/ --browser=${params.BROWSER} --headless=${params.HEADLESS} -v --html=reports/report.html --self-contained-html --alluredir=reports/allure-results
                """
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Generating Allure report...'
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'reports/allure-results']]
                    ])
                }
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
            echo 'Test execution completed successfully!'
            emailext(
                subject: "✅ Test Execution Passed - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Test Execution Summary</h2>
                    <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                    <p><strong>Status:</strong> <span style="color: green;">PASSED ✅</span></p>
                    <p><strong>Browser:</strong> ${params.BROWSER}</p>
                    <p><strong>Headless Mode:</strong> ${params.HEADLESS}</p>
                    <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><strong>Allure Report:</strong> <a href="${env.BUILD_URL}allure">View Report</a></p>
                    <br>
                    <p>All tests executed successfully!</p>
                """,
                to: 'your-email@example.com',
                mimeType: 'text/html'
            )
        }

        failure {
            echo 'Test execution failed!'
            emailext(
                subject: "❌ Test Execution Failed - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Test Execution Summary</h2>
                    <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                    <p><strong>Status:</strong> <span style="color: red;">FAILED ❌</span></p>
                    <p><strong>Browser:</strong> ${params.BROWSER}</p>
                    <p><strong>Headless Mode:</strong> ${params.HEADLESS}</p>
                    <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><strong>Allure Report:</strong> <a href="${env.BUILD_URL}allure">View Report</a></p>
                    <p><strong>Console Output:</strong> <a href="${env.BUILD_URL}console">View Logs</a></p>
                    <br>
                    <p>Please check the attached screenshots and logs for failed tests.</p>
                """,
                to: 'your-email@example.com',
                mimeType: 'text/html',
                attachmentsPattern: 'screenshots/FAILED_*.png'
            )
        }

        unstable {
            echo 'Test execution unstable (some tests failed)'
            emailext(
                subject: "⚠️ Test Execution Unstable - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Test Execution Summary</h2>
                    <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                    <p><strong>Status:</strong> <span style="color: orange;">UNSTABLE ⚠️</span></p>
                    <p><strong>Browser:</strong> ${params.BROWSER}</p>
                    <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><strong>Allure Report:</strong> <a href="${env.BUILD_URL}allure">View Report</a></p>
                    <br>
                    <p>Some tests failed. Please review the report.</p>
                """,
                to: 'your-email@example.com',
                mimeType: 'text/html'
            )
        }
    }
}
