# 📚 Project Index and Navigation Guide

Welcome to the **Heston Model BTC Options Pricing** project! This guide helps you navigate all project files and find what you need.

---

## 🚀 Quick Navigation

### New User? Start Here:
1. **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in 5 minutes
2. **Run**: `python demo.py` (recommended first)
3. **Check outputs**: `outputs/` directory
4. **Having issues?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Want to Understand the Project?
- **[README.md](README.md)** - Complete documentation
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical details

### Looking for Specific Information?
- **Installation**: [QUICKSTART.md](QUICKSTART.md) → Installation section
- **Usage Examples**: [README.md](README.md) → Usage section
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **File Structure**: [FILE_STRUCTURE.md](FILE_STRUCTURE.md)
- **What Changed**: [CHANGELOG.md](CHANGELOG.md)
- **API Reference**: See docstrings in source files

---

## 📖 Documentation Files

| File | Purpose | When to Read |
|------|---------|--------------|
| **[README.md](README.md)** | Main documentation, methodology, features | First time and reference |
| **[QUICKSTART.md](QUICKSTART.md)** | Step-by-step getting started guide | Installation and first run |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | Common issues and solutions | When you encounter errors |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Architecture, design patterns, improvements | Understanding structure |
| **[FILE_STRUCTURE.md](FILE_STRUCTURE.md)** | Complete file tree and dependencies | Navigating the codebase |
| **[CHANGELOG.md](CHANGELOG.md)** | Version history and changes | Seeing what's new |
| **[INDEX.md](INDEX.md)** | This file - navigation guide | Finding other files |

---

## 🐍 Python Source Files

### Execution Scripts

| File | Description | Command |
|------|-------------|---------|
| **[demo.py](demo.py)** | Demo with sample data (no internet needed) | `python demo.py` |
| **[main.py](main.py)** | Full analysis pipeline (requires internet) | `python main.py` |
| **[example.py](example.py)** | Simple usage example | `python example.py` |

### Configuration

| File | Description | Edit For |
|------|-------------|----------|
| **[config.py](config.py)** | Central configuration | Changing parameters |

### Core Models (`src/models/`)

| File | Classes | Use For |
|------|---------|---------|
| **[heston_model.py](src/models/heston_model.py)** | `HestonModel` | Stochastic volatility model, MC simulation |
| **[option_pricer.py](src/models/option_pricer.py)** | `OptionPricer`, `OptionAnalyzer` | Pricing options, error analysis |
| **[mle_optimizer.py](src/models/mle_optimizer.py)** | `MLEOptimizer` | Parameter estimation |

### Utilities (`src/utils/`)

| File | Classes | Use For |
|------|---------|---------|
| **[data_fetcher.py](src/utils/data_fetcher.py)** | `DataFetcher` | Getting market data |
| **[visualization.py](src/utils/visualization.py)** | `SimulationVisualizer`, `OptionVisualizer`, `DataVisualizer` | Creating plots |

### Package Initialization

| File | Purpose |
|------|---------|
| **[src/\_\_init\_\_.py](src/__init__.py)** | Main package |
| **[src/models/\_\_init\_\_.py](src/models/__init__.py)** | Models package |
| **[src/utils/\_\_init\_\_.py](src/utils/__init__.py)** | Utils package |

---

## 📊 Output Files (Generated)

Located in `outputs/` directory (created when you run `main.py`):

| File | Type | Description |
|------|------|-------------|
| **mc_all_paths.png** | Plot | All Monte Carlo simulation paths |
| **mc_sample_paths.png** | Plot | Sample paths with statistics |
| **option_prices_comparison.png** | Plot | Model vs market price comparison |
| **option_pricing_results.csv** | Data | Detailed pricing results table |
| **heston_parameters.csv** | Data | Estimated Heston parameters |

---

## 📦 Other Files

| File | Description |
|------|-------------|
| **[requirements.txt](requirements.txt)** | Python package dependencies |
| **[LICENSE](LICENSE)** | MIT License terms |
| **[.gitignore](.gitignore)** | Git exclusion rules |
| **Heston_BTC (1).ipynb** | Original notebook (unchanged) |

---

## 🎯 Find Information By Topic

### Installation & Setup
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Dependencies**: [requirements.txt](requirements.txt)
- **Configuration**: [config.py](config.py)

### Usage & Examples
- **Main Pipeline**: [main.py](main.py)
- **Simple Example**: [example.py](example.py)
- **Usage Guide**: [README.md](README.md) → Usage section
- **Workflows**: [QUICKSTART.md](QUICKSTART.md) → Common Workflows

### Theory & Methodology
- **Heston Model**: [README.md](README.md) → Methodology section
- **Mathematical Details**: [README.md](README.md) → Heston Model subsection
- **Parameter Estimation**: [README.md](README.md) → MLE section
- **References**: [README.md](README.md) → References section

### Code Structure
- **Architecture**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **File Tree**: [FILE_STRUCTURE.md](FILE_STRUCTURE.md)
- **Dependencies**: [FILE_STRUCTURE.md](FILE_STRUCTURE.md) → Module Dependencies
- **Data Flow**: [FILE_STRUCTURE.md](FILE_STRUCTURE.md) → Data Flow

### API Documentation
- **HestonModel**: [src/models/heston_model.py](src/models/heston_model.py) (docstrings)
- **OptionPricer**: [src/models/option_pricer.py](src/models/option_pricer.py) (docstrings)
- **MLEOptimizer**: [src/models/mle_optimizer.py](src/models/mle_optimizer.py) (docstrings)
- **DataFetcher**: [src/utils/data_fetcher.py](src/utils/data_fetcher.py) (docstrings)
- **Visualizers**: [src/utils/visualization.py](src/utils/visualization.py) (docstrings)

### Results & Output
- **Interpreting Results**: [QUICKSTART.md](QUICKSTART.md) → Understanding Output
- **Error Metrics**: [README.md](README.md) → Performance Metrics
- **Sample Output**: [README.md](README.md) → Results section

### Customization
- **Parameters**: [config.py](config.py)
- **Custom Scripts**: [example.py](example.py) as template
- **Advanced Usage**: [README.md](README.md) → Advanced Usage

### Troubleshooting
- **Common Issues**: [QUICKSTART.md](QUICKSTART.md) → Troubleshooting
- **Known Limitations**: [CHANGELOG.md](CHANGELOG.md) → Known Limitations

### Development
- **Design Patterns**: [FILE_STRUCTURE.md](FILE_STRUCTURE.md) → Key Design Patterns
- **Future Enhancements**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) → Future Enhancements
- **Contributing**: [README.md](README.md) → Contributing section

---

## 🔍 Search Tips

### Looking for...

**"How do I install?"**
→ [QUICKSTART.md](QUICKSTART.md)

**"How does the Heston model work?"**
→ [README.md](README.md) → Methodology

**"What files do what?"**
→ [FILE_STRUCTURE.md](FILE_STRUCTURE.md)

**"How do I use this in my code?"**
→ [example.py](example.py) or [README.md](README.md) → Advanced Usage

**"How do I change parameters?"**
→ [config.py](config.py) or [QUICKSTART.md](QUICKSTART.md) → Customization

**"What's the project structure?"**
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

**"What changed in this version?"**
→ [CHANGELOG.md](CHANGELOG.md)

**"Where's the Monte Carlo code?"**
→ [src/models/heston_model.py](src/models/heston_model.py) → `heston_monte_carlo()`

**"How do I price options?"**
→ [src/models/option_pricer.py](src/models/option_pricer.py) → `OptionPricer` class

**"How are parameters estimated?"**
→ [src/models/mle_optimizer.py](src/models/mle_optimizer.py) → `MLEOptimizer` class

**"How do I fetch data?"**
→ [src/utils/data_fetcher.py](src/utils/data_fetcher.py) → `DataFetcher` class

**"How do I create plots?"**
→ [src/utils/visualization.py](src/utils/visualization.py) → Visualizer classes

---

## 📈 Recommended Reading Order

### For End Users (Run & Analyze)
1. [QUICKSTART.md](QUICKSTART.md) - Setup
2. Run `python main.py`
3. [QUICKSTART.md](QUICKSTART.md) - Understanding Output
4. [README.md](README.md) - Methodology
5. Experiment with [config.py](config.py)

### For Developers (Extend & Modify)
1. [README.md](README.md) - Overview
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Architecture
3. [FILE_STRUCTURE.md](FILE_STRUCTURE.md) - Structure
4. [example.py](example.py) - Usage patterns
5. Source code files with docstrings
6. [CHANGELOG.md](CHANGELOG.md) - What changed

### For Researchers (Understand & Validate)
1. [README.md](README.md) - Methodology section
2. [src/models/heston_model.py](src/models/heston_model.py) - Implementation
3. [src/models/mle_optimizer.py](src/models/mle_optimizer.py) - Estimation
4. Run `python main.py` and analyze results
5. [README.md](README.md) - References

---

## 📞 Getting Help

1. **Check documentation** in this order:
   - [QUICKSTART.md](QUICKSTART.md) for setup issues
   - [README.md](README.md) for general questions
   - Source code docstrings for API details
   - [FILE_STRUCTURE.md](FILE_STRUCTURE.md) for navigation

2. **Review examples**:
   - [example.py](example.py) for basic usage
   - [main.py](main.py) for complete workflow

3. **Check the original notebook**:
   - `Heston_BTC (1).ipynb` for reference

---

## 📝 Quick Commands Reference

```bash
# Setup
pip install -r requirements.txt

# Run full analysis
python main.py

# Run quick example
python example.py

# View documentation
cat README.md              # or open in editor
cat QUICKSTART.md

# Check Python import
python -c "from src.models import HestonModel; help(HestonModel)"

# List output files
ls -lh outputs/

# Check file structure
tree .                     # if tree is installed
# or
find . -type f | grep -v __pycache__
```

---

## 🗂️ File Organization Logic

```
Root Level
├── Documentation (.md files)      → Information for users
├── Execution scripts (.py files)  → What you run
├── Configuration (config.py)      → What you customize
└── Package info (requirements.txt, LICENSE)

src/
├── models/       → Core business logic (Heston, pricing, estimation)
└── utils/        → Supporting functions (data, visualization)

outputs/
└── All generated files (plots, CSVs)

tests/
└── Unit tests (template)
```

---

## 🎓 Learning Path

**Beginner** (Just want to run it)
1. [QUICKSTART.md](QUICKSTART.md)
2. Run `python main.py`
3. Look at outputs

**Intermediate** (Want to customize)
1. Above +
2. [README.md](README.md) - Full documentation
3. Edit [config.py](config.py)
4. Study [example.py](example.py)

**Advanced** (Want to extend)
1. Above +
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
3. [FILE_STRUCTURE.md](FILE_STRUCTURE.md)
4. Read source code with docstrings
5. Modify modules

**Expert** (Want to contribute)
1. Above +
2. [CHANGELOG.md](CHANGELOG.md)
3. Study all source files
4. Understand mathematical derivations
5. Add features/tests

---

## ✅ Checklist for First-Time Users

- [ ] Read [QUICKSTART.md](QUICKSTART.md)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run example: `python example.py`
- [ ] Run full analysis: `python main.py`
- [ ] Check outputs in `outputs/` directory
- [ ] Read [README.md](README.md) for understanding
- [ ] Experiment with [config.py](config.py)
- [ ] Try custom modifications

---

**Last Updated**: December 3, 2025  
**Version**: 1.0.0  
**Total Documentation**: 6 markdown files, ~2000 lines  
**Total Code**: 8 Python modules, ~1270 lines  

---

*This index is your map to the project. Bookmark it for easy navigation!*
