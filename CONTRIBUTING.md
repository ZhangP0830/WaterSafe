# Contributing to WaterSafe 🤝

Thank you for your interest in contributing to WaterSafe! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## 📜 Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please be respectful, inclusive, and constructive in all interactions.

## 🚀 Getting Started

### Prerequisites
- **Node.js** 16+ (for frontend development)
- **Python** 3.8+ (for backend development)
- **MySQL** 8.0+ (for database)
- **Git** (for version control)

### Fork and Clone
1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/your-username/WaterSafe.git
cd WaterSafe
```

3. Add the upstream repository:
```bash
git remote add upstream https://github.com/original-owner/WaterSafe.git
```

## 🛠️ Development Setup

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start backend server
python main.py
```

## 📝 Contributing Guidelines

### Types of Contributions
We welcome various types of contributions:

- 🐛 **Bug fixes**
- ✨ **New features**
- 📚 **Documentation improvements**
- 🧪 **Tests**
- 🎨 **UI/UX improvements**
- 🔧 **Performance optimizations**
- 🌐 **Internationalization**

### Development Workflow

1. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

2. **Make your changes**
   - Write clean, readable code
   - Follow the coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
```bash
# Frontend tests
npm run test

# Backend tests
cd backend
python -m pytest
```

4. **Commit your changes**
```bash
git add .
git commit -m "feat: add new water quality prediction feature"
```

5. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

6. **Create a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Fill out the PR template
   - Submit the PR

## 🔄 Pull Request Process

### PR Template
When creating a pull request, please include:

- **Description**: Clear description of changes
- **Type**: Bug fix, feature, documentation, etc.
- **Testing**: How you tested the changes
- **Screenshots**: For UI changes
- **Breaking Changes**: If any
- **Related Issues**: Link to relevant issues

### PR Guidelines
- Keep PRs focused and atomic
- Ensure all tests pass
- Update documentation as needed
- Request reviews from maintainers
- Address feedback promptly

### Commit Message Format
We use conventional commits:
```
type(scope): description

feat(api): add water quality prediction endpoint
fix(ui): resolve map loading issue
docs(readme): update installation instructions
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

## 🐛 Issue Reporting

### Before Creating an Issue
1. Check existing issues
2. Search for similar problems
3. Ensure you're using the latest version

### Issue Template
When reporting issues, include:

- **Bug Description**: Clear description of the problem
- **Steps to Reproduce**: Detailed steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, browser, versions
- **Screenshots**: If applicable
- **Additional Context**: Any other relevant information

### Feature Requests
For feature requests, include:
- **Feature Description**: Clear description
- **Use Case**: Why this feature is needed
- **Proposed Solution**: How you envision it working
- **Alternatives**: Other solutions considered

## 📏 Coding Standards

### Frontend (Vue.js)
- Use Vue 3 Composition API
- Follow Vue.js style guide
- Use TypeScript when possible
- Implement proper error handling
- Use semantic HTML

### Backend (Python)
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions
- Use meaningful variable names
- Implement proper error handling

### General
- Write clean, readable code
- Use meaningful commit messages
- Add comments for complex logic
- Follow existing code patterns
- Keep functions small and focused

## 🧪 Testing

### Frontend Testing
```bash
# Unit tests
npm run test:unit

# E2E tests
npm run test:e2e

# Coverage report
npm run test:coverage
```

### Backend Testing
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=api --cov-report=html

# Run specific test file
python -m pytest test_guidance_cache.py
```

### Test Guidelines
- Write tests for new features
- Maintain test coverage above 80%
- Use descriptive test names
- Test edge cases and error conditions
- Mock external dependencies

## 📚 Documentation

### Code Documentation
- Add docstrings to functions and classes
- Use clear, concise comments
- Document complex algorithms
- Include examples in docstrings

### API Documentation
- Update API documentation for new endpoints
- Include request/response examples
- Document error codes and messages
- Keep documentation up to date

### README Updates
- Update README for new features
- Include installation instructions
- Add usage examples
- Keep links and badges current

## 🏷️ Release Process

### Version Numbering
We use semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers updated
- [ ] Release notes prepared

## 🤔 Questions?

If you have questions about contributing:

- **GitHub Discussions**: For general questions
- **GitHub Issues**: For bug reports and feature requests
- **Email**: For private discussions

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to WaterSafe! Your efforts help make water safety accessible to communities worldwide.

---

<div align="center">
  <strong>Together, we can make water safety accessible to everyone</strong>
  <br>
  <em>Thank you for your contribution! 🌊</em>
</div>
