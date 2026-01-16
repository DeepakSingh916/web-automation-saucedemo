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
                bat """
                    python -m venv ${VENV_DIR}
                    ${VENV_DIR}\\Scripts\\activate && pip install --upgrade pip
                    ${VENV_DIR}\\Scripts\\activate && pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests - Dev Branch') {
            when {
                branch 'dev'
            }
            steps {
                echo "🧪 Running tests on DEV branch with ${params.BROWSER} browser"
                bat """
                    ${VENV_DIR}\\Scripts\\activate && pytest tests/ --browser=${params.BROWSER} --headless=${params.HEADLESS} -v --html=reports/report.html --self-contained-html
                """
            }
        }

        stage('Run Tests - Main Branch') {
            when {
                branch 'main'
            }
            steps {
                echo "🚀 Running FULL test suite on MAIN branch with ${params.BROWSER} browser"
                bat """
                    ${VENV_DIR}\\Scripts\\activate && pytest tests/ --browser=${params.BROWSER} --headless=${params.HEADLESS} -v --html=reports/report.html --self-contained-html --alluredir=reports/allure-results
                """
            }
        }

        stage('Generate Allure Report') {
            when {
                branch 'main'
            }
            steps {
                echo '📊 Generating Allure report for MAIN branch...'
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
                echo '💾 Archiving test reports and screenshots...'
                archiveArtifacts artifacts: 'reports/**/*.html, screenshots/**/*.png', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up workspace...'
            cleanWs()
        }

        success {
            echo '✅ Test execution completed successfully!'
            script {
                def branchEmoji = env.BRANCH_NAME == 'main' ? '🚀' : '🛠️'
                emailext(
                    subject: "✅ ${branchEmoji} Test Passed - ${env.BRANCH_NAME} - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """
                        <h2>Test Execution Summary</h2>
                        <p><strong>Branch:</strong> ${env.BRANCH_NAME}</p>
                        <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                        <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                        <p><strong>Status:</strong> <span style="color: green;">PASSED ✅</span></p>
                        <p><strong>Browser:</strong> ${params.BROWSER}</p>
                        <p><strong>Headless Mode:</strong> ${params.HEADLESS}</p>
                        <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                        <p><strong>HTML Report:</strong> <a href="${env.BUILD_URL}Pytest_20HTML_20Report">View Report</a></p>
                        ${env.BRANCH_NAME == 'main' ? '<p><strong>Allure Report:</strong> <a href="' + env.BUILD_URL + 'allure">View Allure Report</a></p>' : ''}
                        <br>
                        <p>All tests executed successfully on ${env.BRANCH_NAME} branch!</p>
                    """,
                    to: 'ds248776@gmail.com',
                    mimeType: 'text/html'
                )
            }
        }

        failure {
            echo '❌ Test execution failed!'
            emailext(
                subject: "❌ Test Failed - ${env.BRANCH_NAME} - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Test Execution Summary</h2>
                    <p><strong>Branch:</strong> ${env.BRANCH_NAME}</p>
                    <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                    <p><strong>Status:</strong> <span style="color: red;">FAILED ❌</span></p>
                    <p><strong>Browser:</strong> ${params.BROWSER}</p>
                    <p><strong>Headless Mode:</strong> ${params.HEADLESS}</p>
                    <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><strong>Console Output:</strong> <a href="${env.BUILD_URL}console">View Logs</a></p>
                    <br>
                    <p>Please check the logs and screenshots for failed tests on ${env.BRANCH_NAME} branch.</p>
                """,
                to: 'ds248776@gmail.com',
                mimeType: 'text/html',
                attachmentsPattern: 'screenshots/FAILED_*.png'
            )
        }

        unstable {
            echo '⚠️ Test execution unstable (some tests failed)'
            emailext(
                subject: "⚠️ Test Unstable - ${env.BRANCH_NAME} - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Test Execution Summary</h2>
                    <p><strong>Branch:</strong> ${env.BRANCH_NAME}</p>
                    <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                    <p><strong>Status:</strong> <span style="color: orange;">UNSTABLE ⚠️</span></p>
                    <p><strong>Browser:</strong> ${params.BROWSER}</p>
                    <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><strong>HTML Report:</strong> <a href="${env.BUILD_URL}Pytest_20HTML_20Report">View Report</a></p>
                    <br>
                    <p>Some tests failed on ${env.BRANCH_NAME} branch. Please review the report.</p>
                """,
                to: 'ds248776@gmail.com',
                mimeType: 'text/html'
            )
        }
    }
}
