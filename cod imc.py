# -*- coding: utf-8 -*-

import sqlite3
from PyQt5 import QtWidgets, QtCore  # Certifique-se de que o QtCore seja importado corretamente
from mainwindow import Ui_MainWindow

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('imc.db')  # Conecta ao banco de dados (ou cria um novo)
        self.create_table()

    def create_table(self):
        # Cria a tabela se não existir
        query = '''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            endereco TEXT,
            altura REAL,
            peso REAL,
            imc REAL,
            situacao TEXT
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def insert_data(self, nome, endereco, altura, peso, imc, situacao):
        # Insere os dados na tabela
        query = '''
        INSERT INTO pacientes (nome, endereco, altura, peso, imc, situacao)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.conn.execute(query, (nome, endereco, altura, peso, imc, situacao))
        self.conn.commit()

    def close(self):
        self.conn.close()


class IMCApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.database = Database()  # Instancia o banco de dados

        # Configura o título da janela
        self.setWindowTitle("Cálculo do IMC - Índice de Massa Corporal")

        # Conectar botões às suas funções
        self.calcular_button.clicked.connect(self.calcular_imc)
        self.reiniciar_button.clicked.connect(self.reiniciar)
        self.sair_button.clicked.connect(self.close)

    def calcular_imc(self):
        try:
            # Pega os valores de altura e peso, convertendo altura de cm para metros
            altura_cm = float(self.altura_input.text())
            peso = float(self.peso_input.text())
            altura_m = altura_cm / 100  # Conversão para metros

            # Calcula o IMC
            imc = peso / (altura_m ** 2)

            # Avalia a situação com base no valor do IMC
            if imc < 17:
                situacao = "Muito abaixo do peso"
            elif 17 <= imc <= 18.49:
                situacao = "Abaixo do peso"
            elif 18.5 <= imc <= 24.99:
                situacao = "Peso normal"
            elif 25 <= imc <= 29.99:
                situacao = "Acima do peso"
            elif 30 <= imc <= 34.99:
                situacao = "Obesidade I"
            elif 35 <= imc <= 39.99:
                situacao = "Obesidade II (severa)"
            else:
                situacao = "Obesidade III (mórbida)"

            # Exibe o IMC e a situação no rótulo de resultado
            self.resultado_label.setText(f"IMC: {imc:.2f} - {situacao}")

            # Salvar dados no banco de dados
            nome = self.nome_input.text()
            endereco = self.endereco_input.text()
            self.database.insert_data(nome, endereco, altura_cm, peso, imc, situacao)

        except ValueError:
            # Mensagem de erro para valores inválidos
            self.resultado_label.setText("Por favor, insira valores numéricos válidos para altura e peso.")

    def reiniciar(self):
        # Limpar todos os campos
        self.nome_input.clear()
        self.endereco_input.clear()
        self.altura_input.clear()
        self.peso_input.clear()
        self.resultado_label.setText("RESULTADO")

    def closeEvent(self, event):
        self.database.close()  # Fecha a conexão ao sair
        event.accept()


app = QtWidgets.QApplication([])
window = IMCApp()
window.show()
app.exec_()