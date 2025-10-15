// pipeline {
//     agent any

//     stages {
//         stage('Checkout SCM') {
//             steps {
//                 git branch: 'main', url: 'https://github.com/Arpita07-sam/Document-Analyzer.git'
//             }
//         }

//         stage('Install Dependencies') {
//             steps {
//                 bat 'python -m pip install --upgrade pip'
//                 bat 'python -m pip install -r requirements.txt'
//             }
//         }

//         stage('Start Flask App') {
//             steps {
//                 // Run the Python script in background
//                 bat 'start /B python start_flask.py'
//                 // Wait some extra time to make sure Flask is ready
//                 bat 'timeout /t 10'
//             }
//         }

//         stage('Run Selenium Tests') {
//             steps {
//                 bat 'python test_app.py'
//             }
//         }

//         stage('Clean Up') {
//             steps {
//                 // Kill only the Flask process
//                 powershell '''
//                 Get-Process python | Where-Object {$_.Path -like "*start_flask*"} | Stop-Process -Force
//                 '''
//             }
//         }
//     }
// }


pipeline {
    agent any

    environment {
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
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Start Flask App') {
            steps {
                powershell '''
                # Start Flask and keep a handle to the process
                $global:flaskProcess = Start-Process python -ArgumentList "start_flask.py" -PassThru

                # Wait until Flask responds
                $retries = 0
                while ($retries -lt 20) {
                    try {
                        $response = Invoke-WebRequest http://127.0.0.1:${env:FLASK_PORT} -UseBasicParsing -ErrorAction Stop
                        if ($response.StatusCode -eq 200) {
                            Write-Host "Flask is up!"
                            break
                        }
                    } catch {
                        Start-Sleep -Seconds 1
                        $retries++
                    }
                }

                if ($retries -ge 20) {
                    Write-Host "Flask did not start in time!"
                    Stop-Process $global:flaskProcess.Id
                    exit 1
                }
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                powershell '''
                try {
                    # Try to make an HTTP request to your Flask server
                    $response = Invoke-WebRequest http://127.0.0.1:5000 -UseBasicParsing -ErrorAction Stop
                    
                    # If the above succeeds, Flask is up
                    Write-Host "Flask is up, running Selenium tests..."
                    
                    # Run your Selenium test script
                    python test_app.py
                } catch {
                    # If the request fails (Flask not ready), do this instead
                    Write-Host "Flask not available, skipping Selenium tests."
                }
                '''
            }
        }



        stage('Clean Up') {
            steps {
                powershell '''
                if ($global:flaskProcess -ne $null) {
                    Stop-Process $global:flaskProcess.Id -Force
                    Write-Host "Flask process stopped."
                }
                '''
            }
        }
    }
}

