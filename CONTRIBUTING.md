# Contributing to Mobile Cloud System

First off, thank you for considering contributing to this project! Whether you're fixing a typo, improving documentation, or adding new features, every contribution makes this project better.

This guide will help you get started and ensure a smooth collaboration experience.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Code Guidelines](#code-guidelines)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Process](#pull-request-process)
- [Need Help?](#need-help)

---

## Getting Started

Before diving in, here's what you should know:

- This project contains **4 labs** demonstrating cloud computing concepts and a **React dashboard** for observability
- We use **GitHub Actions** for CI/CD, so please ensure your changes don't break the pipeline
- All contributions should follow the existing code style and structure

---

## Project Structure

Understanding the codebase will help you navigate and contribute effectively:

```
Mobile-Cloud-System/
│
├── Lab1/                    # Virtualization & Cloud Basics
├── Lab2/                    # Redis Distributed Systems
│   ├── app.py              # Flask API with Redis
│   ├── requirements.txt
│   └── tests/              # Unit tests
│
├── Lab3/                    # Containerization & Kubernetes
│   ├── app.py              # Mobile Cloud API
│   ├── Dockerfile.basic
│   ├── Dockerfile.multistage
│   ├── k8s/                # Kubernetes manifests
│   ├── requirements.txt
│   └── tests/              # Unit tests
│
├── Lab4/                    # Microservices Architecture
│   ├── docker-compose.yml
│   ├── order-service/
│   ├── product-service/
│   └── tests/              # Integration tests
│
├── frontend/                # React Observability Dashboard
│
└── .github/workflows/       # CI/CD Pipeline Configuration
```

---

## Development Setup

### Prerequisites

Make sure you have the following installed:

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.9+ | Backend services |
| Node.js | 18+ | Frontend dashboard |
| Docker | Latest | Containerization |
| Docker Compose | Latest | Multi-container orchestration |

### Backend Setup

```bash
# Navigate to a specific lab
cd Lab3

# Install Python dependencies
pip install -r requirements.txt

# Run the test suite
pytest tests/ -v --cov=.

# Start the service locally
python app.py
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

### Docker Development

```bash
# Build and run Lab3 container
docker build -f Lab3/Dockerfile.multistage -t lab3 .
docker run -p 5000:5000 lab3

# Run Lab4 microservices stack
cd Lab4
docker compose up --build
```

---

## How to Contribute

### Step 1: Fork the Repository

Click the "Fork" button at the top right of this repository to create your own copy.

### Step 2: Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/Mobile-Cloud-System.git
cd Mobile-Cloud-System
```

### Step 3: Create a Branch

Create a descriptive branch name that reflects your changes:

```bash
git checkout -b feat/add-new-feature
# or
git checkout -b fix/resolve-issue-123
# or
git checkout -b docs/update-readme
```

### Step 4: Make Your Changes

Write your code, add tests if applicable, and ensure everything works.

### Step 5: Commit Your Changes

Follow our [commit message convention](#commit-message-convention) for clear history.

### Step 6: Push and Create a Pull Request

```bash
git push origin your-branch-name
```

Then open a Pull Request from your fork to the main repository.

---

## Code Guidelines

To maintain consistency across the codebase, please follow these guidelines:

### General Principles

- Write clean, readable, and self-documenting code
- Follow the existing code structure and patterns
- Add comments only when the code isn't self-explanatory
- Keep functions small and focused on a single responsibility

### Python Code

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes

### React/JavaScript Code

- Use functional components with hooks
- Follow the existing component structure
- Keep components modular and reusable

### Testing

- Write tests for new features
- Ensure existing tests pass before submitting
- Aim for meaningful test coverage, not just high numbers

### Linting

Before submitting, run the linters:

```bash
# Python linting
flake8 Lab2 Lab3 Lab4
black --check Lab2 Lab3 Lab4

# Frontend linting
cd frontend && npm run lint
```

---

## Commit Message Convention

We follow **Conventional Commits** to maintain a clean and readable git history.

### Format

```
<type>: <short description>

[optional body]
[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes |
| `style` | Code style changes (formatting, no logic change) |
| `refactor` | Code refactoring (no feature or fix) |
| `test` | Adding or updating tests |
| `ci` | CI/CD configuration changes |
| `chore` | Maintenance tasks |

### Examples

```bash
feat: add real-time latency chart to dashboard
fix: resolve Redis connection timeout issue
docs: update API documentation for order service
refactor: simplify metrics calculation logic
ci: add Docker image security scanning
```

---

## Pull Request Process

### Before Submitting

- [ ] Your code follows the project's style guidelines
- [ ] You've tested your changes locally
- [ ] All existing tests pass
- [ ] You've added tests for new functionality (if applicable)
- [ ] Your commits follow the conventional commit format

### PR Guidelines

1. **Clear Title**: Use a descriptive title that summarizes the change
2. **Detailed Description**: Explain what changed and why
3. **Screenshots**: Include screenshots for any UI changes
4. **Small & Focused**: Keep PRs focused on a single concern
5. **Link Issues**: Reference any related issues (e.g., "Closes #42")

### Review Process

- A maintainer will review your PR as soon as possible
- Be open to feedback and willing to make adjustments
- Once approved, your PR will be merged

---

## API Standards

If you're working on backend services, follow these conventions:

### Health Endpoints

Every service should expose:

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Liveness probe |
| `GET /ready` | Readiness probe |
| `GET /metrics` | Prometheus metrics |

### Response Format

Use a consistent JSON structure:

```json
{
  "status": "success",
  "data": { },
  "message": "Operation completed successfully"
}
```

For errors:

```json
{
  "status": "error",
  "data": null,
  "message": "Human-readable error description"
}
```

---

## Need Help?

If you have questions or run into issues:

- **Check existing issues**: Someone might have had the same question
- **Open a new issue**: Describe your problem clearly with steps to reproduce
- **Reach out**: Feel free to contact the maintainer

We appreciate your interest in contributing and look forward to collaborating with you!

---

**Happy Contributing!**
