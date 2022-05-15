pipeline {
    agent any
    stages {
        stage('pre_validation') {
            steps {
                slackSend channel: '#network-automation', color: "good", message: "Build Started: ${env.JOB_NAME}  ${env.BUILD_NUMBER}  (<${env.BUILD_URL}|Open>) ${env.CHANGE_AUTHOR}"
                script {
                    withCredentials([usernamePassword(credentialsId: 'cisco_pass', passwordVariable: 'GNS3_PASS', usernameVariable: 'GNS3_UNAME')]) {
                        sh 'rm -rf projects/ibgp/output'
                        sh 'mkdir -p projects/ibgp/output'
                        sh 'mkdir projects/ibgp/output/pre_validation'
                        sh 'mkdir projects/ibgp/output/post_validation'
                        sh 'mkdir projects/ibgp/output/configuration'
                        sh 'cd projects/ibgp/output && ls'
                        sh 'python3 projects/ibgp/python_scripts/pre_validation.py'
                    }
                }
            }
        }
        stage('configure') {
            steps {
                slackSend channel: '#network-automation', message: "pushing the configuration: ${env.JOB_NAME}  ${env.BUILD_NUMBER}  (<${env.BUILD_URL}|Open>) ${env.CHANGE_AUTHOR}", color: "good" 
                script {
                    withCredentials([usernamePassword(credentialsId: 'cisco_pass', passwordVariable: 'GNS3_PASS', usernameVariable: 'GNS3_UNAME')]) {
                        sh 'python3 projects/ibgp/python_scripts/config_ibgp.py'
                    }
                }
            }
        }
        stage('post_validation') {
            steps {
                slackSend channel: '#network-automation', message: "performing the post_validation: ${env.JOB_NAME}  ${env.BUILD_NUMBER}  (<${env.BUILD_URL}|Open>) ${env.CHANGE_AUTHOR}", color: "good" 
                script {
                    withCredentials([usernamePassword(credentialsId: 'cisco_pass', passwordVariable: 'GNS3_PASS', usernameVariable: 'GNS3_UNAME')]) {
                        sh 'python3 projects/ibgp/python_scripts/post_validation.py'
                        sh 'zip -r changeReq123_output.zip projects/ibgp/output'
                        archiveArtifacts artifacts: 'changeReq123_output.zip'
                        cleanWs()
                    }
                }
                slackSend channel: '#network-automation', message: "Build Successfully deployed!: ${env.JOB_NAME}  ${env.BUILD_NUMBER}  (<${env.BUILD_URL}|Open>)", color: "good"   
            }
        }
        slackSend failOnError: true, channel: '#network-automation', color: "danger", message: "Build failed at pre_validation stage: ${env.JOB_NAME}  ${env.BUILD_NUMBER}  (<${env.BUILD_URL}|Open>)"

    }
}
