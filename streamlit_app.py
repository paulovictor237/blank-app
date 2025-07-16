import streamlit as st
import pandas as pd
import io

# --- Dicionários de Mapeamento ---
# Baseado nas informações do painel interativo.
# Adicionamos variações (maiúsculas, sem acento) para tornar o script mais robusto.
COMMUNICATION_TYPE_MAP = {
    'CALL': 0,
    'WHATSAPP': 1,
    'DIGISAC': 2,
    'EMAIL': 3,
    'TELEMETRY': 4,
    'TELEMETRIA': 4,
    'AUTOMATIC': 5,
    'AUTOMATICO': 5,
    'SALESFORCE': 6
}

OCCURRENCE_TYPES_MAP = {
    'ACCIDENT': 1,
    'ACIDENTE': 1,
    'PROPERTY_DAMAGE': 2,
    'DANO A PROPRIEDADE': 2,
    'PROPERTY_LOSS': 3,
    'PERDA DE PROPRIEDADE': 3,
    'CARGO_LOSS': 4,
    'PERDA DE CARGA': 4,
    'TRAFFIC_TICKET': 5,
    'MULTA DE TRANSITO': 5,
    'OTHERS': 6,
    'OUTROS': 6,
    'CARGO_DAMAGE': 7,
    'DANO A CARGA': 7,
    'CONTRACT': 8,
    'CONTRATO': 8,
    'PICO DE VELOCIDADE': 17
}

OCCURRENCE_STATUS_MAP = {
    'IN_ANALYSIS': 1,
    'EM ANALISE': 1,
    'IN_BUDGET': 2,
    'EM ORCAMENTO': 2,
    'SELECTING_BUDGET': 3,
    'SELECIONANDO ORCAMENTO': 3,
    'WAITING_NF': 4,
    'AGUARDANDO NF': 4,
    'NEGOTIATING': 5,
    'EM NEGOCIACAO': 5,
    'REFUNDING': 6,
    'EM REEMBOLSO': 6,
    'PAID': 7,
    'PAGO': 7,
    'EXPIRED': 8,
    'EXPIRADO': 8,
    'REJECTED': 9,
    'REJEITADO': 9,
    'WAITING_DRIVER_SIGNATURE': 10,
    'AGUARDANDO ASSINATURA DO MOTORISTA': 10,
    'REVIEW': 11,
    'EM REVISAO': 11,
    'NEGOTIATING_WITH_DRIVER': 12,
    'NEGOCIANDO COM MOTORISTA': 12,
    'FINISHED': 13,
    'CONCLUIDA': 13,
    'CONCLUÍDA': 13
}

def convert_csv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte as colunas de texto para seus códigos numéricos correspondentes.
    """
    # Garante que os nomes das colunas não tenham espaços em branco
    df.columns = df.columns.str.strip()

    # Função auxiliar para mapear valores
    def map_value(value, value_map):
        # Converte para string, remove espaços e coloca em maiúsculo para padronizar
        key = str(value).strip().upper()
        return value_map.get(key, value) # Retorna o valor original se não encontrar

    # Aplica o mapeamento nas colunas, se existirem
    if 'communication_type' in df.columns:
        df['communication_type'] = df['communication_type'].apply(lambda x: map_value(x, COMMUNICATION_TYPE_MAP))
    
    if 'occurrence_types' in df.columns:
        df['occurrence_types'] = df['occurrence_types'].apply(lambda x: map_value(x, OCCURRENCE_TYPES_MAP))

    if 'occurrence_status' in df.columns:
        df['occurrence_status'] = df['occurrence_status'].apply(lambda x: map_value(x, OCCURRENCE_STATUS_MAP))
        
    return df

# --- Interface do Streamlit ---
st.set_page_config(layout="wide")

st.title("Conversor de CSV de Ocorrências ⚙️")
st.write(
    "Faça o upload do seu arquivo CSV (separado por `,` ou `;`) para convertê-lo "
    "para o formato numérico padronizado, pronto para o banco de dados."
)

uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    try:
        # Detecta o separador e lê o CSV para um DataFrame do pandas
        # Usamos 'engine=python' para permitir um separador regex
        dataframe = pd.read_csv(uploaded_file, sep='[;,]', engine='python', on_bad_lines='skip')

        # Remove colunas vazias que podem ser criadas por ponto e vírgula no final da linha
        dataframe.dropna(axis=1, how='all', inplace=True)

        st.subheader("Pré-visualização do Arquivo Original")
        st.dataframe(dataframe.head())

        # Converte o DataFrame
        converted_df = convert_csv(dataframe.copy())

        st.subheader("Pré-visualização do Arquivo Convertido")
        st.dataframe(converted_df.head())

        # Prepara o arquivo para download
        # Convertendo o dataframe para CSV em memória
        output = io.StringIO()
        converted_df.to_csv(output, sep=',', index=False, encoding='utf-8')
        csv_data = output.getvalue()

        st.success("Conversão concluída com sucesso! Clique abaixo para baixar.")

        st.download_button(
            label="📥 Baixar CSV Convertido",
            data=csv_data,
            file_name=f"convertido_{uploaded_file.name}",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")