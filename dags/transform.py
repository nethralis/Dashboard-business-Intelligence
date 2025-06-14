import pandas as pd

def transform_transaction_data(input_path, output_path):
    """
    Fungsi untuk mentransformasi data transaksi dari CSV.
    
    Params:
    - input_path: path ke file CSV mentah
    - output_path: path untuk menyimpan file hasil transformasi
    """
    # Step 1: Load data dengan delimiter ';'
    df = pd.read_csv(input_path, delimiter=';')

    # Step 2: Hapus spasi di nama kolom
    df.columns = [col.strip() for col in df.columns]

    # Step 3: Hapus baris duplikat (jika ada)
    df.drop_duplicates(inplace=True)

    # Step 4: Konversi tipe data numerik
    df['Transaction Amount'] = pd.to_numeric(df['Transaction Amount'], errors='coerce')
    df['Latency (ms)'] = pd.to_numeric(df['Latency (ms)'], errors='coerce')
    df['Slice Bandwidth (Mbps)'] = pd.to_numeric(df['Slice Bandwidth (Mbps)'], errors='coerce')
    df['PIN Code'] = pd.to_numeric(df['PIN Code'], errors='coerce')

    # Step 5: Parsing kolom Timestamp
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

    # Step 7: Simpan hasil transformasi ke CSV
    df.to_csv(output_path, index=False)

    return df
