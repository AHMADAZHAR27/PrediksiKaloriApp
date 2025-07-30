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
            margin-bottom:10px;
        }
        .footer {
            position: fixed;
            bottom: 10px;
            text-align: center;
            width: 100%;
            font-size: 12px;
            color: #888;
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

    with col2:
        sodium = st.number_input("Natrium (mg)", min_value=0.0, step=0.1)
        water = st.number_input("Air (g)", min_value=0.0, step=0.1)
        vitamin_c = st.number_input("Vitamin C (mg)", min_value=0.0, step=0.1)
        vitamin_a = st.number_input("Vitamin A (IU)", min_value=0.0, step=0.1)
        calcium = st.number_input("Kalsium (mg)", min_value=0.0, step=0.1)
        iron = st.number_input("Zat Besi (mg)", min_value=0.0, step=0.1)
        potassium = st.number_input("Kalium (mg)", min_value=0.0, step=0.1)
        magnesium = st.number_input("Magnesium (mg)", min_value=0.0, step=0.1)
        zinc = st.number_input("Zinc (mg)", min_value=0.0, step=0.1)

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
        'Vitamin C': vitamin_c,
        'Vitamin A': vitamin_a,
        'Calcium': calcium,
        'Iron': iron,
        'Potassium': potassium,
        'Magnesium': magnesium,
        'Zinc': zinc
    }])

    result = model.predict(input_data)[0]
    st.subheader("🔥 Hasil Prediksi:")
    st.success(f"Estimasi Kalori: **{result:.2f} kkal**")

    # Kategori
    if result < 100:
        st.info("✅ Kategori: Rendah Kalori")
    elif result < 300:
        st.warning("⚠️ Kategori: Kalori Sedang")
    else:
        st.error("🚨 Kategori: Kalori Tinggi")

# =======================
# FOOTER
# =======================
st.markdown('<div class="footer">© 2025 Prediksi Kalori AI. Dibuat dengan Streamlit.</div>', unsafe_allow_html=True)
