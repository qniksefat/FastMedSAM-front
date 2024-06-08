import streamlit as st
from PIL import Image
from io import BytesIO
import time


class View:
    def __init__(self):
        st.set_page_config(page_title="Fast MedSAM", page_icon="✂️", layout="wide")
        st.title("Fast Segmentation of Medical Images")

    def show_upload_section(self, left_column):
        with left_column:
            st.sidebar.title("Upload Your Image")
            file = st.sidebar.file_uploader("", type=['jpg', 'png', 'jpeg'])
            return file

    def show_samples_section(self, left_column):
        with left_column:
            st.sidebar.divider()
            st.sidebar.title("Use Samples")
            sample_images = {
                "Rose": "static/sample1.png",
                "Daisy": "static/sample2.jpg",
            }
            selected_image = st.sidebar.selectbox("Select Image", list(sample_images.keys()))
            return sample_images[selected_image]

    def show_original_image(self, left_column, original_image):
        with left_column:
            st.subheader("Original Image")
            st.image(original_image)

    def show_segmented_image(self, right_column, segmented_image):
        with right_column:
            st.subheader("Segmented Image")
            st.image(segmented_image)

    def show_download_button(self, right_column, image_bytes):
        with right_column:
            st.sidebar.divider()
            st.sidebar.title("Download Result")
            st.sidebar.download_button(label="Click to Download", data=image_bytes, 
                                       file_name="segmented_image.png", mime="image/png")

class Controller:
    def __init__(self):
        self.view = View()

    def pil_to_bytes(self, img):
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        return byte_im

    def run_sam(self, image):
        with st.spinner("Segmenting..."):
            time.sleep(2)   # Simulate a delay
            segmented_image = image
            return segmented_image

    def run(self):
        left_column, right_column = st.columns(2)
        
        file = self.view.show_upload_section(left_column)
        if file:
            image = Image.open(file)
        else:
            sample_image_path = self.view.show_samples_section(left_column)
            image = Image.open(sample_image_path)

        self.view.show_original_image(left_column, image)
        
        segmented_image = self.run_sam(image)
        self.view.show_segmented_image(right_column, segmented_image)
        image_bytes = self.pil_to_bytes(segmented_image)
        self.view.show_download_button(right_column, image_bytes)

if __name__ == "__main__":
    controller = Controller()
    controller.run()
