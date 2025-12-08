# Contributing to NYC Air Quality Analysis

Thank you for your interest in contributing to this project! This document provides guidelines for contributions.

## 🎯 Project Goals

This project analyzes the relationship between air pollution and respiratory health outcomes in New York City, demonstrating best practices in:
- Data curation and quality assessment
- Reproducible research workflows
- Open science principles
- Software engineering practices

## 🛠️ Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR-USERNAME/IS-477-Project.git
   cd IS-477-Project
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest  # For testing
   ```

4. **Download Data**
   ```bash
   python scripts/download_data.py
   ```

## 📋 Contribution Types

### Data Quality Improvements
- Identify and fix data inconsistencies
- Improve data cleaning logic
- Add data validation checks
- Document data quality issues

### Analysis Enhancements
- Propose new statistical analyses
- Improve visualization clarity
- Add interactive elements
- Optimize performance

### Documentation
- Fix typos and improve clarity
- Add code comments
- Create tutorials or guides
- Translate documentation

### Testing
- Add unit tests
- Improve test coverage
- Document edge cases
- Add integration tests

## 🔍 Code Standards

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### Example
```python
def calculate_borough_mean(df, pollutant, borough):
    """
    Calculate mean pollutant concentration for a specific borough.
    
    Args:
        df: pandas DataFrame with air quality data
        pollutant: str, pollutant name (e.g., 'NO2', 'O3')
        borough: str, NYC borough name
        
    Returns:
        float: Mean concentration value
    """
    subset = df[(df['pollutant'] == pollutant) & 
                (df['borough'] == borough)]
    return subset['concentration'].mean()
```

### Testing
All new features should include tests:

```python
def test_calculate_borough_mean():
    # Create test data
    test_df = pd.DataFrame({
        'pollutant': ['NO2', 'NO2', 'O3'],
        'borough': ['Manhattan', 'Manhattan', 'Brooklyn'],
        'concentration': [20, 30, 40]
    })
    
    # Test calculation
    result = calculate_borough_mean(test_df, 'NO2', 'Manhattan')
    assert result == 25.0
```

Run tests before submitting:
```bash
pytest tests/ -v
```

## 📝 Commit Messages

Use clear, descriptive commit messages:

**Good:**
```
Add missing value imputation for PM2.5 data
Fix borough name standardization bug
Update correlation visualization colors
```

**Avoid:**
```
fix bug
update
changes
```

## 🔄 Pull Request Process

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write clear, documented code
   - Add tests for new features
   - Update documentation

3. **Test Your Changes**
   ```bash
   python scripts/run_all.py  # Full pipeline test
   pytest tests/ -v           # Unit tests
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "Clear description of changes"
   git push origin feature/your-feature-name
   ```

5. **Open Pull Request**
   - Describe what you changed and why
   - Reference any related issues
   - Include screenshots for visual changes

## 🐛 Reporting Issues

When reporting bugs, please include:
- **Description**: What happened vs. what you expected
- **Steps to Reproduce**: Detailed steps to recreate the issue
- **Environment**: Python version, OS, package versions
- **Data**: Sample data if applicable (ensure no sensitive info)
- **Error Messages**: Full error traceback

### Issue Template
```markdown
## Description
Brief description of the issue

## Steps to Reproduce
1. Run command X
2. Observe error Y

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version: 3.12
- OS: Windows 10
- Package versions: (paste requirements_frozen.txt)

## Additional Context
Any other relevant information
```

## 🌟 Feature Requests

We welcome feature ideas! Please include:
- **Use Case**: Why this feature would be valuable
- **Proposed Solution**: How you envision it working
- **Alternatives**: Other approaches you considered

## 📚 Documentation Standards

### README Structure
- Clear project description
- Installation instructions
- Usage examples
- Citation information

### Code Comments
```python
# Good: Explains WHY, not just WHAT
# Use FIPS code ranges to map block groups to boroughs
# because spatial join is too slow for 6,378 records
borough_map = {
    (36005, 36006): 'Bronx',
    ...
}

# Avoid: States the obvious
# Loop through data
for row in data:
    ...
```

### Docstrings
Use NumPy-style docstrings:

```python
def aggregate_health_impacts(df, by='borough'):
    """
    Aggregate health impact estimates by geographic unit.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing health impact estimates
    by : str, default='borough'
        Geographic aggregation level
        
    Returns
    -------
    pandas.DataFrame
        Aggregated health impacts with columns:
        - geographic_unit: Aggregation level name
        - total_symptoms: Sum of respiratory symptoms
        
    Examples
    --------
    >>> impacts = aggregate_health_impacts(benmap_df, by='borough')
    >>> impacts.head()
    """
    pass
```

## 🎓 Learning Resources

### Data Curation
- [FAIR Data Principles](https://www.go-fair.org/fair-principles/)
- [Data Carpentry](https://datacarpentry.org/)

### Python Best Practices
- [PEP 8 Style Guide](https://pep8.org/)
- [Real Python Tutorials](https://realpython.com/)

### Reproducible Research
- [The Turing Way](https://the-turing-way.netlify.app/)
- [Software Carpentry](https://software-carpentry.org/)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License (for code) and CC0 1.0 Universal (for data).

## 🙏 Acknowledgments

Thank you to all contributors who help improve this project! Special thanks to:
- IS 477 course staff for guidance
- NYC DOHMH for open data access
- USDA Forest Service for BenMAP data

## 📧 Contact

Questions? Reach out via:
- GitHub Issues (preferred)
- Email: [Kenneth Shelton, Tianqi Fu]

---

**Remember**: Good contributions don't have to be big! Even fixing typos or improving documentation helps make this project better for everyone. 🚀
