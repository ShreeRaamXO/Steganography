import tkinter as tk
from tkinter import filedialog, messagebox
from funcs import encode_image, decode_image

# Global variable to store the uploaded image path
uploaded_image = None

def main_gui():
    def upload_image():
        global uploaded_image
        uploaded_image = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if uploaded_image:
            messagebox.showinfo("Image Uploaded", f"Image loaded successfully: {uploaded_image}")
            show_options()

    def show_options():
        # Clear initial layout
        for widget in root.winfo_children():
            widget.destroy()

        # Show options
        tk.Button(root, text="Embed Data", command=embed_interface).pack(pady=10)
        tk.Button(root, text="Extract Data", command=extract_interface).pack(pady=10)
        tk.Button(root, text="Back", command=reset_gui).pack(pady=10)

    def embed_interface():
        def embed_action():
            try:
                secret_data = data_entry.get()
                output_file = filedialog.asksaveasfilename(
                    filetypes=[("PNG Files", "*.png")], defaultextension=".png"
                )
                if not output_file or not secret_data:
                    raise ValueError("Missing data or output file!")
                encode_image(uploaded_image, secret_data, output_file)
                messagebox.showinfo("Success", f"Data encoded successfully in {output_file}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Embed interface
        for widget in root.winfo_children():
            widget.destroy()
        tk.Label(root, text="Enter Data to Embed:").pack(pady=5)
        data_entry = tk.Entry(root, width=50)
        data_entry.pack(pady=5)
        tk.Button(root, text="Embed Data", command=embed_action).pack(pady=10)
        tk.Button(root, text="Back", command=reset_gui).pack(pady=10)

    def extract_interface():
        def extract_action():
            try:
                hidden_data = decode_image(uploaded_image)
                result_label.config(text=f"Hidden Data: {hidden_data}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Extract interface
        for widget in root.winfo_children():
            widget.destroy()
        tk.Label(root, text="Decoded Data:").pack(pady=5)
        result_label = tk.Label(root, text="", wraplength=400, justify="center")
        result_label.pack(pady=5)
        tk.Button(root, text="Extract Data", command=extract_action).pack(pady=10)
        tk.Button(root, text="Back", command=reset_gui).pack(pady=10)

    def reset_gui():
        for widget in root.winfo_children():
            widget.destroy()
        tk.Button(root, text="Upload Image", command=upload_image).pack(pady=20)

    # Initialize GUI
    root = tk.Tk()
    root.title("Steganography Tool")
    root.geometry("500x400")  # Set window size
    reset_gui()
    root.mainloop()


if __name__ == "__main__":
    main_gui()
#idhi tk , lawda headache idhi 