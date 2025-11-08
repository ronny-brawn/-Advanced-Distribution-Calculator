# Advanced Distribution Calculator

A professional probability distribution calculator built with Python and Tkinter. 
Perform accurate statistical calculations across 11 distributions with visualization and history tracking.

## Features

### 🎯 Statistical Distributions
- **Discrete**: Binomial, Poisson, Geometric, Hypergeometric
- **Continuous**: Normal, Exponential, Uniform, Weibull, Gamma, Beta, Lognormal
- **Dual Calculation Modes**: Single point probabilities & range probabilities

### 📊 Visualization
- **Interactive Plots**: Real-time PDF/PMF visualization
- **Custom Shading**: Visual probability regions with color picker
- **Plot Export**: Save as PNG, JPEG, or PDF

### 💾 Data Management
- **Complete History**: Track all calculations with timestamps
- **CSV Export**: Save history for further analysis

### 🎨 User Experience
- **Professional UI**: Modern interface with tooltips
- **Dynamic Inputs**: Context-aware parameter fields
- **Font Scaling**: Adjustable text size

## Installation

```bash
git clone https://github.com/ronny-brawn/Advanced-Distribution-Calculator.git
cd Advanced-Distribution-Calculator
pip install scipy matplotlib numpy
python distribution_calculator.py
```

### Requirements
- Python 3.6+
- scipy
- matplotlib
- numpy

## Usage

1. Select a distribution from the dropdown
2. Choose between single point or range mode
3. Enter parameters (fields update dynamically)
4. Click **CALCULATE** or press **Enter**
5. View results and optional plot

## Supported Distributions

| Distribution | Parameters | Type |
|-------------|------------|------|
| Binomial | n, p, k | Discrete |
| Poisson | λ, k | Discrete |
| Normal | μ, σ, x | Continuous |
| Exponential | λ, t | Continuous |
| Geometric | p, k | Discrete |
| Uniform | a, b, x | Continuous |
| Weibull | λ, k, t | Continuous |
| Gamma | α, θ, t | Continuous |
| Beta | α, β, x | Continuous |
| Lognormal | μ_log, σ_log, x | Continuous |
| Hypergeometric | M, n, N, k | Discrete |

## License

MIT License - see LICENSE file for details.

---

**⭐ If you find this project useful, please give it a star on GitHub!**
