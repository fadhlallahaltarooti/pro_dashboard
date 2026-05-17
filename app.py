import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="المحلل الذكي الشامل", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #1E3A8A; font-family: 'Arial'; }
    .stAlert { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 المنصة الذكية لتحليل البيانات")
st.write("ارفع أي ملف بيانات (CSV) وسيقوم النظام بتحليله تلقائياً وتوليد تقارير تفاعلية.")

# رفع الملف
uploaded_file = st.file_uploader("اختر ملف البيانات", type=['csv'])

if uploaded_file:
    # قراءة البيانات
    df = pd.read_csv(uploaded_file)
    st.success(f"تم تحميل الملف بنجاح! يحتوي على {df.shape[0]} سطر و {df.shape[1]} عمود.")

    # قسم الإحصائيات السريعة
    st.divider()
    st.subheader("📋 نظرة عامة على البيانات")
    st.dataframe(df.head(10), use_container_width=True)

    # التحليل التفاعلي
    st.divider()
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("⚙️ إعدادات الرسم البياني")
        all_columns = df.columns.tolist()
        
        x_axis = st.selectbox("اختر المحور الأفقي (X):", all_columns)
        y_axis = st.selectbox("اختر المحور الرأسي (Y):", all_columns)
        chart_type = st.radio("نوع الرسم البياني:", ["أعمدة (Bar)", "خطوط (Line)", "نقاط (Scatter)"])
        
        color_tag = st.selectbox("تصنيف حسب اللون (اختياري):", [None] + all_columns)

    with col2:
        st.subheader("📊 النتائج المرئية")
        if chart_type == "أعمدة (Bar)":
            fig = px.bar(df, x=x_axis, y=y_axis, color=color_tag, template="plotly_white")
        elif chart_type == "خطوط (Line)":
            fig = px.line(df, x=x_axis, y=y_axis, color=color_tag, template="plotly_white")
        else:
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color_tag, template="plotly_white")
        
        st.plotly_chart(fig, use_container_width=True)

    # قسم التحليل التلقائي (الذكاء البسيط)
    st.divider()
    st.subheader("🧠 استنتاجات آلية")
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if num_cols:
        target_col = st.selectbox("اختر عموداً رقمياً لتحليله:", num_cols)
        avg_val = df[target_col].mean()
        max_val = df[target_col].max()
        min_val = df[target_col].min()

        c1, c2, c3 = st.columns(3)
        c1.metric("المتوسط الحسابي", f"{avg_val:.2f}")
        c2.metric("أعلى قيمة", f"{max_val}")
        c3.metric("أقل قيمة", f"{min_val}")
    else:
        st.warning("لا توجد أعمدة رقمية كافية للتحليل الإحصائي.")

else:
    st.info("💡 نصيحة: تأكد أن الملف يحتوي على رؤوس أعمدة (Header) واضحة باللغة العربية أو الإنجليزية.")