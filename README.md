# 🎨 VPK Background Changer (GUI)

> **A modern, stunning, and batch-capable background Changer tool powered by AI.**  
> *Drop your folders, pick a background, and let the magic happen.*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)](https://github.com/vpk404/bgchange)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## ✨ Features

- **🚀 AI-Powered Changer**: Uses `rembg` (U^2-Net) for precise background cutting.
- **🖥️ Modern GUI**: Built with `CustomTkinter` for a clean, dark/light mode compatible interface.
- **📂 Batch Processing**: Process thousands of images from multiple folders at once.
- **🖐️ Drag & Drop**: Simply drag folders or background images directly into the app.
- **🔄 Smart Resizing**: Automatically resizes the background to fit your subject.
- **⚡ GPU Support**: Supports NVIDIA GPU acceleration (via ONNX) for blazing speeds.

---

## 📸 Screenshots

<img width="1004" height="696" alt="Screenshot 2026-01-06 175352" src="https://github.com/user-attachments/assets/163d6848-08b4-4ee2-bf76-4d430f9ebb7a" />


---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/vpk404/bgchange.git
cd bgchange
```

### 2. Set Up Environment
It's recommended to use a virtual environment:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
> **Note for GPU Users:** If you have an NVIDIA GPU, ensure you have installed the CUDA toolkit compatible with `onnxruntime-gpu`.

---

## 🚀 How to Use

1. **Run the App**:
   ```bash
   python bg.py
   ```
2. **Add Input Folders**:
   - Click **`+ Add`** to select folders containing your images.
   - Or **Drag & Drop** folders directly into the "Input Folders" list.
3. **Select Background**:
   - Click **`Browse`** to choose the new background image.
   - Or **Drag & Drop** an image file into the app.
4. **Start Magic**:
   - Click **`START PROCESSING`**.
   - Watch the progress bar as your images are transformed!
5. **Find Results**:
   - All processed images are saved in a new folder named `OUTPUT` on your Desktop (or current directory).

---

## 🧩 Requirements

- **Python 3.8+**
- **Libraries**:
  - `customtkinter` (UI)
  - `tkinterdnd2` (Drag & Drop)
  - `rembg` (AI Engine)
  - `pillow` (Image Processing)
  - `onnxruntime` or `onnxruntime-gpu`

---

## 🤝 Contributing

Got an idea? Found a bug?  
Feel free to [open an issue](https://github.com/vpk404/bgchange/issues) or submit a pull request!

---

<div align="center">

**Made with ❤️ by [VPK404](https://github.com/vpk404)**

</div>
