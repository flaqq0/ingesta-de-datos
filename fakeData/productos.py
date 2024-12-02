import json
import random
from decimal import Decimal
from datetime import datetime, timedelta
from faker import Faker
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal  # Importar Decimal para DynamoDB

# Inicializar Faker
fake = Faker()

# Lista de tenants
tenants = ["uwu", "wong", "plazavea"]

# Categorías y marcas de productos electrónicos
categories = ["Smartphones", "Laptops", "Tablets", "Smartwatches", "Headphones", "Cameras"]
brands = {
    "Smartphones": ["Samsung", "Apple", "Xiaomi", "OnePlus", "Google"],
    "Laptops": ["Dell", "HP", "Apple", "Lenovo", "Asus"],
    "Tablets": ["Apple", "Samsung", "Lenovo", "Huawei"],
    "Smartwatches": ["Apple", "Samsung", "Fitbit", "Garmin"],
    "Headphones": ["Sony", "Bose", "JBL", "Beats", "Sennheiser"],
    "Cameras": ["Canon", "Nikon", "Sony", "Fujifilm", "Panasonic"]
}

# Salida
output_file_products = "productos.json"

# Conexión a DynamoDB
region_name = "us-east-1"  # Cambia esta región según tu configuración
dynamodb = boto3.resource("dynamodb", region_name=region_name)
table = dynamodb.Table("pf_productos")  # Cambia por el nombre de tu tabla

# Función para generar un precio aleatorio
def random_price():
    return Decimal(str(round(random.uniform(50, 3000), 2)))  # Convertir a Decimal

# Función para generar una fecha de lanzamiento aleatoria
def random_release_date():
    start_date = datetime.now() - timedelta(days=365 * 3)  # Hace hasta 3 años
    random_days = random.randint(0, 365 * 3)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

# Generar productos electrónicos
generated_product_ids = set()
products = []

for _ in range(1000):  # Generar 1000 productos
    tenant_id = random.choice(tenants)
    category = random.choice(categories)
    brand = random.choice(brands[category])

    # Generar un product_id único
    while True:
        product_id = f"product_{random.randint(1000, 99999)}"
        if product_id not in generated_product_ids:
            generated_product_ids.add(product_id)
            break

    product_name = f"{brand} {category[:-1]} {random.randint(100, 999)}"
    product_info = {
        "category": category,
        "release_date": random_release_date(),
        "features": fake.sentence(nb_words=8)
    }
    product_price = random_price()  # Generar precio como Decimal

    product = {
        "tenant_id": tenant_id,
        "product_id": product_id,
        "product_name": product_name,
        "product_brand": brand,
        "product_info": product_info,
        "product_price": product_price  # Asegurarse de que sea Decimal
    }
    products.append(product)

    # Subir cada producto a DynamoDB
    try:
        table.put_item(Item=product)
    except ClientError as e:
        print(f"Error al agregar producto {product_id}: {e.response['Error']['Message']}")

# Guardar en productos.json
with open(output_file_products, "w", encoding="utf-8") as outfile:
    # Convertir Decimal a str para guardar en JSON
    json.dump(products, outfile, ensure_ascii=False, indent=4, default=str)

print(f"Archivo '{output_file_products}' generado con éxito y los productos han sido subidos a DynamoDB.")
