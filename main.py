import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Aplicacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualização Estatística")
        self.root.geometry("1000x600")
        self.df = None
        self.criar_interface()

    def criar_interface(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        botoes = [
            ("Abrir CSV", self.abrir_csv),
            ("Estatísticas", self.estatisticas),
            ("Correlação", self.correlacao),
            ("Histograma", self.histograma),
            ("Scatter Plot", self.scatter),
            ("Box Plot", self.boxplot),
        ]

        for i, (texto, comando) in enumerate(botoes):
            tk.Button(frame, text=texto, command=comando).grid(row=0, column=i, padx=5)

        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill="both", expand=True)

    def abrir_csv(self):
        ficheiro = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not ficheiro:
            return
        self.df = pd.read_csv(ficheiro)
        self.mostrar_dados()
        messagebox.showinfo("Sucesso", "CSV carregado com sucesso")

    def mostrar_dados(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.df.columns)
        self.tree["show"] = "headings"

        for col in self.df.columns:
            self.tree.heading(col, text=col)

        for _, linha in self.df.iterrows():
            self.tree.insert("", "end", values=list(linha))

    def estatisticas(self):
        if self.df is None:
            return
        janela = tk.Toplevel()
        janela.title("Estatísticas")
        texto = tk.Text(janela, width=100, height=30)
        texto.pack()
        texto.insert(tk.END, str(self.df.describe()))

    def correlacao(self):
        if self.df is None:
            return
        matriz = self.df.corr(numeric_only=True)
        sns.heatmap(matriz, annot=True)
        plt.title("Matriz de Correlação")
        plt.show()

    def histograma(self):
        if self.df is None:
            return
        coluna = self.df.select_dtypes(include="number").columns[0]
        plt.hist(self.df[coluna], bins=10)
        plt.title(f"Histograma - {coluna}")
        plt.show()

    def scatter(self):
        if self.df is None:
            return
        cols = self.df.select_dtypes(include="number").columns
        if len(cols) < 2:
            return
        plt.scatter(self.df[cols[0]], self.df[cols[1]])
        plt.xlabel(cols[0])
        plt.ylabel(cols[1])
        plt.title("Scatter Plot")
        plt.show()

    def boxplot(self):
        if self.df is None:
            return
        coluna = self.df.select_dtypes(include="number").columns[0]
        sns.boxplot(y=self.df[coluna])
        plt.title(f"Box Plot - {coluna}")
        plt.show()

root = tk.Tk()
Aplicacao(root)
root.mainloop()
