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
        file = st.sidebar.file_uploader("Choose an image", label_visibility="collapsed",
                                        type=['npz'])
        if file is not None:
            resp = requests.post(UPLOAD_ENDPOINT, files={"file": file.getvalue()})
            if resp.status_code == 200:
                st.session_state.image_name = resp.json().get("filename")
                return file
            else:
                st.error("Error uploading image")
        return None

    def show_samples_section(self):
        st.sidebar.title("Or Choose a Sample Image")
        col1, col2 = st.sidebar.columns(2)
        if st.sidebar.button("Rose"):
            return "static/sample1.png"
        if st.sidebar.button("Daisy"):
            return "static/sample2.jpg"
        return None

    def show_original_image(self, left_column, original_image):
        with left_column:
            st.subheader("Original Image")
            st.image(original_image)
    
    def show_mask(self, mask, mask_color=None, alpha=0.5):
        if mask_color is not None:
            color = np.concatenate([mask_color, np.array([alpha])], axis=0)
        else:
            color = np.array([251 / 255, 252 / 255, 30 / 255, alpha])
        h, w = mask.shape[-2:]
        mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
        return mask_image
    
    def visualize_overlay(self, img_3D, gt_3D, seg_3D, idx=0, alpha=0.6):
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
        # Add the mask
        mask_color = [0.80, 0.82, 0.36]
        mask_image = (self.show_mask(seg_3D[idx], mask_color, alpha) * 255).astype(np.uint8)
        mask_resized = np.array(Image.fromarray(mask_image).resize((512, 512)))
        ax.imshow(mask_resized, alpha=alpha)
        ax.axis('off')
        fig.tight_layout()
        return fig

    def show_segmented_image(self, right_column, segmented_image):
        with right_column:
            st.subheader("Segmented Image")
            idx = len(segmented_image['imgs']) // 2
            fig = self.visualize_overlay(segmented_image['imgs'], 
                                         segmented_image['gts'], 
                                         segmented_image['segs'], 
                                         idx=idx, alpha=.6)
            st.pyplot(fig)

    def show_download_button(self, image_bytes):
        st.sidebar.title("Download Result")
        st.sidebar.download_button(label="Click to Download", data=image_bytes,
                                    file_name="segmented_image.png", mime="image/png")

    def show_refresh_button(self):
        st.sidebar.title("Want to try another image?")
        return st.sidebar.button("Refresh")

    def show_submit_button(self):
        return st.sidebar.button("**Segment Image**")

    def show_prompt_input(self):
        st.sidebar.title("Segmentation Parameters")
        text_prompt = st.sidebar.text_input("Write a candidate label")
        return text_prompt


class Controller:
    def __init__(self):
        self.view = View()
        if 'input_given' not in st.session_state:
            st.session_state.input_given = False
        if 'image' not in st.session_state:
            st.session_state.image = None
        if 'text_prompt' not in st.session_state:
            st.session_state.text_prompt = ""

    def pil_to_bytes(self, img):
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        return byte_im

    def run_sam(self, image_name):
        with st.spinner("Segmenting..."):
            resp = requests.get(SEGMENT_ENDPOINT, params={"filename": image_name})
            if resp.status_code == 200:
                segmented_image = BytesIO(resp.content)
                return segmented_image
            else:
                st.error("Error during segmentation")
                return None

    def handle_image(self, image):
        if image:
            st.session_state.image = self.get_mid_layer(image)
            st.session_state.input_given = True
            st.rerun()

    def get_mid_layer(self, npz_file_path):
        npz_data = np.load(npz_file_path)
        images_key = 'imgs' if 'imgs' in npz_data else 'segs'
        imgs = npz_data[images_key]
        mid_layer_index = len(imgs) // 2
        mid_layer = imgs[mid_layer_index]
        return mid_layer

    def run(self):
        left_column, right_column = st.columns(2)

        if not st.session_state.input_given:
            file = self.view.show_upload_section()
            if file:
                self.handle_image(file)

            sample_image_path = self.view.show_samples_section()
            if sample_image_path:
                self.handle_image(sample_image_path)
                
        else:
            self.view.show_original_image(left_column, st.session_state.image)

            st.session_state.text_prompt = self.view.show_prompt_input()

            if self.view.show_submit_button():
                segmented_image = self.run_sam(st.session_state.image_name)
                segmented_image = np.load(segmented_image)
                if segmented_image:
                    self.view.show_segmented_image(right_column, segmented_image)
                    # image_bytes = self.pil_to_bytes(segmented_image)
                    # self.view.show_download_button(image_bytes)

            if self.view.show_refresh_button():
                st.session_state.input_given = False
                st.session_state.image = None
                st.session_state.text_prompt = ""
                st.rerun()

if __name__ == "__main__":
    controller = Controller()
    controller.run()

