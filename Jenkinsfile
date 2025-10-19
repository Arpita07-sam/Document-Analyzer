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

//         stage('Run Tests') {
//             steps {
//                 powershell '''
//                 Write-Host "🧪 Running tests..."
//                 & "$env:WORKON_HOME\\Scripts\\activate"
//                 pytest --maxfail=1 --disable-warnings -q
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


stage('Start Flask App') {
    steps {
        powershell '''
        Write-Host "🚀 Starting Flask app..."
        $logOut = "$env:WORKSPACE\\flask_stdout.txt"
        $logErr = "$env:WORKSPACE\\flask_stderr.txt"
        $scriptPath = "$env:WORKSPACE\\app.py"

        # Start Flask process
        $global:flaskProcess = Start-Process python -ArgumentList $scriptPath `
            -RedirectStandardOutput $logOut `
            -RedirectStandardError $logErr `
            -PassThru

        # Wait for server to respond
        $retries = 0
        $serverReady = $false
        while ($retries -lt 30) {
            try {
                $response = Invoke-WebRequest http://127.0.0.1:5000 -UseBasicParsing -ErrorAction Stop
                if ($response.StatusCode -eq 200) {
                    Write-Host "✅ Flask is running at http://127.0.0.1:5000"
                    $serverReady = $true
                    break
                }
            } catch {
                Start-Sleep -Seconds 1
                $retries++
            }
        }

        if (-not $serverReady) {
            Write-Host "❌ Flask did not start in time. Showing logs..."
            if (Test-Path $logOut) { Write-Host "--- STDOUT ---"; Get-Content $logOut -Tail 20 }
            if (Test-Path $logErr) { Write-Host "--- STDERR ---"; Get-Content $logErr -Tail 20 }
            if ($global:flaskProcess -ne $null) { Stop-Process $global:flaskProcess.Id -Force }
            exit 1
        }
        '''
    }
}
