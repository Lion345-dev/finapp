import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Configurar la API de Gemini
load_dotenv()

def configure_gemini():
    """Configurar la API de Gemini"""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key is None:
        st.error("API key de Gemini no encontrada. Por favor configura la variable de entorno GEMINI_API_KEY.")
        return None
    
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Error al configurar Gemini: {e}")
        return None

st.title("💡 Asistente Financiero AI")
st.markdown("Obtén insights y análisis financieros usando inteligencia artificial (Gemini API).")

# Inicializar el modelo
model = configure_gemini()

if model is not None:
    # Historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar mensajes anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input del usuario
    if prompt := st.chat_input("Haz una pregunta sobre análisis financiero..."):
        # Añadir mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Obtener respuesta de Gemini
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    # Construir contexto basado en el historial
                    context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                    
                    # Configurar el prompt para respuestas financieras
                    full_prompt = f"""
                    Eres un experto analista financiero con 20 años de experiencia en mercados globales, 
                    modelado financiero y gestión de riesgos. Proporciona respuestas profesionales, 
                    técnicas pero accesibles, con datos concretos cuando sea posible.
                    
                    Contexto de la conversación:
                    {context}
                    
                    Pregunta actual:
                    {prompt}
                    
                    Respuesta:
                    """
                    
                    response = model.generate_content(full_prompt)
                    response_text = response.text
                    
                    # Mostrar respuesta
                    st.markdown(response_text)
                    
                    # Añadir a historial
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"Error al generar respuesta: {e}")
    
    # Ejemplos de preguntas
    st.sidebar.markdown("### Ejemplos de preguntas:")
    examples = [
        "Explica el modelo CAPM en términos simples",
        "¿Cómo calcularía el VaR para un portafolio de acciones tecnológicas?",
        "Compara las ventajas de Markowitz vs Black-Litterman",
        "¿Qué indicadores técnicos son más efectivos para mercados volátiles?",
        "Genera un análisis fundamental de AAPL"
    ]
    
    for example in examples:
        if st.sidebar.button(example):
            st.session_state.messages.append({"role": "user", "content": example})
            st.rerun()
    
    # Limpiar historial
    if st.sidebar.button("Limpiar conversación"):
        st.session_state.messages = []
        st.rerun()
