import os
import streamlit as st
import base64
from openai import OpenAI
import openai
#from PIL import Image
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_drawable_canvas import st_canvas

Expert=" "
profile_imgenh=" "
    
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."


# ---------------------------
# Narrativa: Taylor’s Version
# ---------------------------
st.set_page_config(page_title='Tablero Inteligente — Taylor’s Version')
st.title('🎤 Tablero Inteligente — Taylor’s Version')
with st.sidebar:
    st.subheader("Acerca de")
    st.write("Este escenario es nuestro ‘studio session’: haz un boceto como si diseñaras un "
             "elemento para **The Eras Tour** (una portada, un vestuario, un set o un ícono).")
st.subheader("Dibuja tu idea Swiftie en el lienzo y luego presiona **Analizar** para una descripción rápida.")

# Parámetros del canvas
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Ancho de línea', 1, 30, 5)
stroke_color = "#000000"
bg_color = '#FFFFFF'

# Lienzo
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode=drawing_mode,
    key="canvas",
)

# Clave
ke = st.text_input('Ingresa tu API Key de OpenAI')
os.environ['OPENAI_API_KEY'] = ke

# Cliente OpenAI (mantengo tu forma original)
api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)

# Botón
analyze_button = st.button("Analizar boceto (Taylor’s Version) 🎶", type="secondary")

# Lógica original, solo cambia el copy/prompt
if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando tu boceto Swiftie..."):
        # Guardar imagen temporal
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'),'RGBA')
        input_image.save('img.png')
        
        # Codificar en base64
        base64_image = encode_image_to_base64("img.png")
        
        # Prompt con narrativa Taylor
        prompt_text = (
            "En español y brevemente, describe este boceto como si fuera un concepto "
            "para el universo de Taylor Swift (portada, vestuario, utilería o escenografía "
            "de The Eras Tour). Menciona estilo visual, colores dominantes y qué emoción transmite."
        )
    
        # Mensajes (mantengo estructura y modelo)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/png;base64,{base64_image}",
                    },
                ],
            }
        ]
    
        try:
            full_response = ""
            message_placeholder = st.empty()

            # Mantengo tu llamada tal cual
            response = openai.chat.completions.create(
              model="gpt-4o-mini",
              messages=[
                {
                   "role": "user",
                   "content": [
                     {"type": "text", "text": prompt_text},
                     {
                       "type": "image_url",
                       "image_url": {
                         "url": f"data:image/png;base64,{base64_image}",
                       },
                     },
                   ],
                  }
                ],
              max_tokens=500,
            )

            if response.choices[0].message.content is not None:
                full_response += response.choices[0].message.content
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

            if Expert == profile_imgenh:
                st.session_state.mi_respuesta = response.choices[0].message.content

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
else:
    if not api_key:
        st.warning("Por favor ingresa tu API key.")
