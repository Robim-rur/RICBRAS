import streamlit as st
import yfinance as yf
import pandas as pd

# Configuração inicial - DEVE SER A PRIMEIRA LINHA DE CÓDIGO STREAMLIT
st.set_page_config(page_title="Trade Certo - Ricardo Brasil", layout="wide")

def main():
    st.title("📈 App Trade Certo (Buy Side)")
    st.subheader("Foco: Arbitragem de Dividendos e JCP")

    # Sidebar para entrada de dados
    with st.sidebar:
        st.header("Parâmetros do Trade")
        ticker = st.text_input("Ticker do Ativo (ex: PETR4.SA)", value="PETR4.SA").upper()
        valor_dividendo = st.number_input("Valor do Provento (R$)", min_value=0.0, value=1.0, step=0.01)
        data_ex = st.date_input("Data Ex-Dividendo")
        btn_analisar = st.button("Analisar Trade")

    if btn_analisar:
        try:
            with st.spinner(f"Buscando dados de {ticker}..."):
                # Busca dados
                acao = yf.Ticker(ticker)
                dados = acao.history(period="5d")
                
                if dados.empty:
                    st.error("Ticker não encontrado. Lembre-se de usar '.SA' para ações da B3.")
                    return

                preco_fechamento = dados['Close'].iloc[-1]
                yield_evento = (valor_dividendo / preco_fechamento) * 100
                preco_ajustado_ex = preco_fechamento - valor_dividendo

                # Exibição dos resultados
                col1, col2, col3 = st.columns(3)
                col1.metric("Preço Atual", f"R$ {preco_fechamento:.2f}")
                col2.metric("Valor do Provento", f"R$ {valor_dividendo:.2f}")
                col3.metric("Yield do Evento", f"{yield_evento:.2f}%")

                st.markdown("---")
                
                st.success(f"### Estratégia Buy Side: {ticker}")
                st.write(f"""
                - **Data-Com:** Dia útil anterior a {data_ex.strftime('%d/%m/%Y')}.
                - **Impacto no Preço:** No dia {data_ex.strftime('%d/%m/%Y')}, a ação abrirá cotada a aprox. **R$ {preco_ajustado_ex:.2f}**.
                - **Alvo:** Recuperação do valor do dividendo no preço da ação pós-data-ex.
                """)

        except Exception as e:
            st.error(f"Ocorreu um erro técnico: {e}")

if __name__ == "__main__":
    main()
