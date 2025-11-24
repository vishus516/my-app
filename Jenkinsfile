pipeline {
    agent any
    stages {
        stage('Deploy to WSL Ubuntu') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ubuntu-key', keyFileVariable: 'KEY', usernameVariable: 'USER')]) {
                  powershell '''
                        # Debug: Print Jenkins env vars
                        Write-Host "DEBUG: Jenkins $env:USER = $env:USER"
                        Write-Host "DEBUG: Jenkins $env:KEY = $env:KEY (masked)"

                        # Get the exact account name running the job (DOMAIN\\User or MACHINE\\User)
                            $who = (cmd.exe /c whoami).Trim()
                            Write-Host "Running as: $who"

                        # Get WSL IP (Windows → WSL)
                        $rawOutput = wsl -d Ubuntu hostname -I
                        Write-Host "DEBUG: Raw WSL IPs = $rawOutput"
                        $allIPs = $rawOutput.Split(" ")
                        $WSL_IP = $allIPs[0]  # First IP is the NAT one (172.27.4.218)
                        Write-Host "DEBUG: $WSL_IP = $WSL_IP"

                        # PowerShell CANNOT handle ${env:USER} — fix:
                        # Jenkins provides username in $env:USER, NOT ${env:USER}
                        $DestUser = $env:USER
                        Write-Host "DEBUG: $DestUser = $DestUser"

                        $Dest = "$DestUser@$($WSL_IP):/home/vishu/auto-deploy/"
                        Write-Host "DEBUG: $Dest = $Dest"

                    
                        Write-Host "============================================"
                        Write-Host "Deploying to WSL Ubuntu at $WSL_IP"
                        Write-Host "Destination: $Dest"
                        Write-Host "============================================"

                        # Kill old script
                        ssh -i "$env:KEY" -o StrictHostKeyChecking=no "$env:USER@$WSL_IP" "pkill -f cpu_monitor.py || true"

                        # Copy new file (using $Dest to fix colon parsing)
                        scp -i "$env:KEY" -o StrictHostKeyChecking=no cpu_monitor.py "$Dest"

                        # Start new version
                        ssh -i "$env:KEY" -o StrictHostKeyChecking=no "$env:USER@$WSL_IP" "nohup python3 /home/vishu/auto-deploy/cpu_monitor.py > /home/vishu/auto-deploy/cpu.log 2>&1 &"

                        Write-Host "============================================"
                        Write-Host "DEPLOYED SUCCESSFULLY TO UBUNTU WSL!"
                        Write-Host "============================================"
                        '''
                }
            }
        }
    }
}
