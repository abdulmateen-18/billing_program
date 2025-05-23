from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
import numpy as np
import cv2
import base64
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
def covert_to_string(img):
    text = pytesseract.image_to_string(img)
    return text
def grayscale(img):
     return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 
def thresholding(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
##pytessaract implication done
##time to bing in Ai

prompt = "You are a restaurant cashier. Analyze this bill and summarize the items, quantity, price, taxes, and total." 
def gemini_response(dishkau,prompt):
     model = genai.GenerativeModel('gemini-1.5-flash')
     full_input = f"{prompt}\n\nExtracted Text:\n{dishkau}"
     response = model.generate_content(full_input)
     return response.text 
 
st.set_page_config(page_title='bill scanner')
st.header("Bill Reader")
input_path = st.text_input("Path way of the bill image :",key = "input")
submit1 = st.button('tell me everything aboout the bill')
if submit1 :
    if input_path:
        try :
            img = cv2.imread(input_path)
            if img is None:
                st.error("Image not found please check the path")
            else :
                img = grayscale(img)
                img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
                img = cv2.medianBlur(img, 3)
                img = thresholding(img)
                dishkau = covert_to_string(img)   
                response = gemini_response(dishkau, prompt)
                st.subheader("chitti robo resposne ")
                st.write(response)
        except Exception as e :
            st.error(f"An error occurred: {e}")        
    else :
        st.error("Please upload the image path")            
            
            
        
 
     


    
    

  





