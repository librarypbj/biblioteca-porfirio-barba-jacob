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
            "archivo_interno": "",
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
            "archivo_interno": "",
            "imagen_portada": "e105.jpg"
        },
        {
            "codigo": "h106",
            "titulo": "La Cali que yo conocí",
            "autor": "José Ignacio Claros V.",
            "genero": "Historia",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "h106.jpg"
        },
        {
            "codigo": "i107",
            "titulo": "El Nuevo Mundo de los Niños: Grandes Exploradores",
            "autor": "Equipo Editorial",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i107.jpg"
        },
    
        
        {
            "codigo": "nj108",
            "titulo": "El Tesoro de la Pordiosera",
            "autor": "Julia Mercedes Castilla",
            "genero": "Narrativa Juvenil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "nj108.jpg"
        },
         {
            "codigo": "d109",
            "titulo": "Atlas de la Biologia",
            "autor": "Andres Haro Vera",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d109.jpg"
        },
    
         {
            "codigo": "cp110",
            "titulo": "Sabotaje en el Atlantico",
            "autor": "Gordon Thomas & Max Morgan-Witts",
            "genero": "Cronica Periodistica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "cp110.jpg"
        },
         {
            "codigo": "di111",
            "titulo": "Paises del Mundo",
            "autor": "El Tiempo,Editorial",
            "genero": "Divulgacion Informatica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "di111.jpg"
        },
         {
            "codigo": "ac112",
            "titulo": "Cuentos Colombianos Antologia",
            "autor": "Varios Autores",
            "genero": "Antologia de Cuentos",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "ac112.jpg"
        },
         {
            "codigo": "p114",
            "titulo": "Formas Para Almorzar",
            "autor": "Charles Reasoner",
            "genero": "Pedagogia",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "p114.jpg"
        },
         {
            "codigo": "na115",
            "titulo": "¿Quien Dice que no a las Drogas?",
            "autor": "Ricardo Alcantara",
            "genero": "Novela de Aprendizaje",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "na115.jpg"
       },
        {
            "codigo": "vt116",
            "titulo": "Time Out:Buenos Aires",
            "autor": "Equipo de Periodistas",
            "genero": "Viajes, Turismo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "vt116.jpg"
        },
         {
            "codigo": "nh117",
            "titulo": "Ramses the song Light ",
            "autor": "Christian Jacq",
            "genero": "Novela Historica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "nh117.jpg"
        },
         {
            "codigo": "m118",
            "titulo": "Death on the Nile",
            "autor": "Agatha Christie",
            "genero": " Misterio,Policiaca,bilingüe",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "m118.jpg"
        },
         {
            "codigo": "mo119",
            "titulo": "Lo que los Jovenes Preguntan",
            "autor": "Editado por los Testigos de Jehovah",
            "genero": "Manual de Orientacion",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "mo119.jpg"
        },
         {
            "codigo": "i120",
            "titulo": "Habia una vez",
            "autor": "Graciela Montes",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i120.jpg"
        },
         {
            "codigo": "m121",
            "titulo": "Cuentos de Fantasmas",
            "autor": "Varios Autores",
            "genero": "Misterio,Literatura Gotica Clasica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "m121.jpg"
        },
         {
            "codigo": "f122",
            "titulo": "¡Que el Lobo se Muere",
            "autor": "Antonio Rodriguez Almodovar",
            "genero": "Fabula,Cuento Popular tradicional",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "f122.jpg"
        },
         {
            "codigo": "mf123",
            "titulo": "Ang Alamat ng Palay",
            "autor": "Victoria Anonuevo",
            "genero": "Mitologia Filipina",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "mf123.jpg"
        },
     {
            "codigo": "i124",
            "titulo": "Ahora Rio..Ya No Lloro",
            "autor": "Patricia Salazar Patiño",
            "genero": "Cuento Infantil Ilustrado",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i124.jpg"
        },
         {
            "codigo": "i125",
            "titulo": "Tutubi Patrol 10: Si Padrong Pato at Ang Matalinong Kuwago",
            "autor": "Ben s. Alba",
            "genero": "Cuento Infantil Ilustrado, bilingüe",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i125.jpg"
        },
         {
            "codigo": "i126",
            "titulo": "There's a Duwende in my Brother's Soup",
            "autor": "Clara Saguisag",
            "genero": "Cuento Infantil Ilustrado, bilingüe",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i126.jpg"
        },
         {
            "codigo": "i127",
            "titulo": "The Spectacular Tree",
            "autor": "Robert Gunnar Magnuson",
            "genero": "Cuento Infantil Ilustrado, bilingüe",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i127.jpg"
        },
     {
            "codigo": "ri128",
            "titulo": "Diola: Ang Bayani Ng Philippine Eagle",
            "autor": "Mary Ann Ordinario Floresta & Yasmin s.ong",
            "genero": "Relato Infantil Ilustrado, bilingüe",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "ri128.jpg"
        },
         {
            "codigo": "li129",
            "titulo": "Papel de liha/Sandpaper",
            "autor": "Ompong Remigio",
            "genero": "Literatura Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "li129.jpg"
        },
         {
            "codigo": "i130",
            "titulo": "Tutubi Patrol 8:Si Bumbi Bubuyog at ang mga Alitaptap",
            "autor": "Timmy l. Cruz & Luis P. Gatmaitan",
            "genero": "Cuento Infantil Educativo, bilingüe",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i130.jpg"
        },
         {
            "codigo": "ct131",
            "titulo": "Si Pilandok at ang  Manok Na Nangingitlog ng Ginto",
            "autor": "Victoria Anonuevo",
            "genero": "Cuento Tradicional Filipino, bilingüe",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "ct131.jpg"
        },
         {
            "codigo": "a132",
            "titulo": "Zorro",
            "autor": "Johnston McCulley",
            "genero": "Aventura ",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "a132.jpg"
        },
         {
            "codigo": "i133",
            "titulo": "May Pera Sa Basura",
            "autor": "Antonio Lamberto",
            "genero": "Literatura Infantil, Didactica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i133.jpg"
        },
         {
            "codigo": "ci134",
            "titulo": "Tutubi Patrol 2: Si Popoy Palay At ang mga damo",
            "autor": "Tutubi Patrol Team",
            "genero": "Cuento Infantil ",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "ci134.jpg"
        },
        {
            "codigo": "li135",
            "titulo": "muertos de susto",
            "autor": "Maria Fernanda Paz Castillo",
            "genero": "Literatura Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "li135.jpg"
        },
         {
            "codigo": "ie136",
            "titulo": "¿Que Puedes Encontrar? En la Naturaleza",
            "autor": "Coleccion Muchos Animales Para Ver Y Nombrar",
            "genero": "Interactivo Estimulacion",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "ie136.jpg"
        },
         {
            "codigo": "pe137",
            "titulo": "Divina Comedia",
            "autor": "Dante Alighieri",
            "genero": "Literatura Universal",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "pe137.jpg"
        },
         {
            "codigo": "ni138",
            "titulo": "Cara de Chancho",
            "autor": "Anna Lavatelli",
            "genero": "Novela Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "ni138.jpg"
        },
         {
            "codigo": "rc139",
            "titulo": "La Parure Et Autres Nouvelles Realistes",
            "autor": "Guy De Mau Passant",
            "genero": "Relatos Clasicos Francese",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "rc139.jpg"
        },
         {
            "codigo": "li140",
            "titulo": "Munting Sinag Araw",
            "autor": "Gloria Villaraza Guzman",
            "genero": "Cuento Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "li140.jpg"
        },
         {
            "codigo": "ct141",
            "titulo": "Si Pilandok Sa Pulo Ng Pawikan",
            "autor": "Victoria Anonuevo",
            "genero": "Cuento Tradicional",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "ct141.jpg"
        },
        {
            "codigo": "i142",
            "titulo": "The Elephant's Tale",
            "autor": "Avril Rowlands",
            "genero": "infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i142.jpg"
        },
        {
            "codigo": "i143",
            "titulo": "Muting Patak Ulan (A Little Raindrop)",
            "autor": "Gloria Villaraza Guzman",
            "genero": "Infantil, bilingüe",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i143.jpg"
        },
        {
            "codigo": "e144",
            "titulo": "When I Cross The Street",
            "autor": "Lin Acacio Flores",
            "genero": "Educativo, bilingüe",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e144.jpg"
        },
        {
            "codigo": "e145",
            "titulo": "La Gran Esperanza",
            "autor": "Equipo Medico Y Comunicaciones Fundacion Valle Del Lili",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e145.jpg"
        },
         {
            "codigo": "i146",
            "titulo": "Do Your Earns Hang Low?",
            "autor": "Dorothea Deprisco Wang",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i146.jpg"
        },
        {
            "codigo": "i147",
            "titulo": "El Soldadito de Plomo",
            "autor": "Hans Christian Andersen",
            "genero": "Literatura Clasica Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i147.jpg"
        },
        {
            "codigo": "i148",
            "titulo": "La Mena Y Anisilla",
            "autor": "Hernan Garrido Lecca",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i148.jpg"
        },
        {
            "codigo": "ml149",
            "titulo": "Simbad(De Los Cuentos De Las Mil Y Una Noches)",
            "autor": "Ludmila Zeman",
            "genero": "Mitologia Y Leyendas",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "ml149.jpg"
        },
         {
            "codigo": "i150",
            "titulo": "Si Pilandok Sa Kaharian Sa Dagat",
            "autor": "Victoria Añonuevo",
            "genero": "Infantil Bilingüe",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i150.jpg"
        },
         {
            "codigo": "cf151",
            "titulo": "Star Wars:Tatooine Adventures",
            "autor": "Clare Hibbert",
            "genero": "Ciencia Ficcion",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "cf151.jpg"
        },
         {
            "codigo": "gm152",
            "titulo": "El Fin Del Alzheimer",
            "autor": "Dr, Dale Bredesen",
            "genero": "Guia Medica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "gm152.jpg"
        },
        {
            "codigo": "fd153",
            "titulo": "Billy Elliot",
            "autor": "Melvin Burgess",
            "genero": "Ficcion Dramática",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "fd153.jpg"
        },
         {
            "codigo": "fh154",
            "titulo": "Wide Sargasso Sea",
            "autor": "Jean Rhys",
            "genero": "Ficcion Historica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "fh154.jpg"
        },
         {
            "codigo": "d155",
            "titulo": "Ojitos De Angel",
            "autor": "Ramon Fonseca Mora",
            "genero": "Drama",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d155.jpg"
        },
         {
            "codigo": "f156",
            "titulo": "La Cosecha",
            "autor": "Felipe Martinez Cuellar",
            "genero": "Ficcion",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "f156.jpg"
        },
         {
            "codigo": "pe157",
            "titulo": "Obra Literaria De Jorge Gaitan Duran",
            "autor": "Jorge Gaitan Duran",
            "genero": "Poesia, Ensayo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "pe157.jpg"
        },
         {
            "codigo": "av158",
            "titulo": "Juventud En Extasis",
            "autor": "Carlos Cuauhtemoc Sanchez",
            "genero": "Autoayuda, Valores",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "av158.jpg"
        },
         {
            "codigo": "fc159",
            "titulo": "Cancion De Navidad & El Poseido",
            "autor": "Charles Dickens",
            "genero": "Ficcion Clasica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "fc159.jpg"
        },
        {
            "codigo": "fh160",
            "titulo": "Tiempo De Heroes",
            "autor": "Anabel Saiz Ripoll",
            "genero": "Ficcion Historica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "fh160.jpg"
        },
         {
            "codigo": "t161",
            "titulo": "Guia Turistica Huila Colombia",
            "autor": "Ministerio de Comercio, Industria y Turismo",
            "genero": "Turismo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "t161.jpg"
        },
         {
            "codigo": "f162",
            "titulo": "Destinos",
            "autor": "Peter Denne Bart ",
            "genero": "Ficcion",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "f162.jpg"
        },
         {
            "codigo": "e163",
            "titulo": "Secuencias Matematicas 8",
            "autor": "Editorial Pedagogico,Varios Autores",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e163.jpg"
        },
         {
            "codigo": "f164",
            "titulo": "Cipi",
            "autor": "Mario Lodi",
            "genero": "Fabula",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "f164.jpg"
        },
         {
            "codigo": "rs165",
            "titulo": "La Voragine",
            "autor": "Jose Eustasio Rivera",
            "genero": "Realismo Social",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "rs165.jpg"
        },
         {
            "codigo": "fp166",
            "titulo": "El Largo Adios",
            "autor": "Raymond Chandler",
            "genero": "Ficcion Policiaca",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "fp166.jpg"
        },
         {
            "codigo": "nb167",
            "titulo": "Los Doce Del Patibulo",
            "autor": "E. M. Nathanson",
            "genero": "Novela Belica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "nb167.jpg"
        },
         {
            "codigo": "np168",
            "titulo": "La Serpiente Emplumada",
            "autor": "D, H. Lawrence",
            "genero": "Novela Politica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "np168.jpg"
        },
         {
            "codigo": "fp169",
            "titulo": "Reflejos En Tus Ojos Dorados",
            "autor": "Carson McCullers",
            "genero": "Ficcion Psicologica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "fp169.jpg"
        },
         {
            "codigo": "fj170",
            "titulo": "Stone Cold",
            "autor": "Robert Swindells",
            "genero": "Ficcion Juvenil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "fj170.jpg"
        },
        {
            "codigo": "cp171",
            "titulo": "Desterrados",
            "autor": "Alfredo Molano Bravo",
            "genero": "Crónica Periodística",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "cp171.jpg"
        },
         {
            "codigo": "li172",
            "titulo": "Las Palabras Del Abuelo",
            "autor": "Conchita Penilla Cespedes",
            "genero": "Literatura Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "li172.jpg"
        },
         {
            "codigo": "ml173",
            "titulo": "America Cuenta Sus Mitos",
            "autor": "Flor Romero",
            "genero": "Mitologia, Leyendas",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "ml173.jpg"
        },
         {
            "codigo": "e174",
            "titulo": "Español 11 - Literatura Universal  Y Analisis Textual",
            "autor": "Editorial Santillana",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e174.jpg"
        },
         {
            "codigo": "e175",
            "titulo": "Los Caminos Del Saber: Lenguaje 8",
            "autor": "Editorial Santillana",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e175.jpg"
        },
         {
            "codigo": "E176",
            "titulo": "Español 3",
            "autor": "Equipo Editorial Santillana",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e176.jpg"
        },
         {
            "codigo": "li177",
            "titulo": "Los Pigemeos",
            "autor": "Nathaniel Hawthorne",
            "genero": "Literatura Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "li177.jpg"
        },
         {
            "codigo": "mc178",
            "titulo": "La Odisea",
            "autor": "Homero",
            "genero": "Mitologia Clásica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "mc178.jpg"
        },
         {
            "codigo": "a179",
            "titulo": "Padre Rico, Padre Pobre",
            "autor": "Robert Kiyosaki con Sharon Lechter",
            "genero": "Autoayuda",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "a179.jpg"
        },
         {
            "codigo": "ep180",
            "titulo": "Le Sanglot De L'homme Blanc",
            "autor": "Pascal Bruckner",
            "genero": "Ensayo Politico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "ep180.jpg"
        },
         {
            "codigo": "fh181",
            "titulo": "The Doctor's Wife",
            "autor": "Sawako Arriyoshi",
            "genero": "Ficcion Historica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "fh181.jpg"
        },
         {
            "codigo": "nc182",
            "titulo": "El Tercer Patio",
            "autor": "Adolfo Mendez Vides",
            "genero": "Novela Contemporanea",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "nc182.jpg"
        },
         {
            "codigo": "f103",
            "titulo": "The Hobbit",
            "autor": "J.R.R. Tolkien",
            "genero": "Fantasia",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "f103.jpg"
        },
         {
            "codigo": "f183",
            "titulo": "Harry Potter Y La Piedra Filosofal",
            "autor": "J.k. Rowling",
            "genero": "Fantasia",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "f183.jpg"
        },
         {
            "codigo": "cr184",
            "titulo": "Mujeres De Fuego",
            "autor": "Alonso Salazar J.",
            "genero": "Cronica Periodistica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "cr184.jpg"
        },
         {
            "codigo": "i185",
            "titulo": "La Tia Gigante",
            "autor": "Ivan Herrera Orsi",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i185.jpg"
        },
         {
            "codigo": "t186",
            "titulo": "Guia Turistica Arauca Colombia",
            "autor": "Mayra Alejandra Fuentes Rodriguez & Lizneira Roncancio Arias",
            "genero": "Turismo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "t186.jpg"
        },
         {
            "codigo": "e187",
            "titulo": "Test De Biologia Y Quimica(Enciclopedia Infantil)",
            "autor": "Julio Cesar Poveda",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e187.jpg"
        },
         {   
            "codigo": "i188",
            "titulo": "Disney Frozen",
            "autor": "Disney(El Gato de Hojalata)",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i188.jpg"
        },
         {
            "codigo": "li189",
            "titulo": "¡Y Todo Por Este Colegio!",
            "autor": "Juan Gomez",
            "genero": "Literatura Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "li189.jpg"
        },
         {
            "codigo": "lv190",
            "titulo": "Polish Cities",
            "autor": "Philip Ward",
            "genero": "Literatura de Viajes",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "lv190.jpg"
        },
         {
            "codigo": "e191",
            "titulo": "@prende A Prender 10-Matematicas(libro de contenidos)",
            "autor": "Equipo Pedagogico Editorial Norma",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e191.jpg"
        },
         {
            "codigo": "e192",
            "titulo": "@prende A Prender 10-Matematicas(Cuaderno de Ejercicios)",
            "autor": "Equipo Pedagogico Editorial Norma",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e192.jpg"
        },
         {
            "codigo": "e193",
            "titulo": "Gold Experience B1+(Student's Book)",
            "autor": "Fiona Beddall & Megan Roderick",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e193.jpg"
        },
         {
            "codigo": "e194",
            "titulo": "Desafios Comunicativos 8",
            "autor": "Equipo Editorial Santillana",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e194.jpg"
        },
         {
            "codigo": "e195",
            "titulo": "Desafios Comunicativos 9",
            "autor": "Equipo Editorial Santillana",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e195.jpg"
        },
         {
            "codigo": "nc196",
            "titulo": "Las Mil Y Una Noches",
            "autor": "Anonimo",
            "genero": "Narrativa Clasica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "nc196.jpg"
        },
         {
            "codigo": "li197",
            "titulo": "Soloman",
            "autor": "Ramon Garcia Dominguez",
            "genero": "Literatura Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "li197.jpg"
        },
         {
            "codigo": "li198",
            "titulo": "Piper Reed, Navy Brat",
            "autor": "Kimberly Willis Holt",
            "genero": "Literatura Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "li198.jpg"
        },
         {
            "codigo": "i199",
            "titulo": "Team Umizoomi:Playground Power",
            "autor": "Equipo Didactico Leapfrog Enterprise",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i199.jpg"
        },
         {
            "codigo": "i200",
            "titulo": "Charlie Y El Gran Ascensor",
            "autor": "Roald Dahl",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i200.jpg"
        },
         {
            "codigo": "m201",
            "titulo": "Mitos Griegos",
            "autor": "Mary Pope Osborne",
            "genero": "Mitologia",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "m201.jpg"
        },
         {
            "codigo": "lc202",
            "titulo": "Don Quijote De La Mancha",
            "autor": "Miguel De Cervantes Saavedra",
            "genero": "Literatura Clasica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "lc202.jpg"
        },
         {
            "codigo": "dc203",
            "titulo": "Antarctica-Land Of The Penguins",
            "autor": "Jonathan Y Angela Scott",
            "genero": "Divulgacion Cientifica",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "dc203.jpg"
        },
         {
            "codigo": "i204",
            "titulo": "La Cenicienta-Basado Cuento Clasico Tradicional",
            "autor": "Walt Disney",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i204.jpg"
        },
         {
            "codigo": "p205",
            "titulo": "Tecnicas De Motivacion Infantil En La Educacion(Tomo 3)",
            "autor": "Semira Thoumi",
            "genero": "Pedagogia",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "p205.jpg"
        },
         {
            "codigo": "i206",
            "titulo": "La Biblia Infantil",
            "autor": "Editorial Zamora",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i206.jpg"
        },
         {
            "codigo": "e207",
            "titulo": "Science(Delfines)",
            "autor": "Timothy Cooney Co-Autor Scott Fresman",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e207.jpg"
        },
         {
            "codigo": "e208",
            "titulo": "Mi Jardin Secreto:Enciclopedia Infantil(Destrezas Y Habilidades Manuales)",
            "autor": "Editorial Zamora",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e208.jpg"
        },
         {
            "codigo": "i209",
            "titulo": "El Arca De Noe",
            "autor": "Susanne Conrad Y Eva Montanari",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i209.jpg"
        },
         {
            "codigo": "i210",
            "titulo": "Alamat Ng Ampalaya(The Legend Of The Bitter Gound)",
            "autor": "Augie D. Rivera, Jr",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i210.jpg"
        },
         {
            "codigo": "e211",
            "titulo": "El Mundo Magico Del Ingles",
            "autor": "Editorial Zamora",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e211.jpg"
        },
         {
            "codigo": "e212",
            "titulo": "Gente Buena Para Un Mundo Mejor",
            "autor": "Colectivo( Gobernacion Del Valle Del Cauca-Diario Del Pais)",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e212.jpg"
        },
         {
            "codigo": "i213",
            "titulo": "Cuentos Fantasticos",
            "autor": "Anonimo",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i213.jpg"
        },
         {
            "codigo": "e214",
            "titulo": "El Nuevo Mundo De Los Niños(yo:Maquina Perfecta)",
            "autor": "Gustavo De Lorza Martinez",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e214.jpg"
        },
         {
            "codigo": "i215",
            "titulo": "Festiniño(Un Festival De Cuentos Y Actividades Para Los Niños)",
            "autor": "Varios Autores",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i215.jpg"
        },
         {
            "codigo": "cf216",
            "titulo": "Detectives Del ADN",
            "autor": "Angela Posada-Swafford",
            "genero": "Ciencia Ficcion",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "cf216.jpg"
        },
         {
            "codigo": "f217",
            "titulo": "El Pequeño Vampiro",
            "autor": "Angela Sommer-Bodenburg",
            "genero": "Fantasia",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "f217.jpg"
        },
         {
            "codigo": "i218",
            "titulo": "Una Cama Para Tres",
            "autor": "Yolanda Reyes",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i218.jpg"
        },
         {
            "codigo": "i219",
            "titulo": "Examen De Miedo",
            "autor": "Yolanda Reyes",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i219.jpg"
        },
         {
            "codigo": "nj220",
            "titulo": "Flora, La Desconocida Del Espacio",
            "autor": "Pierre-Marie Beaude",
            "genero": "Novela Juvenil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "nj220.jpg"
        },
         {
            "codigo": "e221",
            "titulo": "Lenguaje 9(Colegio Arquidiocesanos)",
            "autor": "Equipo Editorial Norma",
            "genero": "Educativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e221.jpg"
        },
         {
            "codigo": "n222",
            "titulo": "El Viejo Celular Y Otros Relatos",
            "autor": "Victor M. Almanza",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n222.jpg"
        },
         {
            "codigo": "n223",
            "titulo": "Verde Fue Mi Selva",
            "autor": "Edna Iturrable",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n223.jpg"
        },
         {
            "codigo": "i224",
            "titulo": "Horrible Histories:Villainous Victorians",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i224.jpg"
        },
         {
            "codigo": "d225",
            "titulo": "Escribir No Muerde",
            "autor": "Miguel Fernando Caro Gamboa",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d225.jpg"
        },
         {
            "codigo": "n226",
            "titulo": "Cuentos Para Niños Que Creen En Marcianos",
            "autor": "Jordi Sierra i Fabra",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n226.jpg"
        },
         {
            "codigo": "nj227",
            "titulo": "La Habitacion Del Lobo",
            "autor": "Gabriele Clima",
            "genero": "Novela Juvenil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "nj227.jpg"
        },
         {
            "codigo": "n228",
            "titulo": "Asmir No Quiere Pistolas",
            "autor": "Christobel Mattingley",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n228.jpg"
        },
         {
            "codigo": "n229",
            "titulo": "Una (Estupenda) Historia De Dragones Y Princesas(...Mas O Menos)",
            "autor": "Jordi Sierra i Fabra",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n229.jpg"
        },
         {
            "codigo": "i230",
            "titulo": "Disney Junior:Comic 1 Vampirina Y La Guardia Del Leon",
            "autor": "Disney",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i230.jpg"
        },
         {
            "codigo": "n231",
            "titulo": "A Proposito De La Novela Picaresa",
            "autor": "Anonimo",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n231.jpg"
        },
         {
            "codigo": "nj232",
            "titulo": "Momo",
            "autor": "Michael Ende",
            "genero": "Novela Juvenil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "nj232.jpg"
        },
         {
            "codigo": "n233",
            "titulo": "Cuentos Clasicos Bilingues:Caperucita Roja Y El Gato Con Botas",
            "autor": "Charles Perrault",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n233.jpg"
        },
         {
            "codigo": "i234",
            "titulo": "Cenicienta Disney",
            "autor": "Charles Perrault",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i234.jpg"
        },
         {
            "codigo": "d235",
            "titulo": "Tecnicas De La Motivacion Infantil En La Educacion Tomo1 (0 A 2 Años)",
            "autor": "Ediciones Gamma",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d235.jpg"
        },
         {
            "codigo": "d236",
            "titulo": "El Mundo Magico Del Ingles",
            "autor": "Editores Zamora",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d236.jpg"
        },
         {
            "codigo": "n237",
            "titulo": "Cuentos Fantasticos",
            "autor": "Anonimo",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n237.jpg"
        },
         {
            "codigo": "n238",
            "titulo": "La Biblia Infantil",
            "autor": "Editorial Zamora",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n238.jpg"
        },
         {
            "codigo": "f239",
            "titulo": "1984",
            "autor": "George Orwell",
            "genero": "Ficcion",
            "disponible_fisico": False,
            "archivo_interno": "f239.pdf",
            "imagen_portada": "f239.jpg"
        },
         {
            "codigo": "d240",
            "titulo": "Comunicacion Y Lenguaje 6",
            "autor": "Editorial Susaeta",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d240.jpg"
        },
         {
            "codigo": "f241",
            "titulo": "El Mundo Magico De Las Hadas",
            "autor": "Roberto Rosaspini Reynolds",
            "genero": "Fantasia",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "f241.jpg"
        },
         {
            "codigo": "d242",
            "titulo": "Mi Jardin:Enciclopedia-Infantil",
            "autor": "Editorial Zamora",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d242.jpg"
        },
         {
            "codigo": "n243",
            "titulo": "Oh, The Places You'll Go!",
            "autor": "Dr. Seuss Theodor Geisel",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n243.jpg"
        },
         {
            "codigo": "d244",
            "titulo": "El Mundo Mgico Del Ingles(Ch-i)",
            "autor": "Editorial Zamora",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d244.jpg"
        },
         {
            "codigo": "d245",
            "titulo": "Jugando Con La Plastilina-Seres Fantasticos Y Prehistoricos",
            "autor": "Editora Cultural Internacional",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d245.jpg"
        },
         {
            "codigo": "n246",
            "titulo": "El Duende Y Yo:Cuentos, Recuerdos Y Fantasias",
            "autor": "Alberto Jose Holguin Zamorano",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n246.jpg"
        },
         {
            "codigo": "d247",
            "titulo": "Horacio Y Los Opuestos",
            "autor": "Editorial Hola! Colina",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d247.jpg"
        },
         {
            "codigo": "i248",
            "titulo": "I Wonder Why Kangaroos Have Pouches",
            "autor": "Anonimo",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i248.jpg"
        },
         {
            "codigo": "m249",
            "titulo": "Los Heroes Y Los Dioses",
            "autor": "Andres Montañez",
            "genero": "Mitologia",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "m249.jpg"
        },
         {
            "codigo": "i250",
            "titulo": "Las Alergias(Guias Medicos)",
            "autor": "Robert J. Davies",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i250.jpg"
        },
         {
            "codigo": "n251",
            "titulo": "El Cocodrilo No Sirve, Es Dragon",
            "autor": "Francisco Hinojosa",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n251.jpg"
        },
         {
            "codigo": "n252",
            "titulo": "Nani Chocolate Y Paco Cuatrojos",
            "autor": "Nora Carbonell",
            "genero": "Narratvo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n252.jpg"
        },
         {
            "codigo": "e253",
            "titulo": "El Contacto Social",
            "autor": "Jean Jacques Rousseau",
            "genero": "Ensayo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "e253.jpg"
        },
         {
            "codigo": "n254",
            "titulo": "Tod Y Toby",
            "autor": "Walt Disney",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n254.jpg"
        },
         {
            "codigo": "n255",
            "titulo": "El Pequeño Nicolas",
            "autor": "Sempe/Goscinny",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n255.jpg"
        },
         {
            "codigo": "d256",
            "titulo": "Idioma Español 6:Comunicacion Y Lenguaje",
            "autor": "Editorial Susaeta",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d256.jpg"
        },
         {
            "codigo": "l257",
            "titulo": "Antologia Poetica",
            "autor": "Miguel Hernandez",
            "genero": "Lirico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "l257.jpg"
        },
         {
            "codigo": "d258",
            "titulo": "Avanza Lenguaje 11:Guia Para Docentes",
            "autor": "Editorial Norma",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d258.jpg"
        },
         {
            "codigo": "d259",
            "titulo": "Appleton's New Cuyas Dictionary",
            "autor": "The Grolier Society",
            "genero": "Diccionario",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d259.jpg"
        },
         {
            "codigo": "i260",
            "titulo": "El Milagro Metabolico",
            "autor": "Dr. Carlos Jaramillo",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i260.jpg"
        },
         {
            "codigo": "n261",
            "titulo": "The Wind Singer",
            "autor": "William Nicholson",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n261.jpg"
        },
         {
            "codigo": "i262",
            "titulo": "Horrible Histories:Woeful Second World War",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i262.jpg"
        },
         {
            "codigo": "i263",
            "titulo": "Horrible Histories:Frightful First World War",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i263.jpg"
        },
         {
            "codigo": "i264",
            "titulo": "Horrible Histories:Vile Victorians",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i264.jpg"
        },
         {
            "codigo": "i265",
            "titulo": "Horrible Histories:Gorgeous Georgians",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i265.jpg"
        },
         {
            "codigo": "i266",
            "titulo": "Horrible Histories:Terrible Tudors",
            "autor": "Terry Deary & Neil Tongue",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i266.jpg"
        },
         {
            "codigo": "i267",
            "titulo": "Horrible Histories:Measly Middle Ages",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i267.jpg"
        },
         {
            "codigo": "i268",
            "titulo": "Horrible Histories:Incredible Incas",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i268.jpg"
        },
         {
            "codigo": "i269",
            "titulo": "Horrible Histories:Angry Aztecs",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i269.jpg"
        },
         {
            "codigo": "i270",
            "titulo": "Horrible Histories:Stormin Normans",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i270.jpg"
        },
         {
            "codigo": "i271",
            "titulo": "Horrible Histories:Smashing Saxons",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i271.jpg"
       },
        {
            "codigo": "i272",
            "titulo": "Horrible Histories:Vicious Vikings",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i272.jpg"
        },
         {
            "codigo": "i273",
            "titulo": "Horrible Histories:Cut-Throat Celts",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i273.jpg"
        },
         {
            "codigo": "i274",
            "titulo": "Horrible Histories:Rotten Romans",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i274.jpg"
        },
         {
            "codigo": "i275",
            "titulo": "Horrible Hisories:Groovy Greeks",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i275.jpg"
        },
         {
            "codigo": "i276",
            "titulo": "Horrible Histories: Barmy British Empire",
            "autor": "Terry Deary",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i276.jpg"
        },
         {
            "codigo": "n277",
            "titulo": "El Principito",
            "autor": "Antoine Desaint-Exupery",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n277.jpg"
        },
         {
            "codigo": "n278",
            "titulo": "El Huevo De Colon",
            "autor": "Ramon Garcia Dominguez",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n278.jpg"
        },
         {
            "codigo": "n279",
            "titulo": "El Secuestro De Miss Blandish",
            "autor": "J. Hadley Chase",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n279.jpg"
        },
         {
            "codigo": "f280",
            "titulo": "Esopo,Iriarte Y Samaniego",
            "autor": "Esopo, Tomas Iriarte & Felix Samaniego",
            "genero": "Fabula",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "f280.jpg"
        },
         {
            "codigo": "d281",
            "titulo": "Nimba, La Nubecita Viajera",
            "autor": "Anibal Tobon",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d281.jpg"
        },
         {
            "codigo": "i282",
            "titulo": "Homicidio Y Compasion:La Eutanasia En Etica Clinica",
            "autor": "Jean Francois Malherbe",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i282.jpg"
        },
         {
            "codigo": "n283",
            "titulo": "El Mejor Enemigo Del Mundo",
            "autor": "Maria Fernanda Heredia",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n283.jpg"
        },
         {
            "codigo": "n284",
            "titulo": "Cuentos De Susana",
            "autor": "Francisco Montaña",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n284.jpg"
        },
         {
            "codigo": "d285",
            "titulo": "Collins Pocket:Diccionario Español/Ingles/English/Spanish",
            "autor": "Editorial Grijalbo",
            "genero": "Diccionario",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d285.jpg"
        },
         {
            "codigo": "d286",
            "titulo": "Diccionario Practico:Sinonimos Y Antonimos",
            "autor": "Fernando Corripio",
            "genero": "Diccionario",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d286.jpg"
        },
         {
            "codigo": "i287",
            "titulo": "Answers",
            "autor": "Mother Meera",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i287.jpg"
        },
         {
            "codigo": "i288",
            "titulo": "Transgenicos",
            "autor": "Luke Anderson",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i288.jpg"
        },
         {
            "codigo": "i289",
            "titulo": "Alimentacion Y Procedimientos Esteticos",
            "autor": "Health Project",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i289.jpg"
        },
         {
            "codigo": "n290",
            "titulo": "Un Milagro En Belen",
            "autor": "Tanja Jeschke & Sabine Waldmann-Brun",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n290.jpg"
        },
         {
            "codigo": "i291",
            "titulo": "Historia Del Mundo",
            "autor": "Editorial Salvat",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i291.jpg"
        },
         {
            "codigo": "n292",
            "titulo": "El Olvidado Asombro De Estar Vivo",
            "autor": "Jaime Homar",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n292.jpg"
        },
         {
            "codigo": "n293",
            "titulo": "Los Carasucias",
            "autor": "Libardo Duque Velez",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n293.jpg"
        },
         {
            "codigo": "d294",
            "titulo": "Roncar, roncar(Hala Y Observa)",
            "autor": "Editorial Sin Fronteras",
            "genero": "Didactico",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d294.jpg"
        },
         {
            "codigo": "i295",
            "titulo": "Mis 130 Apellidos",
            "autor": "Irene Vasco",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i295.jpg"
        },
         {
            "codigo": "n296",
            "titulo": "Les Miserables (Edicion Escolar-Frances)",
            "autor": "Victor Hugo",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n296.jpg"
        },
         {
            "codigo": "n297",
            "titulo": "Ida B",
            "autor": "Katherine Hannigan",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n297.jpg"
        },
         {
            "codigo": "p298",
            "titulo": "Antologia De Poesia Colombiana Para Jovenes",
            "autor": "Varios Autores",
            "genero": "Poesia",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "p298.jpg"
        },
         {
            "codigo": "n299",
            "titulo": "No Somos Irrompibles(12 Cuentos De Chicos Enamorados)",
            "autor": "Elsa Bornemann",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n299.jpg"
        },
         {
            "codigo": "i300",
            "titulo": "For Girls Only:Wise Words, Good Advice",
            "autor": "Carol Weston",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i300.jpg"
        },
         {
            "codigo": "i301",
            "titulo": "Mi Angel De La Guarda",
            "autor": "June Loves",
            "genero": "Infantil",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i301.jpg"
        },
         {
            "codigo": "a302",
            "titulo": "La Isla Del Tesoro",
            "autor": "Robert Louis Stevenson",
            "genero": "Aventuras",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "a302.jpg"
        },
         {
            "codigo": "n303",
            "titulo": "El Lugar Mas Bonito Del Mundo",
            "autor": "Ann Cameron",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n303.jpg"
        },
         {
            "codigo": "d304",
            "titulo": "Diccionario De Sinonimos Y Antonimos(Tomo 9)",
            "autor": "Educar Editores",
            "genero": "Diccionario",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "d304.jpg"
        },
         {
            "codigo": "n305",
            "titulo": "Tiempo Y Cosas",
            "autor": "Azorin(Jose Martinez Ruiz)",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n305.jpg"
        },
         {
            "codigo": "n306",
            "titulo": "La Orquesta Submarina Y Otros Relatos Juveniles",
            "autor": "Juan Fernando Merino",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n306.jpg"
        },
         {
            "codigo": "i307",
            "titulo": "Los Objetos Fractales",
            "autor": "Benoit Mandelbrot",
            "genero": "Informativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "i307.jpg"
        },
         {
            "codigo": "f308",
            "titulo": "Lo Que Una Vez Hicieron Los Alienigenas",
            "autor": "John Fotzgerald Torres",
            "genero": "ficcion",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "f308.jpg"
        },
         {
            "codigo": "n309",
            "titulo": "Regeneration(Ingles)",
            "autor": "Pat Barker",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n309.jpg"
        },
         {
            "codigo": "n310",
            "titulo": "Aunt Julia And The Scriptwriter(Ingles)",
            "autor": "Mario Vargas Llosa",
            "genero": "Narrativo",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "n310.jpg"
        },
         {
            "codigo": "",
            "titulo": "TÍTULO DEL LIBRO",
            "autor": "NOMBRE DEL AUTOR",
            "genero": "GÉNERO",
            "disponible_fisico": True,
            "archivo_interno": "",
            "imagen_portada": "xx240.jpg"
        },

        

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
st.title("📚 Biblioteca Porfirio Barba Jacob")
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

            st.markdown(titulo_con_hover(libro["titulo"].upper(), imagen), unsafe_allow_html=True)
            
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
