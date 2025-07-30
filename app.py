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
st.markdown("Masukkan kandungan gizi makanan satu per satu. Setelah mengisi, klik 'Lanjut' untuk ke input berikutnya hingga selesai.")
st.divider()

# =======================
# INPUT SATU PER SATU
# =======================
all_features = [
    "Lemak Total (g)", "Lemak Jenuh (g)", "Lemak Tak Jenuh Tunggal (g)", "Lemak Tak Jenuh Ganda (g)", "Karbohidrat (g)", "Gula (g)", "Protein (g)", "Serat (g)", "Kolesterol (mg)", "Air (g)", "Natrium (mg)",
    "Vitamin A (IU)", "Vitamin C (mg)", "Vitamin D (mg)", "Vitamin E (mg)", "Vitamin K (mg)", "Vitamin B1 (mg)", "Vitamin B2 (mg)", "Vitamin B3 (mg)", "Vitamin B5 (mg)", "Vitamin B6 (mg)", "Vitamin B11 (mg)", "Vitamin B12 (mg)",
    "Kalsium (mg)", "Zat Besi (mg)", "Kalium (mg)", "Magnesium (mg)", "Zinc (mg)", "Tembaga (mg)", "Mangan (mg)", "Fosfor (mg)", "Selenium (mg)", "Kepadatan Nutrisi"
]

if "form_index" not in st.session_state:
    st.session_state.form_index = 0
if "nutrisi" not in st.session_state:
    st.session_state.nutrisi = {}

current_feature = all_features[st.session_state.form_index]
with st.form("form_step_input"):
    value = st.number_input(current_feature, min_value=0.0, step=0.1, key=current_feature)
    col1, col2 = st.columns([1, 1])
    with col1:
        kembali = st.form_submit_button("⬅️ Kembali")
    with col2:
        lanjut = st.form_submit_button("➡️ Lanjut")

if kembali and st.session_state.form_index > 0:
    st.session_state.form_index -= 1
elif lanjut:
    st.session_state.nutrisi[current_feature] = value
    if st.session_state.form_index < len(all_features) - 1:
        st.session_state.form_index += 1
    else:
        st.success("✅ Semua data berhasil dimasukkan. Siap diprediksi!")

if st.session_state.form_index == len(all_features) - 1:
    portion = st.number_input("Berat Porsi (g)", min_value=1.0, value=100.0, step=1.0, key="portion")
    if st.button("🔍 Prediksi Kalori"):
        nutrisi = st.session_state.nutrisi
        mapping = {
            "Lemak Total (g)": "Fat", "Lemak Jenuh (g)": "Saturated Fats", "Lemak Tak Jenuh Tunggal (g)": "Monounsaturated Fats",
            "Lemak Tak Jenuh Ganda (g)": "Polyunsaturated Fats", "Karbohidrat (g)": "Carbohydrates", "Gula (g)": "Sugars",
            "Protein (g)": "Protein", "Serat (g)": "Dietary Fiber", "Kolesterol (mg)": "Cholesterol", "Natrium (mg)": "Sodium",
            "Air (g)": "Water", "Vitamin A (IU)": "Vitamin A", "Vitamin B1 (mg)": "Vitamin B1", "Vitamin B11 (mg)": "Vitamin B11",
            "Vitamin B12 (mg)": "Vitamin B12", "Vitamin B2 (mg)": "Vitamin B2", "Vitamin B3 (mg)": "Vitamin B3",
            "Vitamin B5 (mg)": "Vitamin B5", "Vitamin B6 (mg)": "Vitamin B6", "Vitamin C (mg)": "Vitamin C", "Vitamin D (mg)": "Vitamin D",
            "Vitamin E (mg)": "Vitamin E", "Vitamin K (mg)": "Vitamin K", "Kalsium (mg)": "Calcium", "Tembaga (mg)": "Copper",
            "Zat Besi (mg)": "Iron", "Magnesium (mg)": "Magnesium", "Mangan (mg)": "Manganese", "Fosfor (mg)": "Phosphorus",
            "Kalium (mg)": "Potassium", "Selenium (mg)": "Selenium", "Zinc (mg)": "Zinc", "Kepadatan Nutrisi": "Nutrition Density"
        }
        input_data = pd.DataFrame([{mapping[k]: v for k, v in nutrisi.items()}])

        # Validasi fitur sesuai urutan model
        expected_features = model.feature_name_
        for feat in expected_features:
            if feat not in input_data.columns:
                input_data[feat] = 0.0
        input_data = input_data[expected_features]

        kalori_per_100g = model.predict(input_data)[0]
        estimasi_kalori = kalori_per_100g * (portion / 100)

        st.markdown("### 📊 Hasil Prediksi")
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
        st.markdown("#### ⚖️ Komposisi Makronutrien")
        st.pyplot(fig)

        # Grafik vitamin & mineral yang tidak nol
        mikronutrien = {k: v for k, v in nutrisi.items() if ("Vitamin" in k or k in ["Kalsium (mg)", "Zat Besi (mg)", "Magnesium (mg)", "Zinc (mg)"]) and v > 0}
        if mikronutrien:
            st.markdown("#### 🧪 Mikronutrien Terkandung")
            st.bar_chart(pd.Series(mikronutrien))

        # Tombol Download CSV
        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Unduh Hasil (.csv)", data=csv, file_name="hasil_prediksi_kalori.csv", mime="text/csv")

        # Kategori kalori
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
