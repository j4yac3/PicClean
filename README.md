# 📸PicClean

**A lightning-fast, modern, and robust Windows desktop application to declutter your image library.**  
PicClean automatically scans your folders for duplicate images and blurry photos, allowing you to easily sort them out and free up storage space.

---

## ✨ Features

- 🔍 **Smart Duplicate Detection:** Uses perceptual hashing (pHash) to find identical or visually similar images, even if they have been slightly compressed or resized (e.g., WhatsApp images).
- 📉 **Blur Detection:** Utilizes OpenCV (Laplacian variance) to automatically identify blurry and out-of-focus photos.
- 🚀 **Optimized for Low-End PCs:** Drastically reduces RAM usage through on-the-fly thumbnail generation and aggressive Garbage Collection. Scans thousands of images without crashing.
- ⚡ **Asynchronous & Non-Blocking:** Built with Python `asyncio` and `threading`. The beautiful UI stays perfectly responsive while doing heavy lifting in the background.
- 🌍 **Multi-Language Support:** Instantly switch between English, German, French, Spanish, Italian, and Russian with a single click (no restart required).
- 🌗 **Light & Dark Mode:** Toggle between beautifully crafted light and dark themes.
- 🛡️ **Safe File Handling:** Images are **never** deleted. They are safely moved into a dedicated `_Aussortiert_` (Sorted Out) folder, ensuring zero data loss.

---

## 📥 Download & Usage (For standard users)

You don't need to know how to code to use PicClean! 

1. Go to the **[Releases](../../releases)** page.
2. Download the latest `PicClean.zip` or `PicClean.exe`.
3. Extract it and double-click the `.exe` to start the app. No installation required!
4. Click **Scan Folder**, choose your image directory, and wait for the magic to happen.
5. Click on any detected image in the list to view it in the **Preview window**.
6. Choose to move the duplicates/blurry images to a subfolder, or click **Keep** to leave them untouched.

---

## 💻 For Developers (Build it yourself)

If you want to run the code from source or modify it, follow these steps:

### Prerequisites
Make sure you have Python 3.12+ installed.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/j4yac3/PicClean.git
   cd PicClean
