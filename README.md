# Fast MedSAM

## Description
Fast MedSAM is a web application designed for the quick and efficient segmentation of medical images. Utilizing a user-friendly interface, it allows users to upload their own images or choose from sample images, apply segmentation, and download the results. The app connects to a FastAPI backend for processing the segmentation tasks.

## Motivation
The Fast MedSAM project was developed to address a coding task from the UHN AI Hub, focusing on enhancing AI efficiency and accessibility for clinicians. Medical image segmentation is vital for diagnosis and treatment planning. My goal was to optimize the LiteMedSAM model for faster inference while maintaining accuracy and to create a user-friendly interface for easy testing of medical images.

## Quick Start
To quickly get started with Fast MedSAM, visit the deployed app at [fastmedsam.streamlit.app](https://fastmedsam.streamlit.app).

## Usage
1. **Upload Your Image**: Use the sidebar to upload your own image in JPG, PNG, or JPEG format.
2. **Choose a Sample Image**: Alternatively, select a sample image from the provided options.
3. **View Original Image**: The original image will be displayed on the left side of the screen.
4. **Segmentation Parameters**: Enter a candidate label in the sidebar for segmentation.
5. **Segment Image**: Click the "Segment Image" button to start the segmentation process.
6. **View Segmented Image**: The segmented image will be displayed on the right side of the screen.
7. **Download Result**: Use the download button in the sidebar to save the segmented image.
8. **Refresh**: Click the refresh button to start over with a new image.
