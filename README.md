# Scientific Calculator DevOps Pipeline

A Python-based scientific calculator implemented with a simple CLI and a complete CI/CD pipeline: unit tests with pytest, containerization with Docker, automated builds and pushes via Jenkins, deployment using Ansible, and auto-triggers from GitHub webhooks through ngrok.

## Features

- Calculator operations
  - sqrt(x): Valid for $$x \ge 0$$. Raises a domain error for negatives.
  - factorial(n): Valid for non-negative integers. Iterative implementation.
  - ln(x): Natural logarithm. Valid for $$x > 0$$.
  - power(a, b): Supports integer and real exponents; rejects negative base with non-integer exponent to avoid complex outputs.

- CLI
  - Menu-driven interface to select operations, input values, and display results.
  - Input validation with clear error messages for invalid domains or types.

- Tests
  - pytest suite covering correct behavior and domain errors for each function.

- DevOps pipeline
  - Source control: GitHub repo with Jenkinsfile at root.
  - CI: Jenkins Pipeline with stages for checkout, Python setup, tests, Docker build, and Docker push.
  - CD: Optional Ansible deploy stage to pull and run the container on localhost.
  - Image registry: Docker Hub (docker.io/tah1rthet1ger/scientific-calculator).
  - Webhooks: GitHub push events trigger Jenkins via an ngrok HTTPS tunnel.

## Repository structure

- calculator.py: Core functions and domain error class.
- main.py: Interactive CLI menu.
- tests/test_calculator.py: Unit tests.
- Dockerfile: Container image definition for the CLI app.
- Jenkinsfile: Declarative pipeline for CI/CD.
- ansible/
  - inventory.ini: localhost inventory.
  - deploy.yml: Playbook to pull and run container.
- README.md: This file.

## Local development

### Prerequisites

- Python 3.12+
- pip/venv
- Docker Engine (for container build/run)
- Git

### Setup

- Create and activate venv, install test dependencies:
  - python3 -m venv .venv
  - source .venv/bin/activate
  - pip install -U pip pytest

- Run tests:
  - export PYTHONPATH=.
  - pytest -q

- Run CLI locally:
  - python main.py

### Docker

- Build image:
  - docker build -t docker.io/tah1rthet1ger/scientific-calculator:latest .

- Run container:
  - docker run -it --rm docker.io/tah1rthet1ger/scientific-calculator:latest

- Push to Docker Hub:
  - docker login
  - docker push docker.io/tah1rthet1ger/scientific-calculator:latest

## Jenkins CI/CD

### Pipeline stages

- Checkout: Pulls main branch from GitHub.
- Setup Python: Creates venv and installs pytest.
- Test: Runs unit tests with PYTHONPATH set.
- Docker Build: Builds and tags image as BUILD_NUMBER and latest.
- Docker Push: Logs into Docker Hub using Jenkins credentials and pushes both tags.
- Deploy (optional): Runs Ansible playbook to pull and start the container on localhost.

### Prerequisites

- Jenkins installed and running on localhost:8080.
- Jenkins user added to docker group and service restarted:
  - sudo usermod -aG docker jenkins
  - sudo systemctl restart jenkins

- Credentials:
  - Docker Hub: Username/Password credential with ID dockerhub-creds.

- Job configuration:
  - New Item → Pipeline → “Pipeline script from SCM”
  - SCM: Git → Repository URL: https://github.com/Tah1rTheT1ger/scientific-calculator-devops.git
  - Branch: main
  - Script Path: Jenkinsfile
  - Build Triggers: “GitHub hook trigger for GITScm polling” (if using webhooks)

## Ansible deployment

### Files

- ansible/inventory.ini:
  - [local]
    localhost ansible_connection=local ansible_python_interpreter=/usr/bin/python3

- ansible/deploy.yml (passwordless sudo not required if Docker is already running and jenkins is in docker group):
  - Ensure Docker service (optional, requires sudo)
  - Pull image: docker.io/tah1rthet1ger/scientific-calculator:latest
  - Run container: name calc, detached, tty/interactive

### Run

- ansible-galaxy collection install community.docker
- ansible-playbook -i ansible/inventory.ini ansible/deploy.yml

## Verify

- docker ps
- docker attach calc
- Detach without stopping: Ctrl-p then Ctrl-q

## GitHub webhook via ngrok

- Install ngrok v3 and add authtoken.
- Start tunnel to Jenkins:
  - ngrok http 8080

- Copy the HTTPS forwarding URL from ngrok output.
- GitHub repo → Settings → Webhooks → Add webhook:
  - Payload URL: https://YOUR-NGROK-ID.ngrok-free.app/github-webhook/
  - Content type: application/json
  - Events: Just the push event
  - Secret: Optional shared secret for validation

- Push a commit to main; Jenkins should auto-build.

## Security notes

- Docker permissions: The jenkins user must be in the docker group to run docker commands without sudo.
- Sudo in Ansible: If managing services in the deploy stage, either allow passwordless sudo for the specific systemctl commands or run those tasks manually outside Jenkins.

## Troubleshooting

- pytest cannot import calculator:
  - Ensure tests run from repo root and set PYTHONPATH=.

- Docker build in Jenkins cannot find Dockerfile:
  - Confirm Dockerfile is at repo root and committed.

- Jenkins cannot push to Docker Hub:
  - Ensure dockerhub-creds matches Docker Hub username tah1rthet1ger and is referenced in Jenkinsfile.

- Ansible “requests” module error:
  - Use ansible_python_interpreter=/usr/bin/python3, or install requests into the interpreter Ansible uses.

- Jenkins Deploy stage fails with sudo prompt:
  - Either grant passwordless sudo for required commands or remove become and skip service management.

- ngrok agent version too old:
  - Install ngrok v3 and ensure PATH uses the new binary; verify with ngrok version.

## How to use the app

- CLI examples:
  - sqrt: x=9 → 3
  - factorial: n=5 → 120
  - ln: x≈2.718281828 → ≈1
  - power: a=2, b=10 → 1024

- Container runtime:
  - docker run -it --rm docker.io/tah1rthet1ger/scientific-calculator:latest
  - Or deploy via Ansible and attach to the running container calc.


### Tiny Change