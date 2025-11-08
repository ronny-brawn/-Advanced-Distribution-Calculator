# Advanced Distribution Calculator

A professional probability distribution calculator with cross-platform support.

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![SciPy](https://img.shields.io/badge/SciPy-Required-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## Features

- **11 Statistical Distributions**: Binomial, Poisson, Normal, Exponential, Geometric, Uniform, Weibull, Gamma, Beta, Lognormal, Hypergeometric
- **Dual Calculation Modes**: Single point and range probabilities
- **Interactive Visualization**: Real-time PDF/PMF plots
- **Cross-Platform**: Run on Windows, macOS, and Linux
  
📊 Visualization

    Interactive Plots: Real-time PDF/PMF visualization

    Custom Shading: Visual probability regions with color picker

    Plot Export: Save as PNG, JPEG, or PDF

💾 Data Management

    Complete History: Track all calculations with timestamps

    CSV Export: Save history for further analysis

🎨 User Experience

    Professional UI: Modern interface with tooltips

    Dynamic Inputs: Context-aware parameter fields

    Font Scaling: Adjustable text size
    

## Installation

### Linux (Debian/Ubuntu)
```bash
sudo dpkg -i advanced-distribution-calculator.deb
sudo apt-get install -f
```

### From Source
```bash
git clone https://github.com/ronny-brawn/Advanced-Distribution-Calculator.git
cd Advanced-Distribution-Calculator
pip install -r requirements.txt
python distribution_calculator.py
```

## Building Executables

### Creating Windows Executable (.exe)

1. **Install PyInstaller:**
```bash
pip install pyinstaller
```

2. **Build the executable:**
```bash
pyinstaller --onefile --windowed --name "Advanced Distribution Calculator" distribution_calculator.py
```

3. **The executable will be in the `dist` folder**

### Creating macOS Application (.app)

1. **Install PyInstaller:**
```bash
pip install pyinstaller
```

2. **Build the application bundle:**
```bash
pyinstaller --onefile --windowed --name "Advanced Distribution Calculator" distribution_calculator.py
```

3. **The .app bundle will be in the `dist` folder**

### Additional Packaging Options

**For better macOS integration:**
```bash
pyinstaller --windowed --name "Advanced Distribution Calculator" --icon=icon.icns distribution_calculator.py
```

**For Windows with custom icon:**
```bash
pyinstaller --onefile --windowed --name "Advanced Distribution Calculator" --icon=icon.ico distribution_calculator.py
```

**Create Linux AppImage:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed distribution_calculator.py
# Use linuxdeploy or appimagetool to create AppImage
```

## Requirements
- Python 3.6+
- scipy
- matplotlib  
- numpy
- tkinter

## Building Dependencies
```bash
pip install scipy matplotlib numpy
```

## Supported Distributions

| Distribution | Type |
|-------------|------|
| Binomial | Discrete |
| Poisson | Discrete |
| Normal | Continuous |
| Exponential | Continuous |
| Geometric | Discrete |
| Uniform | Continuous |
| Weibull | Continuous |
| Gamma | Continuous |
| Beta | Continuous |
| Lognormal | Continuous |
| Hypergeometric | Discrete |

Usage

    1. Launch from applications menu or run distribution-calculator

    2. Select distribution and calculation mode

    3. Enter parameters

    4. View results with optional visualization

## License

MIT License

---

**⭐ If you find this project useful, please give it a star on GitHub!**
