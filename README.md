
# Advanced Distribution Calculator

A professional **probability distribution calculator** with cross-platform support, interactive visualizations, 
and dual calculation modes.

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![SciPy](https://img.shields.io/badge/SciPy-Required-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

---

## Features

* **11 Statistical Distributions**
  Binomial, Poisson, Normal, Exponential, Geometric, Uniform, Weibull, Gamma, Beta, Lognormal, Hypergeometric

* **Dual Calculation Modes**
  Single-point probability and range probability calculations

* **Interactive Visualization**

  * Real-time PDF/PMF plots
  * Custom shading for probability regions
  * Export plots as PNG, JPEG, or PDF

* **Data Management**

  * Complete calculation history with timestamps
  * CSV export for further analysis

* **Professional User Experience**

  * Modern, intuitive UI with tooltips
  * Dynamic, context-aware input fields
  * Adjustable font scaling

---

## Tool Review

**1. Main Interface**

<img width="1027" height="810" alt="Screenshot from 2025-11-08 05-03-47" src="https://github.com/user-attachments/assets/76ded600-7870-4378-9aa4-abe65d9b8b91" />



**2. PDF/PMF Visualization (Binomial)**

<img width="1028" height="471" alt="Screenshot from 2025-11-08 05-05-18" src="https://github.com/user-attachments/assets/f08344a3-a780-4dfb-8bd7-f42e3322cfa5" />



**3. Range Probability Highlighting**

<img width="1021" height="801" alt="Screenshot from 2025-11-08 05-08-01" src="https://github.com/user-attachments/assets/a4e1a525-9136-4f9b-a182-7f8fe1a864ef" />



**4. Exporting Plots**

<img width="792" height="542" alt="Screenshot from 2025-11-08 05-06-12" src="https://github.com/user-attachments/assets/96266dac-4834-47b7-b27f-b8544f26fc87" />



**5. History review**
<img width="1021" height="801" alt="Screenshot from 2025-11-08 05-08-50" src="https://github.com/user-attachments/assets/e3742d8d-3672-447f-a50c-8df4c21add5d" />

---

## Supported Distributions

| Distribution   | Type       |
| -------------- | ---------- |
| Binomial       | Discrete   |
| Poisson        | Discrete   |
| Normal         | Continuous |
| Exponential    | Continuous |
| Geometric      | Discrete   |
| Uniform        | Continuous |
| Weibull        | Continuous |
| Gamma          | Continuous |
| Beta           | Continuous |
| Lognormal      | Continuous |
| Hypergeometric | Discrete   |

---

## Installation

### 1. Using Source (Recommended)

```bash
git clone https://github.com/ronny-brawn/Advanced-Distribution-Calculator.git
cd Advanced-Distribution-Calculator

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt

python distribution_calculator.py
```

### 2. Linux (.deb Package)

```bash
wget https://www.mediafire.com/file/9ab4651m4a08xm2/advanced-distribution-calculator.deb/file
sudo dpkg -i advanced-distribution-calculator.deb
sudo apt-get install -f
```

> ⚠️ Note: Verify the `.deb` package before installation for security.

---

## Building Executables

### Windows (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Advanced Distribution Calculator" distribution_calculator.py
```

Optional custom icon:

```bash
--icon=icon.ico
```

### macOS (.app)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Advanced Distribution Calculator" distribution_calculator.py
```

Optional custom icon:

```bash
--icon=icon.icns
```

### Linux (AppImage)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed distribution_calculator.py
# Use linuxdeploy or AppImageTool to create AppImage
```

---

## Usage Example

**Scenario:** Probability of exactly 5 successes in 10 trials (Binomial)

1. Launch the calculator
2. Select **Binomial** distribution
3. Enter parameters: `n=10`, `p=0.5`, `x=5`
4. Click **Calculate** → get `P(X=5)`
5. Optional: visualize the PDF with highlighted probability region

**Range probability example:**

* Find probability of `3 ≤ X ≤ 7` with the same parameters

---

## Dependencies

* Python 3.6+
* `scipy`
* `numpy`
* `matplotlib`
* `tkinter`

Install all dependencies:

```bash
pip install scipy matplotlib numpy
```

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

⭐ If you find this project useful, please give it a star on GitHub!

