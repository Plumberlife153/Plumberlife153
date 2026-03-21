"""
Generate a Facebook ad video (animated GIF) for Plumberlife153 Emergency Plumbing.
Facebook recommended video specs: 1080x1080 (square) or 1080x1920 (vertical).
We'll use 1080x1080 square format for maximum compatibility.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# --- Configuration ---
COMPANY_NAME = "MGK PLUMBING"
TAGLINE = "Emergency Plumbing Services"
SERVICES = [
    "24/7 Emergency Repairs",
    "Burst Pipes & Leaks",
    "Drain Cleaning",
    "Water Heater Repair",
]
CTA = "CALL NOW!"
PHONE = "803-448-6866"
WEBSITE = ""  # Add your website here if you have one

WIDTH, HEIGHT = 1080, 1080
FPS = 10
DURATION_PER_SCENE = 2  # seconds per scene
FRAMES_PER_SCENE = FPS * DURATION_PER_SCENE

# Colors
DARK_BLUE = (15, 40, 80)
BRIGHT_BLUE = (30, 100, 200)
WHITE = (255, 255, 255)
YELLOW = (255, 200, 0)
RED = (220, 50, 30)
LIGHT_GRAY = (230, 235, 245)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_font(size, bold=False):
    """Try to load a good font, fall back to default."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    if not bold:
        font_paths = [p.replace("-Bold", "") for p in font_paths] + font_paths
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_water_drop(draw, cx, cy, size, color):
    """Draw a simple water drop shape."""
    pts = [
        (cx, cy - size),
        (cx + size * 0.6, cy + size * 0.2),
        (cx + size * 0.5, cy + size * 0.7),
        (cx, cy + size),
        (cx - size * 0.5, cy + size * 0.7),
        (cx - size * 0.6, cy + size * 0.2),
    ]
    draw.polygon(pts, fill=color)


def draw_wrench(draw, cx, cy, size, color):
    """Draw a simple wrench icon."""
    # Handle
    draw.rectangle(
        [cx - size * 0.08, cy - size * 0.5, cx + size * 0.08, cy + size * 0.3],
        fill=color,
    )
    # Head
    draw.ellipse(
        [cx - size * 0.25, cy - size * 0.7, cx + size * 0.25, cy - size * 0.3],
        fill=color,
    )
    draw.ellipse(
        [cx - size * 0.12, cy - size * 0.6, cx + size * 0.12, cy - size * 0.4],
        fill=DARK_BLUE,
    )


def centered_text(draw, y, text, font, fill):
    """Draw centered text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)


def scene_intro(progress):
    """Scene 1: Company name and logo."""
    img = Image.new("RGB", (WIDTH, HEIGHT), DARK_BLUE)
    draw = ImageDraw.Draw(img)

    # Animated water drops falling
    for i in range(8):
        drop_x = 100 + i * 130
        drop_y = int(-50 + progress * (400 + i * 60)) % (HEIGHT + 100) - 50
        alpha = int(150 + 105 * (i % 2))
        drop_color = (30, 100, 200, alpha) if img.mode == "RGBA" else BRIGHT_BLUE
        draw_water_drop(draw, drop_x, drop_y, 20 + i * 3, drop_color)

    # Company name with fade-in effect
    name_font = get_font(90, bold=True)
    tag_font = get_font(42)

    # Draw background panel
    panel_alpha = min(1.0, progress * 3)
    panel_y = int(300 + (1 - panel_alpha) * 50)
    draw.rounded_rectangle(
        [100, panel_y, WIDTH - 100, panel_y + 350],
        radius=30,
        fill=(255, 255, 255),
    )

    # Wrench icon
    draw_wrench(draw, WIDTH // 2, panel_y + 80, 60, BRIGHT_BLUE)

    centered_text(draw, panel_y + 120, COMPANY_NAME, name_font, DARK_BLUE)
    centered_text(draw, panel_y + 230, TAGLINE, tag_font, BRIGHT_BLUE)

    # Bottom bar
    draw.rectangle([0, HEIGHT - 80, WIDTH, HEIGHT], fill=RED)
    bar_font = get_font(36, bold=True)
    centered_text(draw, HEIGHT - 65, "24/7 AVAILABLE", bar_font, WHITE)

    return img


def scene_services(progress):
    """Scene 2: List of services with slide-in animation."""
    img = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, WIDTH, 200], fill=DARK_BLUE)
    header_font = get_font(56, bold=True)
    centered_text(draw, 60, "OUR SERVICES", header_font, WHITE)

    # Services list with staggered slide-in
    svc_font = get_font(44, bold=True)
    for i, service in enumerate(SERVICES):
        delay = i * 0.15
        item_progress = max(0, min(1, (progress - delay) * 3))
        x_offset = int((1 - item_progress) * WIDTH)

        y = 260 + i * 160
        # Service card
        draw.rounded_rectangle(
            [80 + x_offset, y, WIDTH - 80 + x_offset, y + 120],
            radius=15,
            fill=LIGHT_GRAY,
        )
        # Blue accent bar
        draw.rectangle(
            [80 + x_offset, y, 95 + x_offset, y + 120], fill=BRIGHT_BLUE
        )
        # Checkmark
        check_font = get_font(40, bold=True)
        draw.text((120 + x_offset, y + 30), "\u2713", font=check_font, fill=BRIGHT_BLUE)
        draw.text((170 + x_offset, y + 35), service, font=svc_font, fill=DARK_BLUE)

    # Bottom accent
    draw.rectangle([0, HEIGHT - 15, WIDTH, HEIGHT], fill=BRIGHT_BLUE)

    return img


def scene_emergency(progress):
    """Scene 3: Emergency urgency scene with pulsing effect."""
    img = Image.new("RGB", (WIDTH, HEIGHT), DARK_BLUE)
    draw = ImageDraw.Draw(img)

    # Pulsing red circle
    pulse = 0.8 + 0.2 * abs((progress * 4 % 1) - 0.5) * 2
    radius = int(350 * pulse)
    cx, cy = WIDTH // 2, HEIGHT // 2 - 50
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=RED,
    )

    # Inner circle
    inner_r = int(radius * 0.85)
    draw.ellipse(
        [cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
        fill=DARK_BLUE,
    )

    # Emergency text
    emg_font = get_font(72, bold=True)
    sub_font = get_font(44)
    small_font = get_font(36)

    centered_text(draw, cy - 100, "PLUMBING", emg_font, WHITE)
    centered_text(draw, cy - 20, "EMERGENCY?", emg_font, YELLOW)
    centered_text(draw, cy + 80, "Don't Panic!", sub_font, WHITE)
    centered_text(draw, cy + 140, "We're On Our Way", small_font, LIGHT_GRAY)

    # Water drops decoration
    for i in range(5):
        dx = 150 + i * 200
        dy = int(50 + (progress * 300 + i * 80) % 200)
        draw_water_drop(draw, dx, dy, 15, BRIGHT_BLUE)

    return img


def scene_cta(progress):
    """Scene 4: Call to action."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BRIGHT_BLUE)
    draw = ImageDraw.Draw(img)

    # Background pattern - diagonal stripes
    for i in range(-5, 20):
        x1 = i * 120
        draw.polygon(
            [(x1, 0), (x1 + 60, 0), (x1 + 60 + HEIGHT, HEIGHT), (x1 + HEIGHT, HEIGHT)],
            fill=(25, 90, 185),
        )

    # Central white card
    card_scale = min(1.0, progress * 2.5)
    card_h = int(600 * card_scale)
    card_w = int(800 * card_scale)
    cx, cy = WIDTH // 2, HEIGHT // 2
    draw.rounded_rectangle(
        [cx - card_w // 2, cy - card_h // 2, cx + card_w // 2, cy + card_h // 2],
        radius=30,
        fill=WHITE,
    )

    if card_scale > 0.5:
        cta_font = get_font(80, bold=True)
        phone_font = get_font(52, bold=True)
        web_font = get_font(36)
        name_font = get_font(40, bold=True)

        centered_text(draw, cy - 220, COMPANY_NAME, name_font, DARK_BLUE)

        # Divider
        draw.rectangle([cx - 200, cy - 160, cx + 200, cy - 155], fill=BRIGHT_BLUE)

        centered_text(draw, cy - 120, CTA, cta_font, RED)
        centered_text(draw, cy - 10, PHONE, phone_font, DARK_BLUE)
        if WEBSITE:
            centered_text(draw, cy + 60, WEBSITE, web_font, BRIGHT_BLUE)

        # "Free Estimates" badge
        badge_font = get_font(32, bold=True)
        draw.rounded_rectangle(
            [cx - 160, cy + 130, cx + 160, cy + 190],
            radius=10,
            fill=YELLOW,
        )
        centered_text(draw, cy + 142, "FREE ESTIMATES", badge_font, DARK_BLUE)

    return img


def main():
    scenes = [scene_intro, scene_services, scene_emergency, scene_cta]
    frames = []

    for scene_fn in scenes:
        for f in range(FRAMES_PER_SCENE):
            progress = f / FRAMES_PER_SCENE
            frame = scene_fn(progress)
            frames.append(frame)

        # Hold last frame a bit longer
        for _ in range(FRAMES_PER_SCENE // 2):
            frames.append(frame)

    # Save as animated GIF
    gif_path = os.path.join(OUTPUT_DIR, "mgk_plumbing_facebook_ad.gif")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=1000 // FPS,
        loop=0,
        optimize=True,
    )
    print(f"Ad video saved to: {gif_path}")
    print(f"Total frames: {len(frames)}")
    print(f"Duration: ~{len(frames) / FPS:.1f} seconds")
    print(f"Resolution: {WIDTH}x{HEIGHT}")
    print()
    print("NEXT STEPS:")
    print(f"1. To change details, edit create_ad_video.py and re-run")
    print(f"2. Upload the GIF to Facebook Ads Manager")
    print(f"   (Facebook accepts GIF files for video ads)")


if __name__ == "__main__":
    main()
