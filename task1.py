import cv2
import pandas as pd
from IPython.display import display, Image
from matplotlib import pyplot as plt

# Assuming you have uploaded color.png and colors.csv to the Colab environment
img_path = r"/content/color.png"
csv_path = r"/content/colors.csv"

img = cv2.imread(img_path)

# Check if image loaded successfully
if img is None:
    print(f"Error: Could not load image from {img_path}")
else:
    img = cv2.resize(img, (800, 600))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Try to read colors.csv, if not found, use a sample dataframe
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Warning: {csv_path} not found. Using sample color data.")
        data = {'color_name': ['Red', 'Green', 'Blue', 'Yellow', 'Purple', 'Orange', 'Black', 'White'],
                'hex': ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#800080', '#FFA500', '#000000', '#FFFFFF'],
                'R': [255, 0, 0, 255, 128, 255, 0, 255],
                'G': [0, 255, 0, 255, 0, 165, 0, 255],
                'B': [0, 0, 255, 0, 128, 0, 0, 255]}
        df = pd.DataFrame(data)

    def get_color_name(R, G, B):
        minimum = float('inf')
        cname = ""
        for i in range(len(df)):
            d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
            if d < minimum:
                minimum = d
                cname = df.loc[i, "color_name"]
        return cname

    def detect_color(x, y):
        b, g, r = img[y, x]
        r, g, b = int(r), int(g), int(b)
        color_name = get_color_name(r, g, b)
        print(f"Detected color at ({x}, {y}) → {color_name} | R={r} G={g} B={b}")
        img_copy = img_rgb.copy()
        cv2.rectangle(img_copy, (20, 20), (750, 60), (r, g, b), -1)
        text = f"{color_name} R={r} G={g} B={b}"
        cv2.putText(img_copy, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 255, 255) if r + g + b < 600 else (0, 0, 0), 2)

        plt.figure(figsize=(10, 6))
        plt.imshow(img_copy)
        plt.axis('off')
        plt.title("Color Detection Output")
        plt.show()

    detect_color(300, 150)
