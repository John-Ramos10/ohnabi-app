import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import tempfile
import os
import requests
from PIL import Image
import io
import random


st.set_page_config(page_title="ohnabi 💖", page_icon="💖", layout="centered")

st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #fff0f5 0%, #ffe6f2 100%);
    }
    .block-container {
        padding-top: 2rem;
        max-width: 700px;
    }
    h1, h2, h3 {
        text-align: center;
        color: #ff4d88;
        font-family: 'Arial', sans-serif;
        margin-bottom: 0.5em;
    }
    .card {
        background: none;
        border-radius: 15px;
        padding: 0;
        margin-bottom: 1.5em;
        text-align: center;
    }
    .card-title {
        background: #ffe6f2;
        border-radius: 25px;
        padding: 0.7em 2em;
        margin-bottom: 1em;
        color: #ff4d88;
        font-size: 1.4em;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 2px 12px #ffb3d1;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 2px 12px #ffb3d1; transform: translateY(0px); }
        50% { box-shadow: 0 8px 32px #ff99cc; transform: translateY(-2px); }
        100% { box-shadow: 0 2px 12px #ffb3d1; transform: translateY(0px); }
    }
    .stButton button {
        background: linear-gradient(90deg, #ff99cc 0%, #ff4d88 100%);
        color: white;
        border-radius: 10px;
        padding: 0.45em 1.0em;
        font-weight: bold;
        border: none;
        box-shadow: 0 2px 8px #ffb3d1;
    }
    .gallery-img {
        border-radius: 15px;
        box-shadow: 0 2px 12px #ffb3d1;
        margin: 8px 0;
    }
    .centered {
        display:flex;
        justify-content:center;
        align-items:center;
    }
    .small-muted { font-size:0.9em; color:#a33a67; }
    </style>
""", unsafe_allow_html=True)


ruta_credenciales = "C:/Users/John/OneDrive/Documentos/ohnabi/stone-botany-423821-g9-a2dd01bdd56f.json"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
credenciales = ServiceAccountCredentials.from_json_keyfile_name(ruta_credenciales, scope)
cliente = gspread.authorize(credenciales)
hoja = cliente.open("ohnabi").sheet1 

gauth = GoogleAuth()
gauth.DEFAULT_SETTINGS['client_config_file'] = os.path.join(os.path.dirname(__file__), "client_secrets.json")
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)

def sheet_rows():
    """Devuelve todas las filas (incluyendo encabezado si existe)."""
    return hoja.get_all_values()

def append_row(values):
    hoja.append_row(values)

def update_cell(row_idx, col_idx, value):

    hoja.update_cell(row_idx, col_idx, value)

def delete_row(row_idx):
    hoja.delete_rows(row_idx)

def find_rows_by_prefix(prefix):
    """Busca filas donde la primera columna empieza con prefix."""
    filas = sheet_rows()
    resultados = []
    for i, fila in enumerate(filas, start=1):
        if len(fila) >= 1 and fila[0].startswith(prefix):
            resultados.append((i, fila))
    return resultados

def obtener_fotos():
    filas = sheet_rows()
    fotos = []
    for i, fila in enumerate(filas, start=1):
        if len(fila) >= 2 and "Foto" in fila[0]:
            fotos.append((i, fila[0], fila[1]))
    return fotos

def construir_enlace_drive(enlace_o_id):
    """Recibe un enlace (o id) y devuelve un enlace directo a la imagen en Drive."""
    if not enlace_o_id:
        return None
    if "id=" in enlace_o_id:
        id_archivo = enlace_o_id.split("id=")[-1].strip()
    elif "/d/" in enlace_o_id:
        id_archivo = enlace_o_id.split("/d/")[1].split("/")[0].strip()
    else:
        id_archivo = enlace_o_id.strip()

    return f"https://drive.google.com/uc?export=download&id={id_archivo}"

def mostrar_imagen_por_enlace(enlace, caption=""):
    """Muestra imagen desde un enlace de Drive, asegurando compatibilidad."""
    try:
        resp = requests.get(enlace)
        if resp.status_code == 200:
            img = Image.open(io.BytesIO(resp.content))
            st.image(img, caption=caption, use_container_width=True)
        else:
            st.warning(f"No se pudo cargar la imagen ({resp.status_code})")
    except Exception as e:
        st.error(f"Error cargando imagen: {e}")


PASSWORD = "ohnabi2703" 

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h2 style='text-align:center;'>🔐 Ingresa la contraseña</h2>", unsafe_allow_html=True)

    cols = st.columns([1,2,1])
    with cols[1]:
        pwd = st.text_input("", type="password", placeholder="Escribe la contraseña...", key="pwd_input")
        if st.button("Entrar 💖"):
            if pwd == PASSWORD:
                st.session_state.auth = True
                st.success("Bienvenido 💕")
                st.rerun()
            else:
                st.error("Contraseña incorrecta 💔")
    st.stop()


fecha_inicio = datetime(2025, 3, 27)
aniversario = datetime(2026, 3, 27)
cumple_ella = datetime(2026, 2, 17)
primer_encuentro = datetime(2024, 12, 4)
primer_beso = datetime(2024, 12, 4)
cumple_tuyo = datetime(2026, 5, 10)

hoy = datetime.now()
dias_juntos = (hoy.date() - fecha_inicio.date()).days
diferencia = relativedelta(hoy, fecha_inicio)
meses_juntos = diferencia.years * 12 + diferencia.months
proximo_mes = meses_juntos + 1
fecha_proximo_mes = fecha_inicio + relativedelta(months=proximo_mes)
dias_para_proximo_mes = (fecha_proximo_mes.date() - hoy.date()).days
dias_1_anio = (aniversario.date() - hoy.date()).days
dias_cumple_ella = (cumple_ella.date() - hoy.date()).days

st.markdown("<h1>ohnabi 💖</h1>", unsafe_allow_html=True)
st.markdown(f"<h2>Llevamos <span style='color:#ff4d88'>{dias_juntos}</span> días juntos 🥰</h2>", unsafe_allow_html=True)
st.markdown("---")


def init_session():
    if "imagenes_subidas" not in st.session_state:
        st.session_state.imagenes_subidas = set()
    if "edit_frase_row" not in st.session_state:
        st.session_state.edit_frase_row = None
    if "edit_nota_row" not in st.session_state:
        st.session_state.edit_nota_row = None
    if "edit_mensaje_row" not in st.session_state:
        st.session_state.edit_mensaje_row = None
    if "num_secreto" not in st.session_state:
        st.session_state.num_secreto = random.randint(1, 10)
    if "ppp_choice" not in st.session_state:
        st.session_state.ppp_choice = None
    if "ruleta_pregunta" not in st.session_state:
        st.session_state.ruleta_pregunta = None
    if "ruleta_respuesta" not in st.session_state:
        st.session_state.ruleta_respuesta = ""

init_session()


tab_frases, tab_notas, tab_mensajes, tab_galeria, tab_juegos, tab_fechas, tab_deseos = st.tabs(
    ["💬 Frases", "💌 Notitas", "💜 Mensajes", "📷 Galería", "🎮 Juegos", "📅 Fechas", "🎁 Lista deseos"]
)


with tab_frases:
    st.markdown("<div class='card'><div class='card-title'>Frases favoritas 💬</div></div>", unsafe_allow_html=True)
    remitente_frase = st.selectbox("¿Quién sube la frase?", ["John", "Abi"], key="remitente_frase")
    nueva_frase = st.text_input("Escribe una frase especial", key="frase_nueva")
    if st.button("Guardar frase 💬"):
        if nueva_frase.strip():
            append_row([f"{remitente_frase} dice:", nueva_frase])
            st.success("¡Frase guardada!")
            st.rerun()
        else:
            st.warning("Escribe algo antes de guardar.")


    filas = sheet_rows()
    st.markdown("#### Frases guardadas:")
    for i, fila in enumerate(filas, start=1):
        if len(fila) >= 2:
            first = fila[0]
            second = fila[1]
            if any(tag in first for tag in ["Foto", "Nota", "Mensaje", "Deseo"]):
                continue

            cols = st.columns([6,1,1])
            with cols[0]:
                st.info(f"**{first}** {second}")

            with cols[1]:
                if st.button("Editar", key=f"edit_frase_{i}"):
                    st.session_state.edit_frase_row = i
                    st.session_state.edit_frase_text = second
                    st.rerun()
            with cols[2]:
                if st.button("Borrar", key=f"del_frase_{i}"):
                    delete_row(i)
                    st.session_state.edit_frase_row = None
                    st.session_state.edit_frase_text = ""
                    st.success("Frase eliminada 💥")
                    st.rerun()


    if st.session_state.edit_frase_row:
        row_idx = st.session_state.edit_frase_row
        nuevo_texto = st.text_input("Editar frase:", value=st.session_state.get("edit_frase_text", ""), key="fr_edit_input")
        if st.button("💾 Guardar frase editada"):
            update_cell(row_idx, 2, nuevo_texto)
            st.session_state.edit_frase_row = None
            st.session_state.edit_frase_text = ""
            st.success("Frase editada ✅")
            st.rerun()


with tab_notas:
    st.markdown("<div class='card'><div class='card-title'>Notita 💌</div></div>", unsafe_allow_html=True)
    remitente_nota = st.selectbox("¿Quién manda la nota?", ["John", "Abi"], key="remitente_nota")
    nueva_nota = st.text_area("Escribe tu nota aquí", key="nota_nueva")
    if st.button("Enviar notita 💌"):
        if nueva_nota.strip():
            append_row([f"Nota de {remitente_nota}", nueva_nota])
            st.success("¡Notita enviada!")
            st.rerun()
        else:
            st.warning("¡Escribe algo bonito antes de enviar!")

    st.markdown("#### Notitas guardadas:")
    notas = find_rows_by_prefix("Nota")
    for (row_idx, fila) in notas:
        contenido = fila[1] if len(fila) >= 2 else ""
        cols = st.columns([6,1,1])
        with cols[0]:
            st.info(f"**{fila[0]}** {contenido}")
        with cols[1]:
            if st.button("Editar", key=f"edit_nota_{row_idx}"):
                st.session_state.edit_nota_row = row_idx
                st.session_state.edit_nota_text = contenido
                st.rerun()
        with cols[2]:
            if st.button("Borrar", key=f"del_nota_{row_idx}"):
                delete_row(row_idx)

                st.session_state.edit_nota_row = None
                st.session_state.edit_nota_text = ""
                st.success("Notita eliminada 💥")
                st.rerun()


    if st.session_state.edit_nota_row:
        r = st.session_state.edit_nota_row
        nuevo = st.text_area("Editar notita:", value=st.session_state.get("edit_nota_text", ""), key="nota_edit_input")
        if st.button("💾 Guardar nota editada"):
            update_cell(r, 2, nuevo)
            st.session_state.edit_nota_row = None
            st.session_state.edit_nota_text = ""
            st.success("Notita editada ✅")
            st.rerun()

with tab_mensajes:
    st.markdown("<div class='card'><div class='card-title'>Mensaje bonito 💜</div></div>", unsafe_allow_html=True)
    remitente_mensaje = st.selectbox("¿Quién manda el mensaje?", ["John", "Abi"], key="remitente_mensaje")
    nuevo_mensaje = st.text_area("Escribe tu mensaje bonito aquí", key="mensaje_nuevo")
    if st.button("Enviar mensaje 💜"):
        if nuevo_mensaje.strip():
            append_row([f"Mensaje de {remitente_mensaje}", nuevo_mensaje])
            st.success("¡Mensaje enviado!")
            st.rerun()
        else:
            st.warning("¡Escribe algo bonito antes de enviar!")

    st.markdown("#### Mensajes guardados:")
    mensajes = find_rows_by_prefix("Mensaje")
    for (row_idx, fila) in mensajes:
        contenido = fila[1] if len(fila) >= 2 else ""
        cols = st.columns([6,1,1])
        with cols[0]:
            st.success(f"**{fila[0]}** {contenido}")
        with cols[1]:
            if st.button("Editar", key=f"edit_msg_{row_idx}"):
                st.session_state.edit_mensaje_row = row_idx
                st.session_state.edit_mensaje_text = contenido
                st.rerun()
        with cols[2]:
            if st.button("Borrar", key=f"del_msg_{row_idx}"):
                delete_row(row_idx)

                st.session_state.edit_mensaje_row = None
                st.session_state.edit_mensaje_text = ""
                st.success("Mensaje eliminado 💥")
                st.rerun()

    if st.session_state.edit_mensaje_row:
        r = st.session_state.edit_mensaje_row
        nuevo = st.text_area("Editar mensaje:", value=st.session_state.get("edit_mensaje_text", ""), key="msg_edit_input")
        if st.button("💾 Guardar mensaje editado"):
            update_cell(r, 2, nuevo)
            st.session_state.edit_mensaje_row = None
            st.session_state.edit_mensaje_text = ""
            st.success("Mensaje editado ✅")
            st.rerun()

with tab_galeria:
    st.markdown("<div class='card'><div class='card-title'>Galería de fotos 📷</div></div>", unsafe_allow_html=True)
    remitente_foto = st.selectbox("¿Quién sube la foto?", ["John", "Abi"], key="remitente_foto")
    imagenes = st.file_uploader("", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="file_uploader")

    if "imagenes_subidas" not in st.session_state:
        st.session_state.imagenes_subidas = set()

    if imagenes:
        st.markdown("¿Listo para subir las fotos seleccionadas?")
        if st.button("📤 Subir fotos a la galería"):
            filas_existentes = sheet_rows()
            enlaces_existentes = [fila[1].strip() for fila in filas_existentes if len(fila) >= 2]
            for img in imagenes:
                if img.name in st.session_state.imagenes_subidas:
                    continue

                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(img.read())
                    tmp_file.flush()
                    archivo_drive = drive.CreateFile({'title': img.name})
                    archivo_drive.SetContentFile(tmp_file.name)
                    archivo_drive.Upload()
                    archivo_drive.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
                    enlace = construir_enlace_drive(archivo_drive['id'])
                if enlace not in enlaces_existentes:
                    append_row([f"Foto subida por {remitente_foto}", enlace])
                    st.session_state.imagenes_subidas.add(img.name)
                    st.success(f"¡Foto '{img.name}' guardada en la galería!", icon="✅")
                else:
                    st.warning(f"La imagen '{img.name}' ya fue subida antes. No se duplicó.")

    st.markdown("#### Fotos guardadas:")
    fotos = obtener_fotos()
    if not fotos:
        st.info("Aún no hay fotos. Sube una para ver la galería 💖")
    for (row_idx, texto, enlace) in fotos:
        mostrar_imagen_por_enlace(enlace, caption=texto)
        cols = st.columns([1,1,6])
        if cols[0].button("🗑️ Eliminar", key=f"del_foto_{row_idx}"):

            try:

                if "id=" in enlace:
                    id_archivo = enlace.split("id=")[-1].strip()
                elif "/d/" in enlace:
                    id_archivo = enlace.split("/d/")[1].split("/")[0].strip()
                else:
                    id_archivo = enlace.strip()
                archivo = drive.CreateFile({'id': id_archivo})
                archivo.Delete()
            except Exception:
                pass
            delete_row(row_idx)
            st.success("Imagen eliminada correctamente 💥")
            st.rerun()


with tab_juegos:
    st.markdown("<div class='card'><div class='card-title'>Juegos 🎮</div></div>", unsafe_allow_html=True)
    juego = st.selectbox("🎯 ¿Cuál quieres jugar hoy?", ["Adivina el número", "Piedra, papel o tijera", "Ruleta de preguntas", "Adivinanzas"], key="juego_seleccionado")

    if juego == "Adivina el número":
        intento = st.number_input("🔢 Adivina el número (1-10)", min_value=1, max_value=10, step=1, key="intento_num")
        if st.button("✨ Probar suerte", key="btn_adivinar"):
            if intento == st.session_state.num_secreto:
                st.success("🎉 ¡Bien hecho! Has adivinado el número secreto.")
                st.session_state.num_secreto = random.randint(1, 10)
            else:
                st.warning("💭 No es ese número... inténtalo de nuevo 💕")

    elif juego == "Piedra, papel o tijera":
        opciones = ["🪨 Piedra", "📄 Papel", "✂️ Tijera"]
        eleccion = st.radio("🕹️ Elige tu jugada", opciones, key="jugada_usuario")
        if st.button("💥 Jugar", key="btn_jugar"):
            pc = random.choice(opciones)
            st.write(f"La compu eligió: {pc}")
            if eleccion == pc:
                st.info("🤝 ¡Empate!")
            elif (eleccion == "🪨 Piedra" and pc == "✂️ Tijera") or \
                 (eleccion == "📄 Papel" and pc == "🪨 Piedra") or \
                 (eleccion == "✂️ Tijera" and pc == "📄 Papel"):
                st.success("🏆 ¡Ganaste!")
            else:
                st.error("😢 ¡Perdiste!")

    elif juego == "Ruleta de preguntas":
        preguntas = [
            "¿Qué fue lo primero que pensaste de mí?",
            "¿Cuál es tu recuerdo favorito juntos?",
            "Si pudieras describirme en 3 palabras, ¿cuáles serían?",
            "¿Qué viaje sueñas hacer conmigo?",
            "¿Cuál es nuestro lugar favorito?",
            "¿Qué te hace sonreír de mí?"
        ]
        if st.button("🎡 Girar ruleta"):
            st.session_state.ruleta_pregunta = random.choice(preguntas)
            st.session_state.ruleta_respuesta = ""  

        if st.session_state.ruleta_pregunta:
            st.info(st.session_state.ruleta_pregunta)
            st.text_area("✍️ Tu respuesta:", key="ruleta_respuesta_input", value=st.session_state.get("ruleta_respuesta", ""))
            if st.button("💾 Guardar respuesta a la ruleta"):
                resp_text = st.session_state.get("ruleta_respuesta_input", "").strip()
                if resp_text:
                    append_row([f"Respuesta a ruleta", resp_text])
                    st.success("Respuesta guardada 💕")
                    st.session_state.ruleta_pregunta = None
                    st.session_state.ruleta_respuesta = ""
                    st.rerun()
                else:
                    st.warning("Escribe algo antes de guardar.")

    elif juego == "Adivinanzas":
        adivinanzas = {
            "Blanca por dentro, verde por fuera. Si quieres que te lo diga, espera.": "pera",
            "Vuelo de noche, duermo en el día y nunca verás plumas en ala mía.": "murciélago",
            "Cuanto más lavo, más sucia quedo.": "agua",
            "No es cabeza, pero tiene pecas; no es rana, pero salta en charcas.": "sapo",
            "Si lo pones en una mano te sobra un palmo. Es fuerte, sano y peludo y a caricias lo calmas.":"un gato",
            "Oro parece, plata no es. ¿Qué es?": "plátano",
            "Tiene agujas pero no pincha, da la hora pero no es reloj.": "el pino",
            "Largo, largo como un camino, y no tiene ni pies ni manos.":
            "El río",
            "Blanca por dentro, verde por fuera. Si quieres que te lo diga, espera.": "La pera",
            "Vuelo de noche, duermo en el día y nunca verás plumas en ala mía.": "El murciélago",
            "Cuanto más lavo, más sucia quedo.": "El agua",
            "No es cabeza, pero tiene pecas; no es rana, pero salta en charcas.": "El sapo",
            "Es suave por dentro y peludo por fuera. Con un poco de esfuerzo, lo podrás meter dentro.":"un calcetin"
        }
        enigma, respuesta = random.choice(list(adivinanzas.items()))
        st.write(enigma)
        intento_adv = st.text_input("Tu respuesta:", key="adv_input")
        if st.button("Responder", key="btn_adv"):
            if intento_adv.strip().lower() == respuesta:
                st.success("¡Correcto! 🎉")
            else:
                st.error("Casi... intenta otra vez 💔")

with tab_fechas:
    st.markdown("<div class='card'><div class='card-title'>Fechas especiales</div></div>", unsafe_allow_html=True)
    if st.button("Ver fechas especiales"):
        st.markdown("**Aniversario:** 27/03/2025 💓")
        st.markdown("**Cumpleaños de Abi:** 17/02/2006 🎂")
        st.markdown("**Primer encuentro:** 4/12/2024 💞")
        st.markdown("**Primer beso:** 4/12/2024 💋")
        st.markdown("**Cumpleaños de John:** 10/05/2005 🎉")

with tab_deseos:
    st.markdown("<div class='card'><div class='card-title'>Lista de deseos 🎁</div></div>", unsafe_allow_html=True)
    nuevo_deseo = st.text_input("Agrega algo que quieran hacer juntos", key="deseo_nuevo")
    if st.button("➕ Añadir deseo"):
        if nuevo_deseo.strip():
            append_row(["Deseo", nuevo_deseo])
            st.success("Deseo añadido 🎉")
            st.rerun()
        else:
            st.warning("Escribe algo antes de agregar.")

    st.markdown("#### Deseos guardados:")
    deseos = find_rows_by_prefix("Deseo")
    for (row_idx, fila) in deseos:
        contenido = fila[1] if len(fila) >= 2 else ""
        cols = st.columns([6,1])
        with cols[0]:
            st.write(f"💡 {contenido}")
        with cols[1]:
            if st.button("Borrar", key=f"del_deseo_{row_idx}"):
                delete_row(row_idx)
                st.success("Deseo eliminado 💥")
                st.rerun()


st.markdown("---")
st.markdown("""
<div class="card">
    <div class="card-title">Nuestras músicas favoritas 🎶</div>
</div>
""", unsafe_allow_html=True)

with st.expander("🎶 Nuestras músicas favoritas", expanded=True):
    canciones = {
        "Nuestra canción 💖": "https://www.youtube.com/embed/MldGX_mbS-o",
        "La que siempre cantamos juntos 🎤": "https://www.youtube.com/embed/FMav-RAXQ4E"
    }

    seleccion = st.selectbox("Elige una canción para escuchar", list(canciones.keys()), key="cancion_seleccionada")
    link = canciones[seleccion]

    st.markdown(f"▶️ <b>{seleccion}</b>", unsafe_allow_html=True)
    st.markdown(f"""
        <iframe class='gallery-img' width='100%' height='150' src='{link}' frameborder='0'
        allow='autoplay; encrypted-media' allowfullscreen></iframe>
    """, unsafe_allow_html=True)

