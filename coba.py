from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
from prophet.diagnostics import cross_validation, performance_metrics
from prophet.plot import plot_cross_validation_metric
import os

def ProphetPredict(Lokasi_file):
    file_path = Lokasi_file
    data = pd.read_excel(file_path)

    # Membuat folder untuk menyimpan gambar dan hasil jika belum ada
    if not os.path.exists('Gambar_prediksi'):
        os.makedirs('Gambar_prediksi')

    if not os.path.exists('Hasil_prediksi'):
        os.makedirs('Hasil_prediksi')

    # Preprocessing
    data['Tanggal'] = pd.to_datetime(data['Tanggal'], format='%d/%m/%Y', errors='coerce')
    data = data.dropna(subset=['Tanggal'])
    data = data.drop_duplicates()

    # Menggunakan Interquartile Range (IQR) untuk menghilangkan outlier
    Q1 = data['Total Penjualan Produk'].quantile(0.25)
    Q3 = data['Total Penjualan Produk'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    data_cleaned = data[(data['Total Penjualan Produk'] >= lower_bound) &
                        (data['Total Penjualan Produk'] <= upper_bound)]

    # Format
    data_cleaned = data_cleaned.rename(columns={'Tanggal': 'ds', 'Total Penjualan Produk': 'y'})

    # Membuat model Prophet dengan tren musiman
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
    model.fit(data_cleaned)

    # DataFrame untuk prediksi 30 hari ke depan
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Menyimpan hasil prediksi ke dalam CSV
    forecast_30_days = forecast.iloc[-30:][['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    forecast_30_days.to_csv('Hasil_prediksi/forecast_30_days.csv', index=False)
    print("Hasil prediksi 30 hari ke depan disimpan dalam file: Hasil_prediksi/forecast_30_days.csv")

    # Visualisasi hasil prediksi
    fig = model.plot(forecast)
    plt.title('Prediksi Tren Penjualan')
    plt.xlabel('Tanggal')
    plt.ylabel('Total Penjualan Produk')
    fig.savefig('Gambar_prediksi/prediksi_tren_penjualan.png', dpi=300)  # Menyimpan gambar

    # Visualisasi komponen prediksi
    fig2 = model.plot_components(forecast)
    fig2.savefig('Gambar_prediksi/komponen_prediksi.png', dpi=300)  # Menyimpan gambar

    # Menampilkan hasil prediksi
    print(forecast_30_days)

    # Evaluasi Model dengan Cross-Validation
    df_cv = cross_validation(model, initial='365 days', period='90 days', horizon='30 days')

    # Hitung mean MSE, RMSE, MAPE
    df_metrics = performance_metrics(df_cv)
    print("\nMSE:", df_metrics['mse'].mean())
    print("RMSE:", df_metrics['rmse'].mean())
    print("MAPE:", df_metrics['mape'].mean())

    # Plot grafik akurasi
    fig4 = plot_cross_validation_metric(df_cv, metric='mse')
    fig4.savefig('Gambar_prediksi/mse_horizon.png', dpi=300)
    plt.title("Grafik MSE terhadap Horizon Prediksi")

    fig3 = plot_cross_validation_metric(df_cv, metric='rmse')
    fig3.savefig('Gambar_prediksi/rmse_horizon.png', dpi=300)
    plt.title("Grafik RMSE terhadap Horizon Prediksi")

    fig5 = plot_cross_validation_metric(df_cv, metric='mape')
    fig5.savefig('Gambar_prediksi/mape_horizon.png', dpi=300)
    plt.title("Grafik MAPE terhadap Horizon Prediksi")


