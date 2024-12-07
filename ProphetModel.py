from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
from prophet.diagnostics import cross_validation, performance_metrics
from prophet.plot import plot_cross_validation_metric


def ProphetPredict(Lokasi_file):
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

    # Visualisasi hasil prediksi
    fig = model.plot(forecast)
    plt.title('Prediksi Tren Penjualan')
    plt.xlabel('Tanggal')
    plt.ylabel('Total Penjualan Produk')
    plt.show()

   
    fig2 = model.plot_components(forecast)
    plt.show()
    
   
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30))
    
    #Evaluasi Model dengan Cross-Validation
    df_cv = cross_validation(model, initial='365 days', period='90 days', horizon='30 days')

    # Hitung MSE, RMSE, MAPE,
    df_metrics = performance_metrics(df_cv)
    print("\nMSE:", df_metrics['mse'].mean())
    print("RMSE:", df_metrics['rmse'].mean())
    print("MAPE:", df_metrics['mape'].mean())

    # Plot grafik akurasi 
    fig3 = plot_cross_validation_metric(df_cv, metric='rmse')
    plt.title("Grafik RMSE terhadap Horizon Prediksi")
    plt.show()



