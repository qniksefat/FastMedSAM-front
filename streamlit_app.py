import streamlit as st
from PIL import Image
from io import BytesIO
import time


class View:
    def __init__(self):
        st.set_page_config(page_title="Fast MedSAM", page_icon="✂️", layout="wide")
        st.title("Fast Segmentation of Medical Images")

    def show_upload_section(self):
        st.sidebar.title("Upload Your Image")
        file = st.sidebar.file_uploader("", type=['jpg', 'png', 'jpeg'])
        return file

    def show_samples_section(self):
        st.sidebar.divider()
        st.sidebar.title("Use Samples")
        sample_images = {
            "Rose": "static/sample1.png",
            "Daisy": "static/sample2.jpg",
        }
        selected_image = st.sidebar.selectbox("Select Image", list(sample_images.keys()))
        return sample_images[selected_image]

    def show_original_image(self, original_image):
        st.subheader("Original Image")
        st.image(original_image)

    def show_segmented_image(self, segmented_image):
        st.subheader("Segmented Image")
        st.image(segmented_image)

    def show_download_button(self, image_bytes):
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
        file = self.view.show_upload_section()
        if file:
            image = Image.open(file)
        else:
            sample_image_path = self.view.show_samples_section()
            image = Image.open(sample_image_path)

        self.view.show_original_image(image)

        segmented_image = self.run_sam(image)
        self.view.show_segmented_image(segmented_image)
        image_bytes = self.pil_to_bytes(segmented_image)
        self.view.show_download_button(image_bytes)


if __name__ == "__main__":
    controller = Controller()
    controller.run()
