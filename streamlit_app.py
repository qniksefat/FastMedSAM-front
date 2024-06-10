import streamlit as st
from PIL import Image
from io import BytesIO
import numpy as np
import requests
import os
from matplotlib import pyplot as plt

ENDPOINT = os.environ.get("ENDPOINT", "0.0.0.0:8080")

SEGMENT_ENDPOINT = f"http://{ENDPOINT}/segment/"
UPLOAD_ENDPOINT = f"http://{ENDPOINT}/upload/"


class View:
    def __init__(self):
        st.set_page_config(page_title="Fast MedSAM", page_icon="✂️", layout="wide")
        st.title("Fast Segmentation of Medical Images")

    def show_upload_section(self):
        st.sidebar.title("Upload Your Image")
        file = st.sidebar.file_uploader("Choose an npz file", label_visibility="collapsed", type=['npz'])
        return file

    def show_samples_section(self):
        st.sidebar.title("Or Choose a Sample Image")
        col1, col2 = st.sidebar.columns(2)
        with st.sidebar:
            with col1:
                if st.button("Sample 1"):
                    path = "static/sample1.npz"
                    return BytesIO(open(path, "rb").read())
            with col2:
                if st.button("Sample 2"):
                    path = "static/sample2.npz"
                    return BytesIO(open(path, "rb").read())
        return None

    def show_original_image(self, left_column, original_image):
        with left_column:
            st.subheader("Original Image")
            idx = st.session_state.slice_index if 'slice_index' in st.session_state else len(original_image['imgs']) // 2
            fig = self.visualize_overlay(original_image['imgs'], 
                                         None, None, idx=idx, alpha=0.6)
            st.pyplot(fig)
    
    def show_mask(self, mask, mask_color=None, alpha=0.6):
        if mask_color is not None:
            color = np.concatenate([mask_color, np.array([alpha])], axis=0)
        else:
            color = np.array([251 / 255, 252 / 255, 30 / 255, alpha])
        h, w = mask.shape[-2:]
        mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
        return mask_image
    
    def visualize_overlay(self, img_3D, gt_3D=None, seg_3D=None, idx=0, alpha=0.6):
        # Check if the image is grayscale and convert to RGB
        if img_3D[idx].ndim == 2:
            img_3D_rgb = np.stack((img_3D[idx],) * 3, axis=-1)
        else:
            img_3D_rgb = img_3D[idx]
        # Normalize the image to 0-255 range
        img_3D_rgb = (img_3D_rgb * 255).astype(np.uint8)
        # Resize the image to fit the overlay size if necessary
        img_resized = np.array(Image.fromarray(img_3D_rgb).resize((512, 512)))
        # Create the overlay figure
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(img_resized)
        # Add the segmentation mask
        mask_color = [0.80, 0.82, 0.36]
        if seg_3D is not None:
            mask_image = (self.show_mask(seg_3D[idx], mask_color, alpha) * 255).astype(np.uint8)
            mask_resized = np.array(Image.fromarray(mask_image).resize((512, 512)))
            ax.imshow(mask_resized, alpha=alpha)
        ax.axis('off')
        fig.tight_layout()
        return fig

    # with column
    def show_segmented_image(self, right_column, segmented_image):
        segmented_image = np.load(segmented_image, allow_pickle=True)
        with right_column:
            st.subheader("Segmented Image")
            idx = st.session_state.slice_index if 'slice_index' in st.session_state else len(segmented_image['imgs']) // 2
            fig = self.visualize_overlay(segmented_image['imgs'], 
                                         None, 
                                         segmented_image['segs'], 
                                         idx=idx, alpha=.6)
            st.pyplot(fig)

    def show_download_button(self, segmented_image):
        st.sidebar.title("Download Result")
        st.sidebar.download_button(
            label="Download Segmented Image",
            data=segmented_image,
            file_name="segmented_image.npz",
            mime="application/octet-stream"
        )

    def show_refresh_button(self):
        st.sidebar.title("Want to try another image?")
        return st.sidebar.button("Refresh")

    def show_submit_button(self):
        st.sidebar.title("Segmentation Parameters")
        return st.sidebar.button("**Segment Image**")
    
    def show_slice_slider(self, range):
        st.sidebar.title("Visualizations")
        with st.sidebar:
            with st.container(border=True):
                slice_index = st.slider("Select the slice", 0, range, range // 2)
                return slice_index


class Controller:
    def __init__(self):
        self.view = View()
        if 'input_given' not in st.session_state:
            st.session_state.input_given = False
        if 'image' not in st.session_state:
            st.session_state.image = None
        if 'slice_index' not in st.session_state:
            st.session_state.slice_index = 0
        if 'segmented_image' not in st.session_state:
            st.session_state.segmented_image = None

    def segment_image(self, image_name):
        with st.spinner("Segmenting..."):
            resp = requests.get(SEGMENT_ENDPOINT, params={"filename": image_name})
            if resp.status_code == 200:
                segmented_image = BytesIO(resp.content)
                return segmented_image
            else:
                st.error(f"Error segmenting image {image_name}")
                return None

    # merge with upload_image_to_server
    def handle_image(self, image_path):
        if image_path:
            st.session_state.image = np.load(image_path, allow_pickle=True)
            st.session_state.input_given = True
            st.rerun()

    def upload_image_to_server(self, file):
        if file:
            resp = requests.post(UPLOAD_ENDPOINT, files={"file": file.getvalue()})
            if resp.status_code == 200:
                st.session_state.image_name = resp.json().get("filename")
                self.handle_image(file)
                return file
            else:
                st.error("Error uploading image")
        return None

    def run(self):
        if not st.session_state.input_given:

            uploaded_file = self.view.show_upload_section()
            if uploaded_file:
                self.upload_image_to_server(uploaded_file)

            sample_file = self.view.show_samples_section()
            if sample_file:
                self.upload_image_to_server(sample_file)
                
        else:
            slice_range = len(st.session_state.image['imgs']) - 1
            st.session_state.slice_index = self.view.show_slice_slider(slice_range)
            
            left_column, right_column = st.columns(2)
            self.view.show_original_image(left_column, st.session_state.image)

            if st.session_state.segmented_image is None:
                if self.view.show_submit_button():
                    st.session_state.segmented_image = self.segment_image(st.session_state.image_name)
                    st.rerun()
            else:
                self.view.show_segmented_image(right_column, st.session_state.segmented_image)
                self.view.show_download_button(st.session_state.segmented_image)

            if self.view.show_refresh_button():
                st.session_state.input_given = False
                st.session_state.image = None
                st.session_state.slice_index = 0
                st.rerun()

if __name__ == "__main__":
    controller = Controller()
    controller.run()

