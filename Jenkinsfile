pipeline {
    agent any

    environment {
        IMAGE_NAME = "rishiadl29/employee-management-system"
        IMAGE_TAG  = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Trigger') {
            steps {
                script {
                    def commitMessage = sh(
                        script: 'git log -1 --pretty=%B',
                        returnStdout: true
                    ).trim()

                    if (commitMessage.startsWith('Deploy v') &&
                        commitMessage.endsWith(' via Jenkins')) {

                        echo "Jenkins-generated GitOps commit detected."
                        echo "Skipping build to prevent infinite loop."

                        env.SKIP_BUILD = "true"
                    } else {
                        env.SKIP_BUILD = "false"
                    }
                }
            }
        }

        stage('Verify Tools') {
            when {
                expression {
                    env.SKIP_BUILD != "true"
                }
            }

            steps {
                sh '''
                    docker --version
                    git --version
                '''
            }
        }

        stage('Build Docker Image') {
            when {
                expression {
                    env.SKIP_BUILD != "true"
                }
            }

            steps {
                sh '''
                    set -e

                    docker build \
                      -t "$IMAGE_NAME:$IMAGE_TAG" .

                    docker tag \
                      "$IMAGE_NAME:$IMAGE_TAG" \
                      "$IMAGE_NAME:latest"
                '''
            }
        }

        stage('Push Docker Image') {
            when {
                expression {
                    env.SKIP_BUILD != "true"
                }
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_PASSWORD'
                    )
                ]) {
                    sh '''
                        set -e

                        echo "$DOCKERHUB_PASSWORD" | \
                        docker login \
                          --username "$DOCKERHUB_USERNAME" \
                          --password-stdin

                        docker push "$IMAGE_NAME:$IMAGE_TAG"
                        docker push "$IMAGE_NAME:latest"
                    '''
                }
            }
        }

        stage('Update DEV Image Tag') {
            when {
                expression {
                    env.SKIP_BUILD != "true"
                }
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-credentials',
                        usernameVariable: 'GITHUB_USERNAME',
                        passwordVariable: 'GITHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set -e

                        echo "Updating DEV Helm image tag to $IMAGE_TAG"

                        sed -i \
                          's/tag: "v[0-9]*"/tag: "'"$IMAGE_TAG"'"/' \
                          employee-management-chart/values-dev.yaml

                        git config user.name "jenkins"
                        git config user.email "jenkins@local"

                        git add employee-management-chart/values-dev.yaml

                        if git diff --cached --quiet; then
                            echo "No changes to commit."
                            exit 0
                        fi

                        git commit -m "Deploy $IMAGE_TAG via Jenkins"

                        git remote set-url origin \
                          "https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com/Rishivardan/employee-management-system.git"

                        git push origin HEAD:main
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "CI SUCCESS ✅"
            echo "Built and pushed image: ${IMAGE_NAME}:${IMAGE_TAG}"
            echo "DEV values updated for Argo CD deployment."
        }

        failure {
            echo "CI FAILED ❌"
            echo "Check the failed stage in Jenkins Console Output."
        }

        always {
            sh 'docker logout || true'
        }
    }
}