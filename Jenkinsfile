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
//                 bat 'python -m pip install -r requirements.txt'
//             }
//         }

//         stage('Start Flask App') {
//             steps {
//                 bat 'start /B python app.py'
//                 echo 'Waiting for Flask to become available...'
//                 powershell '''
//                 $retries = 0
//                 while ($retries -lt 10) {
//                     try {
//                         $response = Invoke-WebRequest http://127.0.0.1:5000 -UseBasicParsing -ErrorAction Stop
//                         if ($response.StatusCode -eq 200) {
//                             Write-Host "Flask is up!"
//                             exit 0
//                         }
//                     } catch {
//                         Start-Sleep -Seconds 3
//                         $retries++
//                     }
//                 }
//                 Write-Host "Flask app did not start in time!"
//                 exit 1
//                 '''
//             }
//         }

//         stage('Run Selenium Tests') {
//             steps {
//                 bat 'python test_app.py'
//             }
//         }

//         stage('Clean Up') {
//             steps {
//                 bat 'taskkill /F /IM python.exe'
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
                // Start Flask in a new PowerShell process and keep the PID
                powershell '''
                $global:flaskProcess = Start-Process python -ArgumentList "app.py" -PassThru
                $retries = 0
                while ($retries -lt 10) {
                    try {
                        $response = Invoke-WebRequest http://127.0.0.1:${env:FLASK_PORT} -UseBasicParsing -ErrorAction Stop
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

        stage('Run Selenium Tests') {
            steps {
                bat 'python test_app.py'
            }
        }

        stage('Clean Up') {
            steps {
                powershell '''
                if ($global:flaskProcess -ne $null) {
                    Stop-Process -Id $global:flaskProcess.Id -Force
                    Write-Host "Flask process stopped."
                }
                '''
            }
        }
    }
}


