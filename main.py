import sqlite3
import os


# ======================================= CLASSE PRODUTO =======================================
class Produto():
    def __init__(self,nome,preco,quantidade,quantidadeMin):
        self.nome = str(nome)
        self.preco = float(preco)
        self.quantidade = int(quantidade)
        self.quantidadeMin = int(quantidadeMin)
        self.conn = ''
        self.cursor = ''

    def carregaConn(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'produtos.db'))
        self.cursor = self.conn.cursor()
    
    def cadatroProdutos(self):
        try:
            self.cursor.execute(f"""
            INSERT INTO produtos (nome,preco,quantidade,quantidadeMinima)
            VALUES ('{self.nome}',{self.preco},{self.quantidade},{self.quantidadeMin})
            """)
            self.conn.commit()
            return 0
        except Exception as e:
            return 1
        finally:
           self.conn.close()
        
    
    def adicionaEstoque(self):
        try:
            self.cursor.execute(f"""
            SELECT quantidade FROM produtos
            WHERE nome = '{self.nome}'
            """)
            for x in self.cursor.fetchall():
                numeroAtual = x
            numeroAdicionar = int(numeroAtual[0]) + self.quantidade
            self.cursor.execute(f"""
            UPDATE produtos
            SET quantidade = {numeroAdicionar}
            WHERE nome = '{self.nome}'
            """)
            self.conn.commit()
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            self.conn.close()

    def getQuantidadeAtual(self):
        self.cursor.execute(f"""

    SELECT quantidade FROM produtos
    WHERE nome = '{self.nome}'
""")
        a = self.cursor.fetchall()
        self.conn.close()
        return a
    
    def getTudo(self):
        self.cursor.execute(f"""

    SELECT * FROM produtos

""")
        a = self.cursor.fetchall()
        self.conn.close()
        return a

    def retiraProduto(self):
        self.cursor.execute(f"""
        SELECT quantidade FROM produtos
        WHERE nome = '{self.nome}'
        """)
        for x in self.cursor.fetchall():
            numeroRemover = x
        remover = int(numeroRemover[0]) - self.quantidade
        self.cursor.execute(f"""
        UPDATE produtos
        SET quantidade = {remover}
        WHERE nome = '{self.nome}'
        """)
        self.conn.commit()
        self.conn.close()
            
    def removeProduto(self):
        self.cursor.execute(f"""
        DELETE FROM produtos
        WHERE nome = '{self.nome}'
        """)
        self.conn.commit()
        self.conn.close()

    def produtoAbaixo(self):
        self.cursor.execute("""
SELECT nome FROM produtos
WHERE quantidade < quantidadeMinima
""")
        a = self.cursor.fetchall()
        return a
# =========================================================================================


# ======================================= CLASSE SISTEMA =======================================
class Sistema():
    def __init__(self):
        self.conn = ''
        self.cursor = ''

    def carregaConn(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'produtos.db'))
        self.cursor = self.conn.cursor()
    
    def confereCadastro(self,nome):
        retorno = 0
        self.cursor.execute(f"""
SELECT nome FROM produtos
""")
        a = self.cursor.fetchall()
        
        for x in a:
            if x[0] == nome:
                retorno = 1
        return retorno
# =========================================================================================


if __name__ == '__main__':
    try:
        opcao = 9
        conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'produtos.db'))
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos(
                    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nome varchar(80) not null,
                    preco float not null,
                    quantidade int not null,
                    quantidadeMinima integer not null
        );
    """)
        conn.close()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        input()
    
# =========================================== MENU PRINCIPAL ===========================================
    while opcao != 0: 
        print()
        os.system('cls')
        print(" ESTOQUE DA FRUTEIRA ".center(60,"="))
        print()
        print("OPÇÃO 1 - CADASTRAR PRODUTO")
        print("OPÇÃO 2 - ADICIONAR ESTOQUE")
        print("OPÇÃO 3 - RETIRAR ESTOQUE")
        print("OPÇÃO 4 - REMOVER PRODUTO")
        print("OPÇÃO 5 - VISUALIZAR ESTOQUE")
        print("OPÇÃO 0 - SAIR")
        opcao = int(input("\nInforme a OPÇÃO desejada: "))
# =======================================================================================================

        #=========================================== OPCÃO 1 / CADASTRAR PRODUTO ===========================================
        if opcao == 1:
            os.system('cls')
            print(" CADASTRO DE PRODUTO ".center(60,"="))
            nomeProduto = input("\nInforme o NOME do PRODUTO: ")
            precoProduto = float(input("Informe o PREÇO do PRODUTO: "))
            quantidade = int(input("Informe a QUANTIDADE ATUAL deste PRODUTO: "))
            quantidadeMin = int(input("Informe a QUANTIDADE MÍNIMA que este PRODUTO pode possuir: "))
            chamaSistema = Sistema()
            chamaSistema.carregaConn()
            b = chamaSistema.confereCadastro(nomeProduto)
            
            if b == 0:
                chamaProduto = Produto(nomeProduto,precoProduto,quantidade,quantidadeMin)
                chamaProduto.carregaConn()
                a = chamaProduto.cadatroProdutos()
                print(f"\n=== Produto {nomeProduto} CADASTRADO com SUCESSO! ===")
                input()
            else:
                print("\nERRO ao CADASTRAR PRODUTO!!! PRODUTO JÁ EXISTENTE")
                input()

        # =========================================== OPCÃO 2 / ADICIONAR ESTOQUE ===========================================
        elif opcao == 2:
            os.system('cls')
            print(" ADICIONANDO ESTOQUE ".center(60,"="))
            nome = input("\nInforme o NOME do PRODUTO: ")
            preco = 0
            quantidadeMin = 0
            adicionar = int(input("Informe a QUANTIDADE para ADICIONAR: "))
            chamaSistema = Sistema()
            chamaSistema.carregaConn()
            a = chamaSistema.confereCadastro(nome)

            if a == 1:
                chamaProduto = Produto(nome,preco,adicionar,quantidadeMin)
                chamaProduto.carregaConn()
                chamaProduto.adicionaEstoque()
                chamaProduto.carregaConn()
                a = chamaProduto.getQuantidadeAtual()

                os.system('cls')
                print(" ADICIONADO COM SUCESSO ".center(60,"="))
                for x in a:
                    print(f"\nVOCÊ ADICIONOU UM TOTAL DE {adicionar} {nome}(S)! A QUANTIDADE ATUAL É DE: {x[0]}")
                    input()
            else:
                print("\nNOME DE PRODUTO NÃO ENCONTRADO! ")
                input()
        #=================================================================================================================================

        #=========================================== OPCÃO 3 / RETIRAR ESTOQUE ===========================================
        elif opcao == 3:
            os.system('cls')
            print(" RETIRANDO ESTOQUE ".center(60,"="))
            nome = input("\nInforme o NOME do PRODUTO: ")
            quantidade = int(input("Informe a QUANTIDADE para RETIRAR: "))
            preco = 0
            quantidadeMin = 0
            chamaSistema = Sistema()
            chamaSistema.carregaConn()
            a = chamaSistema.confereCadastro(nome)
            aux = 0
            if a == 1:
                chamaProduto = Produto(nome,preco,quantidade,quantidadeMin)
                chamaProduto.carregaConn()
                atual = chamaProduto.getQuantidadeAtual()
                for x in atual:
                    if x[0] < quantidade:
                        print(f"\nVOCÊ NÃO POSSUI ESTOQUE SUFICIENTE! ESTOQUE ATUAL: {x[0]}")
                        aux = 1
                        input()
                if aux == 0:
                    chamaProduto = Produto(nome,preco,quantidade,quantidadeMin)
                    chamaProduto.carregaConn()
                    chamaProduto.retiraProduto()
                    chamaProduto.carregaConn()
                    atual = chamaProduto.getQuantidadeAtual()
                    os.system('cls')
                    print(" RETIRADO COM SUCESSO ".center(60,"="))
                    for x in atual:
                        print(f"\nVOCÊ RETIROU UM TOTAL DE {quantidade} {nome}(S)! A QUANTIDADE ATUAL É DE: {x[0]}")
                        input()
            else:
                print("\nNOME DE PRODUTO NÃO ENCONTRADO! ")
                input()
        #=================================================================================================================================

        #=========================================== OPCÃO 4 / REMOVER PRODUTO ===========================================
        elif opcao == 4:
            os.system('cls')
            print(" REMOVENDO PRODUTO ".center(60,"="))
            nome = input("\nInforme o PRODUTO que deseja REMOVER: ")
            preco = 0
            quantidade = 0
            quantidadeMin = 0
            chamaSistema = Sistema()
            chamaSistema.carregaConn()
            a = chamaSistema.confereCadastro()
            if a == 1:
                chamaProduto = Produto(nome,preco,quantidade,quantidadeMin)
                chamaProduto.carregaConn()
                chamaProduto.removeProduto()
            else:
                print("\nNOME DE PRODUTO NÃO ENCONTRADO! ")

         #=========================================== OPCÃO 5 / VISUALIZAR ESTOQUE ===========================================
        elif opcao == 5:
            os.system('cls')
            print(" ESTOQUE ATUAL  ".center(60,"="))
            print("\nID - NOME - PREÇO - QUANTIDADE ATUAL - QUANTIDADE MINIMA  ")
            chamaProduto = Produto('',0,0,0)
            chamaProduto.carregaConn()
            a = chamaProduto.getTudo()
            for x in a:
                print(x)
            chamaProduto.carregaConn()
            b = chamaProduto.produtoAbaixo()
            print("\n ====== ATENÇÃO! =====")
            print("PRODUTOS COM A QUANTIDADE ABAIXO DO MÍNIMO: ")
            for x in b:
                print(x[0])
            
            input()