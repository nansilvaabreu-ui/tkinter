import os
import tkinter as tk
from tkinter import filedialog, messagebox

# ==========================================
# DADOS E ESTADO DA APLICAÇÃO
# ==========================================
email_salvo = ""
senha_salva = ""

modo_formulario = ""
linha_edicao_index = None
anexo_selecionado = ""
pagina_atual = {"PACIENTE": 1, "PALESTRA": 1, "CONSULTA": 1}

# Armazena os textos de placeholder atuais de cada campo do formulário
placeholders_form = {
    "esq": "",
    "dir": "",
    "c2": "",
    "c3": "",
    "c4": "",
}

dados_pacientes = [
    ["João Silva", "123.456.789-00", "Masculino", "30", "12/09/2026"],
    ["Maria Oliveira", "987.654.321-11", "Feminino", "42", "15/09/2026"],
    ["Carlos Eduardo", "456.789.123-22", "Masculino", "25", "18/09/2026"],
    ["Ana Beatriz", "321.654.987-33", "Feminino", "38", "20/09/2026"],
    ["Lucas Mendes", "654.987.321-44", "Masculino", "50", "22/09/2026"],
    ["Fernanda Lima", "789.123.456-55", "Feminino", "29", "25/09/2026"],
    ["Roberto Almeida", "111.222.333-44", "Masculino", "45", "28/09/2026"],
    ["Juliana Costa", "555.666.777-88", "Feminino", "33", "30/09/2026"],
]

dados_palestras = [
    ["Nutrição Esportiva", "15/10/2026", "Auditório A", "R$ 150", "2h"],
    ["Saúde Mental no Trabalho", "20/10/2026", "Sala 3", "Gratuito", "1h 30m"],
    ["Primeiros Socorros", "05/11/2026", "Auditório Principal", "R$ 80", "4h"],
    ["Ergonomia e Postura", "12/11/2026", "Online (Zoom)", "R$ 50", "1h"],
    ["Alimentação Saudável", "01/12/2026", "Auditório B", "R$ 100", "2h"],
    ["Prevenção Cardiovascular", "10/12/2026", "Auditório A", "Gratuito", "1h 30m"],
    ["Qualidade do Sono", "15/12/2026", "Sala 2", "R$ 60", "1h"],
    ["Gestão do Estresse", "20/12/2026", "Online (Zoom)", "Gratuito", "2h"],
]

# Estrutura: [Paciente, Médico, Data, Local, Preparo/Obs, Anexo]
dados_consultas = [
    [
        "João Silva",
        "Dr. Carlos Santos",
        "12/09",
        "83145 Maggie Plaza Suite 204 - Lawton, IA / 71846",
        "Jejum de 12 horas",
        "",
    ],
    [
        "Maria Oliveira",
        "Dr. Carlos Santos",
        "14/09",
        "Av. Paulista, 1000 - São Paulo, SP",
        "Trazer exames anteriores",
        "",
    ],
    [
        "Carlos Eduardo",
        "Dra. Ana Costa",
        "18/09",
        "Rua das Flores, 123 - Centro",
        "Jejum de 8 horas",
        "",
    ],
    [
        "Ana Beatriz",
        "Dr. Carlos Santos",
        "20/09",
        "83145 Maggie Plaza Suite 204 - Lawton, IA / 71846",
        "Sem preparo específico",
        "",
    ],
    [
        "Lucas Mendes",
        "Dra. Ana Costa",
        "22/09",
        "Rua das Flores, 123 - Centro",
        "Repouso antes da coleta",
        "",
    ],
    [
        "Fernanda Lima",
        "Dr. Carlos Santos",
        "25/09",
        "Av. Paulista, 1000 - São Paulo, SP",
        "Jejum de 12 horas",
        "",
    ],
    [
        "Roberto Almeida",
        "Dra. Ana Costa",
        "28/09",
        "Rua das Flores, 123 - Centro",
        "Aferição de pressão",
        "",
    ],
    [
        "Juliana Costa",
        "Dr. Carlos Santos",
        "30/09",
        "83145 Maggie Plaza Suite 204 - Lawton, IA / 71846",
        "Retorno clínico",
        "",
    ],
]

# Paleta de cores
COR_AZUL_ESCURO = "#1e88c9"
COR_AZUL_TEXTO = "#2b8cc4"
COR_AZUL_CARD = "#96d8fa"
COR_AZUL_CLARO = "#dff2fd"
COR_AZUL_BORDA = "#bce3fa"
COR_CINZA_CAMPO = "#eaeaea"
COR_SOMBRA = "#d8d8d8"
COR_ZEBRA = "#f4f9fc"
FONTE_PADRAO = "Helvetica Neue"


# ==========================================
# COMPONENTES VISUAIS VETORIAIS (CANVAS)
# ==========================================
def desenhar_retangulo_arredondado(
    canvas, x1, y1, x2, y2, raio=12, fill="", outline="", width=1
):
  pontos = [
      x1 + raio,
      y1,
      x2 - raio,
      y1,
      x2,
      y1,
      x2,
      y1 + raio,
      x2,
      y2 - raio,
      x2,
      y2,
      x2 - raio,
      y2,
      x1 + raio,
      y2,
      x1,
      y2,
      x1,
      y2 - raio,
      x1,
      y1 + raio,
      x1,
      y1,
  ]
  return canvas.create_polygon(
      pontos, smooth=True, fill=fill, outline=outline, width=width
  )


def desenhar_logo_amais(canvas, x, y, escala=1.0):
  s = escala
  canvas.create_text(
      x - 16 * s,
      y,
      text="a",
      font=(FONTE_PADRAO, int(52 * s), "bold"),
      fill="#1e88c9",
  )
  canvas.create_rectangle(
      x + 8 * s,
      y - 24 * s,
      x + 18 * s,
      y + 24 * s,
      fill="#c6d92c",
      outline="",
  )
  canvas.create_rectangle(
      x - 10 * s,
      y - 5 * s,
      x + 36 * s,
      y + 5 * s,
      fill="#c6d92c",
      outline="",
  )
  canvas.create_text(
      x + 14 * s,
      y,
      text="MAIS",
      font=(FONTE_PADRAO, int(13 * s), "bold"),
      fill="#1e88c9",
      angle=12,
  )


def criar_input_arredondado(
    parent,
    largura=360,
    altura=46,
    placeholder="",
    eh_senha=False,
    bg_campo=COR_CINZA_CAMPO,
    borda="",
    com_sombra=True,
    icone=None,
):
  cv = tk.Canvas(
      parent,
      width=largura + 4,
      height=altura + 6,
      bg="white",
      highlightthickness=0,
  )

  if com_sombra:
    desenhar_retangulo_arredondado(
        cv, 2, 4, largura + 2, altura + 4, raio=14, fill=COR_SOMBRA, outline=""
    )

  desenhar_retangulo_arredondado(
      cv,
      2,
      2,
      largura + 2,
      altura + 2,
      raio=14,
      fill=bg_campo,
      outline=borda,
      width=1 if borda else 0,
  )

  largura_texto = largura - (42 if icone else 24)
  ent = tk.Entry(
      cv,
      font=(FONTE_PADRAO, 12),
      bg=bg_campo,
      fg="#777777" if placeholder else COR_AZUL_TEXTO,
      bd=0,
      relief="flat",
      highlightthickness=0,
      insertbackground=COR_AZUL_ESCURO,
  )
  cv.create_window(
      16, (altura // 2) + 2, window=ent, anchor="w", width=largura_texto
  )

  if placeholder:
    ent.insert(0, placeholder)
    ent.bind("<FocusIn>", lambda e: on_focus_in(ent, placeholder, eh_senha))
    ent.bind("<FocusOut>", lambda e: on_focus_out(ent, placeholder, eh_senha))

  if icone == "cadeado":
    ix, iy = largura - 18, (altura // 2) + 2
    cv.create_arc(
        ix - 4,
        iy - 9,
        ix + 4,
        iy - 1,
        start=0,
        extent=180,
        style="arc",
        outline=COR_AZUL_TEXTO,
        width=1.4,
    )
    desenhar_retangulo_arredondado(
        cv,
        ix - 5,
        iy - 4,
        ix + 5,
        iy + 6,
        raio=3,
        fill="white",
        outline=COR_AZUL_TEXTO,
        width=1.4,
    )
    cv.create_oval(ix - 1, iy, ix + 1, iy + 2, fill=COR_AZUL_TEXTO, outline="")

  return cv, ent


def criar_botao_arredondado(
    parent,
    texto,
    comando,
    largura=360,
    altura=46,
    bg=COR_AZUL_ESCURO,
    fg="white",
    borda="",
    com_sombra=True,
    icone_nuvem=False,
):
  cv = tk.Canvas(
      parent,
      width=largura + 4,
      height=altura + 6,
      bg="white",
      highlightthickness=0,
      cursor="hand2",
  )

  if com_sombra:
    desenhar_retangulo_arredondado(
        cv, 2, 4, largura + 2, altura + 4, raio=14, fill=COR_SOMBRA, outline=""
    )

  fundo = desenhar_retangulo_arredondado(
      cv,
      2,
      2,
      largura + 2,
      altura + 2,
      raio=14,
      fill=bg,
      outline=borda,
      width=1.3 if borda else 0,
  )

  txt_id = cv.create_text(
      (largura // 2) + 2,
      (altura // 2) + 2,
      text=texto,
      font=(FONTE_PADRAO, 11, "bold" if not icone_nuvem else "normal"),
      fill=fg,
  )

  if icone_nuvem:
    nx, ny = largura - 24, (altura // 2) + 2
    cv.create_arc(
        nx - 10,
        ny - 4,
        nx - 2,
        ny + 4,
        start=90,
        extent=180,
        style="arc",
        outline=COR_AZUL_TEXTO,
        width=1.3,
    )
    cv.create_arc(
        nx - 6,
        ny - 8,
        nx + 6,
        ny + 4,
        start=0,
        extent=180,
        style="arc",
        outline=COR_AZUL_TEXTO,
        width=1.3,
    )
    cv.create_arc(
        nx + 2,
        ny - 4,
        nx + 10,
        ny + 4,
        start=270,
        extent=180,
        style="arc",
        outline=COR_AZUL_TEXTO,
        width=1.3,
    )
    cv.create_line(
        nx - 6, ny + 4, nx + 6, ny + 4, fill=COR_AZUL_TEXTO, width=1.3
    )
    cv.create_line(nx, ny - 1, nx, ny + 7, fill=COR_AZUL_TEXTO, width=1.4)
    cv.create_line(nx - 3, ny + 2, nx, ny - 1, fill=COR_AZUL_TEXTO, width=1.4)
    cv.create_line(nx + 3, ny + 2, nx, ny - 1, fill=COR_AZUL_TEXTO, width=1.4)

  def on_click(event):
    comando()

  def on_enter(event):
    if bg == COR_AZUL_ESCURO:
      cv.itemconfig(fundo, fill="#166fa6")
    elif bg == COR_AZUL_CLARO:
      cv.itemconfig(fundo, fill="#cceafd")

  def on_leave(event):
    cv.itemconfig(fundo, fill=bg)

  cv.bind("<Button-1>", on_click)
  cv.bind("<Enter>", on_enter)
  cv.bind("<Leave>", on_leave)
  return cv, txt_id


# ==========================================
# NAVEGAÇÃO E LÓGICA DE AUTENTICAÇÃO
# ==========================================
def mostrar_tela(tela_para_mostrar):
  tela_para_mostrar.tkraise()
  janela.focus_set()


def on_focus_in(entry, texto_padrao, eh_senha=False):
  if entry.get() == texto_padrao:
    entry.delete(0, tk.END)
    entry.config(fg=COR_AZUL_TEXTO if not eh_senha else "#333333")
    if eh_senha:
      entry.config(show="*")


def on_focus_out(entry, texto_padrao, eh_senha=False):
  if entry.get().strip() == "":
    if eh_senha:
      entry.config(show="")
    entry.delete(0, tk.END)
    entry.insert(0, texto_padrao)
    entry.config(fg="#88a8bd" if not eh_senha else "#777777")


def vincular_placeholder_dinamico(entry, chave_placeholder):
  """Permite alterar o placeholder dinamicamente conforme o formulário aberto."""
  entry.bind(
      "<FocusIn>",
      lambda e: on_focus_in(entry, placeholders_form[chave_placeholder]),
  )
  entry.bind(
      "<FocusOut>",
      lambda e: on_focus_out(entry, placeholders_form[chave_placeholder]),
  )


def configurar_campo_form(entry, chave, valor_inicial, placeholder_texto):
  placeholders_form[chave] = placeholder_texto
  entry.delete(0, tk.END)
  if valor_inicial:
    entry.insert(0, valor_inicial)
    entry.config(fg=COR_AZUL_TEXTO)
  else:
    entry.insert(0, placeholder_texto)
    entry.config(fg="#88a8bd")


def obter_valor_limpo(entry, chave):
  val = entry.get().strip()
  if val == placeholders_form[chave]:
    return ""
  return val


def salvar_cadastro():
  global email_salvo, senha_salva
  novo_email = entrada_novo_email.get().strip()
  nova_senha = entrada_nova_senha.get().strip()

  if novo_email in ["", "e-mail"] or nova_senha in ["", "senha"]:
    messagebox.showwarning(
        "Aviso", "Preencha todos os campos para cadastrar!"
    )
    return

  email_salvo = novo_email
  senha_salva = nova_senha
  messagebox.showinfo(
      "Sucesso", "Acesso criado com sucesso! Faça o login."
  )
  mostrar_tela(tela_login)


def fazer_login():
  email = entrada_email.get().strip()
  senha = entrada_senha.get().strip()

  if email == email_salvo and senha == senha_salva and email_salvo != "":
    mostrar_tela(tela_dashboard)
  else:
    messagebox.showerror(
        "Erro", "E-mail ou senha incorretos (ou conta não criada)!"
    )


# ==========================================
# CONFIGURAÇÃO DA JANELA PRINCIPAL
# ==========================================
janela = tk.Tk()
janela.title("a+ MAIS - Portal Médico")
janela.geometry("1366x768")
janela.configure(bg="white")

janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)

tela_login = tk.Frame(janela, bg="white")
tela_cadastro = tk.Frame(janela, bg="white")
tela_dashboard = tk.Frame(janela, bg="white")
tela_pacientes = tk.Frame(janela, bg="white")
tela_palestras = tk.Frame(janela, bg="white")
tela_consultas = tk.Frame(janela, bg="white")
tela_formulario_generico = tk.Frame(janela, bg="white")

todas_as_telas = [
    tela_login,
    tela_cadastro,
    tela_dashboard,
    tela_pacientes,
    tela_palestras,
    tela_consultas,
    tela_formulario_generico,
]

for t in todas_as_telas:
  t.grid(row=0, column=0, sticky="nsew")


# ==========================================
# CABEÇALHO PADRÃO DAS TELAS INTERNAS
# ==========================================
def criar_cabecalho(parent, mostrar_voltar=False, comando_voltar=None):
  header = tk.Frame(parent, bg="white")
  header.pack(fill="x", padx=45, pady=(25, 10))

  left_cv = tk.Canvas(
      header, width=420, height=72, bg="white", highlightthickness=0
  )
  left_cv.pack(side="left")

  # Avatar circular
  left_cv.create_oval(
      4, 4, 68, 68, fill="#a4dcfa", outline=COR_AZUL_ESCURO, width=1.5
  )
  left_cv.create_oval(
      26, 16, 46, 36, fill="white", outline=COR_AZUL_ESCURO, width=1.3
  )
  left_cv.create_arc(
      25,
      14,
      47,
      30,
      start=0,
      extent=180,
      fill="#8ccff5",
      outline=COR_AZUL_ESCURO,
      width=1.2,
  )
  left_cv.create_arc(
      16,
      38,
      56,
      74,
      start=0,
      extent=180,
      fill="#8ccff5",
      outline=COR_AZUL_ESCURO,
      width=1.3,
  )
  left_cv.create_polygon(
      36,
      40,
      33,
      54,
      36,
      58,
      39,
      54,
      fill="white",
      outline=COR_AZUL_ESCURO,
      width=1,
  )

  # Pílula BEM VINDO JUAN
  desenhar_retangulo_arredondado(
      left_cv, 88, 16, 265, 56, raio=20, fill=COR_AZUL_CLARO, outline=""
  )
  left_cv.create_text(
      176,
      36,
      text="BEM VINDO JUAN",
      font=(FONTE_PADRAO, 10, "bold"),
      fill=COR_AZUL_ESCURO,
  )

  # Sino de notificações
  bx, by = 305, 36
  left_cv.create_arc(
      bx - 9,
      by - 12,
      bx + 9,
      by + 6,
      start=0,
      extent=180,
      style="arc",
      outline=COR_AZUL_TEXTO,
      width=1.4,
  )
  left_cv.create_line(
      bx - 9, by - 3, bx - 12, by + 8, fill=COR_AZUL_TEXTO, width=1.4
  )
  left_cv.create_line(
      bx + 9, by - 3, bx + 12, by + 8, fill=COR_AZUL_TEXTO, width=1.4
  )
  left_cv.create_line(
      bx - 12, by + 8, bx + 12, by + 8, fill=COR_AZUL_TEXTO, width=1.4
  )
  left_cv.create_arc(
      bx - 3,
      by + 6,
      bx + 3,
      by + 12,
      start=180,
      extent=180,
      style="arc",
      outline=COR_AZUL_TEXTO,
      width=1.4,
  )

  # Logo direita
  right_cv = tk.Canvas(
      header, width=110, height=60, bg="white", highlightthickness=0
  )
  right_cv.pack(side="right")
  desenhar_logo_amais(right_cv, 55, 30, escala=0.52)

  # Botão Voltar
  if mostrar_voltar:
    sub_header = tk.Frame(parent, bg="white")
    sub_header.pack(fill="x", padx=105, pady=(5, 0))

    voltar_cv = tk.Canvas(
        sub_header,
        width=130,
        height=34,
        bg="white",
        highlightthickness=0,
        cursor="hand2",
    )
    voltar_cv.pack(side="left")

    voltar_cv.create_polygon(
        6,
        17,
        18,
        7,
        18,
        13,
        32,
        13,
        32,
        21,
        18,
        21,
        18,
        27,
        fill="white",
        outline=COR_AZUL_TEXTO,
        width=1.3,
    )
    voltar_cv.create_text(
        68, 17, text="Voltar", font=(FONTE_PADRAO, 12), fill=COR_AZUL_TEXTO
    )

    if comando_voltar:
      voltar_cv.bind("<Button-1>", lambda e: comando_voltar())


# ==========================================
# FORMULÁRIO DE ADIÇÃO, EDIÇÃO E EXCLUSÃO
# ==========================================
def selecionar_anexo():
  global anexo_selecionado
  caminho = filedialog.askopenfilename(title="Selecionar Anexo")
  if caminho:
    anexo_selecionado = os.path.basename(caminho)
    btn_anexo_cv.itemconfig(
        txt_anexo_id, text=f"Anexo: {anexo_selecionado[:28]}"
    )


def abrir_formulario(tipo, index=None):
  global modo_formulario, linha_edicao_index, anexo_selecionado
  modo_formulario = tipo
  linha_edicao_index = index
  anexo_selecionado = ""

  eh_edicao = index is not None
  acao_txt = "EDITAR" if eh_edicao else "ADICIONAR"
  lbl_tit_form.config(text=f"{acao_txt} {tipo}")
  btn_salvar_cv.itemconfig(
      txt_salvar_id, text="SALVAR ALTERAÇÕES" if eh_edicao else f"ADICIONAR {tipo}"
  )
  btn_anexo_cv.itemconfig(txt_anexo_id, text="Anexo")

  # Mostrar ou ocultar botão de excluir
  if eh_edicao:
    btn_excluir_lbl.pack(pady=(6, 0))
  else:
    btn_excluir_lbl.pack_forget()

  for f in [
      frame_linha_dupla,
      frame_campo2,
      frame_campo3,
      frame_campo4,
      frame_campo5,
  ]:
    f.pack_forget()

  if tipo == "CONSULTA":
    frame_linha_dupla.pack(pady=6)
    frame_campo2.pack(pady=6)
    frame_campo3.pack(pady=6)
    frame_campo4.pack(pady=6)
    frame_campo5.pack(pady=6)

    d = dados_consultas[index] if eh_edicao else ["", "", "", "", "", ""]
    configurar_campo_form(ent_dupla_esq, "esq", d[0], "Nome do Paciente")
    configurar_campo_form(ent_dupla_dir, "dir", d[2], "Data (DD/MM)")
    configurar_campo_form(ent2, "c2", d[3], "Endereço / Local da Consulta")
    configurar_campo_form(
        ent3, "c3", d[4] if len(d) > 4 else "", "Preparo / Observações"
    )
    configurar_campo_form(ent4, "c4", d[1], "Médico Responsável")

    if eh_edicao and len(d) > 5 and d[5]:
      anexo_selecionado = d[5]
      btn_anexo_cv.itemconfig(
          txt_anexo_id, text=f"Anexo: {anexo_selecionado[:28]}"
      )

  elif tipo == "PACIENTE":
    frame_linha_dupla.pack(pady=6)
    frame_campo2.pack(pady=6)
    frame_campo3.pack(pady=6)
    frame_campo4.pack(pady=6)

    d = dados_pacientes[index] if eh_edicao else ["", "", "", "", ""]
    configurar_campo_form(ent_dupla_esq, "esq", d[0], "Nome Completo do Paciente")
    configurar_campo_form(ent_dupla_dir, "dir", d[3], "Idade")
    configurar_campo_form(ent2, "c2", d[1], "Documento (CPF)")
    configurar_campo_form(ent3, "c3", d[2], "Sexo (Masculino / Feminino)")
    configurar_campo_form(ent4, "c4", d[4], "Última Consulta (DD/MM/AAAA)")

  elif tipo == "PALESTRA":
    frame_linha_dupla.pack(pady=6)
    frame_campo2.pack(pady=6)
    frame_campo3.pack(pady=6)
    frame_campo4.pack(pady=6)

    d = dados_palestras[index] if eh_edicao else ["", "", "", "", ""]
    configurar_campo_form(ent_dupla_esq, "esq", d[0], "Título da Palestra")
    configurar_campo_form(ent_dupla_dir, "dir", d[1], "Data")
    configurar_campo_form(ent2, "c2", d[2], "Local / Auditório")
    configurar_campo_form(ent3, "c3", d[3], "Valor (ex: R$ 100 ou Gratuito)")
    configurar_campo_form(ent4, "c4", d[4], "Duração (ex: 2h)")

  mostrar_tela(tela_formulario_generico)


def salvar_formulario():
  v_esq = obter_valor_limpo(ent_dupla_esq, "esq")
  v_dir = obter_valor_limpo(ent_dupla_dir, "dir")
  v2 = obter_valor_limpo(ent2, "c2")
  v3 = obter_valor_limpo(ent3, "c3")
  v4 = obter_valor_limpo(ent4, "c4")

  if not v_esq:
    messagebox.showwarning(
        "Campo obrigatório", "Por favor, preencha o campo principal!"
    )
    return

  if modo_formulario == "CONSULTA":
    novo_registro = [
        v_esq,
        v4 or "Dr. Carlos Santos",
        v_dir or "A definir",
        v2 or "Consultório",
        v3,
        anexo_selecionado,
    ]
    if linha_edicao_index is not None:
      dados_consultas[linha_edicao_index] = novo_registro
    else:
      dados_consultas.append(novo_registro)
      pagina_atual["CONSULTA"] = ((len(dados_consultas) - 1) // 8) + 1

    construir_tabela(
        tela_consultas,
        "CONSULTAS",
        ["Paciente", "Médico", "Data", "Local", "Ações"],
        dados_consultas,
        "CONSULTA",
    )
    mostrar_tela(tela_consultas)

  elif modo_formulario == "PACIENTE":
    novo_registro = [
        v_esq,
        v2 or "000.000.000-00",
        v3 or "Não informado",
        v_dir or "0",
        v4 or "-",
    ]
    if linha_edicao_index is not None:
      dados_pacientes[linha_edicao_index] = novo_registro
    else:
      dados_pacientes.append(novo_registro)
      pagina_atual["PACIENTE"] = ((len(dados_pacientes) - 1) // 8) + 1

    construir_tabela(
        tela_pacientes,
        "PACIENTES",
        ["Nome", "Documento", "Sexo", "Idade", "Última Consulta", "Ações"],
        dados_pacientes,
        "PACIENTE",
    )
    mostrar_tela(tela_pacientes)

  elif modo_formulario == "PALESTRA":
    novo_registro = [
        v_esq,
        v_dir or "A definir",
        v2 or "Auditório",
        v3 or "Gratuito",
        v4 or "1h",
    ]
    if linha_edicao_index is not None:
      dados_palestras[linha_edicao_index] = novo_registro
    else:
      dados_palestras.append(novo_registro)
      pagina_atual["PALESTRA"] = ((len(dados_palestras) - 1) // 8) + 1

    construir_tabela(
        tela_palestras,
        "PALESTRAS",
        ["Palestra", "Data", "Local", "Valor", "Duração", "Ações"],
        dados_palestras,
        "PALESTRA",
    )
    mostrar_tela(tela_palestras)

  acao_msg = "atualizado" if linha_edicao_index is not None else "adicionado"
  messagebox.showinfo(
      "Sucesso", f"{modo_formulario.capitalize()} {acao_msg} com sucesso!"
  )


def excluir_registro():
  if linha_edicao_index is None:
    return

  if not messagebox.askyesno(
      "Confirmar exclusão",
      f"Deseja realmente excluir este registro de {modo_formulario.lower()}?",
  ):
    return

  if modo_formulario == "CONSULTA":
    dados_consultas.pop(linha_edicao_index)
    pagina_atual["CONSULTA"] = 1
    construir_tabela(
        tela_consultas,
        "CONSULTAS",
        ["Paciente", "Médico", "Data", "Local", "Ações"],
        dados_consultas,
        "CONSULTA",
    )
    mostrar_tela(tela_consultas)

  elif modo_formulario == "PACIENTE":
    dados_pacientes.pop(linha_edicao_index)
    pagina_atual["PACIENTE"] = 1
    construir_tabela(
        tela_pacientes,
        "PACIENTES",
        ["Nome", "Documento", "Sexo", "Idade", "Última Consulta", "Ações"],
        dados_pacientes,
        "PACIENTE",
    )
    mostrar_tela(tela_pacientes)

  elif modo_formulario == "PALESTRA":
    dados_palestras.pop(linha_edicao_index)
    pagina_atual["PALESTRA"] = 1
    construir_tabela(
        tela_palestras,
        "PALESTRAS",
        ["Palestra", "Data", "Local", "Valor", "Duração", "Ações"],
        dados_palestras,
        "PALESTRA",
    )
    mostrar_tela(tela_palestras)


# ==========================================
# CONSTRUTOR DE TABELAS (PACIENTES, PALESTRAS, CONSULTAS)
# ==========================================
def mudar_pagina(parent, titulo, colunas, lista_dados, tipo_entidade, num_pag):
  pagina_atual[tipo_entidade] = num_pag
  construir_tabela(parent, titulo, colunas, lista_dados, tipo_entidade)


def construir_tabela(parent, titulo, colunas, lista_dados, tipo_entidade):
  for widget in parent.winfo_children():
    widget.destroy()

  criar_cabecalho(
      parent,
      mostrar_voltar=True,
      comando_voltar=lambda: mostrar_tela(tela_dashboard),
  )

  # Barra superior com título centralizado e botão + Adicionar
  top_bar = tk.Frame(parent, bg="white")
  top_bar.pack(fill="x", padx=90, pady=(0, 20))
  top_bar.grid_columnconfigure(0, weight=1)
  top_bar.grid_columnconfigure(1, weight=2)
  top_bar.grid_columnconfigure(2, weight=1)

  lbl_titulo = tk.Label(
      top_bar,
      text=titulo,
      font=(FONTE_PADRAO, 22, "bold"),
      fg=COR_AZUL_ESCURO,
      bg="white",
  )
  lbl_titulo.grid(row=0, column=1)

  btn_add, _ = criar_botao_arredondado(
      top_bar,
      f"+ Adicionar {tipo_entidade.capitalize()}",
      lambda: abrir_formulario(tipo_entidade, None),
      largura=175,
      altura=36,
      bg=COR_AZUL_CLARO,
      fg=COR_AZUL_ESCURO,
      com_sombra=False,
  )
  btn_add.grid(row=0, column=2, sticky="e")

  # Tabela
  table_frame = tk.Frame(parent, bg="white")
  table_frame.pack(expand=True, fill="both", padx=90)

  for col_idx in range(len(colunas)):
    table_frame.grid_columnconfigure(col_idx, weight=1)

  for col_idx, col_nome in enumerate(colunas):
    lbl_col = tk.Label(
        table_frame,
        text=col_nome,
        font=(FONTE_PADRAO, 12, "bold"),
        fg=COR_AZUL_ESCURO,
        bg="white",
        pady=12,
    )
    lbl_col.grid(row=0, column=col_idx, sticky="ew")

  sep = tk.Frame(table_frame, bg="#e8f3fa", height=1)
  sep.grid(row=1, column=0, columnspan=len(colunas), sticky="ew")

  itens_por_pagina = 8
  total_paginas = max(1, (len(lista_dados) + itens_por_pagina - 1) // itens_por_pagina)
  pag = min(pagina_atual.get(tipo_entidade, 1), total_paginas)
  pagina_atual[tipo_entidade] = pag

  inicio = (pag - 1) * itens_por_pagina
  fim = inicio + itens_por_pagina
  dados_exibidos = lista_dados[inicio:fim]

  num_cols_dados = len(colunas) - 1

  for row_idx, item in enumerate(dados_exibidos, start=2):
    bg_cor = COR_ZEBRA if row_idx % 2 == 1 else "white"
    idx_real = inicio + (row_idx - 2)

    for col_idx in range(num_cols_dados):
      valor = item[col_idx] if col_idx < len(item) else ""
      if len(str(valor)) > 26:
        valor = str(valor)[:24] + "..."
      lbl_dado = tk.Label(
          table_frame,
          text=valor,
          font=(FONTE_PADRAO, 12),
          fg=COR_AZUL_TEXTO,
          bg=bg_cor,
          pady=11,
      )
      lbl_dado.grid(row=row_idx, column=col_idx, sticky="ew")

    btn_acao = tk.Label(
        table_frame,
        text="Editar",
        font=(FONTE_PADRAO, 12, "underline"),
        fg=COR_AZUL_TEXTO,
        bg=bg_cor,
        cursor="hand2",
        pady=11,
    )
    btn_acao.grid(row=row_idx, column=len(colunas) - 1, sticky="ew")
    btn_acao.bind(
        "<Button-1>", lambda e, idx=idx_real: abrir_formulario(tipo_entidade, idx)
    )

  # Paginação inferior
  pagi_frame = tk.Frame(parent, bg="white")
  pagi_frame.pack(pady=(15, 30))

  qtd_botoes_pag = max(6, total_paginas)
  for p in range(1, qtd_botoes_pag + 1):
    ativo = p == pag
    p_cv = tk.Canvas(
        pagi_frame,
        width=28,
        height=28,
        bg="white",
        highlightthickness=0,
        cursor="hand2",
    )
    p_cv.pack(side="left", padx=3)
    if ativo:
      desenhar_retangulo_arredondado(
          p_cv, 2, 2, 26, 26, raio=6, fill=COR_AZUL_ESCURO, outline=""
      )
    p_cv.create_text(
        14,
        14,
        text=str(p),
        font=(FONTE_PADRAO, 11, "bold" if ativo else "normal"),
        fill="white" if ativo else COR_AZUL_TEXTO,
    )
    p_cv.bind(
        "<Button-1>",
        lambda e, num=p: mudar_pagina(
            parent, titulo, colunas, lista_dados, tipo_entidade, num
        ),
    )


# ==========================================
# 1. TELA DE LOGIN
# ==========================================
login_box = tk.Frame(tela_login, bg="white")
login_box.place(relx=0.5, rely=0.47, anchor="center")

logo_cv = tk.Canvas(
    login_box, width=260, height=130, bg="white", highlightthickness=0
)
logo_cv.pack(pady=(0, 35))

if os.path.exists("image 1.png"):
  minha_imagem = tk.PhotoImage(file="image 1.png")
  logo_cv.create_image(130, 65, image=minha_imagem)
  logo_cv.image = minha_imagem
else:
  desenhar_logo_amais(logo_cv, 125, 65, escala=1.45)

cv_email, entrada_email = criar_input_arredondado(
    login_box, largura=390, altura=48, placeholder="e-mail"
)
cv_email.pack(pady=8)

cv_senha, entrada_senha = criar_input_arredondado(
    login_box, largura=390, altura=48, placeholder="senha", eh_senha=True
)
cv_senha.pack(pady=8)

btn_acessar, _ = criar_botao_arredondado(
    login_box, "ACESSAR", fazer_login, largura=390, altura=48
)
btn_acessar.pack(pady=(16, 28))

link_primeiro_acesso = tk.Label(
    login_box,
    text="PRIMEIRO ACESSO",
    font=(FONTE_PADRAO, 11, "bold"),
    bg="white",
    fg=COR_AZUL_ESCURO,
    cursor="hand2",
)
link_primeiro_acesso.pack()
link_primeiro_acesso.bind("<Button-1>", lambda e: mostrar_tela(tela_cadastro))


# ==========================================
# 2. TELA DE CADASTRO (PRIMEIRO ACESSO)
# ==========================================
cad_box = tk.Frame(tela_cadastro, bg="white")
cad_box.place(relx=0.5, rely=0.47, anchor="center")

logo_cad_cv = tk.Canvas(
    cad_box, width=260, height=130, bg="white", highlightthickness=0
)
logo_cad_cv.pack(pady=(0, 35))

if os.path.exists("image 1.png"):
  logo_cad_cv.create_image(130, 65, image=minha_imagem)
else:
  desenhar_logo_amais(logo_cad_cv, 125, 65, escala=1.45)

cv_novo_email, entrada_novo_email = criar_input_arredondado(
    cad_box, largura=390, altura=48, placeholder="e-mail"
)
cv_novo_email.pack(pady=8)

cv_nova_senha, entrada_nova_senha = criar_input_arredondado(
    cad_box, largura=390, altura=48, placeholder="senha", eh_senha=True
)
cv_nova_senha.pack(pady=8)

btn_salvar_cad, _ = criar_botao_arredondado(
    cad_box, "CADASTRAR E VOLTAR", salvar_cadastro, largura=390, altura=48
)
btn_salvar_cad.pack(pady=(16, 20))

link_voltar_login = tk.Label(
    cad_box,
    text="VOLTAR AO LOGIN",
    font=(FONTE_PADRAO, 10, "bold"),
    bg="white",
    fg=COR_AZUL_TEXTO,
    cursor="hand2",
)
link_voltar_login.pack()
link_voltar_login.bind("<Button-1>", lambda e: mostrar_tela(tela_login))


# ==========================================
# 3. TELA DASHBOARD
# ==========================================
criar_cabecalho(tela_dashboard)

body_frame = tk.Frame(tela_dashboard, bg="white")
body_frame.pack(expand=True)

lbl_perfil = tk.Label(
    body_frame,
    text="PERFIL: MÉDICO",
    font=(FONTE_PADRAO, 10, "bold"),
    fg=COR_AZUL_ESCURO,
    bg="white",
)
lbl_perfil.grid(row=0, column=0, sticky="w", pady=(0, 8), padx=18)

cards_container = tk.Frame(body_frame, bg="white")
cards_container.grid(row=1, column=0)


def criar_card_vetorial(parent, tipo_icone, titulo, comando):
  cv = tk.Canvas(
      parent,
      width=215,
      height=215,
      bg="white",
      highlightthickness=0,
      cursor="hand2",
  )
  fundo = desenhar_retangulo_arredondado(
      cv, 4, 4, 211, 211, raio=22, fill=COR_AZUL_CARD, outline=""
  )

  cx, cy = 107, 88
  if tipo_icone == "paciente":
    cv.create_oval(
        cx - 19,
        cy - 44,
        cx + 19,
        cy - 6,
        fill="white",
        outline=COR_AZUL_ESCURO,
        width=1.6,
    )
    cv.create_arc(
        cx - 21,
        cy - 48,
        cx + 21,
        cy - 20,
        start=0,
        extent=180,
        fill="#b8e5fc",
        outline=COR_AZUL_ESCURO,
        width=1.5,
    )
    cv.create_arc(
        cx - 34,
        cy - 2,
        cx + 34,
        cy + 58,
        start=0,
        extent=180,
        fill="#b8e5fc",
        outline=COR_AZUL_ESCURO,
        width=1.6,
    )
  elif tipo_icone == "calendario":
    cv.create_rectangle(
        cx - 42,
        cy - 42,
        cx + 42,
        cy + 42,
        fill="white",
        outline=COR_AZUL_ESCURO,
        width=1.5,
    )
    cv.create_rectangle(
        cx - 42,
        cy - 42,
        cx + 42,
        cy - 31,
        fill="#b8e5fc",
        outline=COR_AZUL_ESCURO,
        width=1.5,
    )
    cv.create_rectangle(
        cx - 42,
        cy + 34,
        cx + 42,
        cy + 42,
        fill="#b8e5fc",
        outline=COR_AZUL_ESCURO,
        width=1.5,
    )
    cv.create_text(
        cx, cy + 2, text="12", font=(FONTE_PADRAO, 28), fill=COR_AZUL_ESCURO
    )

  cv.create_text(
      107, 165, text=titulo, font=(FONTE_PADRAO, 14, "bold"), fill="white"
  )

  cv.bind("<Button-1>", lambda e: comando())
  cv.bind("<Enter>", lambda e: cv.itemconfig(fundo, fill="#82cef7"))
  cv.bind("<Leave>", lambda e: cv.itemconfig(fundo, fill=COR_AZUL_CARD))
  return cv


card1 = criar_card_vetorial(
    cards_container, "paciente", "PACIENTES", lambda: mostrar_tela(tela_pacientes)
)
card1.pack(side="left", padx=18)

card2 = criar_card_vetorial(
    cards_container,
    "calendario",
    "PALESTRAS",
    lambda: mostrar_tela(tela_palestras),
)
card2.pack(side="left", padx=18)

card3 = criar_card_vetorial(
    cards_container,
    "calendario",
    "CONSULTAS",
    lambda: mostrar_tela(tela_consultas),
)
card3.pack(side="left", padx=18)

footer_frame = tk.Frame(tela_dashboard, bg="white")
footer_frame.pack(side="bottom", pady=45)

ajuda_cv = tk.Canvas(
    footer_frame,
    width=290,
    height=40,
    bg="white",
    highlightthickness=0,
    cursor="hand2",
)
ajuda_cv.pack()
ajuda_cv.create_text(
    115,
    20,
    text="PRECISA DE AJUDA?",
    font=(FONTE_PADRAO, 15, "bold"),
    fill=COR_AZUL_ESCURO,
)

fx, fy = 248, 20
ajuda_cv.create_oval(
    fx - 15,
    fy - 15,
    fx + 15,
    fy + 15,
    fill="#eef7fd",
    outline=COR_AZUL_TEXTO,
    width=1.2,
)
ajuda_cv.create_oval(
    fx - 5, fy - 5, fx - 1, fy - 1, fill="white", outline=COR_AZUL_TEXTO, width=1
)
ajuda_cv.create_oval(
    fx + 2, fy - 5, fx + 6, fy - 1, fill="white", outline=COR_AZUL_TEXTO, width=1
)
ajuda_cv.create_arc(
    fx - 7,
    fy + 3,
    fx + 7,
    fy + 11,
    start=0,
    extent=180,
    style="arc",
    outline=COR_AZUL_TEXTO,
    width=1.2,
)
ajuda_cv.create_text(
    fx - 10, fy - 8, text="?", font=(FONTE_PADRAO, 10, "bold"), fill=COR_AZUL_ESCURO
)
ajuda_cv.bind(
    "<Button-1>",
    lambda e: messagebox.showinfo(
        "Suporte a+ MAIS",
        "Central de Atendimento Médico:\nE-mail: suporte@amais.com.br\nTelefone: (11) 4002-8922",
    ),
)


# ==========================================
# 4. CONSTRUÇÃO INICIAL DAS 3 TABELAS
# ==========================================
construir_tabela(
    tela_pacientes,
    "PACIENTES",
    ["Nome", "Documento", "Sexo", "Idade", "Última Consulta", "Ações"],
    dados_pacientes,
    "PACIENTE",
)
construir_tabela(
    tela_palestras,
    "PALESTRAS",
    ["Palestra", "Data", "Local", "Valor", "Duração", "Ações"],
    dados_palestras,
    "PALESTRA",
)
construir_tabela(
    tela_consultas,
    "CONSULTAS",
    ["Paciente", "Médico", "Data", "Local", "Ações"],
    dados_consultas,
    "CONSULTA",
)


# ==========================================
# 5. TELA DE FORMULÁRIO GENÉRICO (ADICIONAR / EDITAR / EXCLUIR)
# ==========================================
def voltar_do_formulario():
  if modo_formulario == "PACIENTE":
    mostrar_tela(tela_pacientes)
  elif modo_formulario == "PALESTRA":
    mostrar_tela(tela_palestras)
  elif modo_formulario == "CONSULTA":
    mostrar_tela(tela_consultas)


criar_cabecalho(
    tela_formulario_generico,
    mostrar_voltar=True,
    comando_voltar=voltar_do_formulario,
)

lbl_tit_form = tk.Label(
    tela_formulario_generico,
    text="EDITAR CONSULTA",
    font=(FONTE_PADRAO, 22, "bold"),
    fg=COR_AZUL_ESCURO,
    bg="white",
)
lbl_tit_form.pack(pady=(0, 20))

form_container = tk.Frame(tela_formulario_generico, bg="white")
form_container.pack(expand=True, anchor="n")

# Linha 1: Dois campos lado a lado
frame_linha_dupla = tk.Frame(form_container, bg="white")
cv_dupla_esq, ent_dupla_esq = criar_input_arredondado(
    frame_linha_dupla,
    largura=305,
    altura=44,
    bg_campo="#f8fcff",
    borda=COR_AZUL_BORDA,
    com_sombra=False,
    icone="cadeado",
)
cv_dupla_esq.pack(side="left", padx=(0, 12))
vincular_placeholder_dinamico(ent_dupla_esq, "esq")

cv_dupla_dir, ent_dupla_dir = criar_input_arredondado(
    frame_linha_dupla,
    largura=98,
    altura=44,
    bg_campo="#f8fcff",
    borda=COR_AZUL_BORDA,
    com_sombra=False,
    icone="cadeado",
)
cv_dupla_dir.pack(side="left")
vincular_placeholder_dinamico(ent_dupla_dir, "dir")

# Linha 2
frame_campo2 = tk.Frame(form_container, bg="white")
cv_c2, ent2 = criar_input_arredondado(
    frame_campo2,
    largura=418,
    altura=44,
    bg_campo="#f8fcff",
    borda=COR_AZUL_BORDA,
    com_sombra=False,
    icone="cadeado",
)
cv_c2.pack()
vincular_placeholder_dinamico(ent2, "c2")

# Linha 3
frame_campo3 = tk.Frame(form_container, bg="white")
cv_c3, ent3 = criar_input_arredondado(
    frame_campo3,
    largura=418,
    altura=44,
    bg_campo="#f8fcff",
    borda=COR_AZUL_BORDA,
    com_sombra=False,
)
cv_c3.pack()
vincular_placeholder_dinamico(ent3, "c3")

# Linha 4
frame_campo4 = tk.Frame(form_container, bg="white")
cv_c4, ent4 = criar_input_arredondado(
    frame_campo4,
    largura=418,
    altura=44,
    bg_campo="#f8fcff",
    borda=COR_AZUL_BORDA,
    com_sombra=False,
    icone="cadeado",
)
cv_c4.pack()
vincular_placeholder_dinamico(ent4, "c4")

# Linha 5: Botão Anexo
frame_campo5 = tk.Frame(form_container, bg="white")
btn_anexo_cv, txt_anexo_id = criar_botao_arredondado(
    frame_campo5,
    "Anexo",
    selecionar_anexo,
    largura=418,
    altura=44,
    bg="#f8fcff",
    fg=COR_AZUL_TEXTO,
    borda=COR_AZUL_ESCURO,
    com_sombra=False,
    icone_nuvem=True,
)
btn_anexo_cv.pack()

# Botão Salvar / Editar
btn_salvar_cv, txt_salvar_id = criar_botao_arredondado(
    form_container,
    "EDITAR",
    salvar_formulario,
    largura=418,
    altura=46,
    bg=COR_AZUL_CLARO,
    fg=COR_AZUL_ESCURO,
    com_sombra=False,
)
btn_salvar_cv.pack(pady=(14, 4))

# Link discreto para excluir quando estiver no modo edição
btn_excluir_lbl = tk.Label(
    form_container,
    text="EXCLUIR REGISTRO",
    font=(FONTE_PADRAO, 9, "bold"),
    fg="#d9534f",
    bg="white",
    cursor="hand2",
)
btn_excluir_lbl.bind("<Button-1>", lambda e: excluir_registro())

# Iniciar na tela de Login
mostrar_tela(tela_login)
janela.mainloop()
