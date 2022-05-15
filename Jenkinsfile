def COLOR_MAP = [
    'SUCCESS': 'good', 
    'FAILURE': 'danger',
]


def getBuildUser() {
    return currentBuild.rawBuild.getCause(Cause.UserIdCause).getUserId()
}

pipeline {
    // Set up local variables for your pipeline
    environment {
        // test variable: 0=success, 1=fail; must be string
        doError = '0'
        BUILD_USER = ''
    }

    agent any

    stages {
        stage('Error') {
            // when doError is equal to 1, return an error
            when {
                expression { doError == '1' }
            }
            steps {
                echo "Failure :("
                error "Test failed on purpose, doError == str(1)"
            }
        }
        stage('Success') {
            // when doError is equal to 0, just print a simple message
            when {
                expression { doError == '0' }
            }
            steps {
                echo "Success :)"
            }
        }
    }

    // Post-build actions
    post {
        always {
            script {
                BUILD_USER = getBuildUser()
            }
            echo 'I will always say hello in the console.'
            slackSend channel: '#network-automation',
                color: COLOR_MAP[currentBuild.currentResult],
                message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER} by ${BUILD_USER}\n More info at: ${env.BUILD_URL}"
        }
    }
}
