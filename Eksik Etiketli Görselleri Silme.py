import os
import shutil

# Tanımlamalar
data_path = r"C:\Users\90537\OneDrive\Desktop\yolo_format_1"  # Eski veri dizini
images_path = os.path.join(data_path, "images")  # Görsellerin bulunduğu dizin
labels_path = os.path.join(data_path, "labels")  # Etiketlerin bulunduğu dizin
new_output_path = "C:\\Users\\90537\\OneDrive\\Desktop\\new_output"  # Yeni çıktı dizini

# Yeni dizinler oluştur
output_images_path = os.path.join(new_output_path, "images")
output_labels_path = os.path.join(new_output_path, "labels")

os.makedirs(output_images_path, exist_ok=True)
os.makedirs(output_labels_path, exist_ok=True)


def remove_unlabeled_images():
    # Tüm görselleri kontrol et
    image_files = [f for f in os.listdir(images_path) if f.endswith(".jpg")]

    for image_file in image_files:
        base_name = os.path.splitext(image_file)[0]
        label_file = base_name + ".txt"
        if not os.path.exists(os.path.join(labels_path, label_file)):
            # Eksik etiket dosyası olan görselleri sil
            image_path = os.path.join(images_path, image_file)
            os.remove(image_path)
            print(f"Silindi: {image_path}")


def copy_labeled_files():
    # Etiket dosyası olan görselleri kopyala
    image_files = [f for f in os.listdir(images_path) if f.endswith(".jpg")]

    for image_file in image_files:
        base_name = os.path.splitext(image_file)[0]
        label_file = base_name + ".txt"
        if os.path.exists(os.path.join(labels_path, label_file)):
            # Görseli ve etiket dosyasını kopyala
            shutil.copy(os.path.join(images_path, image_file), os.path.join(output_images_path, image_file))
            shutil.copy(os.path.join(labels_path, label_file), os.path.join(output_labels_path, label_file))
            print(f"Kopyalandı: {image_file}")


# Eksik etiket dosyası olan görselleri sil
remove_unlabeled_images()

# Etiket dosyası olan görselleri kopyala
copy_labeled_files()

print("Görsel ve etiket dosyaları işleme tamamlandı.")
