from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    raise SystemExit("Pillow is required. Install it with: python -m pip install pillow")

W = H = 1024
path = Path('assets/icons/app_icon.png')

# Create a text-based icon for "泡泡短剧" with a blue rounded-square look.
image = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# Soft shadow behind the rounded square
shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow)
shadow_draw.rounded_rectangle((70, 90, 954, 954), radius=220, fill=(18, 95, 220, 150))
shadow = shadow.filter(ImageFilter.GaussianBlur(radius=22))
image = Image.alpha_composite(image, shadow)

# Main rounded square background
background = Image.new('RGBA', (W, H), (0, 0, 0, 0))
background_draw = ImageDraw.Draw(background)
background_draw.rounded_rectangle((60, 80, 964, 964), radius=215, fill=(20, 118, 255, 255))

# Add a subtle inner highlight
highlight = Image.new('RGBA', (W, H), (0, 0, 0, 0))
highlight_draw = ImageDraw.Draw(highlight)
highlight_draw.rounded_rectangle((120, 140, 904, 904), radius=180, fill=(67, 162, 255, 110))
background = Image.alpha_composite(background, highlight)
image = Image.alpha_composite(image, background)

# White bubble-like badge for the title area
bubble = Image.new('RGBA', (W, H), (0, 0, 0, 0))
bubble_draw = ImageDraw.Draw(bubble)
bubble_draw.rounded_rectangle((210, 200, 814, 760), radius=110, fill=(255, 255, 255, 255))
image = Image.alpha_composite(image, bubble)

# Blue inner label area to create contrast for the text
label = Image.new('RGBA', (W, H), (0, 0, 0, 0))
label_draw = ImageDraw.Draw(label)
label_draw.rounded_rectangle((250, 250, 774, 700), radius=86, fill=(14, 92, 214, 255))
image = Image.alpha_composite(image, label)

# Text: 泡泡 / 短剧 (two lines)
font_candidates = [
    'C:/Windows/Fonts/msyh.ttc',
    'C:/Windows/Fonts/simhei.ttf',
    'C:/Windows/Fonts/msyhbd.ttc',
    '/System/Library/AssetsV2/com_apple_MobileAsset_Font/…',
]
font = None
for candidate in font_candidates:
    try:
        font = ImageFont.truetype(candidate, size=150)
        break
    except Exception:
        continue

if font is None:
    font = ImageFont.load_default()

lines = ['泡泡', '短剧']
text_color = (255, 255, 255, 255)
line_height = 170
line_widths = [draw.textbbox((0, 0), line, font=font)[2] for line in lines]
max_line_w = max(line_widths)
start_x = (W - max_line_w) / 2

# Center the text block inside the white box by raising it slightly.
start_y = 270

for index, line in enumerate(lines):
    line_x = start_x
    line_y = start_y + index * line_height
    if index == 1:
        line_y += 12
    # Draw shadowed text
    for offset in [(0, 8), (0, 4)]:
        shadow_text = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_text)
        shadow_draw.text((line_x + offset[0], line_y + offset[1]), line, font=font, fill=(24, 72, 176, 180))
        image = Image.alpha_composite(image, shadow_text)
    draw = ImageDraw.Draw(image)
    draw.text((line_x, line_y), line, font=font, fill=text_color)

# Optional soft white rings to make it logo-like
ring_draw = ImageDraw.Draw(image)
ring_draw.ellipse((120, 120, 904, 904), outline=(255, 255, 255, 110), width=12)

path.parent.mkdir(parents=True, exist_ok=True)
image.save(path, format='PNG')
print(f'generated {path}')
