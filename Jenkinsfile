pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main', url: 'https://github.com/Arpita07-sam/Document-Analyzer.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Start Flask App') {
            steps {
                // Run the Python script in background
                bat 'start /B python start_flask.py'
                // Wait some extra time to make sure Flask is ready
                bat 'timeout /t 10'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat 'python test_app.py'
            }
        }

        stage('Clean Up') {
            steps {
                // Kill only the Flask process
                powershell '''
                Get-Process python | Where-Object {$_.Path -like "*start_flask*"} | Stop-Process -Force
                '''
            }
        }
    }
}
