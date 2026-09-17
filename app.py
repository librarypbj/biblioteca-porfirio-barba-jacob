import streamlit as st
import os


# --- 1. CONFIGURACIÓN DE LA INTERFAZ ---
st.set_page_config(page_title="Buscador de Biblioteca", page_icon="📚", layout="wide")

# --- 2. BASE DE DATOS DINÁMICA (Solo Libros Físicos y Digital) ---
if "libros_db" not in st.session_state:
    st.session_state.libros_db = [
        {
            "codigo": "m101",
            "titulo": "La Carta Robada y Otros Cuentos", 
            "autor": "Edgar Allan Poe", 
            "genero": "Misterio",
            "disponible_fisico": True
        },
        {
            "codigo": "rm102",
            "titulo": "Cien años de soledad", 
            "autor": "Gabriel García Márquez", 
            "genero": "Realismo Mágico",
            "disponible_fisico": False  # Falso porque es exclusivo digital
        },
        {
            "codigo": "cf103",
            "titulo": "1984", 
            "autor": "George Orwell", 
            "genero": "Ciencia Ficción / Distopía",
            "disponible_fisico": True
        },
        {
            "codigo": "f104",
            "titulo": "El Hobbit", 
            "autor": "J.R.R. Tolkien", 
            "genero": "Fantasía",
            "disponible_fisico": True
        }
    ]

# --- 3. BARRA LATERAL IZQUIERDA (Navegación y Filtros) ---
with st.sidebar:
    st.header("🗂️ Navegación")
    
    # Lista dinámica de géneros
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
    # Filtramos por género
    libros_filtrados = [l for l in st.session_state.libros_db if l["genero"] == genero_seleccionado]
    
    # Filtramos por barra de búsqueda
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
            
            # Código del libro estilizado en azul rey elegante
            st.markdown(f"**Código:** <span style='color: #1E3A8A; font-weight: bold; font-family: monospace; font-size: 16px;'>{libro['codigo'].upper()}</span>", unsafe_allow_html=True)
            st.write("")
            
            if libro["disponible_fisico"]:
                st.success("✅ Disponible en formato físico en los estantes.")
            else:
             st.info("💻 Disponible solo en formato digital. Solicítalo en la administración.")
            nombre_imagen = f"{libro['codigo'].lower()}.jpg"
            if os.path.exists(nombre_imagen):
                st.image(nombre_imagen, width=150)
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
                nuevo_codigo = st.text_input("Código (ej: e105):")
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
                            "disponible_fisico": dispo_fisico
                        }
                        st.session_state.libros_db.append(nuevo_libro)
                        st.success(f"🎉 ¡El libro '{nuevo_titulo}' ha sido registrado!")
                        st.rerun()
                    else:
                        st.error("⚠️ Por favor, rellena todos los campos.")
