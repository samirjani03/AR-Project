Description:
A web app that does just 2 cool things:

💡 1. Take a video of an object (like a glass of water)
👉 and convert it into a 3D model (formats: .obj, .fbx, .stl, etc.)

📦 2. Generate a QR Code for that 3D model
👉 So anyone can scan and view or download the 3D model.

# 🎥➡️🔺 3D Model Generator from Video + QR Code Viewer Web App

This is a full-stack web application that allows users to upload a video of any object, automatically convert it into a 3D model using photogrammetry (COLMAP pipeline), and then view/download it via a generated QR code. The app also supports AR viewing through `<model-viewer>` and WebXR!

---

## ✨ Features

- Upload a short video of any object
- Extract frames and generate a 3D model using COLMAP
- Convert model into `.obj` or `.stl` format
- Generate QR code to download/view model
- View model interactively in browser
- Optional AR mode support

---

## 🧰 Tech Stack

| Layer       | Tech Used                  |
|-------------|----------------------------|
| Frontend    | React, Model-Viewer, Three.js, qrcode.react |
| Backend     | Node.js, Express, Multer, Python (child_process) |
| 3D Engine   | COLMAP, OpenCV, Blender (optional) |
| Deployment  | Vercel (Frontend), Railway/Render (Backend) |
| QR Tool     | qrcode.react, qrcode-generator |
| Optional AR | 8thWall / WebXR / Scene Viewer (Android) |

---

## 🔧 Folder Structure

```bash
AR-3DModel-QR-WebApp/
├── client/          # React frontend
├── server/          # Node.js + Express backend
├── scripts/         # Python scripts for video to 3D
├── uploads/         # Temporary video uploads
├── models_output/   # Output 3D models
