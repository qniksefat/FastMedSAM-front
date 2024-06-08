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
        file = st.sidebar.file_uploader("Choose an image", label_visibility="collapsed", 
                                        type=['jpg', 'png', 'jpeg'])
        return file

    def show_samples_section(self):
        st.sidebar.title("Or Choose a Sample Image")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.sidebar.button("Rose"):
                return "static/sample1.png"
        with col2:
            if st.sidebar.button("Daisy"):
                return "static/sample2.jpg"
        return None

    def show_original_image(self, left_column, original_image):
        with left_column:
            st.subheader("Original Image")
            st.image(original_image)

    def show_segmented_image(self, right_column, segmented_image):
        with right_column:
            st.subheader("Segmented Image")
            st.image(segmented_image)

    def show_download_button(self, image_bytes):
        st.sidebar.divider()
        st.sidebar.title("Download Result")
        st.sidebar.download_button(label="Click to Download", data=image_bytes, 
                                    file_name="segmented_image.png", mime="image/png")

    def show_refresh_button(self):
        st.sidebar.divider()
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

    def run_sam(self, image):
        with st.spinner("Segmenting..."):
            time.sleep(2)   # Simulate a delay
            segmented_image = image
            return segmented_image
        
    def handle_image(self, image):
        if image:
            image = Image.open(image)
            st.session_state.image = image
            st.session_state.input_given = True
            st.rerun()

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
                segmented_image = self.run_sam(st.session_state.image)
                self.view.show_segmented_image(right_column, segmented_image)
                image_bytes = self.pil_to_bytes(segmented_image)
                self.view.show_download_button(image_bytes)
            
            if self.view.show_refresh_button():
                st.session_state.input_given = False
                st.session_state.image = None
                st.session_state.text_prompt = ""
                st.rerun()


if __name__ == "__main__":
    controller = Controller()
    controller.run()
