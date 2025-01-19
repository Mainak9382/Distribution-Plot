import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.stats import mode
import seaborn as sns  # For KDE plotting


# Create the main application window
root = tk.Tk()
root.title("Distribution Simulator")
root.geometry("1200x750")
root.configure(bg="#f8f8f8")

# Heading Frame for the project title
heading_frame = tk.Frame(root, bg="#283593")
heading_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

# Project Title Label
title_label = tk.Label(
    heading_frame,
    text="Distribution Simulator Project",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#283593"
)
title_label.pack(pady=(10, 0))

# Subtitle Label with Author's Name
author_label = tk.Label(
    heading_frame,
    text="by Mainak",
    font=("Arial", 14, "italic"),
    fg="white",
    bg="#283593"
)
author_label.pack(pady=(0, 10))


def update_parameters(event):
    """Updates parameter input fields based on the selected distribution."""
    dist = distribution_var.get()
    if dist == "Binomial":
        param1_label.config(text="n (trials)")
        param2_label.config(text="p (probability)")
        param1_entry.grid()
        param2_entry.grid()
        param2_label.grid()
    elif dist == "Poisson":
        param1_label.config(text="λ (lambda)")
        param2_entry.grid_remove()
        param2_label.grid_remove()
    elif dist == "Geometric":
        param1_label.config(text="p (probability)")
        param2_entry.grid_remove()
        param2_label.grid_remove()
    elif dist == "Uniform":
        param1_label.config(text="Low")
        param2_label.config(text="High")
        param1_entry.grid()
        param2_entry.grid()
        param2_label.grid()
    elif dist == "Normal":
        param1_label.config(text="Mean (μ)")
        param2_label.config(text="Standard Deviation (σ)")
        param1_entry.grid()
        param2_entry.grid()
        param2_label.grid()
    elif dist == "Exponential":
        param1_label.config(text="Scale (1/λ)")
        param2_entry.grid_remove()
        param2_label.grid_remove()


def plot_distribution():
    """Plots the selected distribution with the chosen visualization type."""
    ax.clear()
    dist = distribution_var.get()
    plot_type = plot_type_var.get()
    try:
        param1 = float(param1_entry.get())
        param2 = float(param2_entry.get()) if param2_entry.winfo_ismapped() else None
        size = int(size_entry.get())
    except ValueError:
        result_label.config(text="Please enter valid numeric parameters.", fg="red")
        return

    # Generate data for each distribution
    if dist == "Binomial":
        data = np.random.binomial(n=int(param1), p=param2, size=size)
    elif dist == "Poisson":
        data = np.random.poisson(lam=param1, size=size)
    elif dist == "Geometric":
        data = np.random.geometric(p=param1, size=size)
    elif dist == "Uniform":
        data = np.random.uniform(low=param1, high=param2, size=size)
    elif dist == "Normal":
        data = np.random.normal(loc=param1, scale=param2, size=size)
    elif dist == "Exponential":
        data = np.random.exponential(scale=param1, size=size)
    else:
        result_label.config(text="Unknown distribution selected.", fg="red")
        return

    # Plot based on selected type
    if plot_type == "Histogram":
        ax.hist(data, bins=30, color='skyblue', edgecolor='black')
    elif plot_type == "CDF":
        sorted_data = np.sort(data)
        cdf = np.arange(len(sorted_data)) / float(len(sorted_data))
        ax.plot(sorted_data, cdf, color='blue', label="CDF")
        ax.legend()
    elif plot_type == "KDE":
        sns.kdeplot(data, ax=ax, fill=True, color="green", alpha=0.5, label="KDE")
        ax.legend()

    ax.set_title(f"{dist} Distribution ({plot_type})")
    canvas.draw()
    result_label.config(text="Plot generated successfully!", fg="green")

    # Calculate statistics
    mean_val = np.mean(data)
    median_val = np.median(data)
    mode_val = mode(data).mode[0]
    variance_val = np.var(data)
    std_dev_val = np.std(data)

    # Update statistics labels
    mean_label.config(text=f"Mean: {mean_val:.2f}")
    median_label.config(text=f"Median: {median_val:.2f}")
    mode_label.config(text=f"Mode: {mode_val:.2f}")
    variance_label.config(text=f"Variance: {variance_val:.2f}")
    std_dev_label.config(text=f"Standard Deviation: {std_dev_val:.2f}")


def export_plot():
    """Exports the current plot as an image file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
    )
    if file_path:
        fig.savefig(file_path)
        result_label.config(text="Plot exported successfully!", fg="green")


# Main layout frames
plot_frame = tk.Frame(root, bg="#f8f8f8")
plot_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

input_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="solid")
input_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Configure column and row weights
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

# Left frame: Matplotlib figure setup
fig, ax = plt.subplots(figsize=(6, 5))
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Right frame: Input fields and controls
distribution_var = tk.StringVar(value="Binomial")
distribution_label = tk.Label(input_frame, text="Select Distribution:", font=("Arial", 14), bg="#ffffff")
distribution_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
distribution_dropdown = ttk.Combobox(input_frame, textvariable=distribution_var, state="readonly", font=("Arial", 12))
distribution_dropdown['values'] = ("Binomial", "Poisson", "Geometric", "Uniform", "Normal", "Exponential")
distribution_dropdown.bind("<<ComboboxSelected>>", update_parameters)
distribution_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Parameter inputs
param1_label = tk.Label(input_frame, text="Parameter 1:", font=("Arial", 14), bg="#ffffff")
param1_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
param1_entry = tk.Entry(input_frame, font=("Arial", 12))
param1_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

param2_label = tk.Label(input_frame, text="Parameter 2:", font=("Arial", 14), bg="#ffffff")
param2_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
param2_entry = tk.Entry(input_frame, font=("Arial", 12))
param2_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

size_label = tk.Label(input_frame, text="Sample Size:", font=("Arial", 14), bg="#ffffff")
size_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
size_entry = tk.Entry(input_frame, font=("Arial", 12))
size_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

plot_type_var = tk.StringVar(value="Histogram")
plot_type_label = tk.Label(input_frame, text="Plot Type:", font=("Arial", 14), bg="#ffffff")
plot_type_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
plot_type_dropdown = ttk.Combobox(input_frame, textvariable=plot_type_var, state="readonly", font=("Arial", 12))
plot_type_dropdown['values'] = ("Histogram", "CDF", "KDE")
plot_type_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

result_label = tk.Label(input_frame, text="", font=("Arial", 12), bg="#ffffff")
result_label.grid(row=5, column=0, columnspan=2, pady=5)

plot_button = tk.Button(input_frame, text="Plot Distribution", command=plot_distribution, font=("Arial", 14), bg="#4CAF50", fg="white")
plot_button.grid(row=6, column=0, columnspan=2, pady=20, sticky="ew")

export_button = tk.Button(input_frame, text="Export Plot", command=export_plot, font=("Arial", 14), bg="#2196F3", fg="white")
export_button.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

# Statistics labels
mean_label = tk.Label(input_frame, text="Mean: N/A", font=("Arial", 12), bg="#ffffff")
mean_label.grid(row=8, column=0, columnspan=2, sticky="w", padx=5, pady=5)

median_label = tk.Label(input_frame, text="Median: N/A", font=("Arial", 12), bg="#ffffff")
median_label.grid(row=9, column=0, columnspan=2, sticky="w", padx=5, pady=5)

mode_label = tk.Label(input_frame, text="Mode: N/A", font=("Arial", 12), bg="#ffffff")
mode_label.grid(row=10, column=0, columnspan=2, sticky="w", padx=5, pady=5)

variance_label = tk.Label(input_frame, text="Variance: N/A", font=("Arial", 12), bg="#ffffff")
variance_label.grid(row=11, column=0, columnspan=2, sticky="w", padx=5, pady=5)

std_dev_label = tk.Label(input_frame, text="Standard Deviation: N/A", font=("Arial", 12), bg="#ffffff")
std_dev_label.grid(row=12, column=0, columnspan=2, sticky="w", padx=5, pady=5)

update_parameters(None)
root.mainloop()
