pipeline {
  agent any

  stages {
    stage('Setup servers and run tests') {
      environment {
        BACKEND_ENV_FILE = credentials('backend-env-variables')
        FRONTEND_ENV_FILE = credentials('frontend-env-variables')
      }

      parallel {
        stage('Setup and run backend server') {
          steps {
            dir('salt-api') {
              // Checkout the backend repository
              git branch: 'development', url: 'https://github.com/saltastroops/salt-api.git'

              sh '''
                cd ../
                ./run-backend-server.sh
              '''
            }
          }
        }

        stage('Setup frontend server and run tests') {
          steps {
            dir('salt-testdata') {
              // Checkout the salt testdata repository
              git branch: 'main', credentialsId: 'github-creds', url: 'https://github.com/saltastroops/salt-testdata.git'
            }

            sh '''
              ./run-frontend-server-and-tests.sh
            '''
          }
        }
      }
    }
  }

  post {
    always {
      cleanWs()
    }
  }
}


