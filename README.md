# StreamFlix — DevOps Practice Project

A small Flask OTT catalogue demo for practising source control, CI/CD, containers, and cloud deployment. This is a learning application, not a real streaming service.

## Features
- Movie catalogue homepage
- User registration and login with hashed passwords
- SQLite database
- Health endpoint: `GET /health`

## Run locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY='replace-with-a-long-random-value'
python app.py
```
Open `http://localhost:5000`.

## Run with Docker
```bash
docker build -t streamflix:local .
docker run -d --name streamflix -p 5000:5000 -e SECRET_KEY='replace-this' -v streamflix-data:/data streamflix:local
```
Health check: `http://localhost:5000/health`.

## DevOps roadmap
1. GitHub source control
2. Jenkins pipeline (`Jenkinsfile` included; agent needs Docker access)
3. Docker image build and smoke test
4. Deploy image to AWS EC2
5. Provision infrastructure with Terraform
6. Configure hosts with Ansible
7. Monitor with Prometheus and Grafana

## Important
This demo does not stream licensed video. Before public production use, configure a strong `SECRET_KEY`, HTTPS, secure cookies, a production database, backups, and secrets management. Never commit passwords, cloud keys, or `.env` files.
Testing automatic GitHub webhook to Jenkins CI/CD integration.
