from datetime import datetime
 
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer, HRFlowable
 
from reportlab.lib import colors
 
from reportlab.lib.pagesizes import A4
 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
 
from reportlab.lib.units import cm
 
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Dados Fixos da Empresa / Pessoa
 
EMPRESA_NOME = "Sua Empresa Ltda"
 
EMPRESA_DOCUMENTO = "CNPJ: 00.000.000/0001-00"
 
EMPRESA_ENDERECO = "Rua Exemplo, 123 - Itajubá/MG"

# Formatação de Número
 
def formatar_real(valor):
 
    texto = f"{valor:,.2f}"
 
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
 
    return f"R$ {texto}"

# Coleta de Dados pelo Usuário
 
numero_recibo = input("Número do recibo: \n")
 
recebido_de = input("Recebido de (nome/empresa): \n")
 
documento_cliente = input("CPF/CNPJ do cliente (opcional, Enter para pular): \n")
 
quantidade_itens = int(input("Quantos itens/serviços tem no recibo? \n"))
 
itens = []
 
for i in range(quantidade_itens):
 
    print(f"             Item {i + 1}            \n")
 
    data_item = input("Data: \n")
 
    nome_item = input("Descrição: \n")
 
    preco_item = float(input("Preço: \n"))
 
    itens.append([data_item, nome_item, preco_item])
 
subtotal = sum(item[2] for item in itens)
 
print(f"Subtotal: {formatar_real(subtotal)}")
 
desconto = float(input("Desconto (digite 0 se não tiver): \n"))
 
total = subtotal - desconto
 
print(f"Total final: {formatar_real(total)}\n")
 
# Formatação de Documento PDF

pdf = SimpleDocTemplate("recibo.pdf", pagesize=A4, topMargin=1.8 * cm, bottomMargin=1.8 * cm, leftMargin=2 * cm, rightMargin=2 * cm)
 
LARGURA_UTIL = pdf.width
 
COR_PRIMARIA = colors.HexColor("#1B3B6F")
 
COR_TEXTO_SECUNDARIO = colors.HexColor("#5A6472")
 
COR_ZEBRA = colors.HexColor("#F7F8FA")
 
COR_LINHA = colors.HexColor("#D8DCE3")
 
estilos = getSampleStyleSheet()
 
elementos = []

# Cabeçalho do Documento PDF
 
estilo_empresa_nome = ParagraphStyle("EmpresaNome", parent=estilos["Normal"], fontSize=15, fontName="Helvetica-Bold", textColor=COR_PRIMARIA, leading=18, spaceAfter=4)
 
estilo_empresa_info = ParagraphStyle("EmpresaInfo", parent=estilos["Normal"], fontSize=8.5, textColor=COR_TEXTO_SECUNDARIO, leading=12)
 
estilo_recibo_label = ParagraphStyle("ReciboLabel", parent=estilos["Normal"], fontSize=9, textColor=colors.white, alignment=TA_CENTER)
 
estilo_recibo_numero = ParagraphStyle("ReciboNumero", parent=estilos["Normal"], fontSize=16, fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_CENTER)
 
bloco_empresa = [Paragraph(EMPRESA_NOME, estilo_empresa_nome), Paragraph(EMPRESA_DOCUMENTO, estilo_empresa_info), Paragraph(EMPRESA_ENDERECO, estilo_empresa_info)]
 
caixa_recibo = Table([[Paragraph("RECIBO Nº", estilo_recibo_label)], [Paragraph(numero_recibo, estilo_recibo_numero)]], colWidths=[4.5 * cm])
 
caixa_recibo.setStyle(TableStyle([
 
    ("BACKGROUND", (0, 0), (-1, -1), COR_PRIMARIA),
 
    ("TOPPADDING", (0, 0), (-1, 0), 6),
 
    ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
 
    ("TOPPADDING", (0, 1), (-1, 1), 0),
 
    ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
 
]))
 
cabecalho = Table([[bloco_empresa, caixa_recibo]], colWidths=[LARGURA_UTIL - 4.5 * cm, 4.5 * cm])
 
cabecalho.setStyle(TableStyle([
 
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
 
    ("ALIGN", (1, 0), (1, 0), "RIGHT"),
 
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
 
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
 
]))
 
elementos.append(cabecalho)
 
elementos.append(Spacer(1, 0.5 * cm))
 
elementos.append(HRFlowable(width="100%", thickness=1.2, color=COR_PRIMARIA))
 
elementos.append(Spacer(1, 0.6 * cm))
 
 
estilo_label = ParagraphStyle("Label", parent=estilos["Normal"], fontSize=9.5, textColor=COR_TEXTO_SECUNDARIO)
 
estilo_valor = ParagraphStyle("Valor", parent=estilos["Normal"], fontSize=10.5, fontName="Helvetica-Bold")
 
data_emissao = datetime.now().strftime("%d/%m/%Y")
 
linhas_cliente = [[Paragraph("RECEBIDO DE", estilo_label), Paragraph("DATA DE EMISSÃO", estilo_label)], [Paragraph(recebido_de, estilo_valor), Paragraph(data_emissao, estilo_valor)]]
 
if documento_cliente.strip():
 
    linhas_cliente[0].insert(1, Paragraph("CPF/CNPJ", estilo_label))
 
    linhas_cliente[1].insert(1, Paragraph(documento_cliente, estilo_valor))
 
    larguras_cliente = [LARGURA_UTIL * 0.45, LARGURA_UTIL * 0.30, LARGURA_UTIL * 0.25]
 
else:
 
    larguras_cliente = [LARGURA_UTIL * 0.65, LARGURA_UTIL * 0.35]
 
tabela_cliente = Table(linhas_cliente, colWidths=larguras_cliente)
 
tabela_cliente.setStyle(TableStyle([
 
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
 
    ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
 
    ("TOPPADDING", (0, 1), (-1, 1), 0),
 
]))
 
elementos.append(tabela_cliente)
 
elementos.append(Spacer(1, 0.7 * cm))

# Formatação da Tabela do Documento PDF
 
DADOS = [["Data", "Descrição", "Valor"]]
 
for item in itens:
 
    DADOS.append([item[0], item[1], formatar_real(item[2])])
 
num_linhas_itens = len(itens)
 
col_data = LARGURA_UTIL * 0.18
 
col_valor = LARGURA_UTIL * 0.22
 
col_descricao = LARGURA_UTIL - col_data - col_valor
 
estilo_tabela = TableStyle([
 
    ("LINEBELOW", (0, 0), (-1, 0), 1, COR_PRIMARIA),
 
    ("LINEBELOW", (0, 1), (-1, -1), 0.5, COR_LINHA),
 
    ("BACKGROUND", (0, 0), (-1, 0), colors.white),
 
    ("TEXTCOLOR", (0, 0), (-1, 0), COR_PRIMARIA),
 
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
 
    ("FONTSIZE", (0, 0), (-1, 0), 9.5),
 
    *[("BACKGROUND", (0, i), (-1, i), COR_ZEBRA if i % 2 == 0 else colors.white) for i in range(1, num_linhas_itens + 1)],
 
    ("FONTSIZE", (0, 1), (-1, -1), 10),
 
    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
 
    ("TOPPADDING", (0, 0), (-1, -1), 7),
 
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
 
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
 
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
 
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
 
    ("ALIGN", (0, 0), (0, -1), "LEFT"),
 
    ("ALIGN", (-1, 0), (-1, -1), "RIGHT"),
 
])
 
tabela = Table(DADOS, colWidths=[col_data, col_descricao, col_valor], style=estilo_tabela)
 
elementos.append(tabela)
 
elementos.append(Spacer(1, 0.5 * cm))
 
 
estilo_total_label = ParagraphStyle("TotalLabel", parent=estilos["Normal"], fontSize=10, alignment=TA_RIGHT)
 
estilo_total_valor = ParagraphStyle("TotalValor", parent=estilos["Normal"], fontSize=10, alignment=TA_RIGHT)
 
estilo_final_label = ParagraphStyle("FinalLabel", parent=estilos["Normal"], fontSize=12, fontName="Helvetica-Bold", textColor=COR_PRIMARIA, alignment=TA_RIGHT)
 
estilo_final_valor = ParagraphStyle("FinalValor", parent=estilos["Normal"], fontSize=12, fontName="Helvetica-Bold", textColor=COR_PRIMARIA, alignment=TA_RIGHT)
 
linhas_totais = [
 
    [Paragraph("Subtotal", estilo_total_label), Paragraph(formatar_real(subtotal), estilo_total_valor)],
 
    [Paragraph("Desconto", estilo_total_label), Paragraph(f"- {formatar_real(desconto)}", estilo_total_valor)],
 
    [Paragraph("TOTAL", estilo_final_label), Paragraph(formatar_real(total), estilo_final_valor)],
 
]
 
largura_totais = LARGURA_UTIL * 0.45
 
tabela_totais = Table(linhas_totais, colWidths=[largura_totais * 0.5, largura_totais * 0.5], hAlign="RIGHT")
 
tabela_totais.setStyle(TableStyle([
 
    ("LINEABOVE", (0, -1), (-1, -1), 1, COR_PRIMARIA),
 
    ("TOPPADDING", (0, 0), (-1, -2), 4),
 
    ("BOTTOMPADDING", (0, 0), (-1, -2), 4),
 
    ("TOPPADDING", (0, -1), (-1, -1), 8),
 
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
 
]))
 
elementos.append(tabela_totais)
 
elementos.append(Spacer(1, 2 * cm))
 
 
estilo_assinatura = ParagraphStyle("Assinatura", parent=estilos["Normal"], alignment=TA_CENTER, fontSize=10)
 
elementos.append(Paragraph("_" * 45, estilo_assinatura))
 
elementos.append(Paragraph(f"{EMPRESA_NOME}", estilo_assinatura))
 
elementos.append(Spacer(1, 1.2 * cm))
 
estilo_rodape = ParagraphStyle("Rodape", parent=estilos["Normal"], alignment=TA_CENTER, fontSize=8, textColor=COR_TEXTO_SECUNDARIO)
 
elementos.append(HRFlowable(width="100%", thickness=0.5, color=COR_LINHA))
 
elementos.append(Spacer(1, 0.3 * cm))
 
elementos.append(Paragraph(f"{EMPRESA_NOME} · {EMPRESA_DOCUMENTO} · Documento gerado eletronicamente", estilo_rodape))
 
# Gera o Documento PDF

pdf.build(elementos)