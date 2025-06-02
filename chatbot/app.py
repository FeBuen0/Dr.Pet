# chatbot_flask/app.py

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__,
            template_folder='./templates/',
            static_folder='./static/',
            root_path='./')

try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Chave da API do Google não encontrada. Defina GOOGLE_API_KEY no seu ambiente ou arquivo .env.")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Erro ao configurar a API do Gemini: {e}")



generation_config = {
  "temperature": 0.7, 
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048, 
}

safety_settings = [ 
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

try:
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", 
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
except Exception as e:
    print(f"Erro ao inicializar o modelo GenerativeModel: {e}")
    model = None 



def get_ai_response(user_message):
    if not model:
        return "Desculpe, o modelo de IA não está disponível no momento."


    prompt_template = f"""
    Você é o Dr.Pet, um chatbot veterinário amigável, prestativo e informativo.
    Sua especialidade é fornecer informações gerais e educativas sobre a saúde, bem-estar, comportamento, 
    e o sistema nervoso de animais de estimação (como cães e gatos).
    Seu tom deve ser calmo, empático e fácil de entender para leigos.

    IMPORTANTE:
    - Mantenha as respostas concisas e focadas na pergunta do usuário, mas informativas.
    - NÃO forneça diagnósticos médicos específicos.
    - NÃO prescreva tratamentos ou medicamentos.
    - Sempre recomende que o usuário consulte um veterinário real para problemas de saúde sérios, diagnósticos ou tratamentos.
    - Se a pergunta for muito complexa, fora do seu escopo (ex: mecânica quântica) ou pedir um diagnóstico, 
      gentilmente decline e reforce a necessidade de consultar um profissional veterinário.
    - Mantenha as respostas concisas e focadas na pergunta do usuário, mas informativas.
    - Responda de forma MUITO DIRETA e CONCISA. Vá direto ao ponto.
    - Evite introduções longas ou frases de preenchimento.
    - Forneça apenas a informação essencial para responder à pergunta.
    - Tente manter suas respostas em no máximo 2-3 frases curtas, sempre que possível.

    Pergunta do usuário: "{user_message}"

    Resposta do Dr.Pet:
    """
    
    try:

        response = model.generate_content(prompt_template)
        

        
        return response.text
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return "Desculpe, ocorreu um erro ao tentar processar sua pergunta com a IA. Tente novamente."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Nenhuma mensagem recebida'}), 400

    ai_reply = get_ai_response(user_message)
    return jsonify({'reply': ai_reply})


if __name__ == '__main__':
    app.run(debug=True)