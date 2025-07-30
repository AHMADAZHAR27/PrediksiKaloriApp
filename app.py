import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# =======================
# CONFIGURASI HALAMAN
# =======================
st.set_page_config(page_title="Prediksi Kalori Makanan", layout="centered")

# =======================
# MUAT MODEL
# =======================
model = joblib.load("lightgbm_model.pkl")

# =======================
# STYLE TAMBAHAN
# =======================
st.markdown("""
    <style>
        .title {
            font-size:40px;
            font-weight:800;
            color:#0e76a8;
            text-align:center;
            margin-bottom:25px;
        }
        .section-title {
            font-size:24px;
            font-weight:700;
            color:#ffffff;
            margin-top:30px;
            margin-bottom:15px;
        }
        .stButton button {
            background-color: #0e76a8;
            color: white;
            font-weight: bold;
            padding: 0.6rem 1.5rem;
            border-radius: 8px;
            transition: all 0.2s;
        }
        .stButton button:hover {
            background-color: #0b5e86;
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

# =======================
# HEADER
# =======================
st.markdown('<div class="title">🍱 Aplikasi Prediksi Kalori Makanan</div>', unsafe_allow_html=True)
st.markdown("Masukkan kandungan gizi makanan untuk memprediksi jumlah **kalori (kkal)** secara otomatis menggunakan AI (LightGBM Model).")
st.divider()

# =======================
# FORM BERTINGKAT (DINAMIS)
# =======================
st.markdown('<div class="section-title">📝 Masukkan Data Gizi:</div>', unsafe_allow_html=True)

nutrisi = {}
form_steps = [
    ["Lemak Total (g)", "Lemak Jenuh (g)", "Lemak Tak Jenuh Tunggal (g)", "Lemak Tak Jenuh Ganda (g)", "Karbohidrat (g)", "Gula (g)", "Protein (g)", "Serat (g)", "Kolesterol (mg)", "Air (g)", "Natrium (mg)"],
    ["Vitamin A (IU)", "Vitamin C (mg)", "Vitamin D (mg)", "Vitamin E (mg)", "Vitamin K (mg)", "Vitamin B1 (mg)", "Vitamin B2 (mg)", "Vitamin B3 (mg)", "Vitamin B5 (mg)", "Vitamin B6 (mg)", "Vitamin B11 (mg)", "Vitamin B12 (mg)"],
    ["Kalsium (mg)", "Zat Besi (mg)", "Kalium (mg)", "Magnesium (mg)", "Zinc (mg)", "Tembaga (mg)", "Mangan (mg)", "Fosfor (mg)", "Selenium (mg)", "Kepadatan Nutrisi"]
]

if "current_step" not in st.session_state:
    st.session_state.current_step = 0

# Navigasi antar langkah
col_prev, col_next = st.columns([1, 1])
with col_prev:
    if st.button("⬅️ Kembali") and st.session_state.current_step > 0:
        st.session_state.current_step -= 1
with col_next:
    if st.button("Lanjut ➡️") and st.session_state.current_step < len(form_steps) - 1:
        st.session_state.current_step += 1

# Form input data
with st.form("form_prediksi", clear_on_submit=False):
    for label in form_steps[st.session_state.current_step]:
        nutrisi[label] = st.number_input(label, min_value=0.0, step=0.1, key=label)
    portion = st.number_input("Berat Porsi (g)", min_value=1.0, value=100.0, step=1.0, key="portion")
    prediksi_btn = st.form_submit_button("🔍 Prediksi Kalori")

# =======================
# OUTPUT HASIL PREDIKSI
# =======================
if prediksi_btn:
    mapping = {
        "Lemak Total (g)": "Fat",
        "Lemak Jenuh (g)": "Saturated Fats",
        "Lemak Tak Jenuh Tunggal (g)": "Monounsaturated Fats",
        "Lemak Tak Jenuh Ganda (g)": "Polyunsaturated Fats",
        "Karbohidrat (g)": "Carbohydrates",
        "Gula (g)": "Sugars",
        "Protein (g)": "Protein",
        "Serat (g)": "Dietary Fiber",
        "Kolesterol (mg)": "Cholesterol",
        "Natrium (mg)": "Sodium",
        "Air (g)": "Water",
        "Vitamin A (IU)": "Vitamin A",
        "Vitamin B1 (mg)": "Vitamin B1",
        "Vitamin B11 (mg)": "Vitamin B11",
        "Vitamin B12 (mg)": "Vitamin B12",
        "Vitamin B2 (mg)": "Vitamin B2",
        "Vitamin B3 (mg)": "Vitamin B3",
        "Vitamin B5 (mg)": "Vitamin B5",
        "Vitamin B6 (mg)": "Vitamin B6",
        "Vitamin C (mg)": "Vitamin C",
        "Vitamin D (mg)": "Vitamin D",
        "Vitamin E (mg)": "Vitamin E",
        "Vitamin K (mg)": "Vitamin K",
        "Kalsium (mg)": "Calcium",
        "Tembaga (mg)": "Copper",
        "Zat Besi (mg)": "Iron",
        "Magnesium (mg)": "Magnesium",
        "Mangan (mg)": "Manganese",
        "Fosfor (mg)": "Phosphorus",
        "Kalium (mg)": "Potassium",
        "Selenium (mg)": "Selenium",
        "Zinc (mg)": "Zinc",
        "Kepadatan Nutrisi": "Nutrition Density"
    }
    input_data = pd.DataFrame([{mapping[k]: v for k, v in nutrisi.items()}])
    kalori_per_100g = model.predict(input_data)[0]
    estimasi_kalori = kalori_per_100g * (portion / 100)

    st.markdown('<div class="section-title">📊 Hasil Prediksi:</div>', unsafe_allow_html=True)
    result_df = pd.DataFrame({
        "Deskripsi": ["Kalori per 100g", "Berat Porsi (g)", "Estimasi Kalori Total"],
        "Nilai": [f"{kalori_per_100g:.2f} kkal", f"{portion:.0f} g", f"{estimasi_kalori:.2f} kkal"]
    })
    st.table(result_df)

    # Komposisi Makronutrien
    macro = {
        "Lemak (g)": nutrisi["Lemak Total (g)"],
        "Karbohidrat (g)": nutrisi["Karbohidrat (g)"],
        "Protein (g)": nutrisi["Protein (g)"]
    }
    fig, ax = plt.subplots()
    ax.pie(macro.values(), labels=macro.keys(), autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.markdown("#### ⚖️ Komposisi Makronutrien:")
    st.pyplot(fig)

    # Grafik vitamin & mineral yang tidak nol
    mikronutrien = {k: v for k, v in nutrisi.items() if ("Vitamin" in k or k in ["Kalsium (mg)", "Zat Besi (mg)", "Magnesium (mg)", "Zinc (mg)"]) and v > 0}
    if mikronutrien:
        st.markdown("#### 🧪 Mikronutrien Terkandung:")
        st.bar_chart(pd.Series(mikronutrien))

    # Tombol Download CSV
    csv = result_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Unduh Hasil (.csv)", data=csv, file_name="hasil_prediksi_kalori.csv", mime="text/csv")

    if kalori_per_100g <= 40:
        st.info("✅ Kategori: Rendah Kalori (≤ 40 kkal/100g)")
        st.markdown("💡 **Saran**: Cocok untuk diet rendah kalori atau makanan ringan.")
    elif kalori_per_100g <= 120:
        st.warning("⚠️ Kategori: Kalori Sedang (41–120 kkal/100g)")
        st.markdown("💡 **Saran**: Cocok sebagai makanan utama dengan kandungan kalori seimbang.")
    else:
        st.error("🚨 Kategori: Kalori Tinggi (> 120 kkal/100g)")
        st.markdown("💡 **Saran**: Perlu dikonsumsi dengan hati-hati, terutama untuk diet atau penderita penyakit metabolik.")

# =======================
# FOOTER
# =======================
st.markdown('<div class="footer">© 2025 Prediksi Kalori AI. Dibuat dengan ❤️ oleh A. Azhar .N 22.11.5175</div>', unsafe_allow_html=True)
