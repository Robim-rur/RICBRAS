import streamlit as st
import pandas as pd
import pandas_ta as ta  # Aqui usa sublinhado (_)
import yfinance as yf

# Configuração da página
st.set_page_config(page_title="Trade Certo - Arbitragem de Dividendos", layout="wide")

def calcular_trade_certo(ticker_symbol, valor_dividendo, data_ex):
    try:
        # Busca dados do papel
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="1d")
        
        if hist.empty:
            return None

        preco_atual = hist['Close'].iloc[-1]
        
        # Lógica Trade Certo: 
        # 1. Compra na data-com (antes da data-ex)
        # 2. O preço cai o valor do dividendo na data-ex
        # 3. O lucro vem da recuperação dessa queda ou do ganho de capital + dividendo
        
        preco_pos_ex = preco_atual - valor_dividendo
        retorno_percentual = (valor_dividendo / preco_atual) * 100
        
        return {
            "Ticker": ticker_symbol.upper(),
            "Preço Atual": f"R$ {preco_atual:.2f}",
            "Dividendo/JCP": f"R$ {valor_dividendo:.2f}",
            "Preço Ajustado (Ex)": f"R$ {preco_pos_ex:.2f}",
            "Yield do Evento": f"{retorno_percentual:.2f}%",
            "Data Ex": data_ex
        }
    except Exception as e:
        return None

# Interface Streamlit
st.title("📈 Simulador Trade Certo")
st.markdown("""
A estratégia consiste em operar a distorção de preços em eventos de proventos.
**Foco: Lado da Compra (Buy Side).**
""")

with st.sidebar:
    st.header("Configurações do Ativo")
    ticker_input = st.text_input("Ticker (ex: PETR4.SA)", value="PETR4.SA")
    valor_prov = st.number_input("Valor do Provento (R$)", min_value=0.01, value=1.0, step=0.01)
    data_ex_input = st.date_input("Data Ex-Dividendos")
    botao_calcular = st.button("Analisar Oportunidade")

if botao_calcular:
    with st.spinner('Buscando dados de mercado...'):
        resultado = calcular_trade_certo(ticker_input, valor_prov, data_ex_input)
        
        if resultado:
            st.subheader(f"Análise de Compra: {resultado['Ticker']}")
            
            # Layout em colunas para os cards
            col1, col2, col3 = st.columns(3)
            col1.metric("Preço de Entrada Est.", resultado["Preço Atual"])
            col2.metric("Yield Bruto", resultado["Yield do Evento"])
            col3.metric("Ajuste na Data-Ex", resultado["Preço Ajustado (Ex)"])
            
            # Detalhes e Explicação
            st.info(f"""
            **Estratégia:** Ao comprar antes da **data-ex ({resultado['Data Ex']})**, 
            você garante o direito ao recebimento de **{resultado['Dividendo/JCP']}**. 
            O mercado descontará esse valor do preço da ação na abertura do dia seguinte.
            """)
            
            # Simulação de Tabela
            df_res = pd.DataFrame([resultado])
            st.table(df_res)
        else:
            st.error("Erro ao buscar dados. Verifique se o ticker está correto (use .SA para ações brasileiras).")

st.markdown("---")
st.caption("Nota: Este app é uma ferramenta de simulação. Verifique sempre as taxas de corretagem e o custo do aluguel de ações (BTC) se for fazer hedge.")
