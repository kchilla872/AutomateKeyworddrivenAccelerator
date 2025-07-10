pipeline {
    agent any

    stages {
        stage('Setup and Test') {
            steps {
                script {
                    bat '''
                        cd "C:\\Users\\karthik.chillara\\PycharmProjects\\DemoParallel0622"
                        call venv\\Scripts\\activate
                        pip install -r requirements.txt
                        playwright install chromium --with-deps
                        if exist allure-results rmdir /s /q allure-results
                        if exist allure-report rmdir /s /q allure-report
                        if exist allure-report\\history (
                            mkdir allure-results
                            xcopy /E /I /Y allure-report\\history allure-results\\history
                        )
                        pytest test_homePage.py -v --alluredir=allure-results
                    '''
                }
            }
        }
        stage('Generate Allure Report') {
            steps {
                script {
                    bat '''
                        cd "C:\\Users\\karthik.chillara\\PycharmProjects\\DemoParallel0622"
                        call venv\\Scripts\\activate
                        allure generate allure-results --clean -o allure-report
                    '''
                }
            }
        }
        stage('Archive Allure Report') {
            steps {
                archiveArtifacts artifacts: 'allure-report/**', allowEmptyArchive: true
            }
        }
    }
    post {
        always {
            publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'allure-report', reportFiles: 'index.html', reportName: 'Allure Report'])
        }
    }
}
