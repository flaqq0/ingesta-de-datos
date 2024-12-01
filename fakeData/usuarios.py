import json
import random
from datetime import datetime, timedelta
from faker import Faker
import hashlib

# Inicializar Faker
fake = Faker()

# Lista de tenants y sus dominios
tenants = [
    "plazavea",
    "uwu",
    "wong"
]

# Salida
output_file_users = "usuarios.json"

# Generar contraseña hasheada
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def random_date():
    start_date = datetime.now() - timedelta(days=30)
    random_days = random.randint(0, 30)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d %H:%M:%S")

# Generar datos para 10,000 usuarios
generated_user_ids = set()

users = []
for _ in range(10000):
    tenant_id = random.choice(tenants)

    while True:
        user_id = f"user_{random.randint(1000, 9999)}"
        if user_id not in generated_user_ids:
            generated_user_ids.add(user_id)
            break
    password = hash_password(fake.password(length=12))
    
    user = {
        "tenant_id": tenant_id,
        "user_id": user_id,
        "password": password,
        "creation_date": random_date()
    }
    users.append(user)

# Guardar en users.json
with open(output_file_users, "w", encoding="utf-8") as outfile:
    json.dump(users, outfile, ensure_ascii=False, indent=4)

print(f"Archivo '{output_file_users}' generado con éxito.")