pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out code from repository..."
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running test suite..."
                bat '''
                    call venv\\Scripts\\activate.bat
                    pytest tests/ -v --html=reports/report.html --self-contained-html
                '''
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
                    reportName: 'Pytest HTML Report',
                    reportTitles: 'Test Execution Report'
                ])
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo 'Archiving test reports and screenshots...'
                archiveArtifacts artifacts: 'reports/*.html, screenshots/*.png', allowEmptyArchive: true
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
        }
        failure {
            echo 'Test execution failed!'
        }
    }
}