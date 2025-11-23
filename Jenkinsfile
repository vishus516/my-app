pipeline {
    agent any

    stages {
        stage('Deploy CPU Monitor to WSL Ubuntu') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'wsl-deploy-key', 
                                                  keyFileVariable: 'KEY', 
                                                  usernameVariable: 'USER')]) {
                    sh '''
                    # Get current WSL IP
                    WSL_IP=$(hostname -I | awk "{print \$1}")

                    echo "Deploying to WSL at $WSL_IP"

                    # Kill old script
                    ssh -i "$KEY" -o StrictHostKeyChecking=no $USER@$WSL_IP "pkill -f cpu_monitor.py || true"

                    # Copy new file
                    scp -i "$KEY" -o StrictHostKeyChecking=no cpu_monitor.py $USER@$WSL_IP:/home/vishu/auto-deploy/

                    # Start new version
                    ssh -i "$KEY" -o StrictHostKeyChecking=no $USER@$WSL_IP "
                        nohup python3 /home/vishu/auto-deploy/cpu_monitor.py > /home/vishu/auto-deploy/cpu.log 2>&1 &
                    "

                    echo "CPU monitor auto-deployed to WSL Ubuntu!"
                    '''
                }
            }
        }
    }

    post {
        success { echo 'Your CPU monitor is now running on Ubuntu WSL!' }
    }
}
