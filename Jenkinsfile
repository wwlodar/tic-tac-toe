pipeline {
 agent any
triggers {
    githubPush()
}

stages {

    stage('Setup'){
       steps{
        dir('.'){
            sh 'python3.8 -m venv ./venv'
        }
        }
     }


stage('Unit Tests'){
           steps{
             dir('.') {
                 sh '. ./venv/bin/activate'
                 sh 'pip install -r requirements.txt'
                 sh 'pytest -v --junitxml=docs/unit-tests/htmlcoverage/coverage.xml --cov-report xml --cov app.main'
             }
            }
         }
       stage('Publish Test Report'){
           steps{
              cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'coverage*.xml', conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false, failUnstable: false, lineCoverageTargets: '80, 0, 0', maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false
              archiveArtifacts artifacts: 'docs/unit-tests/htmlcoverage/*.*'
            }
         }

      }
}