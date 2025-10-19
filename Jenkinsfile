pipeline {
    agent any

    environment {
        PYTHON_PATH = "C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
        FLASK_PORT = "5000"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main', url: 'https://github.com/Arpita07-sam/Document-Analyzer.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "\"${env.PYTHON_PATH}\" -m pip install --upgrade pip"
                bat "\"${env.PYTHON_PATH}\" -m pip install -r requirements.txt"
            }
        }

        stage('Start Flask App') {
            steps {
                powershell '''
                Write-Host "Starting Flask app..."
                $env:PYTHONUNBUFFERED = "1"
                $logPath = "$env:WORKSPACE\\flask_log.txt"
                $scriptPath = "$env:WORKSPACE\\start_flask.py"

                # Start Flask in background and redirect logs
                $global:flaskProcess = Start-Process "${env:PYTHON_PATH}" -ArgumentList $scriptPath `
                    -RedirectStandardOutput $logPath `
                    -RedirectStandardError $logPath `
                    -PassThru

                # Wait up to 30 seconds for Flask to respond
                $retries = 0
                while ($retries -lt 30) {
                    try {
                        $response = Invoke-WebRequest http://127.0.0.1:${env:FLASK_PORT} -UseBasicParsing -ErrorAction Stop
                        if ($response.StatusCode -eq 200) {
                            Write-Host "✅ Flask is up!"
                            break
                        }
                    } catch {
                        Start-Sleep -Seconds 1
                        $retries++
                    }
                }

                if ($retries -ge 30) {
                    Write-Host "❌ Flask did not start in time. Printing log..."
                    Get-Content $logPath -Tail 20
                    if ($global:flaskProcess -ne $null) {
                        Stop-Process $global:flaskProcess.Id -Force
                    }
                    exit 1
                }
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                powershell '''
                Write-Host "Running Selenium tests..."
                & "${env:PYTHON_PATH}" test_app.py
                '''
            }
        }

        stage('Clean Up') {
            steps {
                powershell '''
                if ($global:flaskProcess -ne $null) {
                    Write-Host "Stopping Flask..."
                    Stop-Process $global:flaskProcess.Id -Force
                }
                '''
            }
        }
    }
}
