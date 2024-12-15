from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
from prophet.diagnostics import cross_validation, performance_metrics
from prophet.plot import plot_cross_validation_metric

def ProphetPredict(Lokasi_file, Output_csv, Output_forecast_30_days_csv):
    file_path = Lokasi_file
    data = pd.read_excel(file_path)

    # Preprocessing 
    data['Tanggal'] = pd.to_datetime(data['Tanggal'], format='%d/%m/%Y', errors='coerce')
    data = data.dropna(subset=['Tanggal'])
    data = data.drop_duplicates()

    Q1 = data['Total Penjualan Produk'].quantile(0.25)
    Q3 = data['Total Penjualan Produk'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    data_cleaned = data[(data['Total Penjualan Produk'] >= lower_bound) & 
                        (data['Total Penjualan Produk'] <= upper_bound)]

    data_cleaned = data_cleaned.rename(columns={'Tanggal': 'ds', 'Total Penjualan Produk': 'y'})

    # Membuat model Prophet dengan musiman
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
    model.fit(data_cleaned)

    # Membuat dataframe untuk prediksi 30 hari ke depan
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Menyimpan hanya hasil prediksi 30 hari ke dalam CSV
    forecast_30_days = forecast.iloc[-30:][['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    forecast_30_days.to_csv(Output_forecast_30_days_csv, index=False)
    print(f"Hasil prediksi 30 hari disimpan dalam file: {Output_forecast_30_days_csv}")

    # Visualisasi hasil prediksi
    fig = model.plot(forecast)
    plt.title('Prediksi Tren Penjualan')
    plt.xlabel('Tanggal')
    plt.ylabel('Total Penjualan Produk')
    plt.show()

    # Plot komponen
    fig2 = model.plot_components(forecast)
    plt.show()

    # Print hasil forecast
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30))

    # Evaluasi Model dengan Cross-Validation
    df_cv = cross_validation(model, initial='365 days', period='90 days', horizon='30 days')

    # Hitung mean MSE, RMSE, MAPE
    df_metrics = performance_metrics(df_cv)

    # Menyimpan hasil evaluasi ke CSV
    df_metrics.to_csv(Output_csv, index=False)
    print(f"\nHasil evaluasi disimpan dalam file: {Output_csv}")

    # Cetak nilai MAPE untuk setiap horizon prediksi
    print("\nNilai MAPE untuk setiap horizon prediksi:")
    print(df_metrics[['horizon', 'mape']])

    # Filter nilai MAPE untuk horizon 30 hari dan menyimpannya dalam CSV juga
    mape_30_hari = df_metrics[df_metrics['horizon'] == '30 days']['mape'].values[0]
    with open(Output_csv, 'a') as f:
        f.write(f"\nMAPE for 30 days horizon: {mape_30_hari:.4%}")

    # Plot grafik akurasi
    fig3 = plot_cross_validation_metric(df_cv, metric='rmse')
    plt.title("Grafik RMSE terhadap Horizon Prediksi")
    plt.show()

    fig4 = plot_cross_validation_metric(df_cv, metric='mape')
    plt.title("Grafik MAPE terhadap Horizon Prediksi")
    plt.show()

    fig5 = plot_cross_validation_metric(df_cv, metric='mse')
    plt.title("Grafik MSE terhadap Horizon Prediksi")
    plt.show()


# Path file data penjualan dan output CSV
location_files = "Data_Total_Penjualan_harian.xlsx"
output_csv = "Evaluasi_Prophet.csv"
output_forecast_30_days_csv = "Forecast_30_Days_Prophet.csv"

ProphetPredict(location_files, output_csv, output_forecast_30_days_csv)
