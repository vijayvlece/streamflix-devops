
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'streamflix'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate') {
            steps {
                sh 'python3 -m py_compile app.py'
                sh 'test -f requirements.txt && test -f Dockerfile'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER .'
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    docker rm -f streamflix-ci-test || true
                    docker run -d --name streamflix-ci-test -p 5050:5000 $IMAGE_NAME:$BUILD_NUMBER

                    for i in $(seq 1 20); do
                        if curl -fsS http://localhost:5050/health; then
                            docker rm -f streamflix-ci-test
                            exit 0
                        fi
                        sleep 2
                    done

                    docker logs streamflix-ci-test
                    docker rm -f streamflix-ci-test || true
                    exit 1
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker tag $IMAGE_NAME:$BUILD_NUMBER $DOCKERHUB_USER/streamflix:$BUILD_NUMBER
                        docker tag $IMAGE_NAME:$BUILD_NUMBER $DOCKERHUB_USER/streamflix:latest
                        docker push $DOCKERHUB_USER/streamflix:$BUILD_NUMBER
                        docker push $DOCKERHUB_USER/streamflix:latest
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f streamflix || true
                    docker run -d \
                        --name streamflix \
                        --restart unless-stopped \
                        -p 5000:5000 \
                        -v streamflix-data:/data \
                        $IMAGE_NAME:$BUILD_NUMBER

                    sleep 5
                    curl -fsS http://localhost:5000/health
                '''
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f || true'
        }
    }
}
