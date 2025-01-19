def export_plot():
    """Exports the current plot as an image file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
    )
    if file_path:
        fig.savefig(file_path)
        result_label.config(text="Plot exported successfully!", fg="green")

