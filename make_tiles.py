
from PIL import Image
from pathlib import Path
import math

SOURCE = Path("map.jpg")
OUTPUT = Path("map_files")
TILE_SIZE = 256

if not SOURCE.exists():
    raise FileNotFoundError(
        "Не намирам map.jpg. Провери дали е в папката MapTest."
    )

OUTPUT.mkdir(exist_ok=True)

with Image.open(SOURCE) as original:
    image = original.convert("RGB")
    width, height = image.size
    max_level = math.ceil(math.log2(max(width, height)))

    for level in range(max_level + 1):
        scale = 2 ** (level - max_level)
        w = max(1, math.ceil(width * scale))
        h = max(1, math.ceil(height * scale))

        resized = image.resize(
            (w, h), Image.Resampling.LANCZOS
        )
        level_dir = OUTPUT / str(level)
        level_dir.mkdir(parents=True, exist_ok=True)

        for y in range(math.ceil(h / TILE_SIZE)):
            for x in range(math.ceil(w / TILE_SIZE)):
                tile = resized.crop((
                    x * TILE_SIZE,
                    y * TILE_SIZE,
                    min((x + 1) * TILE_SIZE, w),
                    min((y + 1) * TILE_SIZE, h)
                ))
                tile.save(
                    level_dir / f"{x}_{y}.jpg",
                    "JPEG",
                    quality=90,
                    optimize=True
                )

        print(f"Готово ниво {level}: {w} x {h}")

    dzi = f'''<?xml version="1.0" encoding="UTF-8"?>
<Image TileSize="{TILE_SIZE}" Overlap="0" Format="jpg"
 xmlns="http://schemas.microsoft.com/deepzoom/2008">
  <Size Width="{width}" Height="{height}"/>
</Image>'''

    Path("map.dzi").write_text(dzi, encoding="utf-8")

print("Готово! Създадени са map.dzi и map_files.")