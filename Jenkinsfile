

pipeline {
    agent any

    stages {
        stage('Start Flask App') {
            steps {
                bat 'start /B python app.py'
                echo 'Waiting for Flask to become available...'
                powershell '''
                $retries = 0
                while ($retries -lt 10) {
                    try {
                        $response = Invoke-WebRequest http://127.0.0.1:5000 -UseBasicParsing -ErrorAction Stop
                        if ($response.StatusCode -eq 200) {
                            Write-Host "Flask is up!"
                            exit 0
                        }
                    } catch {
                        Start-Sleep -Seconds 3
                        $retries++
                    }
                }
                Write-Host "Flask app did not start in time!"
                exit 1
                '''
            }
        }

        stage('Checkout SCM') {
            steps {
                git branch: 'main', url: 'https://github.com/Arpita07-sam/Document-Analyzer.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Start Flask App') {
            steps {
                bat 'start /B python app.py'  // Windows
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat 'python test_app.py'
            }
        }

        stage('Clean Up') {
            steps {
                bat 'taskkill /F /IM python.exe'  // Stop Flask server
            }
        }
    }
}
