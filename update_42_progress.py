import os
import requests
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Credenciales de la API de 42
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USERNAME = "jvalle-d"

# URLs de la API
AUTH_URL = "https://api.intra.42.fr/oauth/token"
USER_URL = f"https://api.intra.42.fr/v2/users/{USERNAME}"

# Función para obtener el token de acceso
def get_access_token():
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(AUTH_URL, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Error al obtener el token:", response.json())
        exit(1)

# Función para obtener los datos del usuario
def get_user_data(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(USER_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener los datos del usuario:", response.json())
        exit(1)

# Función para actualizar o reemplazar la sección del README.md
def update_readme(user_data):
    level = user_data["cursus_users"][0]["level"]
    projects = len([p for p in user_data["projects_users"] if p["status"] == "finished"])
    achievements = len(user_data.get("achievements", []))

    # Obtener el último proyecto entregado
    finished_projects = [
        p for p in user_data["projects_users"]
        if p["status"] == "finished" and p["validated?"] is not None
    ]
    finished_projects.sort(key=lambda p: p["updated_at"], reverse=True)
    last_finished_project = finished_projects[0] if finished_projects else None

    # Leer el contenido actual del README.md
    with open("README.md", "r") as readme:
        current_content = readme.read()

    # Crear la nueva sección de progreso
    new_progress_section = f"""
# Mi progreso en 42 Málaga 🎓🚀

**Nivel:** {level} 💯

**Proyectos completados:** {projects} ✅

**Logros obtenidos:** {achievements} 🏆
"""
    if last_finished_project:
        new_progress_section += f"\n**Último proyecto entregado:** {last_finished_project['project']['name']} 🏅\n"

    # Reemplazar la sección existente con la nueva
    if "# Mi progreso en 42 Málaga" in current_content:
        current_content = current_content.replace(
            current_content.split("# Mi progreso en 42 Málaga")[1].split("#")[0],  # Detecta la sección a reemplazar
            new_progress_section.strip()
        )
    else:
        # Si no existe, añadir la nueva sección
        current_content = new_progress_section + "\n" + current_content

    # Agregar el título "jvalle-d" con un emoticono al principio del README
    title = "# jvalle-d 👨‍💻"
    current_content = title + "\n" + current_content

    # Agregar el gif final al final del README
    gif = "![Final Gif](https://i.pinimg.com/originals/90/70/32/9070324cdfc07c68d60eed0c39e77573.gif)"
    current_content += f"\n\n{gif}"

    # Escribir el contenido actualizado en el README.md
    with open("README.md", "w") as readme:
        readme.write(current_content)
    
    print("README.md actualizado con éxito.")

# Flujo principal
if __name__ == "__main__":
    token = get_access_token()
    user_data = get_user_data(token)
    update_readme(user_data)
