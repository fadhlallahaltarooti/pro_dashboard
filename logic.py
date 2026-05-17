import pandas as pd
import numpy as np

def get_data():
    # إنشاء بيانات وهمية لمبيعات 12 شهر
    months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 
              'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    sales = [1200, 1500, 1100, 1800, 2200, 2100, 2500, 2700, 3000, 2900, 3200, 3500]
    return pd.DataFrame({'الشهر': months, 'المبيعات': sales})

def simple_forecast(df):
    # معادلة بسيطة للتوقع: متوسط آخر 3 شهور + 10% نمو
    last_avg = df['المبيعات'].tail(3).mean()
    return round(last_avg * 1.1, 2)