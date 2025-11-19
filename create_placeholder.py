import os
from PIL import Image, ImageDraw, ImageFont

# Create directory
os.makedirs('static/images', exist_ok=True)

# Create 400x400 placeholder
img = Image.new('RGB', (400, 400), color='#e5e7eb')
draw = ImageDraw.Draw(img)

# Draw circle
draw.ellipse([50, 50, 350, 350], fill='#d1d5db', outline='#9ca3af', width=5)

# Add text
try:
    font = ImageFont.truetype("arial.ttf", 48)
except:
    font = ImageFont.load_default()

text = "No Logo"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (400 - text_width) / 2
y = (400 - text_height) / 2

draw.text((x, y), text, fill='#6b7280', font=font)

# Save
img.save('static/images/placeholder-logo.png')
print("✓ Placeholder logo created!")
