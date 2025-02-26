from PIL import Image, ImageDraw, ImageFont

def write_text_on_image(img_path, text, output_path, font_size=25, 
                        text_color=(250,250,250), bg_color=(25,25,25)):
    img = Image.open(img_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("./fonts/yes.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    img_width, img_height = img.size
    x = (img_width - text_width) / 2
    y = img_height - (img_height / 8) - (text_height / 2)
    margin = 10
    rect_coords = [x - margin, y - margin, x + text_width + margin, y + text_height + margin]
    draw.rectangle(rect_coords, fill=bg_color)
    draw.text((x, y), text, font=font, fill=text_color)
    img.save(output_path)
    return output_path