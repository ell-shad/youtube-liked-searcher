# Contributing to YouTube Liked Videos Searcher

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported in [Issues](https://github.com/your-username/youtube-liked-searcher/issues)
2. If not, create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Your operating system and Python version
   - Screenshots (if applicable)

### Suggesting Features
1. Check existing issues for similar feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use case / motivation
   - Possible implementation approach

### Code Contributions

#### Setup Development Environment
```bash
git clone https://github.com/your-username/youtube-liked-searcher.git
cd youtube-liked-searcher
pip install -r requirements.txt
```
#### Making Changes
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Create a Pull Request

#### Code Style
- Follow PEP 8 Python style guidelines
- Use descriptive variable names
- Add comments for complex logic
- Keep functions focused and small

#### Testing
- Test your changes with different scenarios
- Verify authentication still works
- Check that existing features aren't broken

### Pull Request Process
1. Ensure your code follows the style guidelines
2. Update documentation if needed
3. Add a clear description of changes
4. Reference any related issues

## Development Notes

### Project Structure
- `src/youtube_searcher.py` - Main application
- `docs/` - Documentation files
- `requirements.txt` - Dependencies

### Key Components
- **Authentication**: Google OAuth 2.0 flow
- **API Integration**: YouTube Data API v3
- **GUI**: tkinter-based interface
- **Data Management**: Local JSON caching

## Questions?

Feel free to ask questions by creating an issue with the "question" label.

Thank you for contributing! 🎉