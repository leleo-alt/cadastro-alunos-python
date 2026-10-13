import os
import sqlite3

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_banco = os.path.join(diretorio_atual, "sistema_alunos.db")

# Conecta ao banco de dados (cria o arquivo 'sistema_alunos.db' se não existir)
conn = sqlite3.connect(caminho_banco)
cursor = conn.cursor()

# Cria a tabela de alunos caso ela ainda não exista
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        curso TEXT NOT NULL
    )
"""
)
conn.commit()


def limpar_tela():
  # Funciona tanto no Windows quanto no Linux/Mac
  os.system("cls" if os.name == "nt" else "clear")


def cadastrar_aluno():
  print("\n--- CADASTRO DE ALUNO ---")
  nome = input("Informe o nome do aluno: ").strip().capitalize()
  curso = input("E agr, informe o curso em que ele(a) estuda: ").strip().capitalize()

  if nome and curso:
    cursor.execute(
        "INSERT INTO alunos (nome, curso) VALUES (?, ?)", (nome, curso)
    )
    conn.commit()
    print(f"\n{nome} cadastrado com sucesso!")
  else:
    print("\nNome e curso não podem estar em branco.")


def listar_aluno():
  print("\n---- LISTA DE ALUNOS ----")
  cursor.execute("SELECT id, nome, curso FROM alunos")
  alunos = cursor.fetchall()

  if not alunos:
    print("Nenhum aluno cadastrado!")
  else:
    for id_aluno, nome, curso in alunos:
      print(f"ID: {id_aluno} | Nome: {nome} | Curso: {curso}")


def buscar_aluno():
  print("\n---- BUSCAR ALUNO ----")
  busca = input("Digite o nome do aluno para realizar a busca: ").strip().capitalize()

  # O '%' permite buscar por nomes parecidos
  cursor.execute(
      "SELECT id, nome, curso FROM alunos WHERE nome LIKE ?", (f"%{busca}%",)
  )
  resultados = cursor.fetchall()

  if resultados:
    print("\nResultados encontrados:")
    for id_aluno, nome, curso in resultados:
      print(f"ID: {id_aluno} | Nome: {nome} | Curso: {curso}")
  else:
    print("\nAluno não encontrado!")


def atualizar_aluno():
  print("\n---- ATUALIZAR ALUNO (UPDATE) ----")
  listar_aluno()

  id_aluno = input(
      "\nDigite o ID do aluno que deseja atualizar: "
  ).strip()

  cursor.execute("SELECT * FROM alunos WHERE id = ?", (id_aluno,))
  aluno = cursor.fetchone()

  if aluno:
    novo_nome = (
        input(f"Novo nome (Atual: {aluno[1]}): ").strip().capitalize()
    )
    novo_curso = (
        input(f"Novo curso (Atual: {aluno[2]}): ").strip().capitalize()
    )

    nome_final = novo_nome if novo_nome else aluno[1]
    curso_final = novo_curso if novo_curso else aluno[2]

    cursor.execute(
        "UPDATE alunos SET nome = ?, curso = ? WHERE id = ?",
        (nome_final, curso_final, id_aluno),
    )
    conn.commit()
    print("\nDados do aluno atualizados com sucesso!")
  else:
    print("\nAluno não encontrado!")


def deletar_aluno():
  print("\n---- DELETAR ALUNO ----")
  listar_aluno()

  id_aluno = input("\nQual o ID do aluno que deseja remover? ").strip()

  cursor.execute("SELECT nome FROM alunos WHERE id = ?", (id_aluno,))
  aluno = cursor.fetchone()

  if aluno:
    cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))
    conn.commit()
    print(f"\nAluno '{aluno[0]}' removido com sucesso!")
  else:
    print("\nAluno não encontrado!")


# --- MENU PRINCIPAL ---
while True:
  print("\n" + "-" * 25)
  print("Sistema de Gestão Léo")
  print("1 - Cadastrar aluno")
  print("2 - Listar alunos")
  print("3 - Buscar aluno")
  print("4 - Atualizar aluno")
  print("5 - Deletar aluno")
  print("6 - Sair")

  opcao = input("Digite um número: ").strip()

  if opcao == "1":
    cadastrar_aluno()
  elif opcao == "2":
    listar_aluno()
  elif opcao == "3":
    buscar_aluno()
  elif opcao == "4":
    atualizar_aluno()
  elif opcao == "5":
    deletar_aluno()
  elif opcao == "6":
    print("Saindo do sistema... Até logo!")
    conn.close()  # Fecha a conexão com o banco de dados com segurança
    break
  else:
    print("Opção inválida! Tente novamente.")


     
    

