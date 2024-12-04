import sqlite3


class CalculadoraIMC:
    def __init__(self):
        self.conexao = sqlite3.connect('imc_calculadora.db')
        self.cursor = self.conexao.cursor()
        self._criar_tabela()

    def _criar_tabela(self):
        self.conexao.commit()

    def calcular_imc(self, nome, peso, altura):
        try:
            if altura <= 0 or peso <= 0:
                raise ValueError("Peso e altura devem ser maiores que zero.")

            imc = peso / (altura ** 2)
            classificacao = self._classificar_imc(imc)
            self._salvar_registro(nome, peso, altura, imc, classificacao)
            return imc, classificacao
        except Exception as e:
            return f"Erro: {e}"

    def _classificar_imc(self, imc):
        if imc < 18.5:
            return "Abaixo do peso"
        elif 18.5 <= imc < 24.9:
            return "Peso normal"
        elif 25 <= imc < 29.9:
            return "Sobrepeso"
        elif 30 <= imc < 34.9:
            return "Obesidade grau 1"
        elif 35 <= imc < 39.9:
            return "Obesidade grau 2"
        else:
            return "Obesidade grau 3"

    def _salvar_registro(
        self, nome, peso, altura, imc, classificacao):
        self.cursor.execute (nome, peso, altura, imc, classificacao)
        self.conexao.commit()

    def exibir_historico(self):
        registros = self.cursor.fetchall()
        return registros

    def fechar_conexao(self):
        self.conexao.close()


def menu():
    calc = CalculadoraIMC()
    while True:
        print("\n=== Calculadora de IMC ===")
        print("1. Calcular IMC")
        print("2. Ver resultados")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            try:
                nome = input("Digite seu nome: ")
                peso = float(input("Digite seu peso (kg): "))
                altura = float (input("Digite sua altura (m): "))
                imc, classificacao = calc.calcular_imc(nome, peso, altura)
                print(f"\nSeu IMC: {imc:.2f}")
                print(f"Classificação: {classificacao}")
            except ValueError:
                print("Entrada inválida. Certifique-se de digitar números para peso e altura.")
        elif escolha == '2':
            historico = calc.exibir_historico()
            print("\n=== Histórico de IMC ===")
            for reg in historico:
                print(
                    f"ID: {reg[0]} | Nome: {reg[1]} | Peso: {reg[2]}kg | Altura: {reg[3]}m | IMC: {reg[4]:.2f} | Classificação: {reg[5]}")
        elif escolha == '3':
            calc.fechar_conexao()
            print("Encerrando...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == '__main__':
    menu()
