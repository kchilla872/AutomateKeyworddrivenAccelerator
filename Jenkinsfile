pipeline {
    agent any

    stages {
        stage('Setup and Test') {
            steps {
                script {
                    bat '''
                        cd "C:\\Users\\karthik.chillara\\PycharmProjects\\\KeywordDrivenAutomate"
                        venv\\Scripts\\python.exe -m pip install --upgrade pip
                        venv\\Scripts\\python.exe -m pip install -r requirements.txt
                        venv\\Scripts\\python.exe -m playwright install chromium --with-dep
                        venv\\Scripts\\python.exe -m pytest -n 2 --html=report.html --self-contained-html
                    '''
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'report.html'
        }
    }
}
