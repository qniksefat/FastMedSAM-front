import streamlit as st

# Fast API + Streamlit

class View:
    def __init__(self):
        st.set_page_config(page_title="Fast MedSAM", page_icon="✂️", layout="wide")
        st.title("Fast Segmentation of Medical Images")


class Controller:
    def __init__(self):
        self.view = View()

    def run(self):
        pass


if __name__ == "__main__":
    controller = Controller()
    controller.run()
