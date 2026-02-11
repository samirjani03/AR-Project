import os
import subprocess
import uuid
import shutil
import trimesh  # <--- REPLACED open3d with trimesh
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECTS_DIR = os.path.join(BASE_DIR, 'projects')
STATIC_MODELS_DIR = os.path.join(BASE_DIR, 'static', 'models')

# Ensure directories exist
os.makedirs(PROJECTS_DIR, exist_ok=True)
os.makedirs(STATIC_MODELS_DIR, exist_ok=True)

# --- HELPER FUNCTIONS ---

def run_photogrammetry(project_id, images_path):
    """
    Runs the COLMAP pipeline. 
    Stops at 'mapper' (Sparse Point Cloud) for speed on laptops.
    """
    project_path = os.path.join(PROJECTS_DIR, project_id)
    database_path = os.path.join(project_path, 'database.db')
    sparse_path = os.path.join(project_path, 'sparse')
    os.makedirs(sparse_path, exist_ok=True)

    try:
        # 1. Feature Extraction
        print("--> [1/4] Extracting Features...")
        subprocess.run(['colmap', 'feature_extractor', '--database_path', database_path, '--image_path', images_path], check=True)

        # 2. Feature Matching
        print("--> [2/4] Matching Features...")
        subprocess.run(['colmap', 'exhaustive_matcher', '--database_path', database_path], check=True)

        # 3. Mapper (Sparse Reconstruction)
        print("--> [3/4] Creating 3D Points...")
        subprocess.run(['colmap', 'mapper', '--database_path', database_path, '--image_path', images_path, '--output_path', sparse_path], check=True)

        # 4. Convert Sparse Colmap Output to .PLY
        # This is required because Trimesh cannot read raw COLMAP .bin files easily.
        # We assume the model is in folder '0' inside sparse.
        model_0_path = os.path.join(sparse_path, '0') 
        ply_output_path = os.path.join(project_path, 'model.ply')
        
        print("--> [4/4] Converting to readable format...")
        subprocess.run([
            'colmap', 'model_converter', 
            '--input_path', model_0_path, 
            '--output_path', ply_output_path, 
            '--output_type', 'PLY'
        ], check=True)

        return ply_output_path

    except subprocess.CalledProcessError as e:
        print(f"COLMAP Error: {e}")
        return None
    except Exception as e:
        print(f"General Error: {e}")
        return None

def convert_ply_to_glb(ply_path, output_filename):
    """
    Converts .PLY to .GLB using Trimesh.
    """
    try:
        print(f"--> Converting {ply_path} to GLB...")
        
        # Load the mesh/point cloud
        # Trimesh is smart enough to detect if it's just points or a full mesh
        mesh = trimesh.load(ply_path)
        
        # Define output path in the static folder
        glb_path = os.path.join(STATIC_MODELS_DIR, output_filename)
        
        # Export the scene to GLB
        mesh.export(glb_path)
        
        print(f"--> Saved GLB to: {glb_path}")
        return output_filename
    except Exception as e:
        print(f"Conversion Error: {e}")
        return None

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'images' not in request.files:
        return "No images uploaded", 400
    
    files = request.files.getlist('images')
    if not files or files[0].filename == '':
        return "No selected files", 400

    # Create Project ID
    project_id = str(uuid.uuid4())
    current_project_dir = os.path.join(PROJECTS_DIR, project_id)
    images_dir = os.path.join(current_project_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)

    # Save Images
    for file in files:
        file.save(os.path.join(images_dir, file.filename))

    # Run Backend Processing
    ply_file = run_photogrammetry(project_id, images_dir)
    
    if ply_file:
        # Convert to AR format
        final_filename = f"{project_id}.glb"
        result_glb = convert_ply_to_glb(ply_file, final_filename)
        
        if result_glb:
            # Redirect user to the AR Viewer page
            return redirect(url_for('viewer', filename=final_filename))
    
    return "Processing Failed. Check server logs in VS Code terminal.", 500

@app.route('/viewer/<filename>')
def viewer(filename):
    return render_template('viewer.html', filename=filename)

if __name__ == '__main__':
    print("Starting AR Server...")
    app.run(debug=True, port=5000)