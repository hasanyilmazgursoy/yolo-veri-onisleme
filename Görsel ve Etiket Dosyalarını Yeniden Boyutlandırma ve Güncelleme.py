# Başlık: Görsel ve Etiket Dosyalarını Yeniden Boyutlandırma ve Güncelleme
# Açıklama: Bu script, görselleri belirtilen boyutlarda yeniden boyutlandırır ve etiket dosyalarını bu yeni boyutlara göre günceller.

import os
from PIL import Image

# Tanımlamalar
data_path = r"C:\Users\90537\OneDrive\Desktop\data"
images_path = os.path.join(data_path, "images", "train")
labels_path = os.path.join(data_path, "labels", "train")
output_path = r"C:\Users\90537\OneDrive\Desktop\resized_data"

# Yeni dizinler oluştur
output_images_path = os.path.join(output_path, "images", "train")
output_labels_path = os.path.join(output_path, "labels", "train")

os.makedirs(output_images_path, exist_ok=True)
os.makedirs(output_labels_path, exist_ok=True)

# Yeni boyut
new_size = (640, 640)  # Örneğin 640x640

# Görseli yeniden boyutlandırma fonksiyonu
def resize_image(image_path, output_image_path):
    with Image.open(image_path) as img:
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        img.save(output_image_path)

# Etiketleri güncelleme fonksiyonu
def update_labels(label_path, output_label_path, original_size, new_size):
    with open(label_path, 'r') as file:
        lines = file.readlines()

    width_ratio = new_size[0] / original_size[0]
    height_ratio = new_size[1] / original_size[1]

    with open(output_label_path, 'w') as file:
        for line in lines:
            parts = line.split()
            if len(parts) >= 5:
                class_id, x_center, y_center, w, h = parts[:5]
                x_center = float(x_center) * width_ratio
                y_center = float(y_center) * height_ratio
                w = float(w) * width_ratio
                h = float(h) * height_ratio
                file.write(f"{class_id} {x_center} {y_center} {w} {h}\n")

# Görsel ve etiket dosyalarını işleme fonksiyonu
def process_files():
    # Görsel ve etiket dosyalarını işleme
    image_files = [f for f in os.listdir(images_path) if f.endswith(".jpg")]

    for image_file in image_files:
        base_name = os.path.splitext(image_file)[0]
        image_path = os.path.join(images_path, image_file)
        label_path = os.path.join(labels_path, base_name + ".txt")

        if os.path.exists(label_path):
            output_image_path = os.path.join(output_images_path, image_file)
            output_label_path = os.path.join(output_labels_path, base_name + ".txt")

            # Görseli yeniden boyutlandır
            with Image.open(image_path) as img:
                original_size = img.size
                resize_image(image_path, output_image_path)

            # Etiketleri güncelle
            update_labels(label_path, output_label_path, original_size, new_size)
            print(f"İşlendi: {image_file}")

# Dosyaları işle
process_files()
print("Görsel ve etiket dosyaları işleme tamamlandı.")
