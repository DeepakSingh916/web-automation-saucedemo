pipeline {
    agent any
    
    parameters {
        choice(
            name: 'BRANCH',
            choices: ['main', 'dev'],
            description: 'Select branch to build'
        )
        choice(
            name: 'HEADLESS_MODE',
            choices: ['false', 'true'],
            description: 'Run tests in headless mode? (false = Chrome visible, true = background)'
        )
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "=========================================="
                    echo "BUILD CONFIGURATION"
                    echo "=========================================="
                    echo "Branch: ${params.BRANCH}"
                    echo "Headless Mode: ${params.HEADLESS_MODE}"
                    echo "=========================================="
                }
                
                echo "Checking out ${params.BRANCH} branch from repository..."
                git branch: "${params.BRANCH}",
                    url: 'https://github.com/DeepakSingh916/web-automation-saucedemo.git',
                    credentialsId: 'github-credentials'
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
                script {
                    def headlessFlag = params.HEADLESS_MODE == 'true' ? '--headless' : ''
                    
                    echo "Executing tests with configuration:"
                    echo "  - Branch: ${params.BRANCH}"
                    echo "  - Browser: Chrome"
                    echo "  - Headless: ${params.HEADLESS_MODE}"
                    
                    bat """
                        call venv\\Scripts\\activate.bat
                        pytest tests/ -v ${headlessFlag} --html=reports/report.html --self-contained-html
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
                    reportName: "Test Report - ${params.BRANCH} - ${params.HEADLESS_MODE}",
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
            echo "=========================================="
            echo "BUILD SUCCESSFUL!"
            echo "=========================================="
            echo "Branch: ${params.BRANCH}"
            echo "Headless: ${params.HEADLESS_MODE}"
            echo "=========================================="
        }
        failure {
            echo "=========================================="
            echo "BUILD FAILED!"
            echo "=========================================="
            echo "Branch: ${params.BRANCH}"
            echo "Headless: ${params.HEADLESS_MODE}"
            echo "=========================================="
        }
    }
}
