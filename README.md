# Fast MedSAM Frontend Documentation

## Overview

Fast MedSAM is a Streamlit-based web app for rapid medical image segmentation. It allows users to upload images, view original and segmented results, and download outcomes. The app interacts with a backend service for efficient segmentation. This documentation details the project's purpose, structure, methods, tools, and provides installation, usage, and contribution instructions.

## Quick Start

Find the deployed application at [FastMedSAM](https://fastmedsam.streamlit.app/). You can upload your medical images or choose from sample images to segment them. After segmentation, you can download the segmented image.

<p align="center">
  <img src="static/fastmedsam.gif"
  alt="Web Interface" align="middle" width="85%">
</p>

## Scope

The focus of this project is on inferencing 3D images. The input and output handling have been updated to work with NPZ files that contain `imgs` for stacked 2D images stored as numpy arrays and `gts` for ground truth data used to provide hints for segmentation. This way we can handle 3D images as a stack of 2D images without exaustively inputting boxes for each slice.

## Project Structure

The codebase follows an MVC structure, separating the concerns of the application. It is structured into two main classes: `View` and `Controller`.

### View Class

The `View` class is responsible for rendering the user interface components. It includes methods to display upload sections, sample image buttons, original and segmented images, and various control buttons.

### Controller Class

The `Controller` class manages the application logic and controls the flow of the application. It handles user interactions, communicates with the backend services for image segmentation, and updates the session state.

## Installation Instructions

### Running Locally

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/qniksefat/FastMedSAM-front.git
   cd FastMedSAM-front
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Set Up Backend Endpoint:** if you do not run the backend locally at `http://localhost:8080`.
   - Create a `.streamlit` directory in the root of the project.
   - Create a `secrets.toml` file in the `.streamlit` directory.
   - Add your backend endpoint to the `secrets.toml` file:
     ```toml
     ENDPOINT = "http://your-backend-endpoint" 
     ```

4. **Run the Application:**
   ```bash
   streamlit run streamlit_app.py
   ```

### Deployment

The easiest way to deploy your Streamlit UI app is to go to [Streamlit Sharing](https://share.streamlit.io/) and follow the instructions to deploy your app. You should first fork this repository to your GitHub account.

### Configuration

The application requires configuration for the backend endpoints. You have to provide the backend endpoint on your settings panel for the application.

## Usage

### Uploading an Image

1. **Upload Section:**
   - Users can upload an `.npz` file containing the medical image through the sidebar's "Upload Your Image" section.

2. **Sample Images:**
   - Alternatively, users can select from predefined sample images provided in the "Or Choose a Sample Image" section.

### Viewing Images

- **Original Image:**
  - The original image is displayed in the main interface. Users can use a slider to select different slices of the image for visualization.

- **Segmented Image:**
  - Once the image is segmented, the segmented image is displayed alongside the original image.

### Segmentation and Download

- **Segment Image:**
  - Users can start the segmentation process by clicking the "Segment Image" button in the sidebar.

- **Download Segmented Image:**
  - After segmentation, users can download the segmented image using the "Download Segmented Image" button.

### Refresh

- **Refresh Button:**
  - Users can reset the application to try another image by clicking the "Refresh" button in the sidebar.

## API Endpoints

### Segmentation Endpoint

- **URL:** `/segment/`
- **Method:** `GET`
- **Parameters:**
  - `filename`: The name of the file to be segmented.
- **Response:** Returns the segmented image as a binary stream.

### Upload Endpoint

- **URL:** `/upload/`
- **Method:** `POST`
- **Files:**
  - `file`: The image file to be uploaded.
- **Response:** Returns a JSON object containing a unique filename for the uploaded image.

## Methods

### Development Process

The development process involved designing a user-friendly interface using Streamlit, integrating with backend services for image segmentation, and providing visualization tools for displaying original and segmented images.

### Tools and Technologies

- **Streamlit:** Used for building the web interface.
- **Matplotlib:** For creating visualizations and rendering 2D images.
- **Requests:** For making HTTP requests to backend services.

### Future Work

- Streamlit does support inputting point cursor etc., so in the future, I can handle input points and one 2D image.
- Adding more advanced visualization tools, such as 3D rendering by plotly or vtk.
- Implementing user authentication.
