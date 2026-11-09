
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Gold Trader IQ Option",
    page_icon="🥇",
    layout="wide"
)

st.title("🥇 GOLD TRADER IQ OPTION")
st.caption("Análise estatística do Ouro XAU/USD")

st.info(
    "Versão inicial: análise de dados históricos. "
    "Não envia ordens nem gera sinais automáticos."
)

arquivo = st.file_uploader(
    "Importar histórico do ouro (CSV)",
    type=["csv"]
)

if arquivo is not None:
    try:
        df = pd.read_csv(arquivo)
        df.columns = [
            str(c).strip().lower() for c in df.columns
        ]

        obrigatorias = [
            "timestamp", "open", "high",
            "low", "close"
        ]

        faltando = [
            c for c in obrigatorias if c not in df.columns
        ]

        if faltando:
            st.error(
                "Colunas ausentes: " + ", ".join(faltando)
            )
        else:
            df["timestamp"] = pd.to_datetime(
                df["timestamp"], errors="coerce"
            )

            for coluna in ["open", "high", "low", "close"]:
                df[coluna] = pd.to_numeric(
                    df[coluna], errors="coerce"
                )

            df = df.dropna(
                subset=obrigatorias
            ).sort_values("timestamp")

            if df.empty:
                st.error("Não há dados válidos no arquivo.")
            else:
                fuso = st.selectbox(
                    "Fuso horário dos dados",
                    ["Brasília", "UTC"]
                )

                if fuso == "UTC":
                    df["timestamp"] = (
                        df["timestamp"]
                        .dt.tz_localize("UTC")
                        .dt.tz_convert("America/Sao_Paulo")
                    )
                else:
                    df["timestamp"] = (
                        df["timestamp"]
                        .dt.tz_localize("America/Sao_Paulo")
                    )

                df["hora"] = df["timestamp"].dt.hour

                st.success(
                    f"{len(df)} candles carregados."
                )

                st.subheader("Gráfico do ouro")
                grafico = df.set_index("timestamp")
                st.line_chart(grafico["close"])

                st.subheader("Estatísticas por horário")

                df["variacao"] = (
                    df["close"] - df["open"]
                )

                estatisticas = df.groupby("hora").agg(
                    candles=("close", "count"),
                    variacao_media=("variacao", "mean"),
                    alta=("variacao", lambda x: (x > 0).mean() * 100),
                    baixa=("variacao", lambda x: (x < 0).mean() * 100)
                )

                estatisticas = estatisticas.round(3)

                st.dataframe(
                    estatisticas,
                    use_container_width=True
                )

                st.subheader("Resumo do histórico")

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Candles analisados", len(df)
                )

                c2.metric(
                    "Preço mais recente",
                    f'{df["close"].iloc[-1]:.2f}'
                )

                c3.metric(
                    "Maior preço",
                    f'{df["high"].max():.2f}'
                )

    except Exception as erro:
        st.error(f"Erro ao processar arquivo: {erro}")

else:
    st.warning(
        "Envie um arquivo CSV com as colunas: "
        "timestamp, open, high, low e close."
    )

    st.write(
        "Nos próximos módulos vamos desenvolver "
        "análise de sessões, padrões de reversão, "
        "backtests e gerenciamento de risco."
    )
