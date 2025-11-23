pipeline {
    agent any
    stages {
        stage('Deploy to WSL Ubuntu') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ubuntu-key', keyFileVariable: 'KEY', usernameVariable: 'USER')]) {
                  bat '''
                        @echo off
                        :: 100% WORKING WSL IP DETECTION FOR WINDOWS JENKINS
                        for /f "delims=" %%i in (\'wsl -e sh -c "ip route get 1 ^| awk \'{print \$7}\' ^| tr -d \'\\n\'"\') do set WSL_IP=%%i
                        
                        echo ========================================
                        echo Deploying to WSL Ubuntu at %WSL_IP%
                        echo ========================================
                        
                        ssh -i "%KEY%" -o StrictHostKeyChecking=no %USER%@%WSL_IP% "pkill -f cpu_monitor.py || true"
                        scp -i "%KEY%" -o StrictHostKeyChecking=no cpu_monitor.py %USER%@%WSL_IP%:/home/vishu/auto-deploy/
                        ssh -i "%KEY%" -o StrictHostKeyChecking=no %USER%@%WSL_IP% "nohup python3 /home/vishu/auto-deploy/cpu_monitor.py > /home/vishu/auto-deploy/cpu.log 2>&1 &"
                        
                        echo ========================================
                        echo DEPLOYED SUCCESSFULLY TO UBUNTU WSL!
                        echo ========================================
                        '''
                }
            }
        }
    }
}
