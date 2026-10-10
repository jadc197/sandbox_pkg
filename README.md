# ⚠️ PROJECT STATUS NOTICE
This package is now architecturally mature, complete, and stable. 
To ensure future-proof automated testing and open-source maintenance, the active home of this project has moved to GitHub.

*   **New Home / Issues / PRs:** [https://github.com/jadc197/sandbox-pkg](https://github.com/jadc197/sandbox-pkg)
*   **PyPI Releases:** Verified and deployed natively via GitHub Actions.

*Please do not open issues or submit code updates on this Gitea instance.*

# Blueprint: Migrating a Mature Python Package from Gitea to GitHub for Automated Active Stewardship

This guide provides a comprehensive, beginner-friendly walkthrough to safely migrate a Python package from a private, self-hosted Gitea instance over to a public or private GitHub repository. 

Our strategy changes the project's posture from **active internal development** to a low-touch **"set-and-forget" active stewardship model**. By moving to GitHub, you gain access to zero-maintenance automation tools that track security vulnerabilities, run scheduled compatibility tests against new Python releases, and handle secure publishing without you having to touch your local development environment or manage static API tokens.

To practice this risk-free, we will use a **sandbox / mockup name** throughout this guide (`sandbox-pkg`).

---

## Phase 1: Understanding Active Stewardship vs. Abandonment

Before touching any code, it is important to understand why this move matters for a "finished" project:

*   **The Software Illusion:** A Python package is rarely an isolated island. Even if your core logic has zero bugs, the Python environment around it changes. New Python versions (e.g., 3.13, 3.14) come out yearly, and dependencies update. 
*   **Active Stewardship:** This means setting up automated systems that verify your project remains fully functional against changing ecosystems, alerts you to security flaws (CVEs), and provides a transparent communication signal to your users that the code is deliberately finalized, not neglected.
*   **The Advantage of GitHub:** By shifting your stable projects to GitHub, you leverage free cloud-hosted computing (GitHub Actions) and automated security alerts (Dependabot), eliminating the need to maintain your own local Gitea build runners for low-frequency testing.

---

## Phase 2: Preparing Your Workspace & Git Client Layout

To ensure you do not mix up your self-hosted Gitea setup and your new public GitHub space inside your Git GUI client (such as SourceTree or Git Cola), we will use explicit naming patterns.

### 1. Rename Your Git Remotes
By default, cloning a repository names the server endpoint `origin`. Having two endpoints named `origin` creates confusion. We will rename them to match their actual service names.

Open your command line inside your local project repository directory and execute:
```bash
# Rename the existing Gitea connection from 'origin' to 'gitea'
git remote rename origin gitea
```

### 2. Configure Your Git GUI Client for Visual Clarity
*   **In SourceTree:** Go to the Repository settings or sidebar. You will see your remote branches grouped beautifully under a `gitea/` dropdown rather than an ambiguous `origin/`. You can create bookmark folders named `[Internal Gitea - ARCHIVED]` and `[Public GitHub - ACTIVE]` to group your projects visually.
*   **In Git Cola:** The push/pull dialog interface will now clearly ask you to target the `gitea` remote or the `github` remote explicitly.

---

## Phase 3: The Order of Operations for Closing Down Gitea

To ensure internal developers have an unbroken trail to follow, you must write your migration notices **before** locking your Gitea repository.

### Step 1: Update Your Documentation Locally
Open your local project files on your workstation. Add a prominent notice right at the top of your `README.md` file:

```markdown
# ⚠️ PROJECT STATUS NOTICE
This package is now architecturally mature, complete, and stable. 
To ensure future-proof automated testing and open-source maintenance, the active home of this project has moved to GitHub.

*   **New Home / Issues / PRs:** [https://github.com/YOUR_ORGANIZATION/sandbox-pkg](https://github.com/YOUR_ORGANIZATION/sandbox-pkg)
*   **PyPI Releases:** Verified and deployed natively via GitHub Actions.

*Please do not open issues or submit code updates on this Gitea instance.*
```

### Step 2: Push the Final Documentation State to Gitea
With the Gitea instance still unlocked, push this final edit to your repository:
```bash
git push gitea main
```

### Step 3: Archive Your Gitea Repository
1. Open your web browser and navigate to your project repository page on your **Gitea** web instance.
2. Click on **Settings** located in the top-right options bar of the repository layout.
3. Scroll all the way down to the bottom section labeled **Danger Zone**.
4. Click the button labeled **Archive this repository**.

> **What this does:** Gitea appends a highly visible `[Archived]` tag next to the project header. It converts the entire repository to a strict read-only mode. All write configurations are permanently blocked, issue creation is frozen, and any developer trying to force a push via terminal will receive a server error rejection: `Git: Repository is archived and read-only.`

---

## Phase 4: Migrating Your History to GitHub

Now that Gitea is locked, your project history will be moved over to GitHub to host its active maintenance cycle.

### Step 1: Create a Fresh Repository on GitHub
1. Log in to [GitHub](https://github.com/).
2. Click **New Repository**.
3. Name your repository exactly matching your sandbox name (`sandbox-pkg`).
4. **Important:** Do *not* check any boxes for initializing the repository with a README, `.gitignore`, or a License. Keep the repository completely blank.

### Step 2: Push Your Local Repository to GitHub
On your workstation terminal, register the second remote destination as `github` and push all your commit history and historical release tags:

```bash
# Register the empty GitHub repository as your secondary remote alias
git remote add github git@github.com:YOUR_ORGANIZATION/sandbox-pkg.git

# Push all historical branches to GitHub
git push github --all

# Push all release tags to GitHub
git push github --tags
```

### Step 3: Shift Your Local Workspace Target
Tell your local workstation that all future work (such as occasional patches or structural configuration bumps) should track against GitHub by default instead of the old archived Gitea server:
```bash
git branch --set-upstream-to=github/main main
```

---

## Phase 5: Setting Up the Mock Sandbox Environment

To practice your deployment pipelines safely without affecting your production workflows or locking real names on the public index, we will use **TestPyPI**.

### Step 1: Initialize Your Structural Configuration Files
Your sandbox package needs a clean Python configuration structure to bundle itself correctly. Ensure your local files contain the following blueprint structure:

#### `pyproject.toml`
This file configures the build system and defines your package's metadata using modern standard layouts instead of legacy `setup.py` scripts.

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "yourname-sandbox-pkg"  # Give it a unique prefix to prevent collisions on TestPyPI
version = "1.0.0"
description = "A mature sandbox package migrating from Gitea to GitHub"
readme = "README.md"
requires-python = ">=3.8"
license = { text = "MIT" }
classifiers = [
    "Development Status :: 5 - Production/Stable", # Signal that this package is complete
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
dependencies = [] # Add upstream packages here if necessary
```

#### `src/sandbox_pkg/__init__.py`
A bare minimum source file to show that your package contains operational code.
```python
def hello_sandbox():
    return "This package is safely running under GitHub Active Stewardship!"
```

---

## Phase 6: Configuring Secure Trusted Publishing

Instead of generating a text-based password API key and pasting it manually into GitHub Secrets, we will use **PyPI Trusted Publishing (OIDC)**. This creates a secure connection between your GitHub Action environment and your PyPI namespace, generating short-lived temporary tokens for each upload.

### Step 1: Register on TestPyPI
1. Open your browser and navigate to the [TestPyPI Registration Page](https://test.pypi.org/).
2. Create an account and verify your email address.

### Step 2: Register GitHub as a Trusted Publisher
1. Log into your TestPyPI account dashboard.
2. Go to your **Account Settings** -> **Publishing** -> Click **Add Publisher**.
3. Select **GitHub** out of the available providers.
4. Fill in the following specific parameters:
    *   **Owner:** Your exact GitHub username or organization name.
    *   **Repository:** `sandbox-pkg` (Your exact GitHub repository name).
    *   **Workflow name:** `publish.yml` (The exact name of the file we will make in the next phase).
    *   **Environment name:** `test-release` (A protected barrier configuration on GitHub).
5. Click **Add Publisher** to save the binding configuration.

---

## Phase 7: Setting Up Automated CI/CD Actions

With the authentication hooks established on TestPyPI, we will add the automated automation code blocks into our GitHub repository workspace.

Create a nested folder layout in your local project root directory matching: `.github/workflows/`. Inside that folder, create a configuration file named `publish.yml`.

### The `publish.yml` Automation Script
This workflow code will run on a standard cloud environment every single time you publish a new "Release" tag on GitHub, or on a scheduled time sequence to test system durability.

```yaml
name: Automated Active Stewardship Pipeline

on:
  release:
    types: [published]
  schedule:
    # This CRON setting runs automatically every Sunday at midnight.
    # It ensures that even if you don't push code for a year, your test suite
    # checks your code against the changing ecosystem.
    - cron: '0 0 * * 0'

jobs:
  test:
    name: Run Python Compatibility Test Suite
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12', '3.13']

    steps:
    - name: Checkout Code Repository
      uses: actions/checkout@v4

    - name: Set Up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        # If your project has automated tests, install testing dependencies here
        # e.g., pip install pytest

    - name: Run Tests
      run: |
        # Simulate your test runner execution command here
        python -c "import sys; print('Testing compatibility on Python', sys.version)"

  publish:
    name: Build and Securely Publish Distro to TestPyPI
    needs: test
    if: github.event_name == 'release' # Only upload to TestPyPI if this is an explicit release tag event
    runs-on: ubuntu-latest
    environment:
      name: test-release
      url: https://test.pypi.org/p/yourname-sandbox-pkg

    permissions:
      id-token: write  # MANDATORY configuration setting for secure OIDC token handshakes

    steps:
    - name: Checkout Code Repository
      uses: actions/checkout@v4

    - name: Set Up Python 3.12
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Install Build Packaging Tools
      run: python -m pip install build --user

    - name: Compile Distribution Tarball and Wheel Binaries
      run: python -m build

    - name: Publish Package Artifacts to TestPyPI
      uses: pypa/gh-action-pypa-publish@release/v1
      with:
        repository-url: https://test.pypi.org/legacy/ # Forces the upload to use the Sandbox environment instead of Production PyPI
```

Commit these additions and push them to GitHub:
```bash
git add .
git commit -m "ci: add pyproject config and automated active stewardship workflow"
git push github main
```

---

## Phase 8: Running and Verifying Your First Sandbox Run

### Step 1: Create a Mock Target Release on GitHub
1. Open your repository workspace view on the **GitHub** website interface.
2. In the right column panel, find and click the **Releases** link -> **Draft a new release**.
3. Choose a tag version name (e.g., `v1.0.0`).
4. Type a title descriptive of the release (e.g., `Initial Mature Release Migration`).
5. Click the green button labeled **Publish release**.

### Step 2: Track Execution Flow
1. Click the **Actions** tab located at the top center options bar of your GitHub interface layout.
2. You will see your pipeline spinning up. Click into the workflow runner view.
3. Observe the automated matrix checking compatibility across all Python targets (3.10 through 3.13).
4. Watch the `publish` stage request the secure token configuration directly from TestPyPI and upload the bundle safely.

### Step 3: Test Installation Locally
Open your command terminal window anywhere outside of your active working repository directory path and test downloading your newborn sandbox package build instantly over the network:

```bash
pip install --index-url https://test.pypi.org/simple/ yourname-sandbox-pkg
```

---

## Phase 9: Long-Term Low-Touch Operations

Now that your migration is complete, maintenance becomes effortless:

1. **Dependabot Vulnerability Alerts:** In your GitHub repository settings, turn on **Dependabot security updates**. If any upstream dependency gets a security patch, Dependabot will automatically write a pull request updating your project metadata.
2. **Read the Docs Automation:** Log into [Read the Docs](https://readthedocs.org/) using your GitHub credentials, import your GitHub repository, and let its native webhooks build and refresh your API documents automatically every single time a release tag is registered on GitHub.
3. **Weekly Health Checkups:** The `schedule` cron configuration block in your workflow will execute tests silently in the cloud every week. If a future update changes core Python definitions and breaks your mature package syntax, GitHub will send you an analytical email alert instantly. If everything remains stable, your project operates on safe, zero-maintenance cruise control indefinitely.
