# Başlık: Etiket Dosyalarını YOLO Formatına Dönüştürme
# Açıklama:
# Bu script, belirtilen bir dizindeki görseller ve etiket dosyalarını alır ve etiket dosyalarını
# YOLO formatına dönüştürerek belirtilen çıkış dizinine kaydeder.
# Görsellerin `.jpg` formatında olduğu varsayılmaktadır ve etiket dosyalarının her biriyle aynı
# adı taşıyan `.txt` dosyaları içerir. Etiket dosyasındaki her satırda, nesne koordinatları ve
# sınıf ID'si bulunur. Dönüştürme işlemi sırasında, etiketlerin YOLO formatında (class_id x_center y_center width height)
# kaydedilmesi sağlanır.

import os
import cv2
import shutil

# Tanımlamalar
data_path = "C:\\Users\\90537\\OneDrive\\Desktop\\data"  # Verilerin bulunduğu ana dizin
images_path = os.path.join(data_path, "images")  # Görsellerin bulunduğu alt dizin
labels_path = os.path.join(data_path, "labels")  # Etiketlerin bulunduğu alt dizin
output_path = "C:\\Users\\90537\\OneDrive\\Desktop\\yolo_format_1"  # Çıktı dosyalarının kaydedileceği dizin

# Çıktı dizinlerini oluştur
os.makedirs(os.path.join(output_path, "images"), exist_ok=True)  # Görseller için çıktı dizini
os.makedirs(os.path.join(output_path, "labels"), exist_ok=True)  # Etiketler için çıktı dizini

# Sınıflar (0: Deformasyon, 1: Engel, 2: Kırık, 3: Bağlantı Kopması, 4: Hizalama Hatası, 5: Birikinti)
class_labels = {
    0: "Deformasyon",
    1: "Engel",
    2: "Kırık",
    3: "Bağlantı Kopması",
    4: "Hizalama Hatası",
    5: "Birikinti"
}

# Etiket formatını YOLO formatına dönüştürme fonksiyonu
def convert_bbox_format(image_path, label_path, output_label_path):
    # Görseli oku ve boyutlarını al
    image = cv2.imread(image_path)
    h, w, _ = image.shape

    # Etiket dosyasını oku
    with open(label_path, 'r') as file:
        lines = file.readlines()

    # Eğer etiket dosyası boşsa, çıktı dosyasını oluşturma
    if not lines:
        print(f"Etiket dosyası boş: {label_path}")
        return

    # YOLO formatında etiket dosyasını yaz
    with open(output_label_path, 'w') as file:
        for line in lines:
            coords = line.strip().split()
            print(f"Orijinal Koordinatlar: {coords}")  # Koordinatları yazdır

            # En az dört değer bekleniyor, buna göre kontrol ekleyin
            if len(coords) == 5:  # YOLO formatında beş değer var mı?
                try:
                    # Koordinatları oku (class_id x_center y_center width height)
                    class_id, x_center, y_center, width, height = map(float, coords)

                    # Sınıf ID'si belirtilen sınıflar arasında mı kontrol et
                    if int(class_id) in class_labels:
                        file.write(f"{int(class_id)} {x_center} {y_center} {width} {height}\n")
                    else:
                        print(f"Geçersiz sınıf ID'si: {class_id}")
                except ValueError as e:
                    print(f"Koordinat dönüştürme hatası: {e}")
            else:
                print(f"Geçersiz koordinat formatı: {coords}")

# Tüm görselleri ve etiketleri işle
for image_name in os.listdir(images_path):
    if image_name.endswith(".jpg"):
        base_name = os.path.splitext(image_name)[0]  # Görsel ismini al (uzantısız)
        image_path = os.path.join(images_path, image_name)
        label_path = os.path.join(labels_path, f"{base_name}.txt")
        output_label_path = os.path.join(output_path, "labels", f"{base_name}.txt")

        # Görseli çıktı dizinine kopyala
        shutil.copy(image_path, os.path.join(output_path, "images", image_name))

        # Etiket dosyasını dönüştür ve kaydet
        if os.path.exists(label_path):
            convert_bbox_format(image_path, label_path, output_label_path)
        else:
            print(f"Etiket dosyası eksik: {image_name}")

print("Dönüştürme tamamlandı.")
