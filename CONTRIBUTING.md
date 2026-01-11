# Contributing to Music Generator Company

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\Activate.ps1  # Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Install Ollama and pull llama2

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

## Testing

Run tests before submitting:
```bash
python main.py  # Test CLI
python test_api.py  # Test web API
```

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Update documentation if needed
5. Submit PR with clear description

## Reporting Issues

Include:
- Python version
- Operating system
- Error messages
- Steps to reproduce

## Questions?

Open an issue for discussion.
