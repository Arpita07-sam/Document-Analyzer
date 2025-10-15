pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning the repository...'
                git 'https://github.com/Arpita07-sam/Document-Analyzer.git' // change this to your repo URL
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                sh 'python -m venv env'
                sh '.\\env\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('Start Flask App') {
            steps {
                echo 'Starting Flask server...'
                // Run Flask in the background so tests can access http://127.0.0.1:5000
                bat 'start /B cmd /C "env\\Scripts\\activate && python app.py"'
                sleep(time: 5, unit: 'SECONDS') // wait for app to start
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo 'Running Selenium tests...'
                bat '.\\env\\Scripts\\activate && python -m unittest test_app.py'
            }
        }

        stage('Clean Up') {
            steps {
                echo 'Stopping Flask server...'
                // Stop Flask if needed
                bat 'taskkill /F /IM python.exe || exit 0'
            }
        }
    }
}
