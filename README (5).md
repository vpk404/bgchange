# ⚡ GPU Batch Background Replacer (CPU Default)

This project helps you remove image backgrounds in bulk and replace them with a new background image. It’s simple, fast, and works by default on CPU. You can enable GPU support for faster results if your system supports it.

**GitHub Repo:** [https://github.com/vpk404/e-com-automation.git](https://github.com/vpk404/e-com-automation.git)

---

## ✨ Features
- Works with JPG, PNG, BMP, GIF (not animated), and TIFF images.
- Runs on CPU by default (no GPU required).
- Can use GPU with ONNX for faster performance.
- Avoids overwriting files by renaming them (`_1`, `_2`, etc.).
- Simple folder-based workflow.
- Logs and counts all processed images.

---

## 🧩 Requirements
- Python 3.8 or higher  
- Dependencies (already in `requirements.txt`):
  ```
  pillow
  rembg
  onnxruntime
  tqdm
  ```
- `tkinter` (used for selecting background image – usually built-in with Python)

---

## ⚙️ Installation Steps

1. **Clone this repository:**
   ```bash
   git clone https://github.com/vpk404/e-com-automation.git
   cd e-com-automation
   ```

2. **(Optional) Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install all required libraries (CPU version):**
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚡ Want to Use GPU?

If you have a GPU and want to speed up background removal:

1. Open `requirements.txt` and replace this line:
   ```
   onnxruntime
   ```
   with:
   ```
   onnxruntime-gpu
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure your system has:
   - A compatible NVIDIA GPU  
   - CUDA Toolkit and cuDNN installed  
   - Updated GPU drivers  

If GPU is detected, `rembg` will automatically use it.

---

## 🚀 How to Use

1. Place your images and the `bg.py` script in the same folder.  
2. Run the script:
   ```bash
   python bg.py
   ```
3. A file picker will appear – select the background image you want.  
4. The script will:  
   - Scan your folder for supported images  
   - Remove their backgrounds  
   - Add your selected background  
   - Save all results inside a new `output` folder  

---

## 📂 Example Folder Structure
```
e-com-automation/
├─ bg.py
├─ requirements.txt
├─ README.md
├─ photo1.jpg
├─ photo2.png
└─ output/
   ├─ photo1.png
   └─ photo2.png
```

---

## 🧠 How It Works (Simple)
1. The script finds all image files in the same folder.  
2. It removes the background using `rembg` (CPU by default, GPU if enabled).  
3. The chosen background image is resized to match each photo.  
4. The final combined image is saved in the `output/` folder.

---

## ❗ Common Issues
- **No images found:** Make sure your images are in the same folder as `bg.py`.  
- **`tkinter` missing:** On Linux, install it using `sudo apt install python3-tk`.  
- **ONNX errors:** If GPU drivers are missing, switch back to CPU by using `onnxruntime`.  
- **Permission denied:** Run the script from a folder you have write access to.

---

## 🤝 Contributing
Pull requests and suggestions are welcome! You can fork the repo, make changes, and submit a PR.

---

## 📄 License
This project is under the **MIT License** – you’re free to use, modify, and share it.

---

Made with ❤️ by [VPK404](https://github.com/vpk404)
