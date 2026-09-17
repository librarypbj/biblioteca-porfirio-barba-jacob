import streamlit as st
import os

# --- 1. CONFIGURACIÓN DE LA INTERFAZ ---
st.set_page_config(page_title="Buscador de Biblioteca", page_icon="📚", layout="wide")

# --- 2. BASE DE DATOS DINÁMICA FIJA (Exclusivo con tus archivos JPG y PDF locales) ---
if "libros_db" not in st.session_state:
    st.session_state.libros_db = [
        {
            "codigo": "m104",
            "titulo": "La Carta Robada y Otros Cuentos", 
            "autor": "Edgar Allan Poe", 
            "genero": "Misterio",
            "disponible_fisico": True,
            "archivo_interno": "m104.pdf",
            "imagen_portada": "m104.jpg"
        },
        {
            "codigo": "rm101",
            "titulo": "Cien años de soledad", 
            "autor": "Gabriel García Márquez", 
            "genero": "Realismo Mágico",
            "disponible_fisico": False,  # Digital
            "archivo_interno": "a101.pdf",
            "imagen_portada": "a101.jpg"
        },
        {
            "codigo": "e105",
            "titulo": "La selva de los números", 
            "autor": "Ricardo Gómez", 
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "e105.pdf",
            "imagen_portada": "e105.jpg"
        },
        {
            "codigo": "h106",
            "titulo": "La Cali que yo conocí", 
            "autor": "José Ignacio Claros V.", 
            "genero": "Historia",
            "disponible_fisico": True,
            "archivo_interno": "h106.pdf",
            "imagen_portada": "h106.jpg"
        },
        {
            "codigo": "i107",
            "titulo": "El Nuevo Mundo de los Niños: Grandes Exploradores", 
            "autor": "Equipo Editorial", 
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "i107.pdf",
            "imagen_portada": "i107.jpg"
        }
    ]

# --- 3. BARRA LATERAL IZQUIERDA (Navegación y Filtros) ---
with st.sidebar:
    st.header("🗂️ Navegación")
    
    generos_disponibles = sorted(list(set(libro["genero"] for libro in st.session_state.libros_db)))
    opciones_genero = ["Selecciona un género..."] + generos_disponibles
    
    genero_seleccionado = st.selectbox("1. Elige un Género:", opciones_genero)
    
    busqueda = ""
    if genero_seleccionado != "Selecciona un género...":
        st.markdown("---")
        busqueda = st.text_input(
            "2. ¿Qué libro buscas de este género?", 
            placeholder="Escribe el título o autor...",
            key="input_busqueda"
        ).strip()

# --- 4. CUERPO PRINCIPAL DE LA PÁGINA ---
st.title("📚 descubre el conocimiento")
st.write("Usa el menú de la izquierda para seleccionar un género y empezar tu búsqueda.")
st.markdown("---")

# --- 5. FILTRADO INTELIGENTE ---
if genero_seleccionado == "Selecciona un género...":
    st.info("💡 Por favor, selecciona un género en la barra lateral izquierda para explorar los libros disponibles.")
else:
    libros_filtrados = [l for l in st.session_state.libros_db if l["genero"] == genero_seleccionado]
    
    if busqueda:
        resultados = []
        for libro in libros_filtrados:
            if busqueda.lower() in libro["titulo"].lower() or busqueda.lower() in libro["autor"].lower():
                resultados.append(libro)
    else:
        resultados = libros_filtrados

    # --- 6. VISUALIZACIÓN DE RESULTADOS ---
    if resultados:
        st.subheader(f"📚 Libros encontrados en *{genero_seleccionado}*")
        st.markdown("##")
        
        for libro in resultados:
            st.subheader(f"📖 {libro['titulo']}")
            st.write(f"**Autor:** {libro['autor']}")
            st.markdown(f"**Código:** <span style='color: #1E3A8A; font-weight: bold; font-family: monospace; font-size: 16px;'>{libro['codigo'].upper()}</span>", unsafe_allow_html=True)
            st.write("")
            
            # Gestión de Disponibilidad Física
            if libro["disponible_fisico"]:
                st.success("✅ Disponible en formato físico en los estantes.")
            else:
                st.warning("⚠️ No disponible en formato físico.")
            
            # BOTÓN AZUL DE DESCARGA DIRECTA DE PDF LOCAL
            if "archivo_interno" in libro:
                nombre_pdf = libro["archivo_interno"]
                if os.path.exists(nombre_pdf):
                    with open(nombre_pdf, "rb") as archivo_pdf:
                        st.download_button(
                            label="⬇️ Descargar PDF Directo",
                            data=archivo_pdf.read(),
                            file_name=f"{libro['titulo']}.pdf",
                            mime="application/pdf",
                            key=f"btn_{libro['codigo']}"
                        )
            
            # LECTOR NATIVO SEGURO DE IMÁGENES .JPG LOCALES (Previene cuadros rojos de error)
            if "imagen_portada" in libro:
                nombre_img = libro["imagen_portada"]
                if os.path.exists(nombre_img):
                    with open(nombre_img, "rb") as f_img:
                        datos_binarios_imagen = f_img.read()
                    # Pasamos los bytes puros para saltarnos el error gráfico de Streamlit
                    st.image(datos_binarios_imagen, width=150)
                
            st.markdown("---")
    else:
        st.warning(f"❌ No encontramos ningún libro que coincida con '{busqueda}' en este género.")

# --- 7. PANEL DE ADMINISTRACIÓN OCULTO ---
with st.sidebar:
    st.markdown("##")
    st.markdown("---")
    with st.expander("🔐 Panel Administrador"):
        password = st.text_input("Contraseña:", type="password", key="admin_pass")
        if password == "1234":
            st.success("Acceso concedido:")
            with st.form("nuevo_libro_form", clear_on_submit=True):
                nuevo_codigo = st.text_input("Código (ej: e108):")
                nuevo_titulo = st.text_input("Título del Libro:")
                nuevo_autor = st.text_input("Autor:")
                nuevo_genero = st.text_input("Género:")
                dispo_fisico = st.checkbox("¿Está disponible físicamente?", value=True)
                
                boton_guardar = st.form_submit_button("Guardar libro en el sistema")
                
                if boton_guardar:
                    if nuevo_codigo and nuevo_titulo and nuevo_autor and nuevo_genero:
                        nuevo_libro = {
                            "codigo": nuevo_codigo.lower(),
                            "titulo": nuevo_titulo,
                            "autor": nuevo_autor,
                            "genero": nuevo_genero,
                            "disponible_fisico": dispo_fisico,
                            "archivo_interno": f"{nuevo_codigo.lower()}.pdf",
                            "imagen_portada": f"{nuevo_codigo.lower()}.jpg"
                        }
                        st.session_state.libros_db.append(nuevo_libro)
                        st.success(f"🎉 ¡El libro '{nuevo_titulo}' ha sido registrado!")
                        st.rerun()
                    else:
                        st.error("⚠️ Por favor, rellena todos los campos.")
