from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate', methods=['POST'])
def generate_site():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'Missing prompt'}), 400

    full_prompt = f"Generate a single-page HTML website with inline CSS based on: {prompt}"

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        html_code = response.choices[0].message.content.strip()
        lines = html_code.splitlines()

        if lines and lines[0].strip().startswith("```") and lines[-1].strip().startswith("```"):
            html_code = "\n".join(lines[1:-1]).strip()

        return jsonify({'html': html_code})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
