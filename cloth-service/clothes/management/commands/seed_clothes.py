import random

from django.core.management.base import BaseCommand

from clothes.models import Cloth


class Command(BaseCommand):
    help = "Seed cloth data"

    def handle(self, *args, **options):
        clothes_data = [
            {"name": "Áo Thun Basic Cotton", "brand": "BookStyle", "catalog_id": 1, "price": 149000, "size_label": "M", "color": "Trắng", "material": "Cotton 100%", "gender": "Unisex"},
            {"name": "Áo Hoodie Minimal", "brand": "BookStyle", "catalog_id": 1, "price": 389000, "size_label": "L", "color": "Đen", "material": "Nỉ da cá", "gender": "Unisex"},
            {"name": "Sơ Mi Oxford Classic", "brand": "Urban Page", "catalog_id": 2, "price": 329000, "size_label": "M", "color": "Xanh nhạt", "material": "Oxford", "gender": "Nam"},
            {"name": "Áo Polo Premium", "brand": "Urban Page", "catalog_id": 2, "price": 279000, "size_label": "L", "color": "Xám", "material": "Cotton pique", "gender": "Nam"},
            {"name": "Chân Váy Midi Xếp Ly", "brand": "Muse Wear", "catalog_id": 3, "price": 315000, "size_label": "S", "color": "Kem", "material": "Poly blend", "gender": "Nữ"},
            {"name": "Đầm Linen Cổ Vuông", "brand": "Muse Wear", "catalog_id": 3, "price": 459000, "size_label": "M", "color": "Be", "material": "Linen", "gender": "Nữ"},
            {"name": "Quần Jeans Straight Fit", "brand": "North Chapter", "catalog_id": 4, "price": 425000, "size_label": "32", "color": "Xanh denim", "material": "Denim", "gender": "Unisex"},
            {"name": "Quần Kaki Slim", "brand": "North Chapter", "catalog_id": 4, "price": 349000, "size_label": "31", "color": "Nâu", "material": "Kaki co giãn", "gender": "Nam"},
            {"name": "Áo Khoác Gió Light", "brand": "Transit", "catalog_id": 5, "price": 499000, "size_label": "XL", "color": "Rêu", "material": "Poly chống nước", "gender": "Unisex"},
            {"name": "Blazer Soft Tailor", "brand": "Transit", "catalog_id": 5, "price": 679000, "size_label": "M", "color": "Than chì", "material": "Twill", "gender": "Nữ"},
            {"name": "Set Đồ Mặc Nhà Cozy", "brand": "Cloud Home", "catalog_id": 6, "price": 259000, "size_label": "L", "color": "Hồng phấn", "material": "Cotton mềm", "gender": "Nữ"},
            {"name": "Áo Len Gân Cổ Tròn", "brand": "Cloud Home", "catalog_id": 6, "price": 289000, "size_label": "M", "color": "Kem", "material": "Acrylic blend", "gender": "Unisex"},
        ]

        image_urls = [
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600",
            "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=600",
            "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=600",
            "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600",
            "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=600",
            "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=600",
        ]

        descriptions = [
            "Thiết kế tối giản, dễ phối đồ cho đi học và đi làm.",
            "Form mặc thoải mái, chất vải mềm, phù hợp dùng hằng ngày.",
            "Mẫu bán chạy với đường may chắc chắn và bảng màu dễ mặc.",
            "Phong cách hiện đại, phù hợp cửa hàng mở rộng sang thời trang.",
        ]

        created_count = 0
        for cloth_data in clothes_data:
            sku = f"CL{random.randint(100000, 999999)}"
            cloth, created = Cloth.objects.get_or_create(
                name=cloth_data["name"],
                brand=cloth_data["brand"],
                defaults={
                    **cloth_data,
                    "sku": sku,
                    "stock": random.randint(10, 120),
                    "description": random.choice(descriptions),
                    "image_url": random.choice(image_urls),
                    "created_by_staff_id": random.randint(1, 10),
                },
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created cloth: {cloth.name}")
            else:
                self.stdout.write(f"Cloth already exists: {cloth.name}")

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {created_count} clothes"))
