"""
المنصة الذكية لتحليل البيانات - النسخة الكاملة المحسّنة
Smart Data Analysis Platform - Full Enhanced Version

✨ الميزات الجديدة:
- فلترة متقدمة قبل الرسم
- شاشة ترحيب بتأثيرات حركية
- تنبيهات لحجم الملف
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json
import io
from datetime import datetime
from pathlib import Path

# ============================================================================
# الإعدادات الأساسية
# ============================================================================

st.set_page_config(
    page_title="المنصة الذكية لتحليل البيانات",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# عدّاد الزوار
# ============================================================================

VISITOR_FILE = Path("visitors.json")

def get_visitor_count():
    try:
        if VISITOR_FILE.exists():
            with open(VISITOR_FILE, 'r') as f:
                data = json.load(f)
                return data.get('total', 0), data.get('today', 0), data.get('last_date', '')
        return 0, 0, ''
    except Exception:
        return 0, 0, ''

def increment_visitor():
    if 'counted' not in st.session_state:
        st.session_state.counted = True
        try:
            total, today, last_date = get_visitor_count()
            current_date = datetime.now().strftime('%Y-%m-%d')
            if last_date != current_date:
                today = 1
            else:
                today += 1
            total += 1
            with open(VISITOR_FILE, 'w') as f:
                json.dump({'total': total, 'today': today, 'last_date': current_date}, f)
            return total, today
        except Exception:
            return 0, 0
    total, today, _ = get_visitor_count()
    return total, today

# ============================================================================
# تنسيقات CSS - وضع داكن + تأثيرات حركية
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Tajawal', 'Cairo', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1a2e 100%);
    }
    
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
        font-family: 'Tajawal', 'Cairo', sans-serif !important;
        color: #e8e8e8 !important;
    }
    
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    
    /* ===== تأثيرات حركية ===== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.3); }
        50% { box-shadow: 0 0 40px rgba(102, 126, 234, 0.6); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .welcome-hero {
        text-align: center;
        padding: 60px 20px;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .welcome-title {
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, #667eea 0%, #f093fb 50%, #4facfe 100%);
        background-size: 200% 200%;
        animation: gradientShift 4s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 20px;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 25px 20px;
        border-radius: 16px;
        text-align: center;
        min-height: 240px;
        height: auto;
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.4s ease;
        animation: fadeInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.6s;
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        border-color: rgba(102, 126, 234, 0.6);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.3);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 10px;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }
    
    .feature-card:nth-child(1) { animation-delay: 0.1s; }
    .feature-card:nth-child(2) { animation-delay: 0.2s; }
    .feature-card:nth-child(3) { animation-delay: 0.3s; }
    .feature-card:nth-child(4) { animation-delay: 0.4s; }
    
    .upload-hint {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 20px;
        margin: 30px 0;
        text-align: center;
        animation: pulse-glow 2.5s ease-in-out infinite;
    }
    
    /* ===== المقاييس ===== */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 16px;
        border-right: 4px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: transform 0.2s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stMetric"] * {
        color: #e8e8e8 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #667eea !important;
        font-weight: 700 !important;
    }
    
    /* ===== الأزرار ===== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* ===== عدّاد الزوار ===== */
    .visitor-badge {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.5);
        z-index: 999;
        font-family: 'Tajawal', sans-serif;
        animation: float 4s ease-in-out infinite;
    }
    
    /* ===== الشريط الجانبي ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-left: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] * {
        color: #e8e8e8 !important;
    }
    
    /* ===== بطاقات الرؤى ===== */
    .insight-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 18px;
        border-radius: 12px;
        border-right: 4px solid #667eea;
        margin: 10px 0;
        font-family: 'Tajawal', sans-serif;
        font-size: 1rem;
        color: #e8e8e8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        animation: fadeInUp 0.5s ease-out;
        transition: transform 0.2s;
    }
    
    .insight-card:hover {
        transform: translateX(-5px);
    }
    
    .insight-card b {
        color: #667eea;
    }
    
    /* ===== صندوق الفلاتر ===== */
    .filter-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.05));
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
    }
    
    /* ===== الفواصل ===== */
    hr {
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        height: 2px;
        border: none;
        margin: 2rem 0;
    }
    
    /* ===== رفع الملف ===== */
    [data-testid="stFileUploader"] {
        background: rgba(102, 126, 234, 0.08);
        border-radius: 12px;
        padding: 10px;
        border: 1px dashed rgba(102, 126, 234, 0.3);
    }
    
    /* ===== الجداول ===== */
    .stDataFrame {
        background: #1e293b;
        border-radius: 12px;
    }
    
    /* ===== التبويبات ===== */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(102, 126, 234, 0.05);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #e8e8e8;
        border-radius: 8px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* ===== تنبيهات ===== */
    .stAlert {
        border-radius: 12px;
        border-right: 4px solid #667eea;
        animation: fadeInUp 0.4s ease-out;
    }
    
    .stSelectbox label, .stRadio label, .stMultiSelect label {
        color: #e8e8e8 !important;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.08);
        border-radius: 10px;
        color: #e8e8e8 !important;
    }
    
    /* ===== استجابة الموبايل ===== */
    @media (max-width: 768px) {
        /* العنوان الرئيسي على الموبايل */
        h1 {
            font-size: 1.8rem !important;
            line-height: 1.3 !important;
            text-align: center !important;
        }
        
        /* عنوان شاشة الترحيب */
        .welcome-title {
            font-size: 1.5rem !important;
        }
        
        .welcome-hero {
            padding: 30px 10px !important;
        }
        
        .welcome-hero p {
            font-size: 1rem !important;
        }
        
        /* بطاقات الميزات تكون عمودية على الموبايل */
        .feature-card {
            min-height: 180px !important;
            margin-bottom: 15px;
            padding: 20px 15px !important;
        }
        
        .feature-icon {
            font-size: 2.5rem !important;
        }
        
        .feature-card h4 {
            font-size: 1.1rem !important;
        }
        
        /* العداد العائم أصغر على الموبايل */
        .visitor-badge {
            font-size: 0.75rem !important;
            padding: 6px 12px !important;
            bottom: 10px !important;
            left: 10px !important;
        }
        
        /* بطاقات الرؤى */
        .insight-card {
            font-size: 0.9rem !important;
            padding: 14px !important;
        }
        
        /* المقاييس */
        [data-testid="stMetric"] {
            padding: 12px !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.2rem !important;
        }
        
        /* صندوق رفع الملف */
        [data-testid="stFileUploader"] {
            padding: 5px !important;
        }
        
        /* أزرار التحميل */
        .stDownloadButton > button {
            font-size: 0.85rem !important;
            padding: 0.4rem 0.8rem !important;
        }
    }
    
    /* الشاشات الصغيرة جداً */
    @media (max-width: 480px) {
        h1 {
            font-size: 1.5rem !important;
        }
        
        .welcome-title {
            font-size: 1.3rem !important;
        }
        
        .feature-card {
            min-height: 160px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# الشريط الجانبي
# ============================================================================

with st.sidebar:
    st.markdown("### 📊 إحصائيات الموقع")
    total, today = increment_visitor()
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.metric("الزوار الكلي", f"{total:,}")
    with col_v2:
        st.metric("اليوم", f"{today:,}")
    
    st.divider()
    st.markdown("### ℹ️ عن المنصة")
    st.caption("""
منصة مجانية بالكامل لتحليل البيانات:

📁 **الصيغ**: CSV, Excel, JSON, Parquet, TSV

📊 **التحليلات**: 
- إحصاءات وصفية
- رؤى تلقائية
- كشف القيم الشاذة
- تحليل الارتباطات
- فلترة متقدمة

📈 **الرسوم**: 7 أنواع تفاعلية

📤 **التصدير**: Excel, CSV, JSON
    """)
    st.divider()
    st.caption("⭐ التطبيق مجاني 100%")

# ============================================================================
# العنوان
# ============================================================================

st.title("🌐 المنصة الذكية لتحليل البيانات")
st.markdown(
    "<p style='font-size:1.1rem; color:#a0aec0;'>ارفع ملف بياناتك والنظام يحلله تلقائياً ويولّد لك تقارير ذكية ورسوم تفاعلية</p>",
    unsafe_allow_html=True
)

# ============================================================================
# قراءة الملفات
# ============================================================================

def load_data(uploaded_file):
    file_name = uploaded_file.name.lower()
    try:
        if file_name.endswith('.csv'):
            try:
                return pd.read_csv(uploaded_file)
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                return pd.read_csv(uploaded_file, encoding='utf-8-sig')
            except Exception:
                uploaded_file.seek(0)
                return pd.read_csv(uploaded_file, encoding='cp1256')
        elif file_name.endswith(('.xlsx', '.xls')):
            return pd.read_excel(uploaded_file)
        elif file_name.endswith('.json'):
            return pd.read_json(uploaded_file)
        elif file_name.endswith('.parquet'):
            try:
                return pd.read_parquet(uploaded_file)
            except ImportError:
                st.error("⚠️ صيغة Parquet غير مدعومة في النسخة الحالية. استخدم CSV أو Excel أو JSON.")
                return None
        elif file_name.endswith('.tsv'):
            return pd.read_csv(uploaded_file, sep='\t')
        else:
            st.error("صيغة الملف غير مدعومة")
            return None
    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {str(e)}")
        return None

# ============================================================================
# توليد الرؤى التلقائية
# ============================================================================

def generate_insights(df):
    insights = []
    insights.append(f"📊 البيانات تحتوي على <b>{df.shape[0]:,} صف</b> و <b>{df.shape[1]} عمود</b>")
    
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    insights.append(f"🔢 <b>{len(num_cols)}</b> أعمدة رقمية و <b>{len(cat_cols)}</b> أعمدة نصية/فئوية")
    
    missing = df.isnull().sum().sum()
    if missing > 0:
        missing_pct = (missing / (df.shape[0] * df.shape[1])) * 100
        missing_cols = df.columns[df.isnull().any()].tolist()
        insights.append(f"⚠️ يوجد <b>{missing:,}</b> قيمة مفقودة ({missing_pct:.1f}%) في {len(missing_cols)} عمود")
    else:
        insights.append("✅ لا توجد قيم مفقودة - البيانات نظيفة")
    
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        insights.append(f"🔁 يوجد <b>{duplicates:,}</b> صف مكرر")
    
    if num_cols:
        variances = df[num_cols].var().sort_values(ascending=False)
        if len(variances) > 0:
            insights.append(f"📈 العمود <b>{variances.index[0]}</b> يحتوي على أعلى تباين")
        
        outlier_counts = {}
        for col in num_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)).sum()
            if outliers > 0:
                outlier_counts[col] = outliers
        
        if outlier_counts:
            top_outlier = max(outlier_counts, key=outlier_counts.get)
            insights.append(f"⚠️ قيم شاذة في {len(outlier_counts)} عمود، أعلاها في <b>{top_outlier}</b> ({outlier_counts[top_outlier]} قيمة)")
    
    if len(num_cols) >= 2:
        corr = df[num_cols].corr()
        corr_pairs = []
        for i in range(len(num_cols)):
            for j in range(i+1, len(num_cols)):
                corr_pairs.append((num_cols[i], num_cols[j], corr.iloc[i, j]))
        
        if corr_pairs:
            strongest = max(corr_pairs, key=lambda x: abs(x[2]))
            if strongest[2] > 0.7:
                direction = "طردية قوية"
            elif strongest[2] < -0.7:
                direction = "عكسية قوية"
            elif strongest[2] > 0.3:
                direction = "طردية متوسطة"
            elif strongest[2] < -0.3:
                direction = "عكسية متوسطة"
            else:
                direction = "ضعيفة"
            insights.append(f"🔗 أقوى علاقة: بين <b>{strongest[0]}</b> و <b>{strongest[1]}</b> (علاقة {direction}: {strongest[2]:.2f})")
    
    if cat_cols:
        for col in cat_cols[:3]:
            unique_count = df[col].nunique()
            if unique_count == 1:
                insights.append(f"💡 العمود <b>{col}</b> يحتوي على قيمة واحدة فقط (يمكن حذفه)")
            elif unique_count == len(df):
                insights.append(f"🆔 العمود <b>{col}</b> فريد لكل صف")
            elif unique_count <= 10:
                top_val = df[col].value_counts().index[0]
                top_pct = (df[col].value_counts().iloc[0] / len(df)) * 100
                insights.append(f"📌 في <b>{col}</b>: القيمة <b>{top_val}</b> هي الأكثر تكراراً ({top_pct:.1f}%)")
    
    return insights

# ============================================================================
# 🆕 نظام الفلترة المتقدمة
# ============================================================================

def apply_filters(df):
    """يطبق فلاتر متعددة على البيانات حسب اختيارات المستخدم"""
    filtered_df = df.copy()
    
    with st.expander("🔍 **الفلترة المتقدمة** - اضغط لفتح الفلاتر", expanded=False):
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        st.markdown("##### اختر الأعمدة اللي تبي تفلتر فيها:")
        
        # اختيار الأعمدة للفلترة
        all_columns = df.columns.tolist()
        filter_columns = st.multiselect(
            "الأعمدة المُفلترة:",
            options=all_columns,
            default=[],
            help="اختر عمود أو أكثر لتطبيق فلاتر عليه"
        )
        
        if filter_columns:
            st.markdown("---")
            
            for col in filter_columns:
                st.markdown(f"#### 🔹 فلترة: `{col}`")
                
                # إذا العمود رقمي - استخدم slider
                if pd.api.types.is_numeric_dtype(df[col]):
                    min_val = float(df[col].min())
                    max_val = float(df[col].max())
                    
                    if min_val != max_val:
                        col_range = st.slider(
                            f"النطاق لـ {col}:",
                            min_value=min_val,
                            max_value=max_val,
                            value=(min_val, max_val),
                            key=f"slider_{col}"
                        )
                        filtered_df = filtered_df[
                            (filtered_df[col] >= col_range[0]) & 
                            (filtered_df[col] <= col_range[1])
                        ]
                    else:
                        st.info(f"العمود {col} له قيمة واحدة فقط: {min_val}")
                
                # إذا العمود تاريخ
                elif pd.api.types.is_datetime64_any_dtype(df[col]):
                    min_date = df[col].min()
                    max_date = df[col].max()
                    date_range = st.date_input(
                        f"النطاق الزمني لـ {col}:",
                        value=(min_date, max_date),
                        min_value=min_date,
                        max_value=max_date,
                        key=f"date_{col}"
                    )
                    if len(date_range) == 2:
                        filtered_df = filtered_df[
                            (filtered_df[col] >= pd.Timestamp(date_range[0])) & 
                            (filtered_df[col] <= pd.Timestamp(date_range[1]))
                        ]
                
                # إذا العمود نصي/فئوي - استخدم multiselect
                else:
                    unique_vals = df[col].dropna().unique().tolist()
                    
                    # إذا القيم كثيرة (>50) خل المستخدم يبحث
                    if len(unique_vals) > 50:
                        search_term = st.text_input(
                            f"ابحث في {col}:",
                            key=f"search_{col}",
                            placeholder="اكتب نص للبحث..."
                        )
                        if search_term:
                            filtered_df = filtered_df[
                                filtered_df[col].astype(str).str.contains(search_term, case=False, na=False)
                            ]
                            st.caption(f"تم العثور على {len(filtered_df)} صف يحتوي على '{search_term}'")
                    else:
                        selected_vals = st.multiselect(
                            f"القيم المختارة لـ {col}:",
                            options=sorted([str(v) for v in unique_vals]),
                            default=sorted([str(v) for v in unique_vals]),
                            key=f"multi_{col}"
                        )
                        if selected_vals:
                            filtered_df = filtered_df[filtered_df[col].astype(str).isin(selected_vals)]
            
            st.markdown("---")
            
            # عرض ملخص الفلترة
            original_count = len(df)
            filtered_count = len(filtered_df)
            reduction_pct = ((original_count - filtered_count) / original_count * 100) if original_count > 0 else 0
            
            fcol1, fcol2, fcol3 = st.columns(3)
            fcol1.metric("الصفوف الأصلية", f"{original_count:,}")
            fcol2.metric("بعد الفلترة", f"{filtered_count:,}")
            fcol3.metric("نسبة التصفية", f"{reduction_pct:.1f}%")
            
            if filtered_count == 0:
                st.error("⚠️ لا توجد بيانات تطابق الفلاتر المحددة")
                return df  # رجّع الأصلي إذا الفلترة فاضية
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    return filtered_df

# ============================================================================
# رفع الملف
# ============================================================================

st.markdown("### 📁 رفع البيانات")
uploaded_file = st.file_uploader(
    "اختر ملف البيانات",
    type=['csv', 'xlsx', 'xls', 'json', 'tsv'],
    help="الصيغ المدعومة: CSV, Excel, JSON, TSV"
)

if uploaded_file:
    # 🆕 تنبيهات حجم الملف
    file_size_mb = uploaded_file.size / (1024 * 1024)
    
    if file_size_mb > 100:
        st.error(f"🚨 **ملف ضخم جداً** ({file_size_mb:.1f} MB) - قد يسبب بطء شديد أو يفشل التحميل. يُنصح بشدة تقليل الحجم أو تقسيم الملف.")
    elif file_size_mb > 50:
        st.error(f"⚠️ **ملف كبير جداً** ({file_size_mb:.1f} MB) - التحميل سيستغرق وقتاً طويلاً.")
    elif file_size_mb > 20:
        st.warning(f"⚠️ **حجم الملف كبير** ({file_size_mb:.1f} MB) - التحميل قد يستغرق بعض الوقت...")
    elif file_size_mb > 5:
        st.info(f"📦 حجم الملف: {file_size_mb:.1f} MB")
    
    # شريط تحميل أثناء قراءة الملف
    with st.spinner(f"📂 جاري معالجة الملف ({file_size_mb:.2f} MB)..."):
        df = load_data(uploaded_file)
    
    if df is not None and not df.empty:
        # تنبيهات حجم البيانات
        if df.shape[0] > 100000:
            st.warning(f"📊 **بيانات ضخمة:** {df.shape[0]:,} صف - بعض العمليات قد تستغرق وقتاً")
        
        st.success(f"✅ تم تحميل **{uploaded_file.name}** بنجاح ({df.shape[0]:,} صف × {df.shape[1]} عمود)")
        
        # 🆕 تطبيق الفلترة المتقدمة
        st.divider()
        st.markdown("## 🔍 الفلترة المتقدمة")
        st.caption("اختياري: يمكنك فلترة البيانات قبل التحليل والرسم")
        df = apply_filters(df)
        
        # الرؤى التلقائية
        st.divider()
        st.markdown("## 🧠 الرؤى التلقائية")
        insights = generate_insights(df)
        for insight in insights:
            st.markdown(f"<div class='insight-card'>{insight}</div>", unsafe_allow_html=True)
        
        # نظرة عامة
        st.divider()
        st.markdown("## 📋 نظرة عامة على البيانات")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("عدد الصفوف", f"{df.shape[0]:,}")
        m2.metric("عدد الأعمدة", f"{df.shape[1]:,}")
        m3.metric("القيم المفقودة", f"{df.isnull().sum().sum():,}")
        m4.metric("الحجم", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        
        with st.expander("👁️ عرض البيانات (أول 20 صف)", expanded=True):
            st.dataframe(df.head(20), use_container_width=True)
        
        with st.expander("📐 معلومات الأعمدة"):
            info_df = pd.DataFrame({
                'العمود': df.columns,
                'النوع': df.dtypes.astype(str),
                'القيم الفريدة': [df[col].nunique() for col in df.columns],
                'القيم المفقودة': df.isnull().sum().values,
                'النسبة المئوية للمفقود': [f"{(df[col].isnull().sum()/len(df)*100):.1f}%" for col in df.columns]
            })
            st.dataframe(info_df, use_container_width=True, hide_index=True)
        
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if num_cols:
            st.divider()
            st.markdown("## 📈 الإحصاءات الوصفية")
            st.dataframe(df[num_cols].describe().T, use_container_width=True)
        
        # الرسوم البيانية
        st.divider()
        st.markdown("## 📊 الرسوم البيانية التفاعلية")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎨 رسم مخصص",
            "🔗 مصفوفة الارتباطات",
            "📦 التوزيعات",
            "⚠️ القيم الشاذة"
        ])
        
        with tab1:
            col_a, col_b = st.columns([1, 2])
            
            with col_a:
                st.markdown("#### إعدادات الرسم")
                chart_type = st.selectbox(
                    "نوع الرسم:",
                    ["أعمدة", "خطوط", "نقاط", "دائري", "صندوقي", "هيستوغرام", "خريطة حرارية"]
                )
                
                x_axis = st.selectbox("المحور الأفقي (X):", df.columns.tolist(), key="x1")
                
                if chart_type not in ["دائري", "هيستوغرام"]:
                    y_axis = st.selectbox("المحور الرأسي (Y):", df.columns.tolist(), key="y1")
                else:
                    y_axis = None
                
                color_options = [None] + df.columns.tolist()
                color_col = st.selectbox("اللون حسب:", color_options, key="c1")
            
            with col_b:
                try:
                    fig = None
                    if chart_type == "أعمدة":
                        fig = px.bar(df, x=x_axis, y=y_axis, color=color_col, template="plotly_dark")
                    elif chart_type == "خطوط":
                        fig = px.line(df, x=x_axis, y=y_axis, color=color_col, template="plotly_dark")
                    elif chart_type == "نقاط":
                        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_col, template="plotly_dark")
                    elif chart_type == "دائري":
                        value_counts = df[x_axis].value_counts().head(10)
                        fig = px.pie(values=value_counts.values, names=value_counts.index, template="plotly_dark")
                    elif chart_type == "صندوقي":
                        fig = px.box(df, x=x_axis, y=y_axis, color=color_col, template="plotly_dark")
                    elif chart_type == "هيستوغرام":
                        fig = px.histogram(df, x=x_axis, color=color_col, template="plotly_dark", nbins=30)
                    elif chart_type == "خريطة حرارية":
                        if len(num_cols) >= 2:
                            corr = df[num_cols].corr()
                            fig = px.imshow(corr, text_auto='.2f', template="plotly_dark", color_continuous_scale="RdBu_r")
                        else:
                            st.warning("تحتاج عمودين رقميين على الأقل")
                    
                    if fig:
                        fig.update_layout(font=dict(family="Tajawal, Cairo, sans-serif", size=13), height=500)
                        st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"خطأ في الرسم: {str(e)}")
        
        with tab2:
            if len(num_cols) >= 2:
                corr = df[num_cols].corr()
                fig_corr = px.imshow(
                    corr, text_auto='.2f', aspect="auto",
                    color_continuous_scale="RdBu_r", template="plotly_dark",
                    title="مصفوفة الارتباطات بين الأعمدة الرقمية"
                )
                fig_corr.update_layout(font=dict(family="Tajawal, sans-serif"), height=600)
                st.plotly_chart(fig_corr, use_container_width=True)
                
                st.markdown("#### 🔝 أقوى الارتباطات")
                corr_pairs = []
                for i in range(len(num_cols)):
                    for j in range(i+1, len(num_cols)):
                        corr_pairs.append({
                            'العمود 1': num_cols[i],
                            'العمود 2': num_cols[j],
                            'الارتباط': corr.iloc[i, j]
                        })
                corr_df = pd.DataFrame(corr_pairs).sort_values('الارتباط', key=abs, ascending=False)
                st.dataframe(corr_df.head(10), use_container_width=True, hide_index=True)
            else:
                st.info("تحتاج عمودين رقميين على الأقل لعرض مصفوفة الارتباطات")
        
        with tab3:
            if num_cols:
                selected_dist = st.selectbox("اختر العمود:", num_cols, key="dist")
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    fig_hist = px.histogram(df, x=selected_dist, template="plotly_dark", nbins=30,
                                           title=f"توزيع {selected_dist}")
                    fig_hist.update_layout(font=dict(family="Tajawal, sans-serif"))
                    st.plotly_chart(fig_hist, use_container_width=True)
                with col_d2:
                    fig_box = px.box(df, y=selected_dist, template="plotly_dark",
                                     title=f"المخطط الصندوقي لـ {selected_dist}")
                    fig_box.update_layout(font=dict(family="Tajawal, sans-serif"))
                    st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("لا توجد أعمدة رقمية")
        
        with tab4:
            if num_cols:
                st.markdown("#### كشف القيم الشاذة باستخدام طريقة IQR")
                outlier_col = st.selectbox("اختر العمود:", num_cols, key="outlier")
                
                Q1 = df[outlier_col].quantile(0.25)
                Q3 = df[outlier_col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                
                outliers = df[(df[outlier_col] < lower) | (df[outlier_col] > upper)]
                
                o1, o2, o3 = st.columns(3)
                o1.metric("عدد القيم الشاذة", f"{len(outliers):,}")
                o2.metric("الحد الأدنى الطبيعي", f"{lower:.2f}")
                o3.metric("الحد الأعلى الطبيعي", f"{upper:.2f}")
                
                if len(outliers) > 0:
                    st.markdown("##### القيم الشاذة:")
                    st.dataframe(outliers.head(20), use_container_width=True)
            else:
                st.info("لا توجد أعمدة رقمية لكشف القيم الشاذة")
        
        # التصدير
        st.divider()
        st.markdown("## 📤 تصدير التقارير")
        st.caption("💡 سيتم تصدير البيانات بعد تطبيق الفلاتر")
        
        exp_col1, exp_col2, exp_col3 = st.columns(3)
        
        with exp_col1:
            try:
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                    if num_cols:
                        df.describe().to_excel(writer, sheet_name='Statistics')
                    df.dtypes.to_frame('Type').to_excel(writer, sheet_name='Columns')
                
                st.download_button(
                    "📊 تحميل Excel",
                    data=excel_buffer.getvalue(),
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except ImportError:
                st.warning("⚠️ ثبّت openpyxl لتفعيل تصدير Excel")
        
        with exp_col2:
            csv_data = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                "📄 تحميل CSV",
                data=csv_data,
                file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with exp_col3:
            json_data = df.to_json(orient='records', force_ascii=False, indent=2).encode('utf-8')
            st.download_button(
                "🔧 تحميل JSON",
                data=json_data,
                file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True
            )

else:
    # ====================================================================
    # 🆕 شاشة الترحيب الحركية
    # ====================================================================
    
    st.markdown("""
    <div class='welcome-hero'>
        <div style='font-size: 4rem; margin-bottom: 10px; animation: float 3s ease-in-out infinite;'>📊</div>
        <h2 class='welcome-title'>اكتشف قوة بياناتك في ثوانٍ</h2>
        <p style='font-size: 1.2rem; color: #a0aec0; max-width: 600px; margin: 20px auto;'>
            ارفع ملفك الآن واحصل على تحليل ذكي، رسوم تفاعلية، ورؤى تلقائية - كلها مجاناً
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # بطاقات الميزات الحركية
    st.markdown("<br>", unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    
    with f1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📊</div>
            <h4 style='color: #e8e8e8; margin: 10px 0;'>تحليل شامل</h4>
            <p style='color: #a0aec0; font-size: 0.9rem; line-height: 1.6; margin: 0;'>إحصاءات وصفية ورؤى تلقائية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with f2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📈</div>
            <h4 style='color: #e8e8e8; margin: 10px 0;'>رسوم تفاعلية</h4>
            <p style='color: #a0aec0; font-size: 0.9rem; line-height: 1.6; margin: 0;'>7 أنواع رسوم بيانية احترافية</p>
        </div>
        """, unsafe_allow_html=True)
    
    with f3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🔍</div>
            <h4 style='color: #e8e8e8; margin: 10px 0;'>فلترة متقدمة</h4>
            <p style='color: #a0aec0; font-size: 0.9rem; line-height: 1.6; margin: 0;'>تخصيص البيانات قبل التحليل</p>
        </div>
        """, unsafe_allow_html=True)
    
    with f4:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📤</div>
            <h4 style='color: #e8e8e8; margin: 10px 0;'>تصدير متعدد</h4>
            <p style='color: #a0aec0; font-size: 0.9rem; line-height: 1.6; margin: 0;'>Excel, CSV, JSON بنقرة واحدة</p>
        </div>
        """, unsafe_allow_html=True)
    
    # رسالة دعوة للرفع
    st.markdown("""
    <div class='upload-hint'>
        <div style='font-size: 2rem; margin-bottom: 10px;'>👆</div>
        <h4 style='color: #e8e8e8;'>اضغط على "Browse files" بالأعلى للبدء</h4>
        <p style='color: #a0aec0;'>الصيغ المدعومة: CSV, Excel, JSON, TSV</p>
    </div>
    """, unsafe_allow_html=True)

# عدّاد الزوار العائم
total_v, today_v, _ = get_visitor_count()
st.markdown(f"""
<div class='visitor-badge'>
    👥 {total_v:,} زائر  •  📅 اليوم: {today_v:,}
</div>
""", unsafe_allow_html=True)