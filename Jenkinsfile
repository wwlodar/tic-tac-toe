pipeline {
  agent any
  stages {
    stage('Build') {
      parallel {
        stage('Build') {
          steps {
            sh 'echo "building the repo"'
          }
        }
      }
    }

    stage('Test') {
      steps {
        sh 'pip install pytest'
        sh 'pytest app/tests/'
        input(id: "Deploy Gate", message: "Deploy ${params.project_name}?", ok: 'Deploy')
      }
    }

    stage('Deploy')
    {
      steps {
        echo "deploying the application"
      }
    }

  }

  post {
        always {
            echo 'The pipeline completed'
            junit allowEmptyResults: true, testResults:'**/test_reports/*.xml'
        }
        success {

            sh "sudo nohup python3 app.run.py > log.txt 2>&1 &"
            echo "Flask Application Up and running!!"
        }
        failure {
            echo 'Build stage failed'
            error('Stopping early…')
        }
      }
}