pipeline {
    agent any

    stages {
        stage('Setup and Test') {
            steps {
                script {
                    bat '''
                        cd "C:\\Users\\karthik.chillara\\PycharmProjects\\KeywordDrivenAccelerator"
                        call venv\\Scripts\\activate
                        pip install -r requirements.txt
                        playwright install chromium --with-deps
                        if exist allure-results rmdir /s /q allure-results
                        if exist allure-report rmdir /s /q allure-report
                        if exist allure-report\\history (
                            mkdir allure-results
                            xcopy /E /I /Y allure-report\\history allure-results\\history
                        )
                        pytest test_web\\test_runner.py -v --alluredir=allure-results
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
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}
