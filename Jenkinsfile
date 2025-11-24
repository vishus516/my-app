pipeline {
    agent any
    stages {
        stage('Deploy to WSL Ubuntu') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ubuntu-key', keyFileVariable: 'KEY', usernameVariable: 'USER')]) {
                  powershell '''
                    # Get WSL IP using PowerShell (100% reliable)
                    $WSL_IP = (wsl hostname -I).Split(" ")[0]

                    # Build full destination string to avoid parsing errors
                    $DEST = "${env:USER}@$WSL_IP:/home/vishu/auto-deploy/"

                    Write-Host "============================================"
                    Write-Host "Deploying to WSL Ubuntu at $WSL_IP"
                    Write-Host "Destination: $DEST"
                    Write-Host "============================================"

                    # Kill old script
                    ssh -i "$env:KEY" -o StrictHostKeyChecking=no "${env:USER}@$WSL_IP" "pkill -f cpu_monitor.py || true"

                    # Copy new file (using $DEST to fix colon parsing)
                    scp -i "$env:KEY" -o StrictHostKeyChecking=no cpu_monitor.py "$DEST"

                    # Start new version
                    ssh -i "$env:KEY" -o StrictHostKeyChecking=no "${env:USER}@$WSL_IP" "nohup python3 /home/vishu/auto-deploy/cpu_monitor.py > /home/vishu/auto-deploy/cpu.log 2>&1 &"

                    Write-Host "============================================"
                    Write-Host "DEPLOYED SUCCESSFULLY TO UBUNTU WSL!"
                    Write-Host "============================================"
                    '''
                }
            }
        }
    }
}
