# Bu script, görsellerin ve etiket dosyalarının doğruluğunu kontrol eder ve detaylı bir rapor oluşturur.
# 1. Görsel boyutları analiz edilir.
# 2. Etiket dosyalarındaki format hataları, geçersiz koordinatlar ve sınıf ID hataları kontrol edilir.
# 3. Rastgele seçilen örnekler üzerinde hata tespiti yapılır ve raporlanır.

import os
import random
from PIL import Image

# Tanımlamalar
images_path = r"C:\Users\90537\OneDrive\Desktop\data\images\train"  # Görsellerin bulunduğu dizin
labels_path = r"C:\Users\90537\OneDrive\Desktop\data\labels\train"  # Etiketlerin bulunduğu dizin
output_report_path = r"C:\Users\90537\OneDrive\Desktop\report"  # Rapor dosyasının kaydedileceği dizin

# Örnekleme için rastgele seçilecek dosya sayısı
sample_size = 100  # Örnekleme için kullanılacak dosya sayısı

# Etiket dosyasındaki hataları kontrol etme fonksiyonu
def check_label_file(label_file):
    label_path = os.path.join(labels_path, label_file)
    errors = []

    with open(label_path, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            parts = line.strip().split()
            if len(parts) != 5:
                errors.append((i + 1, "Geçersiz etiket formatı", line.strip()))
                continue

            try:
                class_id, x_center, y_center, w, h = map(float, parts)
                if not (0 <= x_center <= 1 and 0 <= y_center <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                    errors.append((i + 1, "Geçersiz koordinatlar", line.strip()))
                if class_id < 0 or class_id > 5:
                    errors.append((i + 1, "Geçersiz sınıf ID'si", line.strip()))
            except ValueError:
                errors.append((i + 1, "Dönüştürme hatası", line.strip()))

    return errors

# Görsel boyutlarını analiz etme fonksiyonu
def analyze_image_size(image_file):
    image_path = os.path.join(images_path, image_file)
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width, height
    except Exception as e:
        return str(e)

# Detaylı raporu oluşturma fonksiyonu
def generate_detailed_report():
    # Görsel dosyalarını al
    image_files = [f for f in os.listdir(images_path) if f.endswith(".jpg")]

    # Rastgele örnekler seç
    sample_files = random.sample(image_files, min(sample_size, len(image_files)))

    os.makedirs(output_report_path, exist_ok=True)

    report_file = os.path.join(output_report_path, "detailed_label_errors_report.txt")
    with open(report_file, 'w') as report:
        for image_file in sample_files:
            label_file = os.path.splitext(image_file)[0] + ".txt"

            if not os.path.exists(os.path.join(labels_path, label_file)):
                report.write(f"{image_file}: Etiket dosyası bulunamadı.\n")
                continue

            # Etiket dosyasındaki hataları kontrol et
            errors = check_label_file(label_file)
            if errors:
                report.write(f"{image_file} - Hatalı etiketler:\n")
                for line_number, error_type, line in errors:
                    report.write(f"  Satır: {line_number}, Hata: {error_type}, İçerik: {line}\n")
            else:
                report.write(f"{image_file}: Etiketler geçerli.\n")

            # Görselin boyutunu analiz et
            size_info = analyze_image_size(image_file)
            if isinstance(size_info, tuple):
                report.write(f"Görsel boyutu: {size_info[0]}x{size_info[1]}\n")
            else:
                report.write(f"Görsel boyutu analiz hatası: {size_info}\n")

            report.write("\n")

    print(f"Detaylı rapor oluşturuldu: {report_file}")

# Raporu oluştur
generate_detailed_report()
