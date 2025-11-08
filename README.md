 Advanced Distribution Calculator

A professional, feature-rich probability distribution calculator built with Python and Tkinter. 
Perform accurate statistical calculations across 11 distributions with beautiful visualizations and comprehensive history tracking.
✨ Features
🎯 Statistical Distributions

    Discrete: Binomial, Poisson, Geometric, Hypergeometric

    Continuous: Normal, Exponential, Uniform, Weibull, Gamma, Beta, Lognormal

    Dual Calculation Modes: Single point probabilities & range probabilities

📊 Visualization

    Interactive Plots: Real-time PDF/PMF visualization

    Custom Shading: Visual probability regions with color picker

    Plot Export: Save as PNG, JPEG, or PDF (300 DPI)

    History Integration: View plots for previous calculations

💾 Data Management

    Complete History: Track all calculations with timestamps

    CSV Export: Save history for further analysis

    Treeview Display: Sortable, organized history table

🎨 User Experience

    Professional UI: Modern, rounded interface with tooltips

    Dynamic Inputs: Context-aware parameter fields

    Font Scaling: Adjustable text size for accessibility

    Keyboard Shortcuts: Enter key for quick calculations

🚀 Quick Start
Installation

    Clone the repository

bash

git clone https://github.com/yourusername/distribution-calculator.git
cd distribution-calculator

    Install dependencies

bash

pip install scipy matplotlib numpy

    Run the application

bash

python distribution_calculator.py

Requirements

    Python 3.6+

    tkinter (usually included with Python)

    matplotlib

    numpy

    scipy

📸 Screenshots

(Add your screenshots here)

    Calculator Tab: Clean interface with parameter inputs and results

    History Tab: Comprehensive calculation history with mini-plots

    Distribution Plots: Professional visualizations with shaded regions

🛠️ Usage
Basic Calculation

    Select a distribution from the dropdown

    Choose between single point or range mode

    Enter parameters (fields update dynamically)

    Click CALCULATE or press Enter

    View results and optional plot

Example: Normal Distribution

    Parameters: μ (mean), σ (standard deviation)

    Single Mode: P(X ≤ value)

    Range Mode: P(lower ≤ X ≤ upper)

Advanced Features

    Plot Toggle: Show/hide distribution visualization

    Color Picker: Customize shading colors

    Font Controls: Adjust UI text size

    Export Options: Save plots and history

🏗️ Architecture
Core Components
python

# Scientific Backend
calculate_distribution()  # Unified SciPy-based calculator

# GUI Framework
DistributionCalculatorApp  # Main application class
History                   # Calculation history manager
ToolTip                   # Contextual help system

# Visualization
_create_plot_figure()     # Matplotlib plot generator
_embed_plot()            # Tkinter canvas integration

Key Design Patterns

    Model-View-Controller: Separation of calculation logic and UI

    Observer Pattern: Real-time UI updates

    Factory Pattern: Dynamic distribution object creation

📈 Supported Calculations
Distribution	Parameters	Discrete/Continuous	Range Support
Binomial	n, p, k	Discrete	✅
Poisson	λ, k	Discrete	✅
Normal	μ, σ, x	Continuous	✅
Exponential	λ, t	Continuous	✅
Geometric	p, k	Discrete	✅
Uniform	a, b, x	Continuous	✅
Weibull	λ, k, t	Continuous	✅
Gamma	α, θ, t	Continuous	✅
Beta	α, β, x	Continuous	✅
Lognormal	μ_log, σ_log, x	Continuous	✅
Hypergeometric	M, n, N, k	Discrete	✅
🔧 Technical Details
Performance Optimizations

    SciPy Integration: Leverages optimized statistical functions

    Efficient Plotting: Smart x-range calculation for each distribution

    Lazy Loading: Plots generated only when needed

Error Handling

    Input Validation: Comprehensive parameter checking

    Graceful Degradation: Fallbacks for missing dependencies

    User-Friendly Messages: Clear error explanations

🤝 Contributing

We welcome contributions! Please feel free to submit pull requests for:

    New statistical distributions

    UI/UX improvements

    Performance enhancements

    Bug fixes

    Documentation updates

Development Setup
bash

git clone https://github.com/yourusername/distribution-calculator.git
cd distribution-calculator
pip install -r requirements.txt

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

    SciPy Community: For the robust statistical functions

    Matplotlib Team: For powerful visualization capabilities

    Tkinter Developers: For the reliable GUI framework

⭐ If you find this project useful, please give it a star on GitHub!
