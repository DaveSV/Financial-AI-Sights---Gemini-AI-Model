import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
# 1. Cambiamos la importación a la nueva librería recomendada
from google import genai

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# 2. Obtenemos tu API key personalizada
my_api_key_gemini = os.getenv('api_key_gemini')

# 3. Inicializamos el nuevo Cliente con tu API Key
# (Si tu variable de entorno se llamara exactamente GEMINI_API_KEY, podrías dejar Client() vacío)
client = genai.Client(api_key=my_api_key_gemini)

app = Flask(__name__)

# Definir el manejador de error 404 para redirigir a la página de inicio
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            prompt = request.form['prompt']
            question = prompt

            # 4. Modificamos la llamada usando el cliente, el submódulo 'models' y tu modelo gemma
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=question
            )

            # 5. La respuesta del SDK actual sigue exponiendo el atributo .text de forma directa
            if response.text:
                print(response.text)
                return response.text
            else:
                return "Sorry, but I think Gemini didn't want to answer that!"
        except Exception as e:
            print(f"Error detectado: {e}") # Añadido para que puedas auditar errores en la terminal
            return "Sorry, but Gemini didn't want to answer that!"

    return render_template('index.html', **locals())

if __name__ == '__main__':
    app.run(debug=True)

