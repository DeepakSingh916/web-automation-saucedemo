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
        stage('Determine Build Strategy') {
            steps {
                script {
                    // Initialize variables
                    def branchToBuild = ''
                    def buildReason = ''
                    def shouldBuild = false
                    
                    echo '=========================================='
                    echo 'WEBHOOK EVENT ANALYSIS'
                    echo '=========================================='
                    
                    // Check if this is a PR event
                    if (env.CHANGE_ID) {
                        // This is a PR event
                        def sourceBranch = env.CHANGE_BRANCH ?: 'unknown'
                        def targetBranch = env.CHANGE_TARGET ?: 'unknown'
                        def prAction = env.CHANGE_TITLE ? 'opened/updated' : 'merged'
                        
                        echo "Event Type: Pull Request"
                        echo "PR Number: ${env.CHANGE_ID}"
                        echo "Source Branch: ${sourceBranch}"
                        echo "Target Branch: ${targetBranch}"
                        echo "PR Action: ${prAction}"
                        
                        // For PR events, build the source branch (the feature branch)
                        branchToBuild = sourceBranch
                        buildReason = "PR #${env.CHANGE_ID}: ${sourceBranch} → ${targetBranch}"
                        shouldBuild = true
                        
                    } else if (env.GIT_BRANCH) {
                        // This is a direct push event
                        def pushedBranch = env.GIT_BRANCH.replaceAll('origin/', '')
                        
                        echo "Event Type: Direct Push"
                        echo "Branch: ${pushedBranch}"
                        
                        // Only build main and dev branches on direct push
                        if (pushedBranch == 'main' || pushedBranch == 'dev') {
                            branchToBuild = pushedBranch
                            buildReason = "Push to ${pushedBranch}"
                            shouldBuild = true
                        } else {
                            echo "Direct push to ${pushedBranch} - Build skipped"
                            echo "Note: Feature branches should be built via Pull Requests"
                            currentBuild.result = 'NOT_BUILT'
                            error("Build skipped - Direct push to feature branch")
                        }
                        
                    } else {
                        // Manual build
                        branchToBuild = params.BRANCH_NAME
                        buildReason = "Manual build"
                        shouldBuild = true
                        
                        echo "Event Type: Manual Build"
                        echo "Selected Branch: ${branchToBuild}"
                    }
                    
                    if (shouldBuild) {
                        echo '=========================================='
                        echo 'BUILD APPROVED'
                        echo "Branch to build: ${branchToBuild}"
                        echo "Reason: ${buildReason}"
                        echo '=========================================='
                        
                        // Store for use in other stages
                        env.BRANCH_TO_BUILD = branchToBuild
                        env.BUILD_REASON = buildReason
                    }
                }
            }
        }
        
        stage('Checkout') {
            steps {
                script {
                    def branchToBuild = env.BRANCH_TO_BUILD ?: params.BRANCH_NAME
                    
                    echo '=========================================='
                    echo 'BUILD CONFIGURATION'
                    echo '=========================================='
                    echo "Branch: ${branchToBuild}"
                    echo "Headless Mode: ${params.HEADLESS_MODE}"
                    echo "Trigger: ${env.BUILD_REASON ?: 'Manual'}"
                    echo '=========================================='
                }
                
                script {
                    def branchToBuild = env.BRANCH_TO_BUILD ?: params.BRANCH_NAME
                    echo "Checking out ${branchToBuild} branch from repository..."
                    
                    git branch: "${branchToBuild}",
                        url: 'https://github.com/DeepakSingh916/web-automation-saucedemo.git',
                        credentialsId: 'github-credentials'
                }
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
                    def branchToBuild = env.BRANCH_TO_BUILD ?: params.BRANCH_NAME
                    
                    echo "Executing tests with configuration:"
                    echo "  - Branch: ${branchToBuild}"
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
                script {
                    def branchToBuild = env.BRANCH_TO_BUILD ?: params.BRANCH_NAME
                    
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'report.html',
                        reportName: "Test Report - ${branchToBuild} - ${params.HEADLESS_MODE}",
                        reportTitles: 'SauceDemo Test Execution Report'
                    ])
                }
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
            script {
                def branchToBuild = env.BRANCH_TO_BUILD ?: params.BRANCH_NAME
                
                echo '=========================================='
                echo 'BUILD SUCCESSFUL!'
                echo '=========================================='
                echo "Branch: ${branchToBuild}"
                echo "Headless: ${params.HEADLESS_MODE}"
                echo "Reason: ${env.BUILD_REASON ?: 'Manual build'}"
                echo '=========================================='
            }
        }
        failure {
            script {
                def branchToBuild = env.BRANCH_TO_BUILD ?: params.BRANCH_NAME
                
                echo '=========================================='
                echo 'BUILD FAILED!'
                echo '=========================================='
                echo "Branch: ${branchToBuild}"
                echo "Headless: ${params.HEADLESS_MODE}"
                echo "Reason: ${env.BUILD_REASON ?: 'Manual build'}"
                echo '=========================================='
            }
        }
    }
}
