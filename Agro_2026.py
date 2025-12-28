import streamlit as st
from fpdf import FPDF
import base64
import os
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DE CAMINHO DA LOGO ---
caminho_logo = os.path.join(os.path.expanduser("~"), "Desktop", "logo_AmazingDrone.png")

# Configuração da Página
st.set_page_config(page_title="AmazingDrone Smart Analytics", layout="wide")


# --- CLASSE PARA PDF PROFISSIONAL COM ACENTUAÇÃO ---
class AmazingPDF(FPDF):
    def header(self):
        if os.path.exists(caminho_logo):
            self.image(caminho_logo, 10, 8, 65)

        self.set_font('Arial', 'B', 12)
        self.set_text_color(100)
        # Texto com acentuação corrigida via latin-1
        self.cell(0, 15,
                  'AmazingDrone - Smart Analytics Agronomia de Precisão'.encode('latin-1', 'replace').decode('latin-1'),
                  0, 1, 'R')

        self.set_draw_color(46, 125, 50)
        self.line(10, 32, 200, 32)
        self.ln(18)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150)
        rodape = f'Documento Gerado por André Aranha - AmazingDrone'
        self.cell(0, 10, rodape.encode('latin-1', 'replace').decode('latin-1'), 0, 0, 'C')


def generate_impact_pdf(dados):
    pdf = AmazingPDF()
    pdf.add_page()

    # Título Principal
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(46, 125, 50)
    titulo = "PROPOSTA TÉCNICA E PROJEÇÃO DE RETORNO"
    pdf.cell(0, 15, titulo.encode('latin-1', 'replace').decode('latin-1'), ln=True, align='L')

    # Dados do Cliente
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0)
    linha1 = f"Cliente: {dados['cliente']} | Área Analisada: {dados['hectares']} ha"
    pdf.cell(0, 7, linha1.encode('latin-1', 'replace').decode('latin-1'), ln=True)

    linha2 = f"Preço Ref: R$ {dados['preco_saca']} | Produtividade Alvo: {dados['prod_alvo']} sc/ha"
    pdf.cell(0, 7, linha2.encode('latin-1', 'replace').decode('latin-1'), ln=True)

    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(200, 0, 0)
    validade = f"VALIDADE DA PROPOSTA: {dados['vencimento']}"
    pdf.cell(0, 7, validade.encode('latin-1', 'replace').decode('latin-1'), ln=True)
    pdf.set_text_color(0)
    pdf.ln(5)

    # QUADRO COMPARATIVO
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('Arial', 'B', 12)
    quadro_titulo = " COMPARATIVO: INVESTIMENTO VS. RETORNO"
    pdf.cell(0, 10, quadro_titulo.encode('latin-1', 'replace').decode('latin-1'), ln=True, fill=True, align='C')

    pdf.set_font('Arial', '', 11)
    pdf.cell(95, 10, " Investimento Total (Serviço + Logística):".encode('latin-1', 'replace').decode('latin-1'), 0, 0)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, f"R$ {dados['total_servico']:,.2f}", 0, 1)

    pdf.set_font('Arial', '', 11)
    pdf.cell(95, 10, " Lucro Líquido Projetado (Recuperação):".encode('latin-1', 'replace').decode('latin-1'), 0, 0)
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(0, 10, f"R$ {dados['total_recuperado']:,.2f}", 0, 1)
    pdf.set_text_color(0)
    pdf.ln(5)

    # MEMORIAL DE CÁLCULO
    pdf.set_fill_color(230, 240, 230)
    pdf.set_font('Arial', 'B', 11)
    memorial_titulo = " MEMORIAL DE CÁLCULO E ORIGEM DOS GANHOS"
    pdf.cell(0, 10, memorial_titulo.encode('latin-1', 'replace').decode('latin-1'), ln=True, fill=True)
    pdf.ln(2)

    servicos = [
        ("1. AUDITORIA DE PLANTIO",
         f"Como alcançamos: Identificação precoce de falhas. Projeção baseada na recuperação de 3% da área útil.\nCálculo: {dados['hectares']}ha x 3% x {dados['prod_alvo']}sc x R${dados['preco_saca']}",
         dados['perda_falha']),
        ("2. MONITORAMENTO DE VIGOR",
         f"Como alcançamos: Otimização da saúde foliar via sensores multiespectrais. Ganho real de 2 sc/ha.\nCálculo: {dados['hectares']}ha x 2sc/ha x R${dados['preco_saca']}",
         dados['ganho_prod']),
        ("3. ECONOMIA EM INSUMOS (VRT)",
         f"Como alcançamos: Aplicação em Taxa Variável reduz o desperdício em 15% sobre o custo operacional.\nCálculo: {dados['hectares']}ha x R${dados['custo_insumo']} x 15%",
         dados['eco_insumo'])
    ]

    for titulo, desc, valor in servicos:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 7, titulo.encode('latin-1', 'replace').decode('latin-1'), ln=True)
        pdf.set_font('Arial', '', 9)
        pdf.multi_cell(0, 5, desc.encode('latin-1', 'replace').decode('latin-1'))
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(0, 7, f"Impacto Projetado: R$ {valor:,.2f}".encode('latin-1', 'replace').decode('latin-1'), ln=True)
        pdf.ln(3)

    return pdf.output(dest='S').encode('latin-1')


# --- INTERFACE DASHBOARD STREAMLIT ---

if os.path.exists(caminho_logo):
    st.sidebar.image(caminho_logo, use_container_width=True)

st.sidebar.markdown("""
    <div style='text-align: center; line-height: 0.8;'>
        <p style='color: #2e7d32; font-weight: bold; font-size: 22px; margin-bottom: 0px;'>Soluções Inteligentes</p>
        <p style='color: #2e7d32; font-weight: bold; font-size: 22px; margin-top: 0px;'>para o campo</p>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")

nome_cliente = st.sidebar.text_input("Produtor / Fazenda", "Cliente Ponta Grossa")
hectares = st.sidebar.number_input("Área Total (ha)", min_value=1, value=500)
distancia_km = st.sidebar.number_input("Distância Percorrida (Ida/Volta km)", min_value=0, value=60)
preco_saca = st.sidebar.slider("Preço Saca (R$)", 100, 200, 142)
produtividade_alvo = st.sidebar.slider("Meta (sc/ha)", 40, 110, 75)
custo_insumos_ha = st.sidebar.number_input("Insumos/ha (R$)", value=1500)
dias_validade = st.sidebar.selectbox("Validade da Proposta (dias)", [5, 7, 10, 15], index=1)
data_vencimento = (datetime.now() + timedelta(days=dias_validade)).strftime("%d/%m/%Y")

# Lógica Financeira
custo_logistica = distancia_km * 2.50
preco_ha_base = 45.0 if hectares <= 500 else 35.0
total_orcamento = (hectares * preco_ha_base) + custo_logistica

# Cálculos de Projeção
perda_falha_rs = (hectares * 0.03) * produtividade_alvo * preco_saca
ganho_vigor_rs = (hectares * 2) * preco_saca
economia_vrt_rs = (hectares * custo_insumos_ha) * 0.15
total_lucro_projetado = perda_falha_rs + ganho_vigor_rs + economia_vrt_rs

# TELA PRINCIPAL
st.title("🚀 Smart Analytics AmazingDrone")
st.subheader(f"Viabilidade Técnica e Financeira: {nome_cliente}")

m1, m2, m3 = st.columns(3)
m1.metric("Seu Orçamento", f"R$ {total_orcamento:,.2f}", "Investimento")
m2.metric("Projeção de Lucro", f"R$ {total_lucro_projetado:,.2f}",
          f"+R$ {total_lucro_projetado - total_orcamento:,.2f} Líquido")
m3.metric("Eficiência ROI", f"{(total_lucro_projetado / total_orcamento):.1f}x", "Retorno por Real")

st.markdown("---")

st.subheader("📊 Como alcançamos esses valores de ganho?")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("#### 📍 Auditoria de Plantio")
    st.write("**O que é:** Detecção de falhas no estande de plantas.")
    st.write(f"**Projeção:** {hectares}ha x 3% x {produtividade_alvo}sc x R${preco_saca}")
    st.markdown(f"### R$ {perda_falha_rs:,.2f}")

with col2:
    st.success("#### 🌿 Vigor Vegetativo")
    st.write("**O que é:** Otimização da saúde foliar (Mavic 3M).")
    st.write(f"**Projeção:** {hectares}ha x 2sc/ha x R${preco_saca}")
    st.markdown(f"### R$ {ganho_vigor_rs:,.2f}")

with col3:
    st.warning("#### 🚜 Economia VRT")
    st.write("**O que é:** Redução de desperdício em taxa variável.")
    st.write(f"**Projeção:** {hectares}ha x R${custo_insumos_ha} x 15%")
    st.markdown(f"### R$ {economia_vrt_rs:,.2f}")

st.markdown("---")

if st.button("📄 Gerar Proposta Comercial PDF"):
    pdf_params = {
        'cliente': nome_cliente, 'hectares': hectares, 'total_servico': total_orcamento,
        'perda_falha': perda_falha_rs, 'ganho_prod': ganho_vigor_rs, 'preco_saca': preco_saca,
        'eco_insumo': economia_vrt_rs, 'total_recuperado': total_lucro_projetado,
        'prod_alvo': produtividade_alvo, 'custo_insumo': custo_insumos_ha,
        'vencimento': data_vencimento
    }
    pdf_bytes = generate_impact_pdf(pdf_params)
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Proposta_AmazingDrone_{nome_cliente}.pdf" style="text-decoration:none;"><button style="background-color:#2e7d32; color:white; padding:15px 35px; border:none; border-radius:8px; cursor:pointer; font-size:16px;">📥 BAIXAR PROPOSTA COM ACENTUAÇÃO</button></a>'
    st.markdown(href, unsafe_allow_html=True)