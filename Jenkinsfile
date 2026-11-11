pipeline {
    agent any
    environment { IMAGE_NAME = 'streamflix' }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Validate') {
            steps {
                sh 'python3 -m py_compile app.py'
                sh 'test -f requirements.txt && test -f Dockerfile'
            }
        }
        stage('Build Docker Image') {
            steps { sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER .' }
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
    }
    post { always { sh 'docker image prune -f || true' } }
}
