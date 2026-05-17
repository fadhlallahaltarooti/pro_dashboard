import pandas as pd
import random

# إنشاء بيانات وهمية لـ 100 عملية بيع سيارات
data = {
    'نوع_السيارة': [random.choice(['Lexus LX', 'Land Cruiser', 'Camry', 'Hilux']) for _ in range(100)],
    'المدينة': [random.choice(['الرياض', 'جدة', 'الدمام', 'أبها']) for _ in range(100)],
    'السعر': [random.randint(120000, 450000) for _ in range(100)],
    'الكمية': [random.randint(1, 5) for _ in range(100)]
}

df = pd.DataFrame(data)
df.to_csv('my_sales_data.csv', index=False)
print("✅ تم إنشاء ملف 'my_sales_data.csv' بنجاح! ارفعه الآن في تطبيقك.")