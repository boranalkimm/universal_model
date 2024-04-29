from flask import Flask, request, jsonify, send_from_directory, url_for
import os
import subprocess

app = Flask(__name__)

# Define the directory to store uploaded files and segmented volumes
UPLOADS_DIR = os.path.join(app.root_path, 'uploads')
SEGMENTED_VOLUMES_DIR = os.path.join(app.root_path, 'static', 'segmented_volumes')
SEGMENTED_IMAGES_DIR = os.path.join(app.root_path, 'static', 'segmented_images')

@app.route('/segment', methods=['POST'])
def segment_nii():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    if 'organ_name' not in request.form:
        return jsonify({'error': 'Organ name not specified'})

    # Get the uploaded file
    file = request.files['file']
    organ_name = request.form['organ_name']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded file
    if file:
        filename = file.filename
        upload_path = os.path.join(UPLOADS_DIR, filename)
        file.save(upload_path)

        # Perform inference to generate the segmented .nii.gz file
        filename_parts = filename.split('.')
        base_filename = filename_parts[0]
        segmented_nii_gz_filename = f"{base_filename}_result.nii.gz"


        # Your inference logic to generate segmented .nii.gz file goes here

        # Move the segmented .nii.gz file to the segmented volumes directory
        segmented_nii_gz_path = os.path.join(SEGMENTED_VOLUMES_DIR, segmented_nii_gz_filename)
        # Move or save the segmented .nii.gz file using your inference logic

        # Convert segmented .nii.gz file to .png file
        segmented_png_filename = f"{base_filename}_image_segmented.png"
        original_png_filename = f"{base_filename}_image_original.png"
        # Your logic to convert segmented .nii.gz to .png goes here

        # Construct the URL for the segmented .nii.gz file
        segmented_nii_gz_url = url_for('static', filename=f'segmented_volumes/{segmented_nii_gz_filename}', _external=True)

        # Construct the URL for the segmented .png file
        segmented_png_url = url_for('static', filename=f'segmented_images/{segmented_png_filename}', _external=True)
        original_png_url = url_for('static', filename=f'original_images/{original_png_filename}', _external=True)

        # Return the URLs to the segmented .nii.gz file and the segmented .png file
        return jsonify({
            'segmented_nii_gz_url': segmented_nii_gz_url,
            'segmented_png_url': segmented_png_url,
            'original_png_url': original_png_url,
            'organ_name': organ_name
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
 
