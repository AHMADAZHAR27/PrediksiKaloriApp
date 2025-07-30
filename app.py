import streamlit as st
import pandas as pd
import joblib

# =======================
# CONFIGURASI HALAMAN
# =======================
st.set_page_config(page_title="Prediksi Kalori Makanan", layout="centered")

# =======================
# MUAT MODEL
# =======================
model = joblib.load("lightgbm_model.pkl")

# =======================
# HEADER
# =======================
st.markdown("""
    <style>
        .title {
            font-size:36px;
            font-weight:bold;
            color:#1f77b4;
            text-align:center;
            margin-bottom:20px;
        }
        .footer {
            position: fixed;
            bottom: 10px;
            text-align: center;
            width: 100%;
            font-size: 12px;
            color: #888;
        }
        .stButton button {
            background-color: #1f77b4;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1.5rem;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🍱 Aplikasi Prediksi Kalori Makanan</div>', unsafe_allow_html=True)
st.markdown("Masukkan kandungan gizi makanan untuk memprediksi jumlah **kalori (kkal)** secara otomatis menggunakan AI (LightGBM Model).")

st.divider()

# =======================
# FORM INPUT USER
# =======================
with st.form("form_prediksi"):
    st.subheader("📝 Masukkan Data Gizi:")
    col1, col2 = st.columns(2)

    with col1:
        fat = st.number_input("Lemak Total (g)", min_value=0.0, step=0.1)
        sat_fat = st.number_input("Lemak Jenuh (g)", min_value=0.0, step=0.1)
        mono_fat = st.number_input("Lemak Tak Jenuh Tunggal (g)", min_value=0.0, step=0.1)
        poly_fat = st.number_input("Lemak Tak Jenuh Ganda (g)", min_value=0.0, step=0.1)
        carbs = st.number_input("Karbohidrat (g)", min_value=0.0, step=0.1)
        sugars = st.number_input("Gula (g)", min_value=0.0, step=0.1)
        protein = st.number_input("Protein (g)", min_value=0.0, step=0.1)
        fiber = st.number_input("Serat (g)", min_value=0.0, step=0.1)
        cholesterol = st.number_input("Kolesterol (mg)", min_value=0.0, step=0.1)
        sodium = st.number_input("Natrium (mg)", min_value=0.0, step=0.1)
        water = st.number_input("Air (g)", min_value=0.0, step=0.1)
        calcium = st.number_input("Kalsium (mg)", min_value=0.0, step=0.1)
        iron = st.number_input("Zat Besi (mg)", min_value=0.0, step=0.1)
        portion = st.number_input("Berat Porsi (g)", min_value=1.0, value=100.0, step=1.0)

    with col2:
        potassium = st.number_input("Kalium (mg)", min_value=0.0, step=0.1)
        magnesium = st.number_input("Magnesium (mg)", min_value=0.0, step=0.1)
        zinc = st.number_input("Zinc (mg)", min_value=0.0, step=0.1)
        vitamin_a = st.number_input("Vitamin A (IU)", min_value=0.0, step=0.1)
        vitamin_c = st.number_input("Vitamin C (mg)", min_value=0.0, step=0.1)
        vitamin_b1 = st.number_input("Vitamin B1 (mg)", min_value=0.0, step=0.1)
        vitamin_b11 = st.number_input("Vitamin B11 (mg)", min_value=0.0, step=0.1)
        vitamin_b12 = st.number_input("Vitamin B12 (mg)", min_value=0.0, step=0.1)
        vitamin_b2 = st.number_input("Vitamin B2 (mg)", min_value=0.0, step=0.1)
        vitamin_b3 = st.number_input("Vitamin B3 (mg)", min_value=0.0, step=0.1)
        vitamin_b5 = st.number_input("Vitamin B5 (mg)", min_value=0.0, step=0.1)
        vitamin_b6 = st.number_input("Vitamin B6 (mg)", min_value=0.0, step=0.1)
        vitamin_d = st.number_input("Vitamin D (mg)", min_value=0.0, step=0.1)
        vitamin_e = st.number_input("Vitamin E (mg)", min_value=0.0, step=0.1)
        vitamin_k = st.number_input("Vitamin K (mg)", min_value=0.0, step=0.1)
        copper = st.number_input("Tembaga (mg)", min_value=0.0, step=0.1)
        manganese = st.number_input("Mangan (mg)", min_value=0.0, step=0.1)
        phosphorus = st.number_input("Fosfor (mg)", min_value=0.0, step=0.1)
        selenium = st.number_input("Selenium (mg)", min_value=0.0, step=0.1)
        nutrition_density = st.number_input("Kepadatan Nutrisi", min_value=0.0, step=0.1)

    prediksi_btn = st.form_submit_button("🔍 Prediksi Kalori")

# =======================
# OUTPUT HASIL PREDIKSI
# =======================
if prediksi_btn:
    input_data = pd.DataFrame([{
        'Fat': fat,
        'Saturated Fats': sat_fat,
        'Monounsaturated Fats': mono_fat,
        'Polyunsaturated Fats': poly_fat,
        'Carbohydrates': carbs,
        'Sugars': sugars,
        'Protein': protein,
        'Dietary Fiber': fiber,
        'Cholesterol': cholesterol,
        'Sodium': sodium,
        'Water': water,
        'Vitamin A': vitamin_a,
        'Vitamin B1': vitamin_b1,
        'Vitamin B11': vitamin_b11,
        'Vitamin B12': vitamin_b12,
        'Vitamin B2': vitamin_b2,
        'Vitamin B3': vitamin_b3,
        'Vitamin B5': vitamin_b5,
        'Vitamin B6': vitamin_b6,
        'Vitamin C': vitamin_c,
        'Vitamin D': vitamin_d,
        'Vitamin E': vitamin_e,
        'Vitamin K': vitamin_k,
        'Calcium': calcium,
        'Copper': copper,
        'Iron': iron,
        'Magnesium': magnesium,
        'Manganese': manganese,
        'Phosphorus': phosphorus,
        'Potassium': potassium,
        'Selenium': selenium,
        'Zinc': zinc,
        'Nutrition Density': nutrition_density
    }])

    kalori_per_100g = model.predict(input_data)[0]
    estimasi_kalori = kalori_per_100g * (portion / 100)

    st.subheader("🔥 Hasil Prediksi:")
    st.success(f"Estimasi Kalori: **{estimasi_kalori:.2f} kkal** (untuk {portion}g makanan)")

    # Kategori Berdasarkan WHO/FDA (per 100g)
    if kalori_per_100g <= 40:
        st.info("✅ Kategori: Rendah Kalori (≤ 40 kkal/100g)")
    elif kalori_per_100g <= 120:
        st.warning("⚠️ Kategori: Kalori Sedang (41–120 kkal/100g)")
    else:
        st.error("🚨 Kategori: Kalori Tinggi (> 120 kkal/100g)")

# =======================
# FOOTER
# =======================
st.markdown('<div class="footer">© 2025 Prediksi Kalori AI. Dibuat dengan ❤️ oleh A. Azhar</div>', unsafe_allow_html=True)
