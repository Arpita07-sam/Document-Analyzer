// pipeline {
//     agent any

//     environment {
//         PYTHON_PATH = 'C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'   // ✅ change if your Python path differs
//         FLASK_PORT = '5000'
//         WORKON_HOME = "${WORKSPACE}\\venv"
//     }

//     stages {

//         stage('Checkout') {
//             steps {
//                 echo '📥 Checking out code...'
//                 checkout scm
//             }
//         }

//         stage('Setup Python Environment') {
//             steps {
//                 powershell '''
//                 Write-Host "🐍 Setting up Python virtual environment..."
//                 if (Test-Path $env:WORKON_HOME) {
//                     Write-Host "Existing venv found — removing..."
//                     Remove-Item -Recurse -Force $env:WORKON_HOME
//                 }
//                 python -m venv $env:WORKON_HOME
//                 & "$env:WORKON_HOME\\Scripts\\activate"
//                 python -m pip install --upgrade pip
//                 pip install -r requirements.txt
//                 '''
//             }
//         }

//         stage('Start Flask App') {
            

//             steps {
//                 powershell '''
//                 Write-Host "🚀 Starting Flask app..."

//                 # Activate virtual environment
//                 & "$env:WORKON_HOME\\Scripts\\activate"

//                 # Set environment variables
//                 $env:FLASK_APP = "$env:WORKSPACE\\app.py"
//                 $env:FLASK_ENV = "development"
//                 $env:FLASK_RUN_HOST = "0.0.0.0"
//                 $env:FLASK_RUN_PORT = "5000"


//                 $env:PYTHONUNBUFFERED = "1"
//                 $logOut = "$env:WORKSPACE\\flask_stdout.txt"
//                 $logErr = "$env:WORKSPACE\\flask_stderr.txt"
//                 $scriptPath = "$env:WORKSPACE\\app.py"

//                 # Start Flask in background
//                 $global:flaskProcess = Start-Process "${env:PYTHON_PATH}" -ArgumentList $scriptPath `
//                     -RedirectStandardOutput $logOut `
//                     -RedirectStandardError $logErr `
//                     -PassThru

//                 Write-Host "Waiting for Flask to start on port ${env:FLASK_PORT}..."
//                 $retries = 0
//                 while ($retries -lt 30) {
//                     try {
//                         $response = Invoke-WebRequest http://127.0.0.1:${env:FLASK_PORT} -UseBasicParsing -ErrorAction Stop
//                         if ($response.StatusCode -eq 200) {
//                             Write-Host "✅ Flask is running!"
//                             break
//                         }
//                     } catch {
//                         Start-Sleep -Seconds 1
//                         $retries++
//                     }
//                 }

//                 if ($retries -ge 30) {
//                     Write-Host "❌ Flask did not start in time. Showing logs..."
//                     if (Test-Path $logOut) { Write-Host "`n--- STDOUT ---"; Get-Content $logOut -Tail 20 }
//                     if (Test-Path $logErr) { Write-Host "`n--- STDERR ---"; Get-Content $logErr -Tail 20 }
//                     if ($global:flaskProcess -ne $null) { Stop-Process $global:flaskProcess.Id -Force }
//                     exit 1
//                 }
//                 '''
//             }
//         }

//         stage('Run Selenium Tests') {
//             steps {
//                 powershell '''
//                 Write-Host "🧪 Running Selenium tests from test_app.py..."

//                 # Activate Python virtual environment
//                 & "$env:WORKON_HOME\\Scripts\\activate"

//                 # Run the Selenium unittest file
//                 python -m unittest "$env:WORKSPACE\\test_app.py"
//                 '''
//             }
//         }


//     }

//     post {
//         always {
//             powershell '''
//             Write-Host "🧹 Cleaning up..."
//             if ($global:flaskProcess -ne $null) {
//                 Stop-Process $global:flaskProcess.Id -Force
//                 Write-Host "✅ Flask process stopped."
//             }
//             '''
//         }
//         success {
//             echo '🎉 Build successful!'
//         }
//         failure {
//             echo '❌ Build failed!'
//         }
//     }
// }

pipeline {
    agent any

    environment {
        PYTHON = "venv\\Scripts\\python.exe"
    }

    stages {
        stage('Setup Python') {
            steps {
                echo "Setting up Python environment..."
                bat '''
                if not exist venv (
                    python -m venv venv
                )
                venv\\Scripts\\pip.exe install --upgrade pip
                venv\\Scripts\\pip.exe install -r requirements.txt
                venv\\Scripts\\pip.exe install selenium webdriver-manager
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Running Selenium tests..."
                bat '''
                %PYTHON% test_app.py
                '''
            }
        }
    }

    
    post {
        always {
            echo "Cleaning up..."
            bat """
            @echo off
            setlocal
            set ERRORLEVEL=0
            for /F "tokens=2" %%a in ('tasklist ^| find "python.exe"') do (
                taskkill /PID %%a /F >nul 2>&1 || set ERRORLEVEL=0
            )
            endlocal
            """
        }
    }

}
