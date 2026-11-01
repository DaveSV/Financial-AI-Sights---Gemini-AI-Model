import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from google import genai
from google.genai import types

load_dotenv()

my_api_key_gemini = os.getenv('api_key_gemini')
client = genai.Client(api_key=my_api_key_gemini)

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            # 1. Capturamos las instrucciones del usuario (prompt)
            prompt = request.form.get('prompt',
                                      'Haz un resumen ejecutivo, estructurado y analítico de este documento financiero.')

            # 2. Verificamos si el usuario subió un archivo
            file = request.files.get('financial_file')

            contents_payload = []

            if file and file.filename != '':
                # Leemos los bytes del archivo directamente en memoria
                file_bytes = file.read()
                mime_type = file.content_type

                # Preparamos el archivo en el formato que requiere el nuevo SDK de GenAI
                financial_doc = types.Part.from_bytes(
                    data=file_bytes,
                    mime_type=mime_type
                )
                contents_payload.append(financial_doc)

            # Añadimos el prompt de texto al contenido enviado al modelo
            contents_payload.append(prompt)

            # Si no hay prompt ni archivo, devolvemos un aviso
            if len(contents_payload) == 0 or (len(contents_payload) == 1 and prompt == ''):
                return "Por favor, escribe una pregunta o sube un documento financiero."

            # 3. Llamamos al modelo gratuito recomendado
            response = client.models.generate_content(
                model='gemini-3.5-flash-lite',
                contents=contents_payload
            )

            if response.text:
                return response.text
            else:
                return "Lo siento, la IA no pudo procesar o interpretar el documento."

        except Exception as e:
            print(f"Error en el servidor: {e}")
            return f"Hubo un inconveniente al procesar tu solicitud: {str(e)}"

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
