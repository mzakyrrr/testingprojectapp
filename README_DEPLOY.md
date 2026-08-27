# Trimatch Streamlit Deployment

## Struktur

```text
trimatch_streamlit/
├── app.py
├── model.pkl                  # ditambahkan setelah model final tersedia
├── requirements.txt
├── assets/
│   └── Logo_Trimatch.jpeg
├── data/
│   └── eda_summary.json
├── pages/
│   ├── 1_EDA.py
│   ├── 2_Model_Performance.py
│   ├── 3_Prediction.py
│   └── 4_About.py
└── utils/
    ├── config.py
    ├── eda.py
    ├── inference.py
    └── style.py
```

## Menjalankan aplikasi lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Menambahkan model final

Letakkan file:

```text
model.pkl
```

di root folder, sejajar dengan `app.py`.

Sebelum deployment final, cek kembali fungsi preprocessing di:

```text
utils/inference.py
```

agar benar-benar sama dengan preprocessing model final.

## Catatan

Versi ini sengaja belum mengunci metrik performa model karena model baru masih dalam proses finalisasi.
Setelah model selesai, update halaman:

```text
pages/2_Model_Performance.py
```

dengan accuracy, precision, recall, F1-score, confusion matrix, dan training history final.
