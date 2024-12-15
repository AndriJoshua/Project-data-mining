import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo
from datetime import datetime
import csv
from PIL import Image, ImageTk
from coba import ProphetPredict
import threading
from pystray import Icon, Menu, MenuItem
import sys
import pandas as pd
from tkinter import filedialog
from tkinter.messagebox import showinfo, showerror


class AppKedaiKopi:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Penjualan Kedai Kopi Selera Anambas")
        self.root.geometry("800x600")
        self.sales_data = []  
        self.sales_data_individu = []
        self.tray_icon = None 

        # Daftar Produk
        self.products = [
            {"name": "Mie Goreng Tarempa", "price": 10000},
            {"name": "Ayam Sambal Matah", "price": 20000},
            {"name": "Ayam Cabe Hijau", "price": 20000},
            {"name": "Ayam Geprek", "price": 20000},
            {"name": "Ikan Sambal Salai", "price": 10000},
            {"name": "Bihun Goreng", "price": 15000},
            {"name": "Lakse Kuah", "price": 13000},
            {"name": "Lakse Goreng", "price": 13000},
            {"name": "Nasi Goreng", "price": 13000},
            {"name": "Kwetiau", "price": 13000},
            {"name": "Bubur Pedas", "price": 10000},
            {"name": "Indomie", "price": 10000},
            {"name": "Kernas", "price": 10000},
            {"name": "Luti Gendang", "price": 10000},
            {"name": "Cekong", "price": 8000},
            {"name": "Kentang Goreng", "price": 10000},
            {"name": "Kopi o", "price": 6000},
            {"name": "Kopi Susu", "price": 8000},
            {"name": "Kopi Milo", "price": 8000},
            {"name": "Teh O", "price": 5000},
            {"name": "Teh Obeng", "price": 6000},
            {"name": "Teh Susu", "price": 8000},
            {"name": "Teh Tarik", "price": 8000},
            {"name": "Capucino", "price": 8000},
            {"name": "Milo", "price": 8000},
            {"name": "Lemon Tea", "price": 8000},
            {"name": "Extrajos Susu", "price": 8000},
            {"name": "Kukubima Susu", "price": 8000},
            {"name": "Chocolatos", "price": 8000},
            {"name": "Sirup", "price": 8000},
            {"name": "Es Kosong", "price": 2000},
        ]
        
        # Main Container
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Navigasi
        self.setup_navigation()

        #View
        self.show_menu_produk()
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

    def setup_navigation(self):
        # Sidebar
        self.sidebar = tk.Frame(self.main_frame, bg="#6B4E3D", width=200)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="Menu", font=("Poppins", 16, "bold"), bg="#6B4E3D", fg="white").pack(pady=20)

        btn_menu_produk = tk.Button(self.sidebar, text="Menu Produk", bg="#A6765A", fg="white",
                                    font=("Poppins", 14), command=self.show_menu_produk)
        btn_menu_produk.pack(fill="x", pady=5)

        btn_penjualan_harian = tk.Button(self.sidebar, text="Penjualan Harian(total)", bg="#A6765A", fg="white",
                                         font=("Poppins", 14), command=self.show_penjualan_harian)
        btn_penjualan_harian.pack(fill="x", pady=5)
        
        btn_penjualan_harian2 = tk.Button(self.sidebar,text ="Penjualan Harian",bg="#A6765A",fg="white",
                                          font=("Poppins",14), command=self.show_penjualan_harian_individu)
        btn_penjualan_harian2.pack(fill="x",pady=5)

        btn_prediksi = tk.Button(self.sidebar, text="Prediksi", bg="#A6765A", fg="white",
                                 font=("Poppins", 14), command=self.show_prediksi)
        btn_prediksi.pack(fill="x", pady=5)
        
        btn_penjualan_harian2 = tk.Button(self.sidebar,text ="Conver CSV ke Excel",bg="#A6765A",fg="white",
                                          font=("Poppins",14), command=self.ConvertCsvToExcel)
        btn_penjualan_harian2.pack(fill="x",pady=5)
        
        

    def clear_main_content(self):
        for widget in self.main_frame.winfo_children():
            if widget != self.sidebar:
                widget.destroy()

    def show_menu_produk(self):
        self.clear_main_content()
        content_frame = tk.Frame(self.main_frame, bg="white")
        content_frame.pack(side="right", fill="both", expand=True)

        # fungsi Scroll
        canvas = tk.Canvas(content_frame, bg="white")
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scrollable_frame, text="Menu Produk", font=("Poppins", 18, "bold"), bg="white").pack(pady=20)

        for product in self.products:
            product_frame = tk.Frame(scrollable_frame, bg="#F5F5F5", relief="solid", borderwidth=1)
            product_frame.pack(pady=10, padx=10, fill="x")
            

            tk.Label(product_frame, text=product["name"], font=("Poppins", 14), bg="#F5F5F5").pack(side="left", padx=10)
            tk.Label(product_frame, text=f"Rp{product['price']}", font=("Poppins", 12), bg="#F5F5F5", fg="#6B4E3D").pack(side="left", padx=10)

            quantity_label = tk.Label(product_frame, text="Jumlah:", font=("Poppins", 12), bg="#F5F5F5")
            quantity_label.pack(side="left", padx=10)

            quantity_entry = tk.Entry(product_frame, width=5)
            quantity_entry.pack(side="left", padx=5)

            tk.Button(product_frame, text="Tambah(Penjualan Total)", bg="#6B4E3D", fg="white", font=("Poppins", 12),
                      command=lambda p=product, q=quantity_entry: self.add_to_sales(p, q)).pack(side="right", padx=10)
            
            tk.Button(product_frame, text="Tambah", bg="#6B4E3D", fg="white", font=("Poppins", 12),
                      command=lambda p=product, q=quantity_entry: self.add_to_sales_individu(p, q)).pack(side="right", padx=10)
            
    def add_to_sales(self, product, quantity_entry):
        try:
            quantity = int(quantity_entry.get())
            if quantity <= 0:
                raise ValueError

            current_date = datetime.now().strftime("%Y-%m-%d")
            total_price = product["price"] * quantity

            for sale in self.sales_data:
                if sale["date"] == current_date and sale["item"] == product["name"]:
                    sale["quantity"] += quantity
                    sale["total"] += total_price
                    showinfo("Penjualan", f"{quantity} {product['name']} ditambahkan ke penjualan.")
                    return

            self.sales_data.append({
                "date": current_date,
                "item": product["name"],
                "quantity": quantity,
                "total": total_price
            })
            showinfo("Penjualan", f"{quantity} {product['name']} ditambahkan ke penjualan.")

        except ValueError:
            showinfo("Error", "Masukkan jumlah yang valid.")

    def show_penjualan_harian(self):
        self.clear_main_content()
        content_frame = tk.Frame(self.main_frame, bg="white")
        content_frame.pack(side="right", fill="both", expand=True)

        tk.Label(content_frame, text="Penjualan Harian", font=("Poppins", 18, "bold"), bg="white").pack(pady=20)

        table_frame = tk.Frame(content_frame, bg="white")
        table_frame.pack(fill="x", padx=20)

        headers = ["Tanggal", "Produk", "Jumlah", "Total", "Aksi"]
        for i, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=("Poppins", 12, "bold"), bg="white", fg="#6B4E3D").grid(row=0, column=i, padx=5, pady=5)

        for row, sale in enumerate(self.sales_data, start=1):
            tk.Label(table_frame, text=sale["date"], bg="white", font=("Poppins", 12)).grid(row=row, column=0, padx=5, pady=5)
            tk.Label(table_frame, text=sale["item"], bg="white", font=("Poppins", 12)).grid(row=row, column=1, padx=5, pady=5)
            tk.Label(table_frame, text=sale["quantity"], bg="white", font=("Poppins", 12)).grid(row=row, column=2, padx=5, pady=5)
            tk.Label(table_frame, text=f"Rp{sale['total']}", bg="white", font=("Poppins", 12)).grid(row=row, column=3, padx=5, pady=5)

            delete_button = tk.Button(table_frame, text="Hapus", bg="#D9534F", fg="white", font=("Poppins", 10),
                                       command=lambda r=row-1: self.delete_sale(r))
            delete_button.grid(row=row, column=4, padx=5, pady=5)

        save_button = tk.Button(content_frame, text="Simpan ke CSV", bg="#6B4E3D", fg="white", font=("Poppins", 14),
                                command=self.save_to_csv)
        save_button.pack(pady=20)
        
    def add_to_sales_individu(self, product, quantity_entry):
        try:
            quantity = int(quantity_entry.get())
            if quantity <= 0:
                raise ValueError

            current_date = datetime.now().strftime("%Y-%m-%d")
            current_time = datetime.now().strftime("%H:%M")  # Tambahkan waktu saat ini
        
            total_price = product["price"] * quantity

        # Tambahkan pesanan sebagai entri baru di self.sales_data
            self.sales_data_individu.append({
                "date": current_date,
                "time": current_time,  # Simpan waktu ke data
                "item": product["name"],
                "quantity": quantity,
                "total": total_price
            })
            showinfo("Penjualan", f"{quantity} {product['name']} ditambahkan ke penjualan.")
        except ValueError:
            showinfo("Error", "Masukkan jumlah yang valid.")
            
    def show_penjualan_harian_individu(self):
        self.clear_main_content()
        content_frame = tk.Frame(self.main_frame, bg="white")
        content_frame.pack(side="right", fill="both", expand=True)

        tk.Label(content_frame, text="Penjualan Harian", font=("Poppins", 18, "bold"), bg="white").pack(pady=20)

        table_frame = tk.Frame(content_frame, bg="white")
        table_frame.pack(fill="x", padx=20)

        headers = ["Tanggal", "Jam", "Produk", "Jumlah", "Total", "Aksi"]  # Tambahkan kolom Jam
        for i, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=("Poppins", 12, "bold"), bg="white", fg="#6B4E3D").grid(row=0, column=i, padx=5, pady=5)

        for row, sale in enumerate(self.sales_data_individu, start=1):
            tk.Label(table_frame, text=sale["date"], bg="white", font=("Poppins", 12)).grid(row=row, column=0, padx=5, pady=5)
            tk.Label(table_frame, text=sale["time"], bg="white", font=("Poppins", 12)).grid(row=row, column=1, padx=5, pady=5)  # Tampilkan Jam
            tk.Label(table_frame, text=sale["item"], bg="white", font=("Poppins", 12)).grid(row=row, column=2, padx=5, pady=5)
            tk.Label(table_frame, text=sale["quantity"], bg="white", font=("Poppins", 12)).grid(row=row, column=3, padx=5, pady=5)
            tk.Label(table_frame, text=f"Rp{sale['total']}", bg="white", font=("Poppins", 12)).grid(row=row, column=4, padx=5, pady=5)

            delete_button = tk.Button(table_frame, text="Hapus", bg="#D9534F", fg="white", font=("Poppins", 10),
                                   command=lambda r=row-1: self.delete_sale_individu(r))
            delete_button.grid(row=row, column=5, padx=5, pady=5)

        save_button = tk.Button(content_frame, text="Simpan ke CSV", bg="#6B4E3D", fg="white", font=("Poppins", 14),
                            command=self.save_to_csv_individu)
        save_button.pack(pady=20)



    
    def delete_sale(self, index):
        try:
            deleted_item = self.sales_data.pop(index)
            showinfo("Hapus Data", f"Data penjualan '{deleted_item['item']}' berhasil dihapus.")
            self.show_penjualan_harian()
        except IndexError:
            showinfo("Error", "Gagal menghapus data.")
            
    def delete_sale_individu(self, index):
        try:
            deleted_item = self.sales_data_individu.pop(index)
            showinfo("Hapus Data", f"Data penjualan '{deleted_item['item']}' berhasil dihapus.")
            self.show_penjualan_harian_individu()
        except IndexError:
            showinfo("Error", "Gagal menghapus data.")

    def save_to_csv(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if not filename:
                return

            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Tanggal","Produk", "Jumlah", "Total"])
                for sale in self.sales_data:
                    writer.writerow([sale["date"], sale["item"], sale["quantity"], sale["total"]])

            showinfo("Sukses", f"Data penjualan berhasil disimpan ke {filename}")
        except Exception as e:
            showinfo("Error", f"Gagal menyimpan data: {e}")
            
    def save_to_csv_individu(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if not filename:
                return

            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Tanggal","Jam","Produk", "Jumlah", "Total"])
                for sale in self.sales_data_individu:
                    writer.writerow([sale["date"],sale["time"] ,sale["item"], sale["quantity"], sale["total"]])

            showinfo("Sukses", f"Data penjualan berhasil disimpan ke {filename}")
        except Exception as e:
            showinfo("Error", f"Gagal menyimpan data: {e}")
            
    def ConvertCsvToExcel(self):
        try:
        # Membuka dialog untuk memilih file CSV
            csv_file = filedialog.askopenfilename(
            title="Pilih File CSV",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        
        # Jika file tidak dipilih, batalkan proses
            if not csv_file:
                showinfo("Informasi", "Tidak ada file yang dipilih.")
                return
        
        # Membaca file CSV
            data = pd.read_csv(csv_file)
        
        # Menentukan nama file Excel
            excel_file = filedialog.asksaveasfilename(
            title="Simpan Sebagai File Excel",
            defaultextension=".xlsx",
            filetypes=(("Excel Files", "*.xlsx"), ("All Files", "*.*"))
        )
        
        # Jika lokasi penyimpanan tidak dipilih, batalkan proses
            if not excel_file:
                showinfo("Informasi", "Penyimpanan file dibatalkan.")
                return
        
        # Menyimpan data ke file Excel
            data.to_excel(excel_file, index=False)
        
        # Menampilkan pesan sukses
            showinfo("Sukses", f"File CSV berhasil dikonversi ke Excel:\n{excel_file}")
        except Exception as e:
        # Menampilkan pesan error jika terjadi kesalahan
            showerror("Error", f"Gagal mengonversi file CSV ke Excel.\n\nDetail: {str(e)}")

    def show_prediksi(self):
        self.clear_main_content()
        content_frame = tk.Frame(self.main_frame, bg="white")
        content_frame.pack(side="right", fill="both", expand=True)

    # Canvas dan scrollbar 
        canvas = tk.Canvas(content_frame, bg="white")
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        self.prediction_frame = tk.Frame(canvas, bg="white")

        self.prediction_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.prediction_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # Label dan tombol di bagian prediksi
        tk.Label(self.prediction_frame, text="Prediksi Penjualan", font=("Poppins", 18, "bold"), bg="white").pack(pady=20)

        upload_button = tk.Button(self.prediction_frame, text="Upload File", bg="#6B4E3D", fg="white", font=("Poppins", 14),
                               command=self.upload_file)
        upload_button.pack(pady=20)

        self.loading_label = tk.Label(self.prediction_frame, text="", font=("Poppins", 12), bg="white", fg="green")
        self.loading_label.pack(pady=10)

        self.view_image_button = tk.Button(self.prediction_frame, text="Lihat Gambar", bg="#6B4E3D", fg="white",
                                       font=("Poppins", 14), command=self.view_images)
        self.view_image_button.pack(pady=10)
       
        self.view_image_button.pack_forget()   # <---- untuk Sembunyikan tombol hingga prediksi selesai

        self.images_frame = tk.Frame(self.prediction_frame, bg="white")
        self.images_frame.pack(fill="both", expand=True)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if file_path:
            showinfo("File Uploaded", f"File berhasil diunggah: {file_path}")
            self.run_prediction(file_path)

    def run_prediction(self, file_path):
        try:
            self.loading_label.config(text="Memproses prediksi, harap tunggu...")
            #self.root.update_idletasks()  #<---- untuk Refresh GUI untuk menampilkan label loading

        # menjalankan fungsi ProphetPredict yang tadi dibuat
            ProphetPredict(file_path)  #<--- gambar akan tersimpan di folder Gambar_prediksi

        # Gambar yang dihasilkan
            self.image_paths = [
                'Gambar_prediksi/prediksi_tren_penjualan.png',
                'Gambar_prediksi/komponen_prediksi.png',
                'Gambar_prediksi/rmse_horizon.png',
                'Gambar_prediksi/mse_horizon.png',
                'Gambar_prediksi/mape_horizon.png'
            ]

            self.loading_label.config(text="Prediksi selesai.")
            self.view_image_button.pack()  #<---- untuk menampilkan tombol lihnat gambar

        except Exception as e:
            self.loading_label.config(text="")
            showinfo("Error", f"Gagal memproses prediksi: {e}")

    def view_images(self):
        for widget in self.images_frame.winfo_children():
            widget.destroy()  #<----- untuk menghapus gambar sebelumnya

        for img_path in self.image_paths:
            try:
                img = Image.open(img_path)
                img = img.resize((600, 400), Image.Resampling.LANCZOS) 
                photo = ImageTk.PhotoImage(img)

                label = tk.Label(self.images_frame, image=photo, bg="white")
                label.image = photo  
                label.pack(pady=10)
            except Exception as e:
                tk.Label(self.images_frame, text=f"Gagal memuat gambar: {e}", bg="white", fg="red").pack(pady=10)


    
    def minimize_to_tray(self):
        # Sembunyikan jendela dan tambahkan ke tray
        self.root.withdraw()

        image = self.create_image_for_tray()
        menu = Menu(
            MenuItem("Tampilkan", self.restore_window),
            MenuItem("Keluar", self.exit_app)
        )
        self.tray_icon = Icon("AppKedaiKopi", image, "Aplikasi Kedai Kopi", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def restore_window(self, _icon=None, _item=None):
        # Tampilkan kembali
        self.root.deiconify()
        if self.tray_icon:
            self.tray_icon.stop()

    def create_image_for_tray(self):
    # Membuat ikon tray 
        width, height = 64, 64
        image = Image.new("RGBA", (width, height), (192, 192, 192, 255))  # Warna abu-abu
        return image


    def exit_app(self, _icon=None, _item=None):
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppKedaiKopi(root)
    root.mainloop()
