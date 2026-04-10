import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Funcionários",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard de Análise de Funcionários")


@st.cache_data
def carregar_dados_exemplo():
    np.random.seed(42)
    n = 50
    nomes = [
        "Ana", "Bruno", "Carlos", "Daniela", "Eduardo",
        "Fernanda", "Gabriel", "Helena", "Igor", "Julia",
        "Kevin", "Larissa", "Marcos", "Natalia", "Otávio",
        "Paula", "Rafael", "Sabrina", "Thiago", "Vanessa",
        "William", "Ximena", "Yuri", "Zara", "André",
        "Beatriz", "César", "Diana", "Elias", "Flávia",
        "Gustavo", "Hannah", "Ítalo", "Joana", "Lucas",
        "Mariana", "Nicolas", "Olga", "Pedro", "Quésia",
        "Rodrigo", "Simone", "Tânia", "Ulisses", "Vera",
        "Wagner", "Xênia", "Yan", "Zilda", "Augusto"
    ]
    dados = {
        "nome": nomes[:n],
        "idade": np.random.randint(22, 55, n).astype(float),
        "cidade": np.random.choice(["SP", "RJ", "MG", "RS", "BA"], n),
        "salario": np.random.choice(
            [2500, 3000, 3500, 4000, 4500, 5000, 6000, 7000], n
        ).astype(float),
        "data_contratacao": pd.to_datetime(
            np.random.choice(
                pd.date_range("2018-01-01", "2024-12-31"), n
            )
        ),
    }

    # Inserir alguns NaN para simular dados reais
    idx_nan_idade = np.random.choice(n, 3, replace=False)
    idx_nan_sal   = np.random.choice(n, 3, replace=False)
    for i in idx_nan_idade:
        dados["idade"][i] = np.nan
    for i in idx_nan_sal:
        dados["salario"][i] = np.nan

    df = pd.DataFrame(dados)

    # Limpeza
    df["idade"]   = df["idade"].fillna(df["idade"].mean())
    df["salario"] = df["salario"].fillna(df["salario"].median())

    # Feature engineering
    df["salario_anual"]   = df["salario"] * 12
    df["ano_contratacao"] = df["data_contratacao"].dt.year
    df["categoria_salario"] = df["salario"].apply(
        lambda x: "Alto" if x > 4500 else ("Médio" if x > 3000 else "Baixo")
    )

    return df


def preparar_df_upload(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara um DataFrame vindo de upload de CSV,
    criando as colunas derivadas se não existirem.
    """
    df = df_raw.copy()

    # Tenta converter data se existir
    if "data_contratacao" in df.columns:
        df["data_contratacao"] = pd.to_datetime(df["data_contratacao"], errors="coerce")
        df["ano_contratacao"] = df["data_contratacao"].dt.year

    if "salario" in df.columns:
        df["salario"] = pd.to_numeric(df["salario"], errors="coerce")
        df["salario"] = df["salario"].fillna(df["salario"].median())
        df["salario_anual"] = df["salario"] * 12
        df["categoria_salario"] = df["salario"].apply(
            lambda x: "Alto" if x > 4500 else ("Médio" if x > 3000 else "Baixo")
        )

    if "idade" in df.columns:
        df["idade"] = pd.to_numeric(df["idade"], errors="coerce")
        df["idade"] = df["idade"].fillna(df["idade"].mean())

    return df


# ─────────────────────────────────────────────
# SEÇÃO 09 — UPLOAD (🔴 DESAFIO DIFÍCIL)
# Upload substitui os dados de exemplo
# ─────────────────────────────────────────────
st.sidebar.header("📂 Fonte de Dados")

uploaded_file = st.sidebar.file_uploader(
    "Envie um CSV para substituir os dados de exemplo",
    type=["csv"]
)

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    df = preparar_df_upload(df_raw)
    st.sidebar.success(f"✅ CSV carregado: {len(df)} registros")
else:
    df = carregar_dados_exemplo()
    st.sidebar.info("ℹ️ Usando dados de exemplo (50 funcionários)")

# ─────────────────────────────────────────────
# SEÇÃO 04 — SIDEBAR & FILTROS
# ─────────────────────────────────────────────
st.sidebar.header("🔎 Filtros")

# Filtro de cidade (só exibe se coluna existir)
if "cidade" in df.columns:
    cidades_disponiveis = sorted(df["cidade"].dropna().unique().tolist())
    cidades = st.sidebar.multiselect(
        "Cidade",
        options=cidades_disponiveis,
        default=cidades_disponiveis
    )
else:
    cidades = None

# Filtro de faixa salarial
if "salario" in df.columns:
    sal_min = float(df["salario"].min())
    sal_max = float(df["salario"].max())
    faixa_salario = st.sidebar.slider(
        "Faixa Salarial (R$)",
        min_value=sal_min,
        max_value=sal_max,
        value=(sal_min, sal_max),
        step=100.0
    )
else:
    faixa_salario = None

# 🔵 DESAFIO FÁCIL — selectbox de categoria_salario
if "categoria_salario" in df.columns:
    categorias_disponiveis = ["Todos"] + sorted(df["categoria_salario"].dropna().unique().tolist())
    categoria_selecionada = st.sidebar.selectbox(
        "Categoria Salarial",
        options=categorias_disponiveis
    )
else:
    categoria_selecionada = "Todos"

# ─────────────────────────────────────────────
# APLICAR FILTROS
# ─────────────────────────────────────────────
df_filtrado = df.copy()

if cidades is not None and "cidade" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["cidade"].isin(cidades)]

if faixa_salario is not None and "salario" in df_filtrado.columns:
    df_filtrado = df_filtrado[
        (df_filtrado["salario"] >= faixa_salario[0]) &
        (df_filtrado["salario"] <= faixa_salario[1])
    ]

if categoria_selecionada != "Todos" and "categoria_salario" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["categoria_salario"] == categoria_selecionada]

# ─────────────────────────────────────────────
# SEÇÃO 05 — KPIs
# ─────────────────────────────────────────────
st.subheader("📌 Indicadores")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Total Funcionários",
    df_filtrado.shape[0],
    delta=f"{df_filtrado.shape[0] - df.shape[0]} vs total"
)

if "salario" in df_filtrado.columns and not df_filtrado.empty:
    col2.metric(
        "💰 Salário Médio",
        f"R$ {df_filtrado['salario'].mean():,.2f}"
    )
    col3.metric(
        "📈 Salário Máximo",
        f"R$ {df_filtrado['salario'].max():,.2f}"
    )
    col4.metric(
        "📉 Salário Mínimo",
        f"R$ {df_filtrado['salario'].min():,.2f}"
    )

# ─────────────────────────────────────────────
# SEÇÃO 06 — TABELA
# ─────────────────────────────────────────────
st.subheader("📋 Tabela de Funcionários")
st.dataframe(df_filtrado, use_container_width=True)

# ─────────────────────────────────────────────
# SEÇÃO 07 — GRÁFICOS
# 🟡 DESAFIO MÉDIO — Plotly com cores e tooltip
# ─────────────────────────────────────────────
st.subheader("📊 Visualizações")

if df_filtrado.empty:
    st.warning("Nenhum dado para exibir com os filtros selecionados.")
else:
    col_g1, col_g2 = st.columns(2)

    # Gráfico 1 — Salário médio por cidade (Plotly com cores por categoria)
    if "cidade" in df_filtrado.columns and "salario" in df_filtrado.columns:
        with col_g1:
            df_cidade = (
                df_filtrado
                .groupby(["cidade", "categoria_salario"], as_index=False)["salario"]
                .mean()
                .rename(columns={"salario": "salario_medio"})
            )
            fig1 = px.bar(
                df_cidade,
                x="cidade",
                y="salario_medio",
                color="categoria_salario",           # 🟡 cores por categoria
                color_discrete_map={
                    "Alto":  "#2196F3",
                    "Médio": "#FF9800",
                    "Baixo": "#F44336"
                },
                barmode="group",
                title="Salário Médio por Cidade e Categoria",
                labels={
                    "cidade": "Cidade",
                    "salario_medio": "Salário Médio (R$)",
                    "categoria_salario": "Categoria"
                },
                hover_data={"salario_medio": ":.2f"},  # 🟡 tooltip customizado
            )
            fig1.update_layout(legend_title_text="Categoria Salarial")
            st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2 — Distribuição de salários (histograma Plotly)
    if "salario" in df_filtrado.columns:
        with col_g2:
            fig2 = px.histogram(
                df_filtrado,
                x="salario",
                color="categoria_salario",
                color_discrete_map={
                    "Alto":  "#2196F3",
                    "Médio": "#FF9800",
                    "Baixo": "#F44336"
                },
                nbins=15,
                title="Distribuição de Salários",
                labels={
                    "salario": "Salário (R$)",
                    "count": "Nº de Funcionários",
                    "categoria_salario": "Categoria"
                },
                hover_data=df_filtrado.columns,       # 🟡 tooltip com todos os dados
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3 — Contratações por ano (linha)
    if "ano_contratacao" in df_filtrado.columns:
        df_ano = df_filtrado.groupby("ano_contratacao").size().reset_index(name="contratacoes")
        fig3 = px.line(
            df_ano,
            x="ano_contratacao",
            y="contratacoes",
            markers=True,
            title="Contratações por Ano",
            labels={"ano_contratacao": "Ano", "contratacoes": "Nº de Contratações"}
        )
        st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────
# SEÇÃO 08 — PIVOT TABLE
# ─────────────────────────────────────────────
if "cidade" in df_filtrado.columns and "categoria_salario" in df_filtrado.columns and "salario" in df_filtrado.columns:
    st.subheader("🔢 Pivot Table — Salário Médio por Cidade e Categoria")
    pivot = df_filtrado.pivot_table(
        values="salario",
        index="cidade",
        columns="categoria_salario",
        aggfunc="mean"
    ).round(2)
    st.dataframe(pivot, use_container_width=True)

# ─────────────────────────────────────────────
# SEÇÃO 09 — DOWNLOAD
# ─────────────────────────────────────────────
st.subheader("💾 Exportar Dados Filtrados")

csv = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Baixar CSV filtrado",
    data=csv,
    file_name="dados_filtrados.csv",
    mime="text/csv"
)