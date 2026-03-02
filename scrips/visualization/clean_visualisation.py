import os
import pandas as pd
import tkinter as tk
from tkinter import ttk

def show_raw_csv():
    # Obtener la carpeta donde está este script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construir ruta a ../data/raw/sampler.csv
    path = os.path.join(script_dir, "..", "..", "data", "processed", "cleaned_sampler.csv")
    # Normalizar la ruta (eliminar ..)
    path = os.path.normpath(path)
    
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"Archivo no encontrado en {path}. Verifica la ruta.")
        return

    root = tk.Tk()
    root.title("Vista cruda del CSV")
    root.geometry("1200x600")

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    vsb = ttk.Scrollbar(frame, orient="vertical")
    hsb = ttk.Scrollbar(frame, orient="horizontal")

    tree = ttk.Treeview(frame, columns=list(df.columns), show="headings",
                        yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, minwidth=80, stretch=False)  # Redimensionable manualmente

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    for idx, row in df.iterrows():
        values = [str(v) if pd.notna(v) else "" for v in row]
        tree.insert("", "end", values=values)

    info_label = ttk.Label(root, text=f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
    info_label.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    show_raw_csv()