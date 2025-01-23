import requests

# Credenciales de la API de 42
CLIENT_ID = "u-s4t2ud-71ad745c3ee922bda62aad88fde783c858e34511b41d645e9f640628f427b03e"
CLIENT_SECRET = "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"
USERNAME = "jvalle-d"  # Cambia esto a tu usuario en 42

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

# Actualiza el archivo README.md
def update_readme(user_data):
    level = user_data["cursus_users"][0]["level"]
    projects = len([p for p in user_data["projects_users"] if p["status"] == "finished"])
    achievements = len(user_data.get("achievements", []))

    with open("README.md", "w") as readme:
        readme.write("# Progreso en 42 Málaga\n\n")
        readme.write(f"**Nivel:** {level}\n\n")
        readme.write(f"**Proyectos completados:** {projects}\n\n")
        readme.write(f"**Logros obtenidos:** {achievements}\n\n")
        readme.write("¡Sigue adelante y conquista más retos en 42! 🚀")

# Flujo principal
if __name__ == "__main__":
    token = get_access_token()
    user_data = get_user_data(token)
    update_readme(user_data)
    print("Archivo README.md actualizado con éxito.")
