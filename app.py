import os
import textwrap
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template_string, request, url_for
from PIL import Image, ImageDraw, ImageFont

APP_ROOT = Path(__file__).parent
GENERATED_DIR = APP_ROOT / "static" / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)

def create_image_from_prompt(prompt: str) -> str:
    """Create an image that visualises the prompt text."""
    width, height = 1024, 512
    background_color = (245, 245, 245)
    accent_color = (66, 135, 245)
    text_color = (33, 33, 33)

    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Draw a simple gradient rectangle as a decorative element
    for i in range(width):
        gradient_color = (
            accent_color[0],
            accent_color[1],
            int(accent_color[2] * (i / width)) + 50,
        )
        draw.line([(i, 0), (i, height // 2)], fill=gradient_color)

    # Draw prompt text on image
    font_size = 36
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    wrapped_prompt = "\n".join(textwrap.wrap(prompt, width=40)) or "(Trống)"
    text_width, text_height = draw.multiline_textsize(wrapped_prompt, font=font, spacing=8)

    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2 + height // 6
    draw.multiline_text((text_x, text_y), wrapped_prompt, fill=text_color, font=font, align="center", spacing=8)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{uuid.uuid4().hex}.png"
    file_path = GENERATED_DIR / filename
    image.save(file_path)
    return filename


@app.route("/", methods=["GET", "POST"])
def index():
    prompt = ""
    image_url = None

    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        image_name = create_image_from_prompt(prompt)
        image_url = url_for("static", filename=f"generated/{image_name}")

    return render_template_string(
        """
        <!doctype html>
        <html lang="vi">
        <head>
            <meta charset="utf-8">
            <title>Trình tạo ảnh từ prompt</title>
            <style>
                body { font-family: Arial, sans-serif; background: #f3f4f6; margin: 0; padding: 0; }
                main { max-width: 640px; margin: 40px auto; background: white; padding: 32px; border-radius: 16px; box-shadow: 0 20px 30px rgba(15, 23, 42, 0.1); }
                h1 { margin-top: 0; font-size: 2rem; color: #1f2937; }
                form { display: flex; flex-direction: column; gap: 16px; }
                textarea { min-height: 120px; padding: 12px; font-size: 1rem; border-radius: 8px; border: 1px solid #d1d5db; }
                button { align-self: flex-start; background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 1rem; cursor: pointer; }
                button:hover { background: #1d4ed8; }
                .result { margin-top: 24px; }
                img { max-width: 100%; border-radius: 12px; box-shadow: 0 10px 20px rgba(30, 41, 59, 0.15); }
                .prompt-preview { margin-top: 12px; font-style: italic; color: #4b5563; }
            </style>
        </head>
        <body>
            <main>
                <h1>Tạo ảnh từ prompt</h1>
                <p>Nhập mô tả (prompt) của bạn và ứng dụng sẽ tạo ra một ảnh minh hoạ chứa nội dung đó.</p>
                <form method="post">
                    <label for="prompt">Prompt</label>
                    <textarea id="prompt" name="prompt" placeholder="Ví dụ: hoàng hôn trên biển với con thuyền nhỏ" required>{{ prompt }}</textarea>
                    <button type="submit">Tạo ảnh</button>
                </form>
                {% if image_url %}
                <div class="result">
                    <h2>Kết quả</h2>
                    <img src="{{ image_url }}" alt="Ảnh tạo từ prompt">
                    <div class="prompt-preview">Prompt: {{ prompt or '(Trống)' }}</div>
                </div>
                {% endif %}
            </main>
        </body>
        </html>
        """,
        prompt=prompt,
        image_url=image_url,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
