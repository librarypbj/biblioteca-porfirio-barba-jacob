import streamlit as st
import os
import base64

# --- 1. CONFIGURACIÓN DE LA INTERFAZ ---
st.set_page_config(page_title="Buscador de Biblioteca", page_icon="📚", layout="centered")

# TRUCO PARA PONER IMAGEN DE FONDO CON FIGURAS
def poner_imagen_fondo(ruta_imagen):
    if os.path.exists(ruta_imagen):
        with open(ruta_imagen, "rb") as archivo:
            datos_imagen = archivo.read()
        imagen_base64 = base64.b64encode(datos_imagen).decode()
        estilo_css = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpeg;base64,{imagen_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(estilo_css, unsafe_allow_html=True)

# Activamos tu fondo de burbujas pastel
poner_imagen_fondo("fondo.jpeg")

# Imagen de encabezado
st.image("descubre el conocimiento.jpg",)


st.title("📚 biblioteca porfirio barba jacob")
st.write("Busca por título, autor o género. Los libros y sus detalles aparecerán al instante.")

# --- 2. BASE DE DATOS DINÁMICA (Guarda cambios en memoria) ---
if "libros_db" not in st.session_state:
    st.session_state.libros_db = [
        {
            "codigo": "a101",
            "titulo": "Cien años de soledad", 
            "autor": "Gabriel García Márquez", 
            "genero": "Realismo Mágico",
            "disponible_fisico": True,
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

# --- 3. SISTEMA DE FILTROS AVANZADOS ---
col_filtro, col_texto = st.columns(2)

with col_filtro:
    criterio = st.selectbox("Filtrar por:", ["Título", "Autor", "Género"])

with col_texto:
    busqueda = st.text_input(f"Escribe el {criterio.lower()} que buscas:", placeholder="Empieza a escribir...").strip()

st.markdown("---")

# --- 4. FILTRADO Y VISUALIZACIÓN DE RESULTADOS ---
resultados = []
if busqueda:
    for libro in st.session_state.libros_db:
        if criterio == "Título" and busqueda.lower() in libro["titulo"].lower():
            resultados.append(libro)
        elif criterio == "Autor" and busqueda.lower() in libro["autor"].lower():
            resultados.append(libro)
        elif criterio == "Género" and busqueda.lower() in libro["genero"].lower():
            resultados.append(libro)
else:
    resultados = st.session_state.libros_db

# Desplegar libros encontrados
if resultados:
    for libro in resultados:
        col_info, col_foto = st.columns([2, 1])
        
        with col_info:
            st.subheader(f"📖 {libro['titulo']}")
            st.write(f"**Autor:** {libro['autor']}")
            st.write(f"**Género:** *{libro['genero']}*")
            
            # Código del libro estilizado con diseño para máxima legibilidad
            st.markdown(f"**Código:** <span style='color: #1E1E24; background-color: rgba(255,255,255,0.85); padding: 3px 8px; border-radius: 4px; font-weight: bold; font-family: sans-serif;'>{libro['codigo'].upper()}</span>", unsafe_allow_html=True)
            st.write("") # Espacio corto
            
            if libro["disponible_fisico"]:
                st.success("✅ Disponible en formato físico.")
            else:
                st.warning("⚠️ No disponible en físico.")
                
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
                st.image(libro["imagen_portada"], width=160)
            else:
                st.caption("🖼️ [Portada no disponible]")
        
        st.markdown("---")
else:
    st.info("❌ No se encontraron libros con esos criterios.")

# --- 5. FORMULARIO OCULTO PARA ADMINISTRADOR ---
st.markdown("##")
with st.expander("🔐 Panel de Administración (Oculto)"):
    password = st.text_input("Ingresa la clave de administrador:", type="password")
    
    if password == "1234":
        st.success("Acceso concedido. Registra un nuevo libro:")
        
        with st.form("nuevo_libro_form", clear_on_submit=True):
            nuevo_codigo = st.text_input("Código del Catálogo (ej: a104):")
            nuevo_titulo = st.text_input("Título del libro:")
            nuevo_autor = st.text_input("Autor:")
            nuevo_genero = st.text_input("Género:")
            dispo_fisico = st.checkbox("¿Está disponible físicamente en los estantes?", value=True)
            
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
                    st.success(f"🎉 ¡'{nuevo_titulo}' ha sido registrado exitosamente!")
                    st.rerun()
                else:
                    st.error("⚠️ Por favor, rellena todos los campos antes de guardar.")
