# Başlık: Görsel Boyutlarını Kontrol Etme
# Açıklama:
# Bu script, belirtilen görsel dizinindeki tüm `.jpg` ve `.png` formatındaki görsellerin boyutlarını kontrol eder.
# Görsellerin boyutları, `expected_size` olarak belirlenen değere uygun olup olmadığına göre kontrol edilir.
# Eğer görselin boyutu beklenen boyutla uyuşmazsa, görselin adı ve mevcut boyutları ekrana yazdırılır.

import os
import cv2

# Görsel dizini
images_path = r"C:\Users\90537\OneDrive\Desktop\data\images\train"  # Görsellerin bulunduğu dizin

# Beklenen boyut
expected_size = (640, 640)  # Hedeflenen boyut (640x640)

# Görsel boyutlarını kontrol etme fonksiyonu
def check_image_sizes():
    # Tüm görselleri kontrol et
    for image_file in os.listdir(images_path):
        if image_file.endswith(".jpg") or image_file.endswith(".png"):  # .jpg veya .png dosyalarını kontrol et
            image_path = os.path.join(images_path, image_file)

            # Görseli yükle
            image = cv2.imread(image_path)
            height, width, _ = image.shape  # Görsel boyutlarını al

            # Boyutu kontrol et
            if (width, height) != expected_size:  # Boyut uyuşmazsa
                print(f"Boyut uyuşmazlığı: {image_file} (Boyut: {width}x{height})")

# Başlangıç mesajı
print("Boyut kontrolü başladı...")

# Boyut kontrol fonksiyonunu çağır
check_image_sizes()

# Bitiş mesajı
print("Boyut kontrolü tamamlandı.")
