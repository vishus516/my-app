pipeline {
    agent any
    stages {
        stage('Deploy to WSL Ubuntu') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'wsl-deploy-key', keyFileVariable: 'KEY', usernameVariable: 'USER')]) {
                    bat '''
                    @echo off
                    set WSL_IP=
                    for /f "skip=1 tokens=1" %%i in (\'wsl hostname -I 2^>nul\') do if not defined WSL_IP set WSL_IP=%%i

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
