import streamlit as st
import os

# --- 1. CONFIGURACIÓN DE LA INTERFAZ ---
st.set_page_config(page_title="Buscador de Biblioteca", page_icon="📚", layout="wide")

# --- 2. BASE DE DATOS DINÁMICA (Guarda cambios en memoria) ---
if "libros_db" not in st.session_state:
    st.session_state.libros_db = [
        {
            "codigo": "a101",
            "titulo": "Cien años de soledad", 
            "autor": "Gabriel García Márquez", 
            "genero": "Realismo Mágico",
            "disponible_fisico": False,
            "archivo_interno": "a101.pdf",
            "imagen_portada": "a101.jpg"
        },
        {
            "codigo": "a102",
            "titulo": "1984", 
            "autor": "George Orwell", 
            "genero": "Ciencia Ficción / Distopía",
            "disponible_fisico": False,
            "archivo_interno": "a102.pdf",
            "imagen_portada": "a102.jpg"
        },
        {
            "codigo": "a103",
            "titulo": "El Hobbit", 
            "autor": "J.R.R. Tolkien", 
            "genero": "Fantasía",
            "disponible_fisico": False,
            "archivo_interno": "a103.pdf",
            "imagen_portada": "a103.jpg"
        }
    ]

# --- 3. BARRA LATERAL IZQUIERDA (Sidebar para Géneros y Búsqueda) ---
with st.sidebar:
    st.header("🗂️ Navegación")
    
    # Extraemos todos los géneros únicos de la base de datos para armar la lista dinámica
    generos_disponibles = sorted(list(set(libro["genero"] for libro in st.session_state.libros_db)))
    
    # Añadimos una opción inicial vacía o neutra para que no muestre nada al cargar
    opciones_genero = ["Selecciona un género..."] + generos_disponibles
    
    # Desplegable tipo flecha hacia abajo
    genero_seleccionado = st.selectbox("1. Elige un Género:", opciones_genero)
    
    busqueda = ""
    # Solo si el usuario elige un género real, aparece la barra de búsqueda debajo
    if genero_seleccionado != "Selecciona un género...":
        st.markdown("---")
        busqueda = st.text_input(
            "2. ¿Qué libro buscas de este género?", 
            placeholder="Escribe el título o autor...",
            key="input_busqueda"
        ).strip()

# --- 4. CUERPO PRINCIPAL DE LA PÁGINA ---
st.title("📚 Biblioteca porfirio barba jacob")
st.write("Usa el menú de la izquierda para seleccionar un género y empezar tu búsqueda.")
st.markdown("---")

# --- 5. FILTRADO INTELIGENTE ---
# Si no se ha seleccionado un género, la página principal se mantiene limpia y vacía
if genero_seleccionado == "Selecciona un género...":
    st.info("💡 Por favor, selecciona un género en la barra lateral izquierda para explorar los libros disponibles.")
else:
    # 1. Filtramos primero por el género seleccionado
    libros_filtrados = [l for l in st.session_state.libros_db if l["genero"] == genero_seleccionado]
    
    # 2. Si el usuario escribió en la barra de búsqueda, filtramos aún más por título o autor
    if busqueda:
        resultados = []
        for libro in libros_filtrados:
            if busqueda.lower() in libro["titulo"].lower() or busqueda.lower() in libro["autor"].lower():
                resultados.append(libro)
    else:
        resultados = libros_filtrados # Si no busca nada en la barra, muestra todos los de ese género

    # --- 6. VISUALIZACIÓN DE RESULTADOS ---
    if resultados:
        st.subheader(f"📚 Libros encontrados en *{genero_seleccionado}*")
        st.markdown("##")
        
        for libro in resultados:
            col_info, col_foto = st.columns(2)
            
            with col_info:
                st.subheader(f"📖 {libro['titulo']}")
                st.write(f"**Autor:** {libro['autor']}")
                st.markdown(f"**Código:** <span style='color: #1E3A8A; font-weight: bold; font-family: monospace; font-size: 16px;'>{libro['codigo'].upper()}</span>", unsafe_allow_html=True)
                st.write("")
                
                if libro["disponible_fisico"]:
                    st.success("✅ Disponible en formato físico.")
                else:
                    st.markdown("<div style='color: #856404; background-color: #fff3cd; border: 1px solid #ffeeba; padding: 10px; border-radius: 5px; font-weight: bold; display: inline-block; margin-bottom: 10px;'>💻 Disponible solo en formato digital</div>", unsafe_allow_html=True)
                    
                    nombre_pdf = libro["archivo_interno"]
                    if os.path.exists(nombre_pdf):
                        with open(nombre_pdf, "rb") as archivo_pdf:
                            st.download_button(
                                label="⬇️ Descargar PDF",
                                data=archivo_pdf.read(),
                                file_name=f"{libro['titulo']}.pdf",
                                mime="application/pdf",
                                key=f"btn_{libro['codigo']}"
                            )
                    else:
                        st.error("🚨 Archivo PDF no cargado en el sistema.")
            
            with col_foto:
                if os.path.exists(libro["imagen_portada"]):
                    st.image(libro["imagen_portada"], width=150)
                else:
                    st.caption("🖼️ [Portada no disponible]")
            
            st.markdown("---")
    else:
        st.warning(f"❌ No encontramos ningún libro que coincida con '{busqueda}' en este género.")

# --- 7. PANEL DE ADMINISTRACIÓN OCULTO EN LA BARRA LATERAL ---
with st.sidebar:
    st.markdown("##")
    st.markdown("---")
    with st.expander("🔐 Panel Administrador"):
        password = st.text_input("Contraseña:", type="password", key="admin_pass")
        if password == "1234":
            st.success("Acceso concedido:")
            with st.form("nuevo_libro_form", clear_on_submit=True):
                nuevo_codigo = st.text_input("Código (ej: a104):")
                nuevo_titulo = st.text_input("Título:")
                nuevo_autor = st.text_input("Autor:")
                nuevo_genero = st.text_input("Género:")
                dispo_fisico = st.checkbox("¿Disponible físico?", value=False)
                dispo_pdf = st.checkbox("¿Está disponible en formato digital (PDF)?", value=False)

                boton_guardar = st.form_submit_button("Guardar libro")
                
                if boton_guardar:
                    if nuevo_codigo and nuevo_titulo and nuevo_autor and nuevo_genero:
                        nuevo_libro = {
                            "codigo": nuevo_codigo.lower(),
                            "titulo": nuevo_titulo,
                            "autor": nuevo_autor,
                            "genero": nuevo_genero,
                            "disponible_fisico": dispo_fisico,
                            "disponible_pdf": dispo_pdf,

                            "archivo_interno": f"{nuevo_codigo.lower()}.pdf",
                            "imagen_portada": f"{nuevo_codigo.lower()}.jpg"
                        }
                        st.session_state.libros_db.append(nuevo_libro)
                        st.success(f"🎉 ¡Registrado!")
                        st.rerun()
                    else:
                        st.error("⚠️ Rellena todos los campos.")
