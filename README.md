# ALX Backend Python Projects

This repository contains a collection of Python backend development projects and exercises, focusing on Django web framework, advanced Python concepts, and software engineering best practices.

## Repository Overview

This repository is organized into multiple project directories, each focusing on different aspects of backend development with Python and Django. The projects progress from fundamental Python concepts to advanced Django features.

## Project Structure

```
alx-backend-python/
├── python-generators-0x00/              # Python generators: seeding, streaming, batching
├── python-decorators-0x01/               # Python decorators and function wrappers
├── python-context-async-operations-0x02/ # Context managers and async operations
├── 0x03-Unittests_and_integration_tests/ # Unit testing and integration testing
├── Django-Middleware-0x03/              # Django middleware implementation
├── Django-signals_orm-0x04/              # Django signals, ORM, and caching
├── messaging_app/                        # Standalone messaging application
└── venv/                                 # Virtual environment (gitignored)
```

The repository is hosted at:  
**GitHub**: [Adika-Junior/alx-backend-python](https://github.com/Adika-Junior/alx-backend-python)

## Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Django 4.2**: Web framework for backend development
- **Django REST Framework**: Building RESTful APIs
- **SQLite/MySQL**: Database systems

### Key Libraries & Tools
- **pytest**: Testing framework
- **JWT (Simple JWT)**: Authentication tokens
- **django-filters**: Advanced filtering
- **LocMemCache**: In-memory caching

## Projects

### 1. Python Generators (python-generators-0x00)
**Focus**: Python generators for efficient data processing
- MySQL database seeding
- Streaming rows with generators
- Batch processing
- Lazy pagination
- Memory-efficient aggregate computations

**Key Concepts**: Generators, iterators, memory optimization, database cursors

### 2. Python Decorators (python-decorators-0x01)
**Focus**: Python decorators and function wrappers
- Function decorators
- Class decorators
- Decorator patterns
- Function wrapping and modification

**Key Concepts**: Decorators, closures, function composition, metaprogramming

### 3. Context Managers & Async Operations (python-context-async-operations-0x02)
**Focus**: Context managers and asynchronous programming
- Context manager implementation
- Async/await patterns
- Resource management
- Asynchronous I/O operations

**Key Concepts**: Context managers, async/await, resource cleanup, concurrent programming

### 4. Unit Tests & Integration Tests (0x03-Unittests_and_integration_tests)
**Focus**: Testing methodologies and best practices
- Unit testing with pytest/unittest
- Integration testing
- Test fixtures and mocking
- Test coverage and quality

**Key Concepts**: TDD, test isolation, mocking, fixtures, coverage

### 5. Django Middleware (Django-Middleware-0x03)
**Focus**: Django middleware development
- Custom middleware implementation
- Request/response processing
- Authentication middleware
- Logging and monitoring middleware
- Access control middleware

**Key Concepts**: Middleware, request processing, authentication, authorization

### 6. Django Signals, ORM & Caching (Django-signals_orm-0x04)
**Focus**: Advanced Django features
- **Django Signals**: Event-driven programming with post_save, pre_save, post_delete
- **Advanced ORM**: select_related, prefetch_related, custom managers, query optimization
- **Caching**: View-level caching, LocMemCache configuration
- **Threaded Conversations**: Self-referential models, recursive queries
- **Custom Managers**: UnreadMessagesManager for efficient filtering

**Key Concepts**: Signals, ORM optimization, caching strategies, query optimization, N+1 problem

### 7. Messaging App (messaging_app)
**Focus**: Standalone messaging application
- User authentication
- Conversation management
- Message handling
- RESTful API design

#### Messaging App – Features

- **JWT-based authentication**:
  - Uses `djangorestframework-simplejwt` to issue and verify access/refresh tokens.
  - Custom user model (`chats.User`) configured via `AUTH_USER_MODEL`.
- **Conversations & messages API**:
  - RESTful endpoints built with Django REST Framework.
  - Nested routing via `drf-nested-routers` for resources like `/conversations/{id}/messages/`.
- **Filtering, search, and ordering**:
  - Uses `django-filter` and DRF filter backends for flexible querying.
- **Pagination & performance**:
  - Page-number pagination with configurable page size.
  - Query optimization in ORM to avoid N+1 where applicable.
- **MySQL-backed persistence**:
  - `mysqlclient` used to connect to a MySQL database in both local and Kubernetes environments.
- **Comprehensive testing and quality checks**:
  - `pytest` + `pytest-django` for unit/integration tests.
  - `flake8` for linting and style enforcement.
  - `coverage` for code coverage metrics and CI artifacts.
- **Containerization & orchestration**:
  - Dockerfile for building an app image.
  - Kubernetes manifests for deployments, services, ConfigMaps, and ingress.
- **CI/CD automation**:
  - Jenkins Pipeline for Dockerized CI and image publishing.
  - GitHub Actions workflows for testing, linting, coverage, and Docker image builds.

#### Messaging App – Development & Production Setup

- **Development (local)**:
  - From the repository root:
    ```bash
    cd messaging_app
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
  - Start a MySQL instance (recommended: use the provided `docker-compose.yml`):
    ```bash
    cd messaging_app
    docker-compose up -d
    ```
  - Apply migrations and run the development server:
    ```bash
    python manage.py migrate
    python manage.py runserver 0.0.0.0:8000
    ```

- **Environment configuration (dev & prod)**:
  - `messaging_app/messaging_app/settings.py` is environment‑aware:
    - **`DJANGO_SECRET_KEY`**: secret key for production.
    - **`DJANGO_DEBUG`**: `"True"`/`"False"` to control debug mode.
    - **`DJANGO_ALLOWED_HOSTS`**: comma‑separated list of allowed hosts (e.g. `example.com,api.example.com`).
    - **Database** (MySQL) uses:
      - `MYSQL_DB` / `MYSQL_DATABASE`
      - `MYSQL_USER`
      - `MYSQL_PASSWORD`
      - `MYSQL_HOST`
      - `MYSQL_PORT`
  - In development, `DJANGO_DEBUG` defaults to `True` and `ALLOWED_HOSTS` is relaxed; in production, set `DJANGO_DEBUG=False` and configure `DJANGO_ALLOWED_HOSTS` explicitly.

- **Production (Docker image)**:
  - The app ships with a `Dockerfile` in `messaging_app/` that:
    - Uses `python:3.10-slim`.
    - Installs dependencies from `requirements.txt`.
    - Copies the project and exposes port `8000`.
  - A production container can be run with the appropriate environment variables:
    ```bash
    docker run -d --name messaging_app \
      -p 8000:8000 \
      -e DJANGO_SECRET_KEY=your-production-secret \
      -e DJANGO_DEBUG=False \
      -e DJANGO_ALLOWED_HOSTS=your-domain.com \
      -e MYSQL_DB=messaging_app \
      -e MYSQL_USER=messaging_user \
      -e MYSQL_PASSWORD=messaging_password \
      -e MYSQL_HOST=db-host \
      -e MYSQL_PORT=3306 \
      your-dockerhub-username/messaging_app:latest
    ```

#### CI/CD for Messaging App

- **Jenkins Pipeline (CI + Docker image build)**:
  - Jenkins is expected to run in Docker, for example:
    ```bash
    docker run -d --name jenkins \
      -p 8080:8080 -p 50000:50000 \
      -v jenkins_home:/var/jenkins_home \
      jenkins/jenkins:lts
    ```
  - The pipeline definition lives in `messaging_app/Jenkinsfile` and:
    - Checks out this repository from GitHub: [Adika-Junior/alx-backend-python](https://github.com/Adika-Junior/alx-backend-python).
    - Sets up a Python virtual environment in `messaging_app/`.
    - Installs dependencies plus `pytest` and `pytest-django`.
    - Runs tests with `pytest` and publishes a JUnit XML test report in Jenkins.
    - Builds a Docker image from `messaging_app/Dockerfile`.
    - Pushes the Docker image to Docker Hub using Jenkins credentials.
  - Jenkins requirements:
    - Git, Pipeline, and ShiningPanda plugins.
    - Credentials:
      - GitHub credentials (ID: `github-credentials-id`) to access the repo.
      - Docker Hub credentials (ID: `dockerhub-credentials-id`) to push images.
    - The `DOCKER_IMAGE` environment in the `Jenkinsfile` should be set to your Docker Hub repository name (e.g. `your-dockerhub-username/messaging_app`).

- **GitHub Actions – Testing, Linting, Coverage**:
  - Workflow file: `messaging_app/.github/workflows/ci.yml`.
  - Triggers:
    - On `push` and `pull_request` affecting `messaging_app/**`.
  - Job behavior:
    - Spins up a MySQL 8.0 service configured to match the Django MySQL settings.
    - Uses `actions/setup-python` (Python 3.10).
    - Installs project dependencies plus `pytest`, `pytest-django`, `flake8`, and `coverage`.
    - Runs migrations with `python manage.py migrate`.
    - Executes tests with coverage using `coverage run -m pytest`.
    - Generates `coverage.xml` and uploads it as a build artifact.
    - Runs `flake8 .` to enforce PEP 8; any linting errors fail the build.

- **GitHub Actions – Docker Image Build & Push**:
  - Workflow file: `messaging_app/.github/workflows/dep.yml`.
  - Trigger:
    - On `push` to `main` that touches `messaging_app/**`.
  - Job behavior:
    - Uses `docker/setup-qemu-action` and `docker/setup-buildx-action` to enable multi‑platform builds.
    - Logs in to Docker Hub using repository secrets:
      - `DOCKERHUB_USERNAME`
      - `DOCKERHUB_TOKEN`
    - Uses `docker/build-push-action` to build and push:
      - `${DOCKERHUB_USERNAME}/messaging_app:latest`
      - `${DOCKERHUB_USERNAME}/messaging_app:${{ github.sha }}`

This CI/CD setup ensures the messaging app has:
- **Development**: Local `venv` or `docker-compose` with MySQL, debug‑friendly configuration.
- **Production**: Docker image build and push via Jenkins and GitHub Actions, with environment‑driven settings for security and scalability.

#### Messaging App – Folder Structure Overview

Key folders and files for the messaging app:

- **`messaging_app/`** (project root)
  - **`manage.py`**: Django management entry point (runserver, migrate, etc.).
  - **`requirements.txt`**: Single source of dependencies for runtime, tests, linting, and coverage.
  - **`docker-compose.yml`**: Local development stack with a Django web service and MySQL database.
  - **`Dockerfile`**: Builds the Django app container image (used locally, by Jenkins, and by GitHub Actions).
  - **`KUBERNETES_SETUP.md`**: Step‑by‑step guide for deploying to Kubernetes (Minikube) and doing scaling/rollout exercises.
  - **`mysql-config.yaml`**: Kubernetes ConfigMap/Secret definitions for database configuration.
  - **`deployment.yaml`**, `blue_deployment.yaml`, `green_deployment.yaml`: Kubernetes deployment specs for base, blue, and green versions of the app.
  - **`kubeservice.yaml`**: Kubernetes Service definition for exposing the app internally.
  - **`ingress.yaml`**: Kubernetes Ingress configuration to expose the API via HTTP.
  - **`kubctl-0x01`, `kubctl-0x02`, `kubctl-0x03`, `kurbeScript`**: Helper scripts for scaling, blue‑green deployments, and rolling updates in Kubernetes.
  - **`.github/workflows/ci.yml`**: GitHub Actions workflow for tests, lint, and coverage.
  - **`.github/workflows/dep.yml`**: GitHub Actions workflow for Docker image build and push.
  - **`Jenkinsfile`**: Jenkins Pipeline definition (also mirrored under `messaging_app/messaging_app/Jenkinsfile` to satisfy checker requirements).
- **`messaging_app/messaging_app/`** (Django project package)
  - **`__init__.py`**: Marks the package.
  - **`settings.py`**: Django settings, made environment‑driven for dev/prod.
  - **`urls.py`**: Root URL configuration for API endpoints.
  - **`wsgi.py` / `asgi.py`**: WSGI/ASGI entry points for production servers.
  - **`Jenkinsfile`**: Pipeline file duplicated here for automated checks; functionally similar to the root `messaging_app/Jenkinsfile`.
  - **`.github/workflows/`**: Optional project‑scoped workflows (`ci.yml`, `dep.yml`) used by some automated checkers.
- **`messaging_app/chats/`** (Django app for messaging domain)
  - Models for users, conversations, messages.
  - Serializers for converting models to/from JSON.
  - Viewsets and routers for REST API endpoints.

This structure separates **infrastructure concerns** (Docker, Kubernetes, CI/CD) at the project root from **application logic** under the Django project and `chats` app, while keeping all automation (Jenkins and GitHub Actions) close to the `messaging_app` codebase.

## Learning Path

The projects are designed to be completed in sequence, building upon previous concepts:

1. **Fundamentals** (Generators, Decorators, Context Managers)
   - Master Python core concepts
   - Understand memory efficiency
   - Learn async programming

2. **Testing** (Unit & Integration Tests)
   - Write comprehensive tests
   - Understand test-driven development
   - Learn mocking and fixtures

3. **Django Basics** (Middleware)
   - Understand Django request/response cycle
   - Implement custom middleware
   - Handle authentication and authorization

4. **Django Advanced** (Signals, ORM, Caching)
   - Event-driven programming with signals
   - Optimize database queries
   - Implement caching strategies
   - Build scalable applications

## Common Patterns & Best Practices

### Code Organization
- Modular app structure
- Separation of concerns
- DRY (Don't Repeat Yourself) principle
- Clear naming conventions

### Database Optimization
- Use `select_related()` for foreign keys
- Use `prefetch_related()` for reverse relations
- Implement custom managers for common queries
- Avoid N+1 query problems

### Performance
- Implement caching where appropriate
- Optimize database queries
- Use generators for large datasets
- Profile and measure performance

### Testing
- Write tests for all features
- Maintain high test coverage
- Use fixtures for test data
- Test edge cases and error handling

### Security
- Use JWT for authentication
- Implement proper permissions
- Validate all user input
- Follow Django security best practices

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (venv)
- Git

### Setup

1. **Clone the repository**:
```bash
git clone https://github.com/Adika-Junior/alx-backend-python.git
cd alx-backend-python
```

2. **Create a virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies** (project-specific):
```bash
cd <project-directory>
pip install -r requirements.txt
```

4. **Run migrations** (for Django projects):
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Start the development server** (for Django projects):
```bash
python manage.py runserver
```

## Project-Specific Documentation

Each project directory contains its own README with:
- Detailed project overview
- Installation instructions
- Usage examples
- API documentation (where applicable)
- Testing guidelines

## Contributing

This is a learning repository. Contributions should:
- Follow Python PEP 8 style guidelines
- Include comprehensive tests
- Update relevant documentation
- Maintain code quality standards

## License

This repository is part of the ALX Backend Python curriculum.

## Author

ALX Backend Python Program

## Resources

### Django Documentation
- [Django Official Docs](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Signals](https://docs.djangoproject.com/en/stable/topics/signals/)

### Python Documentation
- [Python Official Docs](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://pep8.org/)

### Learning Resources
- Django for Beginners
- Two Scoops of Django
- Python Tricks

## Notes

- Each project is self-contained and can be run independently
- Virtual environments are recommended for each project
- Database files (db.sqlite3) are typically gitignored
- Always review project-specific README files for detailed instructions

