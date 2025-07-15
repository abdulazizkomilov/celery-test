README = """
# 🛰️ Celery bilan ishlovchi Django loyihasi

Ushbu loyiha **Django** asosida yozilgan bo‘lib, unda asinxron fon vazifalarini bajarish uchun **Celery**, **Redis**, va **Celery Beat** ishlatiladi. Loyihada foydalanuvchi rollari, menejer yaratish, SMS navbatlari, rejalashtirilgan vazifalar va **Flower** monitoring mavjud.

## 🚀 Texnologiyalar

- **Django** – Backend veb freymvork
- **Celery** – Tarqatilgan vazifa navbati
- **Redis** – Celery uchun broker (xabar almashinuvi)
- **Celery Beat** – Vaqtli vazifalarni avtomatik ishga tushirish
- **Flower** – Celery monitoring uchun veb-interfeys
- **PostgreSQL** – Ma’lumotlar bazasi (konfiguratsiya qilinadi)
- **DRF (Django Rest Framework)** – API ishlab chiqish
- **Makefile** – Oddiy buyruqlar to‘plami

## 📦 Loyihaning imkoniyatlari

### 🔐 Foydalanuvchi boshqaruvi
- `admin`, `manager`, `user` rollari bilan kengaytirilgan foydalanuvchi modeli
- Bir martalik parol orqali yangi menejer yaratish API
- Menejer foydalanuvchilarni CSV ko‘rinishida eksport qilish

### ⏱️ Vazifalarni rejalashtirish
- Navbatga asoslangan vazifalar (`default`, `sms_queue`)
- `Celery Beat` orqali avtomatik vaqtli ishlar
- SMS javoblarini `sms_responses.json` faylga yozish

### 📊 Monitoring
- Flower bilan fon ishlarini kuzatish
- HTTP orqali kirish himoyasi (login/parol)

## 🧪 O‘rnatish va ishga tushirish

### 1. Loyihani klonlash va o‘rnatish

```bash
git clone git@github.com:<your_username>/celery-test.git
cd celery-test
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Muhit sozlamalari (.env)

```bash
DJANGO_SECRET_KEY=your-secret
DEBUG=True
ALLOWED_HOSTS=*
REDIS_URL=redis://localhost:6379/0
```

### 3. Ma’lumotlar bazasini sozlash

```bash
make make     # makemigrations
make migrate  # migrate
make create   # superuser yaratish
```

### 4. Django serverni ishga tushurish

```bash
make run
```

## 🎯 Celery va vazifalar

### Odatiy ishchini ishga tushurish

```bash
make worker
```

### SMS navbati ishchisi

```bash
make worker-sms
```

### Celery Beat (vaqtli ishlar uchun)

```bash
make beat
```

### Flower monitoring

```bash
make flower
```

Flower sahifasi: http://localhost:5555/flower

Kirish:
Login: login  
Parol: password

## 🧪 API endpointlar

### ➕ Menejer yaratish (faqat admin uchun)

POST /api/manager/create/

```json
{
  "username": "testmanager",
  "email": "manager@example.com"
}
```

Javob:
```json
{
  "username": "testmanager",
  "one_time_password": "zXQ8s3Fa9kL2",
  "role": "manager"
}
```

### 📤 Menejerlarni CSV shaklida yuklab olish

GET /api/manager/export/
Ixtiyoriy: ?username=testmanager

CSV faylni yuklab beradi.

## 📋 Vazifalar

### 1. send_sms
- Navbat: sms_queue
- Tasodifiy SMS kodini yaratadi va `sms_responses.json` faylga yozadi

### 2. task_1
- Navbat: default
- Kiritilgan raqamni log ga yozadi

### 3. process_schedule
- Navbat: default
- `Schedule` obyektining holatini yangilaydi

### 4. auto_task_runner
- Navbat: default
- Belgilangan `Schedule` obyektlarini avtomatik ishga tushuradi

## ⚙️ Makefile buyruqlari

| Buyruq            | Tavsifi                                |
|-------------------|----------------------------------------|
| make run          | Django serverni ishga tushirish        |
| make make         | Migrations yaratish                    |
| make migrate      | Migrationsni qo‘llash                  |
| make create       | Superuser yaratish                     |
| make shell        | Django shell terminali                 |
| make worker       | Odatiy Celery ishchisini boshlash      |
| make worker-sms   | SMS ishchisini boshlash                |
| make beat         | Celery Beat boshlash                   |
| make flower       | Flower monitoring interfeys            |

## 📂 Loyihaning tuzilishi

celery-test/
├── core/                   # Sozlamalar va celery initsializatsiyasi  
├── app/                    # Model, view, tasklar  
├── templates/  
├── static/  
├── requirements.txt  
├── manage.py  
├── Makefile  

## 🧠 Izohlar

- Redis server ishga tushgan bo‘lishi kerak.
- Celery Beat orqali ishga tushadigan vazifalarni sozlashingiz mumkin.
- Docker yoki Supervisor yordamida serverga deploy qilishingiz mumkin.

## 📬 Hissa qo‘shish

Fork qilishingiz, PR yuborishingiz yoki issue ochishingiz mumkin.

## 📝 Litsenziya

Ushbu loyiha **MIT** litsenziyasi asosida tarqatiladi.
"""
