import os
import shutil
import threading
import sys
from PIL import Image
from rembg import remove, new_session
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# ============================================================
# Configuration & Assets
# ============================================================

# Colors for "Pure White" Theme
COLOR_BG_MAIN = "#FFFFFF"       # Pure White
COLOR_BG_SIDEBAR = "#F5F5F7"    # Very light gray (Apple style)
COLOR_ACCENT = "#007AFF"        # Modern Blue
COLOR_TEXT = "#1D1D1F"          # Soft Black
COLOR_BORDER = "#E5E5E5"        # Subtle Border
COLOR_SUCCESS = "#34C759"       # Green
COLOR_DANGER = "#FF3B30"        # Red
COLOR_STATUS_BAR = "#FAFAFA"    # Bottom Bar

# Optional Drag-Drop Support
DRAG_DROP_AVAILABLE = False
DND_FILES = None
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DRAG_DROP_AVAILABLE = True
except ImportError:
    pass

# ============================================================
# Utility Functions
# ============================================================

def find_images_recursive(base_folder):
    """Recursively find all images."""
    exts = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')
    img_files = []
    for root, _, files in os.walk(base_folder):
        for f in files:
            if f.lower().endswith(exts):
                img_files.append(os.path.join(root, f))
    return sorted(img_files)

def clear_output_root(output_root):
    """Recreate output folder safely."""
    if os.path.exists(output_root):
        try:
            shutil.rmtree(output_root)
        except Exception as e:
            print(f"Error clearing output: {e}")
    os.makedirs(output_root, exist_ok=True)

# ============================================================
# Modern App Class
# ============================================================

bases = (ctk.CTk,)
if DRAG_DROP_AVAILABLE:
    bases += (TkinterDnD.DnDWrapper,)

class VpkBgApp(*bases):
    def __init__(self):
        super().__init__()

        # Setup Drag & Drop
        if DRAG_DROP_AVAILABLE:
            self.TkdndVersion = TkinterDnD._require(self)
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self.on_drop)

        # Global Appearance Settings
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # Window Setup
        self.title("VPK BG")
        self.geometry("1000x700")
        self.configure(fg_color=COLOR_BG_MAIN)

        # Variables
        self.folders = []
        self.folder_frames = []
        self.background_path = None
        self.cancel_event = threading.Event()

        # Output Path
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            self.output_root = os.path.join(desktop, "OUTPUT")
        except:
            self.output_root = os.path.join(os.getcwd(), "OUTPUT")

        # Load AI
        self.ai_loaded = False
        threading.Thread(target=self.load_ai_model, daemon=True).start()

        self.setup_modern_ui()

    def load_ai_model(self):
        """Loads AI in background so UI opens instantly."""
        try:
            self.session = new_session("u2netp")
            self.ai_loaded = True
            self.update_status("AI Engine Ready", COLOR_SUCCESS)
        except Exception as e:
            self.update_status(f"AI Failed: {e}", COLOR_DANGER)

    def setup_modern_ui(self):
        # Grid Layout: 2 Columns (Sidebar, Content), 2 Rows (Main, Status Bar)
        self.grid_columnconfigure(0, weight=0, minsize=300) # Sidebar fixed width
        self.grid_columnconfigure(1, weight=1)              # Content flexible
        self.grid_rowconfigure(0, weight=1)                 # Main Area
        self.grid_rowconfigure(1, weight=0, minsize=30)     # Status Bar

        # ==========================================
        # 1. LEFT SIDEBAR
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, fg_color=COLOR_BG_SIDEBAR, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1) # Push buttons to bottom if needed

        # Title
        title_lbl = ctk.CTkLabel(
            self.sidebar, 
            text="VPK", 
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color=COLOR_TEXT
        )
        title_lbl.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="w")

        # Section: Input Folders
        ctk.CTkLabel(self.sidebar, text="INPUT FOLDERS", font=ctk.CTkFont(size=12, weight="bold"), text_color="#888").grid(row=1, column=0, padx=20, pady=(10,5), sticky="w")
        
        self.folder_scroll = ctk.CTkScrollableFrame(
            self.sidebar, 
            height=150, 
            fg_color="white", 
            border_width=1, 
            border_color=COLOR_BORDER
        )
        self.folder_scroll.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        # Folder Buttons
        f_btn_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        f_btn_frame.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        ctk.CTkButton(f_btn_frame, text="+ Add", width=80, fg_color="#E0E0E0", text_color="black", hover_color="#D0D0D0", command=self.add_folder).pack(side="left", padx=(0,5))
        ctk.CTkButton(f_btn_frame, text="Clear", width=80, fg_color="white", border_width=1, border_color="#DDD", text_color=COLOR_DANGER, hover_color="#FFF0F0", command=self.clear_folders).pack(side="left")

        # Section: Background Image
        ctk.CTkLabel(self.sidebar, text="BACKGROUND IMAGE", font=ctk.CTkFont(size=12, weight="bold"), text_color="#888").grid(row=4, column=0, padx=20, pady=(20,5), sticky="w")
        
        self.bg_frame = ctk.CTkFrame(self.sidebar, fg_color="white", border_width=1, border_color=COLOR_BORDER)
        self.bg_frame.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        self.bg_frame.columnconfigure(0, weight=1)

        self.bg_label = ctk.CTkLabel(self.bg_frame, text="No image selected", text_color="#AAA", anchor="w")
        self.bg_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkButton(self.bg_frame, text="Browse", width=60, height=24, fg_color=COLOR_ACCENT, command=self.select_background).grid(row=0, column=1, padx=10, pady=10)

        # Action Area (Bottom of Sidebar)
        action_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        action_box.grid(row=6, column=0, padx=20, pady=30, sticky="ew")

        self.process_btn = ctk.CTkButton(
            action_box, 
            text="START PROCESSING", 
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLOR_ACCENT,
            corner_radius=8,
            command=self.start_processing
        )
        self.process_btn.pack(fill="x", pady=(0, 10))

        self.cancel_btn = ctk.CTkButton(
            action_box, 
            text="STOP", 
            height=40,
            fg_color="#F2F2F7",
            text_color=COLOR_DANGER,
            hover_color="#E5E5EA",
            state="disabled",
            command=self.cancel_processing
        )
        self.cancel_btn.pack(fill="x")

        # ==========================================
        # 2. RIGHT CONTENT AREA (LOGS)
        # ==========================================
        self.content = ctk.CTkFrame(self, fg_color=COLOR_BG_MAIN, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        # Header for logs
        log_header = ctk.CTkFrame(self.content, fg_color="transparent")
        log_header.grid(row=0, column=0, sticky="ew", pady=(10, 10))
        ctk.CTkLabel(log_header, text="Activity Log", font=ctk.CTkFont(size=18, weight="bold"), text_color=COLOR_TEXT).pack(side="left")
        
        if DRAG_DROP_AVAILABLE:
            ctk.CTkLabel(log_header, text="(Drag & Drop Folders Here)", font=ctk.CTkFont(size=12), text_color="#AAA").pack(side="right")

        # The Log Box
        self.log_text = ctk.CTkTextbox(
            self.content, 
            fg_color="#FAFAFA", 
            text_color="#333", 
            border_width=1, 
            border_color="#EEE",
            corner_radius=6,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.log_text.grid(row=1, column=0, sticky="nsew")
        self.log_text.insert("end", "Waiting for input...\n")

        # ==========================================
        # 3. MODERN STATUS BAR (BOTTOM)
        # ==========================================
        self.statusbar_frame = ctk.CTkFrame(self, height=35, fg_color=COLOR_STATUS_BAR, corner_radius=0)
        self.statusbar_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.statusbar_frame.grid_columnconfigure(1, weight=1) # Spacer

        # Status Icon/Text
        self.status_indicator = ctk.CTkLabel(self.statusbar_frame, text="●", font=("Arial", 16), text_color="#AAA")
        self.status_indicator.pack(side="left", padx=(15, 5))
        
        self.status_text = ctk.CTkLabel(self.statusbar_frame, text="Initializing...", font=("Arial", 12), text_color="#555")
        self.status_text.pack(side="left")

        # Progress Bar (Integrated into status bar on the right)
        self.progress = ctk.CTkProgressBar(self.statusbar_frame, width=200, height=8, progress_color=COLOR_SUCCESS)
        self.progress.pack(side="right", padx=20)
        self.progress.set(0)

    # ============================================================
    # Logic
    # ============================================================

    def log(self, msg, type="info"):
        """Logs message to the main text box."""
        prefix = "  "
        if type == "error": prefix = "❌ "
        elif type == "success": prefix = "✅ "
        
        self.log_text.insert("end", f"{prefix}{msg}\n")
        self.log_text.see("end")

    def update_status(self, text, color=None):
        """Updates the bottom status bar."""
        self.status_text.configure(text=text)
        if color:
            self.status_indicator.configure(text_color=color)

    def add_folder(self):
        f = filedialog.askdirectory(title="Select a Folder")
        if f and f not in self.folders:
            self.folders.append(f)
            self.refresh_folder_list()
            self.log(f"Added source: {os.path.basename(f)}")

    def refresh_folder_list(self):
        for w in self.folder_frames: w.destroy()
        self.folder_frames = []
        for i, f in enumerate(self.folders):
            # Create a nice row for each folder
            frm = ctk.CTkFrame(self.folder_scroll, fg_color="transparent")
            frm.pack(fill="x", pady=2)
            
            icon = ctk.CTkLabel(frm, text="📁", text_color="#888")
            icon.pack(side="left", padx=5)
            
            lbl = ctk.CTkLabel(frm, text=os.path.basename(f), text_color="#333", anchor="w")
            lbl.pack(side="left", fill="x", expand=True)
            self.folder_frames.append(frm)

    def clear_folders(self):
        self.folders = []
        self.refresh_folder_list()
        self.log("All folders cleared.")

    def select_background(self):
        p = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg *.webp")])
        if p:
            self.background_path = p
            name = os.path.basename(p)
            # Truncate if too long
            if len(name) > 25: name = name[:20] + "..."
            self.bg_label.configure(text=name, text_color="#333")
            self.log(f"Background set: {name}")

    def on_drop(self, event):
        paths = self.master.tk.splitlist(event.data)
        for p in paths:
            if os.path.isdir(p) and p not in self.folders:
                self.folders.append(p)
                self.refresh_folder_list()
                self.log(f"Dropped folder: {os.path.basename(p)}")
            elif os.path.isfile(p) and not self.background_path:
                self.background_path = p
                self.bg_label.configure(text=os.path.basename(p), text_color="#333")
                self.log(f"Dropped background: {os.path.basename(p)}")

    def start_processing(self):
        if not self.ai_loaded:
            messagebox.showwarning("Wait", "AI Model is still loading...")
            return

        if not self.folders or not self.background_path:
            messagebox.showerror("Missing Input", "Please select input folders and a background image.")
            return

        self.process_btn.configure(state="disabled", fg_color="#BBB")
        self.cancel_btn.configure(state="normal")
        self.cancel_event.clear()
        
        self.log("--- Starting Batch Process ---")
        self.update_status("Processing...", COLOR_ACCENT)
        threading.Thread(target=self.run_process, daemon=True).start()

    def cancel_processing(self):
        self.cancel_event.set()
        self.update_status("Stopping...", COLOR_DANGER)
        self.log("Stop signal sent. Finishing current image...", "error")

    def run_process(self):
        try:
            bg_pil = Image.open(self.background_path).convert("RGBA")
            clear_output_root(self.output_root)
            self.log(f"Output Directory: {self.output_root}")

            all_files = []
            for folder in self.folders:
                imgs = find_images_recursive(folder)
                for img in imgs:
                    all_files.append((img, folder))

            total = len(all_files)
            if total == 0:
                self.log("No images found in folders.", "error")
                self.reset_ui()
                return

            success_count = 0
            
            for i, (img_path, root_folder) in enumerate(all_files):
                if self.cancel_event.is_set(): break

                fname = os.path.basename(img_path)
                self.update_status(f"Processing: {fname}", COLOR_ACCENT)
                
                try:
                    # Path Logic
                    parent_of_root = os.path.dirname(root_folder)
                    rel_path = os.path.relpath(img_path, start=parent_of_root)
                    out_path = os.path.join(self.output_root, rel_path)
                    out_path = os.path.splitext(out_path)[0] + ".png"
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)

                    # AI Logic
                    img = Image.open(img_path).convert("RGBA")
                    cutout = remove(img, session=self.session)
                    
                    bg_resized = bg_pil.resize(img.size).convert("RGBA")
                    final_img = Image.alpha_composite(bg_resized, cutout)
                    
                    final_img.save(out_path, "PNG")
                    success_count += 1
                    self.log(f"Processed: {rel_path}", "success")

                except Exception as e:
                    self.log(f"Error {fname}: {e}", "error")

                self.progress.set((i + 1) / total)

            if not self.cancel_event.is_set():
                self.update_status("Completed Successfully", COLOR_SUCCESS)
                self.log(f"Done! {success_count}/{total} images processed.")
                messagebox.showinfo("Complete", f"Processed {success_count} images.")
            else:
                self.update_status("Cancelled", COLOR_DANGER)

        except Exception as e:
            self.log(f"Critical System Error: {e}", "error")
        finally:
            self.reset_ui()

    def reset_ui(self):
        self.process_btn.configure(state="normal", fg_color=COLOR_ACCENT)
        self.cancel_btn.configure(state="disabled")
        self.progress.set(0)
        if not self.cancel_event.is_set():
             self.update_status("Ready", COLOR_SUCCESS)

if __name__ == "__main__":
    app = VpkBgApp()
    app.mainloop()
