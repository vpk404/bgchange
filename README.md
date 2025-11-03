# GPU-Optimized Batch Background Replacer

A small, high-performance Python script that removes backgrounds from images in a folder and composites them onto a selected background image. Outputs PNG files and avoids overwriting existing files by adding suffixes when needed.

---

## Features
- Supports JPG, JPEG, PNG, BMP, GIF (static only), TIFF
- GPU-accelerated inference if `onnxruntime-gpu` is installed
- Skips animated GIFs automatically
- Case-insensitive file detection
- Prevents overwrites by appending `_1`, `_2`, etc. to output filenames
- Logs saved filenames and counts unique outputs

---

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Usage](#usage)
4. [How it works (brief)](#how-it-works-brief)
5. [Example output structure](#example-output-structure)
6. [Troubleshooting](#troubleshooting)
7. [Contributing](#contributing)
8. [License](#license)

---

## Requirements
- Python 3.8+
- The script dependencies listed in `requirements.txt`:

```
pillow
rembg
onnxruntime-gpu
tqdm
```

> Note: `tkinter` is used for the file picker and is usually included with the system Python. On some Linux distributions you may need to install `python3-tk` separately.

---

## Installation
1. Clone the repository:

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS / Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

If you do not have a GPU or prefer CPU-only, replace `onnxruntime-gpu` with `onnxruntime` in `requirements.txt`.

---

## Usage
1. Put the `bg.py` script into the folder containing the images you want to process (or run it from that folder).
2. Run the script:

```bash
python bg.py
```

3. A file picker window will open. Choose the background image you want to composite onto all found images.
4. The script will scan the current folder for supported images and process them one by one. Outputs are saved as PNG files in an `output/` folder located next to the script.

**Notes:**
- Animated GIFs are detected and skipped.
- If an output filename already exists, the script will append `_1`, `_2`, etc., to avoid overwriting.

---

## How it works (brief)
1. The script finds images in the script's directory using case-insensitive extension matching.
2. Each static image is opened and passed through `rembg.remove()` which removes the background (uses ONNX runtime, GPU if available).
3. The selected background image is resized to match the source image size.
4. The background and foreground (with transparent alpha) are alpha-composited and saved as PNG.

---

## Example output structure
```
your-repo/
â”œâ”€ bg.py
â”œâ”€ requirements.txt
â”œâ”€ README.md
â”œâ”€ sample.jpg
â”œâ”€ sample2.png
â””â”€ output/
   â”œâ”€ sample.png
   â””â”€ sample2.png
```

---

## Troubleshooting
- **No images found**: Make sure the script is run from the folder that contains the images or move the script into the images folder.
- **`tkinter` missing on Linux**: Install with your package manager, e.g. `sudo apt install python3-tk`.
- **ONNX runtime errors**: If you installed `onnxruntime-gpu` but lack a compatible GPU or drivers, either install `onnxruntime` (CPU) or fix GPU drivers/CUDA toolkit.
- **Permission errors saving files**: Ensure you have write permissions in the script folder.

---

## Contributing
Contributions welcome! Open an issue or a PR with bugfixes, enhancements, or improvements to documentation.

---

## License
Specify a license (e.g., MIT) or keep it as you prefer. Example:

```
MIT License
```

---

*Made with â¤ï¸ â€” feel free to ask for badges, a short demo GIF, or version-pinned requirements.*
