from PIL import Image, ImageDraw


def find_origin(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return int(round((334 - width) / 2))


def text_wrap(text, font, max_width=300):
    """
    Wraps text to fit within a given width.
    """
    lines = []
    if font.getbbox(text)[2] <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and font.getbbox(line + words[i])[2] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines