pipeline {
    agent any
    stages {
        stage('Deploy to WSL Ubuntu') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ubuntu-key', keyFileVariable: 'KEY', usernameVariable: 'USER')]) {
                  powershell '''
                        # Get WSL IP (Windows → WSL)
                        $WSL_IP = (wsl hostname -I).Split(" ")[0]

                        # PowerShell CANNOT handle ${env:USER} — fix:
                        # Jenkins provides username in $env:USER, NOT ${env:USER}
                        $DestUser = $env:USER
                        $Dest = "$DestUser@$($WSL_IP):/home/vishu/auto-deploy/"

                        Write-Host "============================================"
                        Write-Host "Deploying to: $Dest"
                        Write-Host "============================================"

                        # Convert Windows key path to MSYS path for scp
                        $KeyFile = $env:KEY
                        if ($KeyFile -match '^[A-Z]:\\\\') {
                            $drive = $KeyFile.Substring(0,1).ToLower()
                            $rest = $KeyFile.Substring(2) -replace '\\\\','/'
                            $KeyFile = "/$drive/$rest"
                        }

                        # Run SCP to WSL
                        $cmd = "scp -i `"$KeyFile`" -o StrictHostKeyChecking=no -r * $Dest"
                        Write-Host "Running: $cmd"
                        cmd.exe /c $cmd

                        if ($LASTEXITCODE -ne 0) {
                            Write-Error "SCP failed with exit code $LASTEXITCODE"
                            exit $LASTEXITCODE
                        } else {
                            Write-Host "Deployment completed successfully."
                        }
                    '''
                }
            }
        }
    }
}
