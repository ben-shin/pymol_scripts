import colorsys
from collections import Counter
from pymol import cmd

# name and specify domain positions
domains = [
        ("NLS", 1, 108),
        ("DUF1726", 109, 203),
        ("Helicase", 258, 497),
        ("GNAT", 511, 767),
        ("RNA", 768, 929)
]

# assign lightness in order of domains specified
lightness = [0.85, 0.7, 0.55, 0.4, 0.25]

for obj in cmd.get_names("objects"):
    if cmd.get_type(obj) != "object:molecule":
        continue

    colors = []
    cmd.iterate(
        f"({obj}) and name CA",
        "colors.append(color)",
        space={"colors": colors}
    )

    if not colors:
        continue

    index = Counter(
        colors
    ).most_common(1)[0][0]

    rgb = cmd.get_color_tuple(index)
    h, l, s = colorsys.rgb_to_hls(*rgb)

    if s < 0.05:
        print(f"skipping {obj}: grayscale base")
        continue

    for (name, start, end), L in zip(
        domains, lightness
    ):
        shade = colorsys.hls_to_rgb(h, L, s)
        color_name = f"{obj}_{name}_shade"

        cmd.set_color(color_name, list(shade))
        cmd.color(
            color_name,
            f"({obj}) and resi {start}-{end}"
        )

    print(f"colored {obj}")
PY
