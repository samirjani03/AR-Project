
# 📸 Image-to-3D Reconstruction (COLMAP + Flask + Trimesh)

A full-stack photogrammetry web application that converts multiple images of an object (taken from different angles) into a downloadable 3D model.

This project uses:

- 🧠 COLMAP (Photogrammetry Engine)
- 🐍 Flask (Backend Web Server)
- 🔁 Trimesh (3D format conversion)
- 🌐 HTML Templates (Frontend)
- 📦 Output: `.glb` 3D model for AR / Web viewing

---

# 🚀 How It Works

1. User uploads ~20 images of an object from different angles
2. Backend runs COLMAP pipeline:
   - Feature Extraction
   - Feature Matching
   - Sparse Reconstruction
3. Output `.bin` files are converted to `.ply`
4. `.ply` is converted to `.glb`
5. User can view or download 3D model

---

# ⚙️ Requirements

Before starting, install:

- Python 3.9+
- Git
- COLMAP (Windows installation required)
- Visual Studio C++ Redistributables (for COLMAP)

---

# 🦙 Step 1 — Install COLMAP (Windows)

### 1️⃣ Download COLMAP

Go to:

https://github.com/colmap/colmap/releases

Download:

```

COLMAP-x.x-windows-cuda.zip

```

Extract it somewhere permanent, for example:

```

C:\COLMAP

```

---

### 2️⃣ Add COLMAP to System PATH

1. Press **Windows Key**
2. Search: `Environment Variables`
3. Click **Edit the system environment variables**
4. Click **Environment Variables**
5. Under *System Variables*, select **Path**
6. Click **Edit**
7. Click **New**
8. Add:

```

C:\COLMAP\bin

````

9. Click OK on all windows

---

### 3️⃣ Verify Installation

Open new CMD:

```bash
colmap
````

If help menu appears → installation successful.

---

# 🐍 Step 2 — Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/image-to-3d.git
cd image-to-3d
```

---

# 🐍 Step 3 — Setup Python Environment

### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

---

### Install dependencies

```bash
pip install -r requirements.txt
```

Dependencies include 

---

# ▶️ Step 4 — Run Application

```bash
python app.py
```

Server will start at:

```
http://127.0.0.1:5000
```

---

# 🧠 Backend Pipeline Details

The backend logic is defined in 

It runs:

1. `feature_extractor`
2. `exhaustive_matcher`
3. `mapper`
4. `model_converter`

Then converts `.ply → .glb` using Trimesh.

---

# 📦 Output

Generated models are stored in:

```
static/models/
```

Each project is stored inside:

```
projects/<project_id>/
```

---

# ⚠️ Notes for Better Results

* Use 20–40 high-resolution images
* Ensure good lighting
* Avoid motion blur
* Capture 360° coverage
* Maintain consistent distance from object

---

# 🛠 Common Issues

### ❌ 'colmap' is not recognized

Fix:

* Ensure correct PATH setup
* Restart terminal after editing environment variables

---

### ❌ CUDA errors

If you don’t have GPU:

Download non-CUDA version of COLMAP.

---

### ❌ Processing Failed

Check terminal logs in VS Code.
COLMAP errors will appear there.

---