import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime
import csv
import platform

# --- PERFORMANCE IMPROVEMENT: Use SciPy for all statistical calculations ---
try:
    from scipy import stats

    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("WARNING: SciPy not found. Statistical functions will fail.")


# --- Core Calculation Functions (SciPy-based) ---

def calculate_distribution(dist_name, is_range, vals):
    """
    Core function to calculate probability using SciPy based on distribution and mode.
    Handles parameter mapping for SciPy objects.

    Args:
        dist_name (str): Name of the distribution.
        is_range (bool): True if calculating a range (P(X1 <= X <= X2)).
        vals (list): List of parameter values. Order depends on the distribution and range mode.
            For range: [X_low, X_high, P1, P2, ...]
            For single: [X_val, P1, P2, ...]

    Returns: (result_string, dist_object, is_discrete)
    """
    if not SCIPY_AVAILABLE:
        return "Error: SciPy is required for this calculation.", None, None

    # Constants and Parameter Mapping
    dist_map = {
        "Binomial": (stats.binom, 'k', 'n', 'p'),
        "Poisson": (stats.poisson, 'k', 'λ'),
        "Normal": (stats.norm, 'x', 'μ', 'σ'),
        "Exponential": (stats.expon, 't', 'λ'),
        "Geometric": (stats.geom, 'k', 'p'),
        "Uniform": (stats.uniform, 'x', 'a', 'b'),
        "Weibull": (stats.weibull_min, 't', 'λ', 'k'),
        "Gamma": (stats.gamma, 't', 'α', 'θ'),
        "Beta": (stats.beta, 'x', 'α', 'β'),
        "Lognormal": (stats.lognorm, 'x', 'μ', 'σ'),
        "Hypergeometric": (stats.hypergeom, 'k', 'M', 'n', 'N'),
    }

    if dist_name not in dist_map:
        return "Unsupported distribution.", None, None

    DistClass, X_symbol, *ParamSymbols = dist_map[dist_name]

    # --- Parameter Conversion and Object Initialization ---
    try:
        if is_range:
            # X_low and X_high are the first two values in vals
            dist_params = vals[2:]
        else:
            # X_val is the first value in vals
            dist_params = vals[1:]

        # Initialize SciPy distribution object based on name and parameters
        if dist_name == "Binomial":
            n, p = dist_params
            dist = DistClass(int(n), p)
            is_discrete = True
        elif dist_name == "Poisson":
            lam = dist_params[0]
            dist = DistClass(lam)
            is_discrete = True
        elif dist_name == "Normal":
            mu, sigma = dist_params
            dist = DistClass(loc=mu, scale=sigma)
            is_discrete = False
        elif dist_name == "Exponential":
            lam = dist_params[0]
            dist = DistClass(scale=1 / lam)  # SciPy scale is 1/rate (1/λ)
            is_discrete = False
        elif dist_name == "Geometric":
            p = dist_params[0]
            dist = DistClass(p)
            is_discrete = True
        elif dist_name == "Uniform":
            a, b = dist_params
            dist = DistClass(loc=a, scale=b - a)  # SciPy scale is (b-a)
            is_discrete = False
        elif dist_name == "Weibull":
            lam, k_shape = dist_params
            # SciPy weibull_min: c=k (shape), scale=lambda
            dist = DistClass(c=k_shape, scale=lam)
            is_discrete = False
        elif dist_name == "Gamma":
            alpha, theta = dist_params  # alpha (shape), theta (scale)
            dist = DistClass(alpha, scale=theta)
            is_discrete = False
        elif dist_name == "Beta":
            alpha, beta = dist_params
            dist = DistClass(alpha, beta)
            is_discrete = False
        elif dist_name == "Lognormal":
            mu_log, sigma_log = dist_params
            # SciPy lognorm: s=sigma (shape), scale=exp(mu) (often 1.0)
            dist = DistClass(sigma_log, scale=math.exp(mu_log))
            is_discrete = False
        elif dist_name == "Hypergeometric":
            M, n, N = dist_params  # M (Pop), n (Sample), N (Pop Successes)
            dist = DistClass(M=int(M), n=int(n), N=int(N))
            is_discrete = True
        else:
            return "Unsupported distribution.", None, None

    except Exception as e:
        return f"Parameter Error: {e}", None, None

    # --- Calculation Logic ---
    if is_range:
        # Range Calculation P(X_low <= X <= X_high)
        X_low, X_high = vals[0], vals[1]

        if is_discrete:
            X_low_int, X_high_int = int(X_low), int(X_high)
            # P(X <= k_high) - P(X <= k_low - 1)
            prob = dist.cdf(X_high_int) - dist.cdf(X_low_int - 1)
            result = f"P({X_low_int}≤{X_symbol}≤{X_high_int}) = {prob * 100:.2f}%"

        else:
            # P(X <= x_high) - P(X <= x_low)
            prob = dist.cdf(X_high) - dist.cdf(X_low)
            result = f"P({X_low:.2f}≤{X_symbol}≤{X_high:.2f}) = {prob * 100:.2f}%"

    else:
        # Single Point/CDF Calculation
        X_val = vals[0]

        if is_discrete:
            # Single Point P(X = k)
            prob = dist.pmf(int(X_val))
            result = f"P({X_symbol}={int(X_val)}) = {prob * 100:.2f}%"
        else:
            # CDF P(X <= x)
            prob = dist.cdf(X_val)
            result = f"P({X_symbol}≤{X_val:.2f}) = {prob * 100:.2f}%"

    return result, dist, is_discrete


# --- ToolTip Class (Unchanged) ---
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tooltip: return
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f"+{x}+{y}")
        label = ttk.Label(self.tooltip, text=self.text, background="#ffffe0",
                          relief="solid", borderwidth=1, padding=3)
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


# --- Calculation History (Unchanged) ---
class History:
    def __init__(self):
        self.entries = []

    def add(self, distribution, params_structured, result):
        self.entries.append({
            "time": datetime.now(),
            "distribution": distribution,
            "params": params_structured,  # List of (symbol, value)
            "result": result
        })

    def clear(self):
        self.entries.clear()

    def recent(self, n=10):
        return self.entries[-n:]


# --- Main Application ---

class DistributionCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📈 Advanced Distribution Calculator")
        # Increased default geometry for better auto-fitting
        self.root.geometry("1024x768")

        if platform.system() == "Darwin" or platform.system() == "Linux":
            try:
                self.root.wm_attributes('-alpha', 1.0)
            except:
                pass

        # Font size management (11 is the default/Medium size)
        self.font_size_options = [('Small', 10), ('Medium', 11), ('Large', 12), ('Extra Large', 14)]
        self.font_size_base = tk.IntVar(value=11)  # Default to Medium (11)
        self.font_size_base.trace_add('write', lambda *args: self._update_font_size())

        self.current_mode = tk.StringVar(value="Normal")
        self.range_mode = tk.BooleanVar(value=False)
        self.show_plot = tk.BooleanVar(value=False)
        self.custom_shade_color = tk.StringVar(value="#007bff")
        self.history = History()

        self.param_vars = [tk.StringVar() for _ in range(4)]
        self.input_widgets = []
        self.calculate_button = None
        self.history_plot_canvas = None

        self._setup_style()
        self._build_ui()
        self.update_inputs()
        self.refresh_history()
        self._update_font_size()  # Apply initial font settings

        self.root.bind("<Return>", lambda e: self.calculate())

    # --- Font and Style Methods (Updated for dynamic font size) ---

    def _setup_style(self):
        """Configure ttk styles including rounded corners for elements."""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure styles with placeholder font sizes, updated by _update_font_size
        self._update_font_size()

        style.configure("Rounded.TButton",
                        background="#007bff",
                        foreground="white",
                        focuscolor="none",
                        relief="flat",
                        padding=[10, 5])
        style.map("Rounded.TButton",
                  background=[('active', '#0056b3')],
                  foreground=[('active', 'white')])

        style.configure("Rounded.TFrame", background="#f8f9fa", relief="flat", borderwidth=0, padding=15)

        style.configure("Card.TLabelframe",
                        background="#ffffff",
                        foreground="#343a40",
                        relief="flat",
                        borderwidth=1,
                        padding=15,
                        )
        style.configure("TLabel.Card.TLabelframe", background="#ffffff")

        style.configure("TNotebook", background="#f8f9fa", borderwidth=0)
        style.configure("TNotebook.Tab", background="#e9ecef", foreground="#495057",
                        padding=[10, 5], borderwidth=0, relief="raised")
        style.map("TNotebook.Tab",
                  background=[('selected', '#ffffff')],
                  foreground=[('selected', '#007bff')],
                  expand=[('selected', [1, 1, 1, 0])])
        style.layout("TNotebook.Tab", [
            ('Notebook.tab', {'children': [
                ('Notebook.padding', {'side': 'top', 'children': [
                    ('Notebook.focus', {'children': [
                        ('Notebook.label', {'sticky': 'nswe'})
                    ]})
                ]})
            ], 'sticky': 'nswe'})
        ])

    def _update_font_size(self):
        """Dynamically updates the font size of all styled widgets."""
        base = self.font_size_base.get()

        style = ttk.Style()

        # Standard Label, Entry, OptionMenu, Checkbutton text
        style.configure("TLabel", background="#f8f9fa", font=('Segoe UI', base))
        style.configure("TEntry", font=('Segoe UI', base))
        style.configure("TMenubutton", font=('Segoe UI', base))
        style.configure("TCheckbutton", font=('Segoe UI', base))
        style.configure("Treeview", font=('Segoe UI', base))

        # Header/Title text
        style.configure("Header.TLabel", font=('Segoe UI', base + 2, 'bold'))
        style.configure("Result.TLabel", font=('Segoe UI', base + 1, 'bold'))
        style.configure("Rounded.TButton", font=('Segoe UI', base + 1, 'bold'))
        style.configure("Card.TLabelframe", font=('Segoe UI', base + 1, 'bold'))
        style.configure("Treeview.Heading", font=('Segoe UI', base, 'bold'))

        # Update all widgets to refresh the font settings
        self.root.update_idletasks()

        # --- Parameter Definitions Helper (Unchanged) ---

    def _get_param_definitions(self, dist, is_range):
        """Returns the (symbol, description) list for a given distribution and mode."""

        if dist == "Binomial":
            if is_range:
                return [("n", "Trials (int ≥ 0)"), ("k₁", "Lower Successes"), ("k₂", "Upper Successes"),
                        ("p", "Probability (0–1)")]
            else:
                return [("n", "Trials (int ≥ 0)"), ("k", "Successes"), ("p", "Probability (0–1)")]
        elif dist == "Poisson":
            if is_range:
                return [("λ", "Rate (λ > 0)"), ("k₁", "Lower Occurrences"), ("k₂", "Upper Occurrences")]
            else:
                return [("λ", "Rate (λ > 0)"), ("k", "Occurrences (int ≥ 0)")]
        elif dist == "Normal":
            if is_range:
                return [("μ", "Mean"), ("σ", "Std. Dev. (σ>0)"), ("x₁", "Lower Value"), ("x₂", "Upper Value")]
            else:
                return [("μ", "Mean"), ("σ", "Std. Dev. (σ>0)"), ("x", "Value")]
        elif dist == "Exponential":
            if is_range:
                return [("λ", "Rate (λ > 0)"), ("t₁", "Lower Time (≥ 0)"), ("t₂", "Upper Time (≥ 0)")]
            else:
                return [("λ", "Rate (λ > 0)"), ("t", "Time (≥ 0)")]
        elif dist == "Geometric":
            if is_range:
                return [("p", "Probability (0–1)"), ("k₁", "Lower Trial (≥1)"), ("k₂", "Upper Trial (≥1)")]
            else:
                return [("p", "Probability (0–1)"), ("k", "Trial (≥1)")]
        elif dist == "Uniform":
            if is_range:
                return [("a", "Global Lower Bound"), ("b", "Global Upper Bound (b>a)"), ("x₁", "Range Lower Value"),
                        ("x₂", "Range Upper Value")]
            else:
                return [("a", "Lower bound"), ("b", "Upper bound (b>a)"), ("x", "Value")]
        elif dist == "Weibull":
            if is_range:
                return [("λ", "Scale (λ > 0)"), ("k", "Shape (k > 0)"), ("t₁", "Lower Time (≥ 0)"),
                        ("t₂", "Upper Time (≥ 0)")]
            else:
                return [("λ", "Scale (λ > 0)"), ("k", "Shape (k > 0)"), ("t", "Time (≥ 0)")]
        elif dist == "Gamma":
            if is_range:
                return [("α", "Shape (α > 0)"), ("θ", "Scale (θ > 0)"), ("t₁", "Lower Time (≥ 0)"),
                        ("t₂", "Upper Time (≥ 0)")]
            else:
                return [("α", "Shape (α > 0)"), ("θ", "Scale (θ > 0)"), ("t", "Time (≥ 0)")]
        elif dist == "Beta":
            if is_range:
                return [("α", "Shape (α > 0)"), ("β", "Shape (β > 0)"), ("x₁", "Lower Value (0–1)"),
                        ("x₂", "Upper Value (0–1)")]
            else:
                return [("α", "Shape (α > 0)"), ("β", "Shape (β > 0)"), ("x", "Value (0–1)")]
        elif dist == "Lognormal":
            if is_range:
                return [("μ_log", "Log Mean"), ("σ_log", "Log Std. Dev. (>0)"), ("x₁", "Lower Value (>0)"),
                        ("x₂", "Upper Value (>0)")]
            else:
                return [("μ_log", "Log Mean"), ("σ_log", "Log Std. Dev. (>0)"), ("x", "Value (>0)")]
        elif dist == "Hypergeometric":
            if is_range:
                return [("M", "Pop Size (int)"), ("n", "Sample Size (int)"), ("N", "Pop Successes (int)"),
                        ("k₁", "Lower Successes"), ("k₂", "Upper Successes")]
            else:
                return [("M", "Pop Size (int)"), ("n", "Sample Size (int)"), ("N", "Pop Successes (int)"),
                        ("k", "Successes")]

        return []

    # --- UI Building Methods (Updated Header) ---

    def _build_ui(self):
        """Build the main UI layout with tabs"""
        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_calc = ttk.Frame(self.notebook, style="Rounded.TFrame")
        self.tab_history = ttk.Frame(self.notebook, style="Rounded.TFrame")
        self.notebook.add(self.tab_calc, text="Calculator")
        self.notebook.add(self.tab_history, text="History")

        self._build_calculator_tab()
        self._build_history_tab()

    def _build_calculator_tab(self):
        """Build the calculator tab content"""
        header = ttk.Frame(self.tab_calc, style="Rounded.TFrame")
        header.pack(fill="x", pady=10)

        # Left side: Distribution selection
        dist_frame = ttk.Frame(header)
        dist_frame.pack(side="left", padx=5)
        ttk.Label(dist_frame, text="Distribution:", style="Header.TLabel").pack(side="left")

        distributions = ["Binomial", "Poisson", "Normal", "Exponential", "Geometric",
                         "Uniform", "Weibull", "Gamma", "Beta", "Lognormal", "Hypergeometric"]

        ttk.OptionMenu(dist_frame, self.current_mode, self.current_mode.get(), *distributions,
                       command=lambda _: self.update_inputs()).pack(side="left", padx=10)

        # Center: Font Adjuster
        font_frame = ttk.Frame(header)
        font_frame.pack(side="left", padx=20)
        ttk.Label(font_frame, text="Font Size:", style="Header.TLabel").pack(side="left")

        font_names = [name for name, size in self.font_size_options]
        font_map = {name: size for name, size in self.font_size_options}

        def set_font_size(selected_name):
            self.font_size_base.set(font_map[selected_name])

        # Set initial display value for OptionMenu to 'Medium' (which is the default size 11)
        default_font_name = next(name for name, size in self.font_size_options if size == self.font_size_base.get())
        font_var = tk.StringVar(value=default_font_name)
        ttk.OptionMenu(font_frame, font_var, font_var.get(), *font_names, command=set_font_size).pack(side="left")

        # Right side: Settings
        settings_frame = ttk.Frame(header)
        settings_frame.pack(side="right", padx=5)

        ttk.Checkbutton(settings_frame, text="Range Mode", variable=self.range_mode,
                        command=self.update_inputs).pack(side="left", padx=5)
        ttk.Checkbutton(settings_frame, text="Show Plot", variable=self.show_plot).pack(side="left", padx=5)
        ttk.Button(settings_frame, text="Shade Color", command=self.change_shading_color,
                   style="Rounded.TButton").pack(side="left", padx=5)
        ttk.Button(settings_frame, text="Export Plot", command=self.export_plot,
                   style="Rounded.TButton").pack(side="left", padx=5)

        # Inputs
        self.input_frame = ttk.LabelFrame(self.tab_calc, text="Parameters", style="Card.TLabelframe", padding=10)
        self.input_frame.pack(fill="x", padx=10, pady=10)

        # Create widgets once
        if not self.input_widgets:
            for i in range(4):
                frame = ttk.Frame(self.input_frame)
                lbl = ttk.Label(frame, width=25, anchor="w")
                entry = ttk.Entry(frame, width=25, textvariable=self.param_vars[i])
                lbl.pack(side="left")
                entry.pack(side="left", fill="x", expand=True)
                self.input_widgets.append((lbl, entry, frame))

        # Calculate Button
        self.calculate_button = ttk.Button(self.tab_calc, text="CALCULATE", style="Rounded.TButton",
                                           command=self.calculate)
        self.calculate_button.pack(fill="x", padx=10, pady=10)

        # Result
        self.result_frame = ttk.LabelFrame(self.tab_calc, text="Result", style="Card.TLabelframe", padding=10)
        self.result_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.result_label = ttk.Label(self.result_frame, text="Enter parameters and click CALCULATE.",
                                      style="Result.TLabel", wraplength=1000, justify="center")
        self.result_label.pack(fill="x")

        # Plot frame
        self.plot_frame = ttk.Frame(self.result_frame)
        self.plot_frame.pack(fill="both", expand=True)
        self.plot_canvas = None

    def _build_history_tab(self):
        """Build the history tab content"""
        top = ttk.Frame(self.tab_history, style="Rounded.TFrame")
        top.pack(fill="x", pady=5)

        ttk.Button(top, text="Clear History", command=self.clear_history, style="Rounded.TButton").pack(side="left",
                                                                                                        padx=5)
        ttk.Button(top, text="Export CSV", command=self.export_history, style="Rounded.TButton").pack(side="left",
                                                                                                      padx=5)

        cols = ("Time", "Distribution", "Parameters", "Result")
        self.tree = ttk.Treeview(self.tab_history, columns=cols, show="headings")

        self.tree.column("Time", width=120, anchor=tk.W)
        self.tree.column("Distribution", width=100, anchor=tk.W)
        self.tree.column("Parameters", width=250, anchor=tk.W)
        self.tree.column("Result", width=250, anchor=tk.W)

        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for col in cols:
            self.tree.heading(col, text=col)

        # Plot Display Area (Mini Display)
        self.history_plot_frame = ttk.LabelFrame(self.tab_history, text="Selected Distribution Plot",
                                                 style="Card.TLabelframe", padding=10)
        self.history_plot_frame.pack(fill="x", padx=10, pady=10, ipady=5)

        self.history_plot_canvas = None

        self.tree.bind('<<TreeviewSelect>>', self.show_plot_from_history)

    # --- Calculation and Plotting Methods ---

    def _animate_success(self, button_widget):
        """Displays a pulsating checkmark on the button after success."""
        style = ttk.Style()
        style_name = "Rounded.TButton"
        original_text = "CALCULATE"
        original_bg = "#007bff"
        active_bg = "#0056b3"
        success_bg = "#28a745"

        def pulse(count=0):
            if count >= 6:
                button_widget.config(text=original_text)
                style.configure(style_name, background=original_bg)
                style.map(style_name, background=[('active', active_bg), ('!active', original_bg)])
                return

            new_bg = success_bg if count % 2 == 0 else original_bg

            button_widget.config(text="✓ Success!")
            style.configure(style_name, background=new_bg)
            style.map(style_name, background=[('active', active_bg), ('!active', new_bg)])

            self.root.after(150, lambda: pulse(count + 1))

        pulse()

    def _is_range_calc_from_params(self, param_list):
        """Determines if the current list of structured parameters represents a range calculation."""
        # Range calculation is indicated by having parameter symbols like '₁' or '₂'
        return any('₁' in p[0] or '₂' in p[0] for p in param_list)

    def _embed_plot(self, master_frame, canvas_reference, dist_name, dist_obj, is_discrete, parsed_params):
        """Generic function to destroy previous plot and embed a new one."""

        # Determine the canvas reference name dynamically
        canvas_attr_name = 'plot_canvas' if master_frame == self.plot_frame else 'history_plot_canvas'

        current_canvas = getattr(self, canvas_attr_name)
        if current_canvas:
            current_canvas.get_tk_widget().destroy()
            setattr(self, canvas_attr_name, None)

        try:
            fig = self._create_plot_figure(dist_name, dist_obj, is_discrete, parsed_params)
            new_canvas = FigureCanvasTkAgg(fig, master=master_frame)
            new_canvas.draw()
            new_canvas.get_tk_widget().pack(fill="both", expand=True)
            setattr(self, canvas_attr_name, new_canvas)

        except Exception as e:
            raise e

    def _create_plot_figure(self, dist_name, dist_obj, is_discrete, parsed_params):
        """
        Core function to create the matplotlib figure using the SciPy distribution object.
        """
        fig, ax = plt.subplots(figsize=(6, 3))
        shade_color = self.custom_shade_color.get()

        # Determine the x-range for plotting
        if dist_name == "Normal":
            x_min, x_max = dist_obj.ppf(0.001), dist_obj.ppf(0.999)
        elif dist_name in ["Exponential", "Weibull", "Gamma", "Lognormal"]:
            x_min, x_max = 0, dist_obj.ppf(0.95)
        elif dist_name == "Uniform":
            a = dist_obj.kwds['loc']
            b = a + dist_obj.kwds['scale']
            x_min, x_max = a - (b - a) * 0.1, b + (b - a) * 0.1
        elif dist_name == "Beta":
            x_min, x_max = 0, 1
        elif is_discrete:
            if dist_name == "Geometric":
                x_min, x_max = 1, dist_obj.ppf(0.95) + 1
            elif dist_name == "Binomial":
                x_min, x_max = 0, dist_obj.args[0]
            elif dist_name == "Poisson":
                x_min, x_max = 0, dist_obj.ppf(0.99)
            elif dist_name == "Hypergeometric":
                x_min, x_max = dist_obj.support()[0], dist_obj.support()[1] + 1
        else:  # Default fallback
            x_min, x_max = dist_obj.ppf(0.01), dist_obj.ppf(0.99)

        x_min = max(0.0, x_min) if x_min < 0 and not dist_name == "Normal" else x_min

        # --- Plotting Data Generation ---
        if is_discrete:
            x_values = np.arange(int(x_min), int(x_max) + 1, dtype=int)
            y_values = dist_obj.pmf(x_values)
            ax.bar(x_values, y_values, color="skyblue", alpha=0.5, label='PMF')
            x_values_for_shade = x_values
            y_values_for_shade = y_values

        else:
            x_values = np.linspace(x_min, x_max, 300)
            y_values = dist_obj.pdf(x_values)
            ax.plot(x_values, y_values, 'b-', label='PDF')
            x_values_for_shade = x_values
            y_values_for_shade = y_values

        # --- Shading Logic ---
        is_range_calc = self._is_range_calc_from_params(parsed_params)

        # Extract X-values using parameter symbols (x, x1, x2, k, k1, k2, etc.)
        if is_range_calc:
            X_low = next((p[1] for p in parsed_params if '₁' in p[0] or 'x₁' in p[0] or 't₁' in p[0] or 'k₁' in p[0]),
                         None)
            X_high = next((p[1] for p in parsed_params if '₂' in p[0] or 'x₂' in p[0] or 't₂' in p[0] or 'k₂' in p[0]),
                          None)

            if X_low is not None and X_high is not None:
                if is_discrete:
                    X_low_int, X_high_int = int(X_low), int(X_high)
                    shade_mask = (x_values_for_shade >= X_low_int) & (x_values_for_shade <= X_high_int)
                    ax.bar(x_values_for_shade[shade_mask], y_values_for_shade[shade_mask],
                           color=shade_color, alpha=1.0, label=f'P({X_low_int} ≤ X ≤ {X_high_int})')
                else:
                    shade_mask = (x_values_for_shade >= X_low) & (x_values_for_shade <= X_high)
                    ax.fill_between(x_values_for_shade, 0, y_values_for_shade,
                                    where=shade_mask, color=shade_color, alpha=0.5,
                                    label=f'P({X_low:.2f} ≤ X ≤ {X_high:.2f})')
        else:
            X_val = next((p[1] for p in parsed_params if p[0] in ['x', 'k', 't']), None)

            if X_val is not None:
                if is_discrete:
                    X_val_int = int(X_val)
                    shade_mask = (x_values_for_shade == X_val_int)
                    ax.bar(x_values_for_shade[shade_mask], y_values_for_shade[shade_mask],
                           color=shade_color, alpha=1.0, label=f'P(X = {X_val_int})')
                else:
                    shade_mask = (x_values_for_shade <= X_val)
                    ax.fill_between(x_values_for_shade, 0, y_values_for_shade,
                                    where=shade_mask, color=shade_color, alpha=0.5,
                                    label=f'P(X ≤ {X_val:.2f})')

        # Apply labels and cleanup
        ax.set_title(f"{dist_name} Distribution PDF/PMF")
        ax.grid(alpha=0.3)
        ax.legend(loc='upper right', prop={'size': 8})
        plt.tight_layout()
        return fig

    def plot_main_distribution(self, dist_name, dist_obj, is_discrete, parsed_params):
        """Plotting function for the main Calculator tab."""
        try:
            self._embed_plot(self.plot_frame, self.plot_canvas, dist_name, dist_obj, is_discrete, parsed_params)
        except Exception as e:
            if self.plot_canvas: self.plot_canvas.get_tk_widget().destroy()
            self.plot_canvas = None
            messagebox.showerror("Plot Error", f"Could not generate main plot: {str(e)}")

    # --- History Plotting (Fixed) ---

    def show_plot_from_history(self, event):
        """When a history item is selected, display its corresponding plot and details."""
        selected_item = self.tree.selection()
        if not selected_item:
            self.clear_history_plot()
            return

        try:
            # The iid of the tree item is set to the index in self.history.entries
            index = int(selected_item[0])
            entry = self.history.entries[index]

            dist = entry["distribution"]
            parsed_params = entry["params"]  # List of (symbol, value) tuples
            result = entry["result"]

            # 1. Update the main result label for context
            param_str = ", ".join([f"{p[0]}={p[1]:.4g}" for p in parsed_params])
            self.result_label.config(
                text=f"History Result ({dist}, Params: {param_str}): {result}"
            )

            # 2. Generate the plot in the mini display
            self.plot_history_entry(dist, parsed_params)

        except IndexError:
            self.clear_history_plot()
        except Exception as e:
            self.clear_history_plot()
            print(f"Plot Error in History: {str(e)}")

    def plot_history_entry(self, dist_name, parsed_params):
        """
        Generates the distribution object and plots it in the history tab's mini-display.
        FIXED: Ensures the correct parameter order is passed to calculate_distribution.
        """
        try:
            is_range_calc = self._is_range_calc_from_params(parsed_params)

            if is_range_calc:
                # Find the X values (those with ₁ or ₂)
                X_low = next(p[1] for p in parsed_params if '₁' in p[0] or 'x₁' in p[0] or 't₁' in p[0] or 'k₁' in p[0])
                X_high = next(
                    p[1] for p in parsed_params if '₂' in p[0] or 'x₂' in p[0] or 't₂' in p[0] or 'k₂' in p[0])

                # Non-X values are the actual distribution parameters (P1, P2, etc.)
                # Filter out the X-value symbols (x/k/t with 1 or 2 subscripts)
                non_x_params = [p for p in parsed_params if not ('₁' in p[0] or '₂' in p[0])]
                non_x_values = [p[1] for p in non_x_params]

                # Construct the input array for calculate_distribution: [X1, X2, P1, P2...]
                calc_vals = [X_low, X_high] + non_x_values
            else:
                # Single point/CDF: (X, P1, P2, P3...) - just the values in order
                x_value = next(p[1] for p in parsed_params if p[0] in ['x', 'k', 't'])
                param_values = [p[1] for p in parsed_params if p[0] not in ['x', 'k', 't']]
                calc_vals = [x_value] + param_values

            # Re-initialize the SciPy object
            _, dist_obj, is_discrete = calculate_distribution(dist_name, is_range_calc, calc_vals)

            if not dist_obj:
                raise ValueError("Could not initialize distribution object for history plot.")

            # Embed the plot using the original structured parameters for correct shading logic
            self._embed_plot(self.history_plot_frame, self.history_plot_canvas, dist_name, dist_obj, is_discrete,
                             parsed_params)

        except Exception as e:
            if self.history_plot_canvas: self.history_plot_canvas.get_tk_widget().destroy()
            self.history_plot_canvas = None
            raise e

            # --- Other UI/History Methods (Unchanged) ---

    def export_plot(self):
        """Export the currently displayed plot as an image file."""
        if not self.plot_canvas:
            messagebox.showinfo("Export Plot", "No plot is currently displayed.")
            return

        try:
            fig = self.plot_canvas.figure

            path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG Image", "*.png"),
                                                           ("JPEG Image", "*.jpg"),
                                                           ("PDF Document", "*.pdf")])
            if not path:
                return

            fig.savefig(path, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Export Plot", f"Plot successfully saved to {path}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to save plot: {str(e)}")

    def change_shading_color(self):
        """Open a color picker dialog and update the shading color variable."""
        color_code = colorchooser.askcolor(title="Choose Shading Color",
                                           initialcolor=self.custom_shade_color.get())
        if color_code and color_code[1]:
            self.custom_shade_color.set(color_code[1])
            if self.show_plot.get():
                self.calculate()

    def clear_result(self):
        """Clear the result display and plot"""
        self.result_label.config(text="Result: Ready.")
        if self.plot_canvas:
            self.plot_canvas.get_tk_widget().destroy()
            self.plot_canvas = None

    def clear_history_plot(self):
        """Clear the plot in the history tab."""
        if self.history_plot_canvas:
            self.history_plot_canvas.get_tk_widget().destroy()
            self.history_plot_canvas = None

    def update_inputs(self):
        """Update input fields based on selected distribution and range mode"""
        is_range = self.range_mode.get()
        dist = self.current_mode.get()

        params = self._get_param_definitions(dist, is_range)

        # Clear input fields and hide unused ones
        for i in range(4):
            lbl, ent, frame = self.input_widgets[i]
            frame.pack_forget()
            self.param_vars[i].set("")
            ent.config(state='normal')
            ent.unbind("<KeyRelease>")

            # Display and configure relevant inputs
        for i, (symbol, desc) in enumerate(params):
            lbl, ent, frame = self.input_widgets[i]

            base_desc = desc.split('(')[0].strip()
            lbl.config(text=f"{symbol} - {base_desc}:")

            update_func = lambda e, idx=i, s=symbol, d=desc: self._update_label_on_key(idx, s, d)
            ent.bind("<KeyRelease>", update_func)

            self._update_label_on_key(i, symbol, desc)

            frame.pack(fill="x")
            ToolTip(lbl, desc)
            ToolTip(ent, desc)

    def _update_label_on_key(self, i, symbol, desc):
        """Updates parameter label to show value or description."""
        self.clear_result()
        lbl, entry, frame = self.input_widgets[i]
        current_value = self.param_vars[i].get()

        base_desc = desc.split('(')[0].strip()

        if current_value:
            new_text = f"{symbol} = {current_value}"
        else:
            new_text = f"{symbol} - {base_desc}:"

        lbl.config(text=new_text)

    def _parse_inputs(self):
        """
        Parse and validate input values.
        Returns a list of (symbol, value) tuples.
        """
        parsed_params = []

        dist = self.current_mode.get()
        is_range = self.range_mode.get()
        param_defs = self._get_param_definitions(dist, is_range)

        for i, (lbl, ent, frame) in enumerate(self.input_widgets):
            if not frame.winfo_ismapped(): continue

            symbol = param_defs[i][0]
            txt = ent.get().strip()

            if not txt: raise ValueError(f"Missing value for parameter '{symbol}'")

            # Special handling for discrete distributions (must be integers for k/n/M/N)
            is_discrete = dist in ["Binomial", "Poisson", "Geometric", "Hypergeometric"]
            is_discrete_param = is_discrete and symbol in ['k', 'k₁', 'k₂', 'n', 'M', 'N']

            if is_discrete_param:
                try:
                    val = int(txt)
                except ValueError:
                    raise ValueError(f"'{symbol}' must be an integer.")
            else:
                try:
                    val = float(txt)
                except ValueError:
                    raise ValueError(f"'{symbol}' must be numeric.")

            parsed_params.append((symbol, val))

        return parsed_params

    def calculate(self):
        """Perform the selected distribution calculation"""
        dist = self.current_mode.get()
        is_range = self.range_mode.get()

        try:
            # parsed_params is a list of (symbol, value) tuples
            parsed_params = self._parse_inputs()

            # Reorder vals to match the calculation function's expected input: [X_val(s), P1, P2...]
            if is_range:
                # Assuming X-values are the two parameters with '1'/'2' subscripts
                x_values = [p[1] for p in parsed_params if '₁' in p[0] or '₂' in p[0] or 'x' in p[0] or 't' in p[0]]
                param_values = [p[1] for p in parsed_params if
                                not ('₁' in p[0] or '₂' in p[0] or 'x' in p[0] or 't' in p[0])]
                vals = x_values + param_values
            else:
                # X_val is the parameter without a parameter symbol name
                x_value = next(p[1] for p in parsed_params if p[0] in ['x', 'k', 't'])
                param_values = [p[1] for p in parsed_params if p[0] not in ['x', 'k', 't']]
                vals = [x_value] + param_values

            # --- Call the unified, SciPy-based calculation function ---
            result, dist_obj, is_discrete = calculate_distribution(dist, is_range, vals)

            if "Error:" in result:
                messagebox.showerror("Calculation Error", result)
                self.result_label.config(text=f"Error: {result}")
                return

            self.result_label.config(text=f"Result: {result}")

            self.history.add(dist, parsed_params, result)
            self.refresh_history()

            if self.show_plot.get():
                self.plot_main_distribution(dist, dist_obj, is_discrete, parsed_params)

            self._animate_success(self.calculate_button)

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.result_label.config(text=f"Error: {e}")

    def refresh_history(self):
        """Populate the Treeview with recent history"""
        for i in self.tree.get_children():
            self.tree.delete(i)

        for index, entry in enumerate(self.history.entries):
            t = entry["time"].strftime("%Y-%m-%d %H:%M:%S")
            p_formatted = ", ".join([f"{p[0]}={p[1]:.4g}" for p in entry["params"]])

            self.tree.insert("", "end", iid=index, values=(t, entry["distribution"], p_formatted, entry["result"]))

    def clear_history(self):
        """Clear all entries from history"""
        self.history.clear()
        self.refresh_history()
        self.clear_history_plot()

    def export_history(self):
        """Export history to a CSV file"""
        if not self.history.entries:
            messagebox.showinfo("Export", "No history to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Time", "Distribution", "Parameters", "Result"])
                for entry in self.history.entries:
                    p_formatted_for_csv = ", ".join([f"{p[0]}={p[1]:.4g}" for p in entry["params"]])
                    writer.writerow([entry["time"], entry["distribution"],
                                     p_formatted_for_csv, entry["result"]])
            messagebox.showinfo("Export", f"Successfully saved to {path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to save file: {str(e)}")


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DistributionCalculatorApp(root)
    root.mainloop()