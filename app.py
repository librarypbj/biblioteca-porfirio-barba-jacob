import streamlit as st
import os
import io
import html
import base64
from PIL import Image, ImageOps

# --- 1. CONFIGURACIÓN DE LA INTERFAZ ---
st.set_page_config(page_title="Buscador de Biblioteca", page_icon="📚", layout="wide")

# Carpeta donde está este archivo (así encuentra los PDF y JPG sin importar desde dónde se ejecute)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
            "archivo_interno": "rm101.pdf",   # antes decía a101.pdf
            "imagen_portada": "rm101.jpg"    # antes decía a101.jpg
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
        },
    
        
        {
            "codigo": "nj108",
            "titulo": "El Tesoro de la Pordiosera",
            "autor": "Julia Mercedes Castilla",
            "genero": "Narrativa Juvenil",
            "disponible_fisico": True,
            "archivo_interno": "nj108.pdf",
            "imagen_portada": "nj108.jpg"
        },
         {
            "codigo": "d109",
            "titulo": "Atlas de la Biologia",
            "autor": "Andres Haro Vera",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "d109.pdf",
            "imagen_portada": "d109.jpg"
        },
    
            {
            "codigo": "cp110",
            "titulo": "Sabotaje en el Atlantico",
            "autor": "Gordon Thomas & Max Morgan-Witts",
            "genero": "Cronica Periodistica",
            "disponible_fisico": True,
            "archivo_interno": "cp110.pdf",
            "imagen_portada": "cp110.jpg"
        },
        {
            "codigo": "di111",
            "titulo": "Paises del Mundo",
            "autor": "El Tiempo,Editorial",
            "genero": "Divulgacion Informatica",
            "disponible_fisico": True,
            "archivo_interno": "di111.pdf",
            "imagen_portada": "di111.jpg"
        },
       {
            "codigo": "ac112",
            "titulo": "Cuentos Colombianos Antologia",
            "autor": "Varios Autores",
            "genero": "Antologia de Cuentos",
            "disponible_fisico": True,
            "archivo_interno": "ac112.pdf",
            "imagen_portada": "ac112.jpg"
        },
       {
            "codigo": "p114",
            "titulo": "Formas Para Almorzar",
            "autor": "Charles Reasoner",
            "genero": "Pedagogia",
            "disponible_fisico": True,
            "archivo_interno": "p114.pdf",
            "imagen_portada": "p114.jpg"
        },
        {
            "codigo": "na115",
            "titulo": "¿Quien Dice que no a las Drogas?",
            "autor": "Ricardo Alcantara",
            "genero": "Novela de Aprendizaje",
            "disponible_fisico": True,
            "archivo_interno": "na115.pdf",
            "imagen_portada": "na115.jpg"
       },
      {
            "codigo": "vt116",
            "titulo": "Time Out:Buenos Aires",
            "autor": "Equipo de Periodistas",
            "genero": "Viajes, Turismo",
            "disponible_fisico": True,
            "archivo_interno": "vt116.pdf",
            "imagen_portada": "vt116.jpg"
        },
        {
            "codigo": "nh117",
            "titulo": "Ramses the song Light ",
            "autor": "Christian Jacq",
            "genero": "Novela Historica",
            "disponible_fisico": True,
            "archivo_interno": "nh117.pdf",
            "imagen_portada": "nh117.jpg"
        },
         {
            "codigo": "m118",
            "titulo": "Death on the Nile",
            "autor": "Agatha Christie",
            "genero": " Misterio,Policiaca,bilingüe",
            "disponible_fisico": True,
            "archivo_interno": "m118.pdf",
            "imagen_portada": "m118.jpg"
        },
         {
            "codigo": "mo119",
            "titulo": "Lo que los Jovenes Preguntan",
            "autor": "Editado por los Testigos de Jehovah",
            "genero": "Manual de Orientacion",
            "disponible_fisico": True,
            "archivo_interno": "mo119.pdf",
            "imagen_portada": "mo119.jpg"
        },
         {
            "codigo": "i120",
            "titulo": "Habia una vez",
            "autor": "Graciela Montes",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "i120.pdf",
            "imagen_portada": "i120.jpg"
        },
         {
            "codigo": "m121",
            "titulo": "Cuentos de Fantasmas",
            "autor": "Varios Autores",
            "genero": "Misterio,Literatura Gotica Clasica",
            "disponible_fisico": True,
            "archivo_interno": "m121.pdf",
            "imagen_portada": "m121.jpg"
        },
         {
            "codigo": "f122",
            "titulo": "¡Que el Lobo se Muere",
            "autor": "Antonio Rodriguez Almodovar",
            "genero": "Fabula,Cuento Popular tradicional",
            "disponible_fisico": True,
            "archivo_interno": "f122.pdf",
            "imagen_portada": "f122.jpg"
        },
         {
            "codigo": "xx111",
            "titulo": "TÍTULO",
            "autor": "AUTOR",
            "genero": "GÉNERO",
            "disponible_fisico": True,
            "archivo_interno": "xx111.pdf",
            "imagen_portada": "xx111.jpg"
        }
 ]
    

      
   
# --- FUNCIONES AUXILIARES ---
def buscar_archivo(nombre_archivo):
    """Busca el archivo aunque tenga doble extensión (d109.jpg.jpeg, m104.jpg.jpg),
    cambie mayúsculas/minúsculas, e ignora archivos vacíos (0 bytes)."""
    if not nombre_archivo:
        return None
    buscado = nombre_archivo.lower()
    try:
        for f in os.listdir(BASE_DIR):
            if f.lower().startswith(buscado):
                ruta = os.path.join(BASE_DIR, f)
                if os.path.isfile(ruta) and os.path.getsize(ruta) > 0:
                    return ruta
    except Exception:
        pass
    return None
   

def cargar_imagen_segura(nombre_archivo):
    """Devuelve (bytes, formato) si la imagen es válida; si no, None."""
    ruta = buscar_archivo(nombre_archivo)
    if ruta is None:
        return None
    try:
        with open(ruta, "rb") as f:
            datos = f.read()
        img = Image.open(io.BytesIO(datos))
        formato = (img.format or "JPEG").lower()
        img.verify()  # comprueba que no esté corrupta
        return datos, formato
    except Exception:
        return None


def titulo_con_hover(titulo, imagen):
    """Título que muestra la portada al pasar el puntero."""
    titulo_safe = html.escape(titulo)
    if imagen is None:
        return f"<h3>📖 {titulo_safe}</h3>"
    datos, formato = imagen
    b64 = base64.b64encode(datos).decode()
    return f"""
    <h3 class="tip">📖 {titulo_safe}
        <span class="pic"><img src="data:image/{formato};base64,{b64}"></span>
    </h3>
    """


# Estilo del efecto hover (se define una sola vez)
st.markdown("""
<style>
.tip { position: relative; display: inline-block; cursor: pointer; }
.tip .pic {
    visibility: hidden; opacity: 0; position: absolute;
    left: 0; top: 100%; z-index: 9999;
    background: white; padding: 6px; border-radius: 8px;
    box-shadow: 0 4px 14px rgba(0,0,0,.35);
    transition: opacity .2s;
}
.tip:hover .pic { visibility: visible; opacity: 1; }
.tip .pic img { width: 180px; display: block; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

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
            imagen = cargar_imagen_segura(libro.get("imagen_portada", ""))

            st.subheader(f"📖 {libro['titulo'].upper()}")
            
            st.write(f"**Autor:** {libro['autor']}")
            st.markdown(
                f"**Código:** <span style='color: #1E3A8A; font-weight: bold; font-family: monospace; font-size: 16px;'>{libro['codigo'].upper()}</span>",
                unsafe_allow_html=True
            )
            st.write("")

            # Gestión de Disponibilidad Física
            if libro["disponible_fisico"]:
                st.success("✅ Disponible en formato físico en los estantes.")
            else:
                st.warning("⚠️ No disponible en formato físico.")
             # Disponibilidad en PDF
            if buscar_archivo(libro.get("archivo_interno", "")):
                st.info("📄 Disponible en formato PDF.")
            else:
                st.info("📄 Este libro no tiene versión en PDF.")

            # BOTÓN DE DESCARGA DIRECTA DE PDF LOCAL
            nombre_pdf = libro.get("archivo_interno", "")
            ruta_pdf = buscar_archivo(nombre_pdf)
            if ruta_pdf:
                with open(ruta_pdf, "rb") as archivo_pdf:
                    st.download_button(
                        label="⬇️ Descargar PDF Directo",
                        data=archivo_pdf.read(),
                        file_name=f"{libro['titulo']}.pdf",
                        mime="application/pdf",
                        key=f"btn_{libro['codigo']}"
                    )

            # PORTADA VISIBLE (si el archivo es válido; si no, avisa sin romper la app)
            if imagen:
                img_portada = Image.open(io.BytesIO(imagen[0]))
                img_portada = img_portada.rotate(-90, expand=True)
                img_recortada = ImageOps.fit(img_portada, (150, 220), Image.LANCZOS)
                st.image(img_recortada, width=150)
            else:
               st.caption(f"🖼️ Portada no disponible ({libro.get('imagen_portada', '')} no encontrada, vacía o inválida).")
               
            st.markdown("---")
         # --- LIBROS RELACIONADOS (mismo género) ---
        if busqueda:
            codigos_mostrados = {l["codigo"] for l in resultados}
            relacionados = [l for l in libros_filtrados if l["codigo"] not in codigos_mostrados]

            if relacionados:
                st.subheader(f"📚 Más libros de {genero_seleccionado}")
                columnas = st.columns(4)
                for i, rel in enumerate(relacionados):
                    with columnas[i % 4]:
                        img_rel = cargar_imagen_segura(rel.get("imagen_portada", ""))
                        if img_rel:
                            st.image(img_rel[0], use_container_width=True)
                        st.markdown(f"**{rel['titulo']}**")
                        st.caption(rel["autor"])

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