from flask import Flask, request, jsonify
import openai
import os
import re

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate', methods=['POST'])
def generate_site():
    data = request.get_json()
    print("=== RAW POST DATA ===", data)  # This will log the whole JSON
    prompt = data.get('prompt', '')
    prompt2 = """
    Create a single-page business website described by {prompt}
    The page should include at a minimum:
    - A hero section with a catchy headline and call-to-action button.
    - An 'About Us' section with a short paragraph.
    - A 'Services' section with three service cards.
    - A 'Contact' section with a simple contact form.
    Add any other pages or colors or menu items the user requests in {prompt}
    Use a clean, modern, responsive design with colors inspired by {prompt}.
    Write all HTML and CSS in a single file using inline <style> tags. 
    Do not include any explanations — output only the HTML code.
    """

    if not prompt:
        return jsonify({'error': 'Missing prompt'}), 400

    full_prompt = f"Generate a single-page HTML website with inline CSS based on: {prompt2}"

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

        raw_content = response.choices[0].message.content.strip()
        print("=== RAW AI RESPONSE ===")
        print(raw_content)

        # Extract only the HTML code block if present
        match = re.search(r"```(?:html)?\s*(.*)```", raw_content, re.DOTALL)
        if match:
            html_code = match.group(1).strip()
        else:
            html_code = raw_content  # fallback if no code block is found

        return jsonify({'html': html_code})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
