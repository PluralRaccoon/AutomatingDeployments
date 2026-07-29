# Automated CI/CD Workflow Overview

Hello you beautiful people! 

Welcome to the automated Continuous Integration and Continuous Delivery (CI/CD) pipeline for this project! The main goal of this workflow is to keep our code squeaky clean, automatically test it across different Python versions, and seamlessly publish new releases to the Python Package Index (PyPI).

This overview breaks down how the entire process works, step-by-step. You can reference the ProjectDiagram.jpg and ImplementationExplanation files in this repository for a visual and detailed companion to this guide! 

## The Trigger: Pushing Code

The magic starts the moment a developer commits new code and pushes it to our remote GitHub repository. This simple push acts as the trigger that wakes up our primary workflow, affectionately known as the Python CI Workflow (python-ci.yaml). 

## Continuous Integration (CI): Code Quality & Testing

Once awake, the Python CI Workflow gets straight to work. It spins up several tasks in parallel (meaning they run at the same time to save us waiting) to ensure our new code is robust and meets all our project standards. 

### Quality Checks

First up, the workflow runs a suite of automated checks using standard Python tools to keep our codebase healthy:

    Linting Checks: It uses Ruff (a super-fast Python tool that analyzes code) to spot syntax errors and stylistic issues before they become problems.

    Formatting Checks: It brings in Black (a strict code formatter) to automatically format the code so it looks consistent, no matter who wrote it.

    Typing Checks: It uses mypy (a tool that checks data types) to verify that our type hints are used correctly, which helps prevent unexpected errors when the code actually runs.

    Security Checks: Finally, it runs Bandit (a security scanner) to look for common vulnerabilities in the Python code.

### Automated Tests

While the quality checks are running, the workflow simultaneously kicks off our automated test suite using pytest (a popular framework for writing software tests). Crucially, it runs these tests across a *matrix* of multiple Python versions (currently 3.9, 3.10, 3.11, and 3.12). This ensures that our code library will work perfectly for anyone, no matter which of these Python environments they are using! 

## Automated Release Creation

If—and only if—our code passes all the quality checks and all the automated tests with flying colors, the workflow moves on to the exciting part: creating a release.

This stage leverages a tool called Python Semantic Release (**PSR**). **PSR** is incredibly smart; it automates the versioning process just by reading our Git commit messages!

    Semantic Versioning (SemVer): If the commit messages tell **PSR** that we added a new feature, fixed a bug, or made a breaking change, it will automatically bump our version number up for us (for example, moving from v1.2.0 to v1.3.0).

    GitHub Release: **PSR** will then generate a nice changelog of what's new and create an official Release right here on GitHub.

A quick note: If our commit messages don't actually require a new version (like if we just fixed a typo in the **README**), the workflow happily stops here. It has done its job of checking the code (Continuous Integration) without needing to trigger a new delivery! 
## Continuous Delivery (CD): Publishing the Package

The creation of a new GitHub Release serves as our second trigger. It wakes up a totally separate workflow: the Publish Workflow (publish.yaml).

We keep this workflow separate to ensure a clear division of responsibilities; we only ever try to publish a package to the public when a verified release is explicitly created. Downloading / Rebuilding Artifacts

First, this workflow gets the actual package files ready (these are the .whl or .tar.gz files people download). It does this either by downloading them straight from the newly created GitHub Release or by checking out the code and rebuilding them from scratch. Publishing to TestPyPI

Before we push anything to the real world, the workflow safely uploads our package to TestPyPI (which is a sandbox version of the Python Package Index just for testing).

    Secure Authentication: We use OpenID Connect (**OIDC**) to securely log in to TestPyPI. **OIDC** is a modern security standard that creates a temporary, short-lived *trust* connection between GitHub and PyPI. This is awesome because it means we don't have to store permanent, sensitive **API** passwords in our repository!

Publishing to PyPI (Production)

Once we successfully upload to TestPyPI and everything looks good, the final step is to publish our package to the official, public PyPI.

    Just like before, this step uses that secure **OIDC** authentication to upload the files. Once this finishes, our brand new version is instantly available for developers around the world to install using pip install!

If you have any feedback about this little project, please please please do not hesitate to send me a message. I am always up to improve and craft.

Made with ❤️ in Costa Rica