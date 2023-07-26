import streamlit as st
import numpy as np
import cv2

st.set_page_config(layout="wide",page_title="Image to Cartoon Converter")
st.title("Image to Cartoon Converter")

def image_to_cartoon(image):

    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray=cv2.medianBlur(gray, 5)

    edges=cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    
    color=cv2.bilateralFilter(image, 9, 250, 250)
    cartoon=cv2.bitwise_and(color, color, mask=edges)
    
    cv2.imwrite("cartoon.png",cartoon)

img=st.file_uploader("Upload an image",type=['jpeg','png','jpg','avif'])

if img is not None:
    image=np.frombuffer(img.getvalue(),dtype=np.uint8)
    image=cv2.imdecode(image,cv2.IMREAD_COLOR)
    convert=st.button("Convert")
    if convert:
        image_to_cartoon(image)
        col1,col2=st.columns(2)
        with col1:
            st.image(img,caption="Original Image")
        with col2:
            st.image("cartoon.png",caption="cartoon")

            with open("cartoon.png","rb") as file:
                btn_id=st.download_button(
                    label="Download cartoon",
                    data=file,
                    file_name="cartoon.png",
                    mime="image/png"
                )
