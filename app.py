import streamlit as st
import os

# --- 1. CONFIGURACIÓN DE LA INTERFAZ ---
st.set_page_config(page_title="Buscador de Biblioteca", page_icon="📚", layout="centered")

# Imagen de encabezado
st.image("biblioteca.jpg", use_container_width=True)

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
col_filtro, col_texto = st.columns([1, 2])

with col_filtro:
    criterio = st.selectbox("Filtrar por:", ["Título", "Autor", "Género"])

with col_texto:
    busqueda = st.text_input(f"Escribe el {criterio.lower()} que buscas:", placeholder="Empieza a escribir...").strip()

st.markdown("---")

# --- 4. FILTRADO Y VISUALIZACIÓN DE RESULTADOS ---
# Filtramos la lista según la opción seleccionada por el usuario
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
    resultados = st.session_state.libros_db  # Muestra todos si no hay búsqueda

# Desplegar libros encontrados
if resultados:
    for libro in resultados:
        col_info, col_foto = st.columns([2, 1])
        
        with col_info:
            st.subheader(f"📖 {libro['titulo']}")
            st.write(f"**Autor:** {libro['autor']}")
            st.write(f"**Género:** *{libro['genero']}*")
            st.write(f"**Código:** `{libro['codigo'].upper()}`")
            
            if libro["disponible_fisico"]:
                st.success("✅ Disponible en formato físico.")
            else:
                st.warning("⚠️ No disponible en físico.")
                
                # Gestión del botón PDF
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
st.markdown("##") # Espacio en blanco para alejarlo de la vista
with st.expander("🔐 Panel de Administración (Oculto)"):
    # Una contraseña simple para simular seguridad externa
    password = st.text_input("Ingresa la clave de administrador:", type="password")
    
    if password == "1234":  # Cambia esta clave por la que quieras
        st.success("Acceso concedido. Registra un nuevo libro:")
        
        # Formulario para capturar los datos
        with st.form("nuevo_libro_form", clear_on_submit=True):
            nuevo_codigo = st.text_input("Código del Catálogo (ej: a104):")
            nuevo_titulo = st.text_input("Título del libro:")
            nuevo_autor = st.text_input("Autor:")
            nuevo_genero = st.text_input("Género:")
            dispo_fisico = st.checkbox("¿Está disponible físicamente en los estantes?", value=True)
            
            # Botón para guardar
            boton_guardar = st.form_submit_button("Guardar libro en el sistema")
            
            if boton_guardar:
                if nuevo_codigo and nuevo_titulo and nuevo_autor and nuevo_genero:
                    # Creamos la nueva ficha del libro
                    nuevo_libro = {
                        "codigo": nuevo_codigo.lower(),
                        "titulo": nuevo_titulo,
                        "autor": nuevo_autor,
                        "genero": nuevo_genero,
                        "disponible_fisico": dispo_fisico,
                        "archivo_interno": f"{nuevo_codigo.lower()}.pdf",
                        "imagen_portada": f"{nuevo_codigo.lower()}.jpg"
                    }
                    # Lo añadimos a la base de datos en memoria
                    st.session_state.libros_db.append(nuevo_libro)
                    st.success(f"🎉 ¡'{nuevo_titulo}' ha sido registrado exitosamente!")
                    st.rerun() # Recarga la página para mostrar el nuevo libro arriba
                else:
                    st.error("⚠️ Por favor, rellena todos los campos antes de guardar.")

