from flask import Flask, request, json, jsonify
from flask_cors import CORS
from google import genai


TOKEN = "AIzaSyBiMjXw11k30SPkcig8cTJbROT985hcfuE"
SYSTEM_INSTRUCTION = """Ты - чат-бот помощник в рамках приложения OpenWays.
OpenWays - доступная карта для людей с инвалидностью, где можно посмотреть доступность мест (специальные лифты, пандусы и т.д.),
а также проложить оптимальный маршрут с учётом особенностей конкретного человека.
Отвечай только по делу, а на все левые, не касающиеся OpenWays, инклюзии и доступности вопросы отвечай: Простите, я не могу Вам с этим помочь. Задавайте вопросы по теме, пожалуйста."""

client = genai.Client(api_key=TOKEN)


app = Flask(__name__)

# Включить CORS для всех источников
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})


@app.route("/", methods=["POST", "OPTIONS"])
def index():
    # Обработка preflight запросов
    if request.method == "OPTIONS":
        return "", 200
    
    try:
        query = request.json.get("query")
        
        if not query:
            return jsonify({"response": "Ошибка: пустой запрос"}), 400

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query,
            config={
                "system_instruction": SYSTEM_INSTRUCTION
            }
        )

        return jsonify({
            "response": response.text
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"response": f"Ошибка сервера: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
