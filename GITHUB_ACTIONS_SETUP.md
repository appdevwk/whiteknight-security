# WhiteKnight GitHub Actions Setup Instructions

## 📁 File Placement for GitHub Actions

The CI/CD workflow file needs to be placed in the correct location in your repository:

### Step 1: Create GitHub Workflows Directory

```bash
cd ~/whiteknightai-fortress

# Create the workflows directory if it doesn't exist
mkdir -p .github/workflows

# The directory structure should be:
# .github/
# └── workflows/
#     └── main.yml
```

### Step 2: Copy the CI/CD Workflow File

The file `cicd-workflow.yml` that was created needs to be renamed and placed:

```bash
# Copy the workflow file to the correct location
cp cicd-workflow.yml .github/workflows/main.yml

# Verify it was created correctly
ls -la .github/workflows/main.yml
```

### Step 3: Commit and Push

```bash
# Stage all changes
git add .github/workflows/main.yml
git add -A  # Add all other generated files

# Create comprehensive commit
git commit -m "Initial commit: WhiteKnight Security v1.0.0 complete setup

- Comprehensive GitHub Actions CI/CD pipeline
- Security scanning and code quality checks
- Automated testing with pytest and coverage
- Debian package building
- Docker container support
- Complete documentation suite
- Pre-commit hooks for code quality
- Systemd service with hardening

This includes all GitHub Copilot recommendations:
✓ Code quality (linting, type hints, formatting)
✓ Security (secret scanning, dependency updates)
✓ Testing (unit tests, integration tests)
✓ Documentation (API docs, deployment guides)
✓ CI/CD pipeline (GitHub Actions automation)
✓ Contribution guidelines and code of conduct
✓ Security policy and responsible disclosure

Ready for production deployment."

# Push to GitHub
git push -f origin main
```

### Step 4: Monitor the Workflow

Once pushed, you can monitor the CI/CD pipeline:

1. **Go to GitHub**: https://github.com/appdevwk/whiteknight-security/actions

2. **Watch the workflow execute**:
   - First run will trigger on your push to `main`
   - All jobs will run in parallel (security, linting, testing)
   - Job results will appear as they complete

3. **Check for any failures**:
   - If security scan finds secrets: Remove them and retry
   - If tests fail: Fix code and push again
   - If package build fails: Check the logs for specific error

════════════════════════════════════════════════════════════════════════════════

## 🔍 Workflow Jobs Breakdown

The `.github/workflows/main.yml` includes these jobs:

### 1. **security-scan** (runs first)
   - Trivy vulnerability scanner
   - Gitleaks secret detection
   - SARIF report upload

### 2. **lint-python** (runs in parallel)
   - Tests Python 3.8, 3.9, 3.10, 3.11
   - Black code formatting
   - isort import sorting
   - Flake8 style checking
   - Pylint analysis
   - MyPy type checking

### 3. **lint-javascript** (runs in parallel)
   - ESLint JavaScript validation
   - Prettier format checking

### 4. **unit-tests** (runs after linting)
   - Tests on multiple Python versions
   - pytest with coverage reporting
   - Codecov upload

### 5. **integration-tests** (runs after unit tests)
   - Full integration test suite
   - Database tests
   - API endpoint tests

### 6. **dependency-check** (runs in parallel)
   - Safety vulnerability check
   - pip-audit package audit
   - Bandit security check
   - npm audit for JavaScript

### 7. **build-deb** (runs after tests pass)
   - Builds Debian package
   - Uploads to artifacts

### 8. **build-docker** (runs after tests pass)
   - Builds Docker image
   - Multi-stage build

### 9. **documentation** (runs in parallel)
   - Generates Sphinx documentation
   - Uploads documentation artifact

### 10. **release** (runs only on main branch push, if all jobs pass)
   - Creates GitHub release
   - Attaches Debian package
   - Uses CHANGELOG.md for release notes

════════════════════════════════════════════════════════════════════════════════

## ⚙️ GitHub Repository Settings

After first successful workflow run, configure these settings:

### 1. Enable Branch Protection

Settings → Branches → Add Rule for `main`

```
Branch name pattern: main

□ Require a pull request before merging
  ├─ Require reviews: 1
  └─ Dismiss stale reviews

□ Require status checks to pass before merging
  ├─ Security scanning (required)
  ├─ lint-python-3.10 (required)
  ├─ unit-tests-3.10 (required)
  ├─ integration-tests (required)
  ├─ dependency-check (required)
  └─ build-deb (required)

□ Require branches to be up to date before merging
□ Require code owners approval
□ Restrict who can push to matching branches
```

### 2. Enable Secret Scanning

Settings → Code security and analysis → Secret scanning

```
☑ Secret scanning
☑ Push protection
```

### 3. Configure Secrets for CI/CD

Settings → Secrets and variables → Actions

Add any secrets needed for your CI/CD:

```
CODECOV_TOKEN          - For coverage reporting
DOCKER_USERNAME        - If pushing Docker images
DOCKER_TOKEN           - If pushing Docker images
GITHUB_TOKEN           - Pre-configured by GitHub
```

### 4. Enable Dependabot

Settings → Code security and analysis → Dependabot

```
☑ Enable Dependabot version updates
  └─ Check daily for updates
  
☑ Enable Dependabot security updates
```

════════════════════════════════════════════════════════════════════════════════

## 🚀 Triggering Workflows

The workflow runs automatically on:

1. **Push to main**: Full workflow runs
2. **Push to develop**: Full workflow runs  
3. **Pull requests**: Full workflow runs
4. **Daily schedule**: 2 AM UTC - Security scanning only

### Manual Trigger

You can also manually trigger the workflow:

1. Go to: https://github.com/appdevwk/whiteknight-security/actions/workflows/main.yml
2. Click "Run workflow"
3. Select branch and click green button

════════════════════════════════════════════════════════════════════════════════

## 📊 Viewing Workflow Results

### Success Indicators ✓

- All jobs show green checkmark
- No failed tests
- No security vulnerabilities found
- Build artifacts available for download

### Common Issues & Fixes

#### Issue: Push protection blocks push
```bash
# Solution: Remove secrets and use git-filter-repo
git filter-repo --replace-text replacements.txt
git push -f origin main
```

#### Issue: Tests failing
```bash
# Solution: Run tests locally first
pytest tests/ -v --cov
# Fix issues, then push again
```

#### Issue: Linting failures
```bash
# Solution: Auto-format code
black api_server.py main.py
isort api_server.py main.py
# Then push again
```

#### Issue: Build fails
```bash
# Check build logs in Actions tab
# Most common: missing dependencies in requirements.txt
# Add to requirements.txt and push again
```

════════════════════════════════════════════════════════════════════════════════

## 📈 Performance Optimization

To speed up workflows:

1. **Use caching**:
   ```yaml
   - uses: actions/setup-python@v4
     with:
       cache: 'pip'  # Caches pip dependencies
   ```

2. **Parallel execution**:
   - Workflow already optimized with parallel jobs
   - Dependencies ensure correct execution order

3. **Skip workflows**:
   Include `[skip ci]` in commit message:
   ```bash
   git commit -m "Update README [skip ci]"
   ```

════════════════════════════════════════════════════════════════════════════════

## 🔐 Workflow Security

The workflow includes multiple security layers:

- **Secret scanning**: Prevents credential leaks
- **Dependency checks**: Finds vulnerable packages
- **Code analysis**: Identifies security issues
- **Access control**: Only runs from main/develop branches
- **Artifact retention**: Limited to 90 days

════════════════════════════════════════════════════════════════════════════════

## 📝 Workflow Modification

To modify the workflow:

1. Edit `.github/workflows/main.yml`
2. Add/remove jobs as needed
3. Commit and push changes
4. GitHub will use the updated workflow automatically

Common modifications:

- Add additional Python versions to test
- Add notification integrations (Slack, email)
- Add deployment steps to production
- Add performance benchmarking

════════════════════════════════════════════════════════════════════════════════

## ✅ Verification Checklist

After setting up GitHub Actions:

- [ ] Workflow file placed in `.github/workflows/main.yml`
- [ ] First workflow run completed successfully
- [ ] All jobs passed (except release, which only runs on tag)
- [ ] Build artifacts available in workflow artifacts
- [ ] Branch protection configured for `main`
- [ ] Secret scanning enabled
- [ ] Push protection working (tests commit with dummy secret)
- [ ] GitHub release automatically created (on manual tag push)
- [ ] Emails configured for notifications (optional)

════════════════════════════════════════════════════════════════════════════════

## 🎯 Next Steps

1. Copy workflow file to `.github/workflows/main.yml`
2. Commit and push to GitHub
3. Monitor first workflow run at: https://github.com/appdevwk/whiteknight-security/actions
4. Configure branch protection rules
5. Enable secret scanning
6. Add required secrets if needed
7. Test with sample pull request

════════════════════════════════════════════════════════════════════════════════

For detailed workflow documentation, see:
- GitHub Actions Documentation: https://docs.github.com/actions
- WhiteKnight CI/CD Workflow: `.github/workflows/main.yml`
- Setup Guide: `SETUP_COMPLETE.md`
- Contributing Guide: `CONTRIBUTING.md`
