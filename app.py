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
st.markdown("Masukkan data gizi berdasarkan kategori di bawah ini. Setelah mengisi tiap bagian, klik 'Lanjut'.")
st.divider()

# =======================
# DEFINISI FORM MULTISTEP
# =======================
form_pages = {
    "Makronutrien": ["Lemak Total (g)", "Lemak Jenuh (g)", "Lemak Tak Jenuh Tunggal (g)", "Lemak Tak Jenuh Ganda (g)", "Karbohidrat (g)", "Gula (g)", "Protein (g)", "Serat (g)"],
    "Mineral": ["Kolesterol (mg)", "Air (g)", "Natrium (mg)", "Kalsium (mg)", "Zat Besi (mg)", "Kalium (mg)", "Magnesium (mg)", "Zinc (mg)", "Tembaga (mg)", "Mangan (mg)", "Fosfor (mg)", "Selenium (mg)"],
    "Vitamin": ["Vitamin A (IU)", "Vitamin C (mg)", "Vitamin D (mg)", "Vitamin E (mg)", "Vitamin K (mg)", "Vitamin B1 (mg)", "Vitamin B2 (mg)", "Vitamin B3 (mg)", "Vitamin B5 (mg)", "Vitamin B6 (mg)", "Vitamin B11 (mg)", "Vitamin B12 (mg)"],
    "Lainnya": ["Kepadatan Nutrisi"]
}

form_keys = list(form_pages.keys())
if "form_step" not in st.session_state:
    st.session_state.form_step = 0
if "nutrisi" not in st.session_state:
    st.session_state.nutrisi = {}

current_key = form_keys[st.session_state.form_step]
st.markdown(f"### Langkah {st.session_state.form_step+1} dari {len(form_keys)}: {current_key}")

with st.form(f"form_{current_key}"):
    for kolom in form_pages[current_key]:
        st.session_state.nutrisi[kolom] = st.number_input(
            kolom,
            min_value=0.0,
            step=0.1,
            value=st.session_state.nutrisi.get(kolom, 0.0)
        )
    col1, col2 = st.columns([1, 1])
    with col1:
        kembali = st.form_submit_button("⬅️ Kembali")
    with col2:
        lanjut = st.form_submit_button("➡️ Lanjut")

if kembali and st.session_state.form_step > 0:
    st.session_state.form_step -= 1
elif lanjut and st.session_state.form_step < len(form_keys) - 1:
    st.session_state.form_step += 1

# =======================
# FORM FINAL UNTUK PREDIKSI
# =======================
if st.session_state.form_step == len(form_keys) - 1:
    st.markdown("---")
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

        macro = {
            "Lemak (g)": nutrisi["Lemak Total (g)"],
            "Karbohidrat (g)": nutrisi["Karbohidrat (g)"],
            "Protein (g)": nutrisi["Protein (g)"]
        }
        fig, ax = plt.subplots(figsize=(5, 5))
        colors = ['#FF9999', '#66B3FF', '#99FF99']
        wedges, texts, autotexts = ax.pie(
            macro.values(),
            labels=macro.keys(),
            autopct="%1.1f%%",
            startangle=90,
            colors=colors,
            textprops={'fontsize': 10, 'color': 'black'}
        )
        ax.axis("equal")
        plt.setp(autotexts, size=10, weight="bold")
        plt.title("Distribusi Makronutrien", fontsize=14, weight='bold')
        st.markdown("#### ⚖️ Komposisi Makronutrien")
        st.pyplot(fig)

        mikronutrien = {k: v for k, v in nutrisi.items() if ("Vitamin" in k or k in ["Kalsium (mg)", "Zat Besi (mg)", "Magnesium (mg)", "Zinc (mg)"]) and v > 0}
        if mikronutrien:
            st.markdown("#### 🧪 Mikronutrien Terkandung")
            st.bar_chart(pd.Series(mikronutrien))

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
