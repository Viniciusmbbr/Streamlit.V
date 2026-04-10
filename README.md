**# 📊 Dashboard de Análise de Funcionários

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-28a745?style=for-the-badge)

Aplicação web interativa para análise de dados de funcionários, construída com **Python + Streamlit**. Permite filtrar, visualizar e exportar dados em tempo real, sem necessidade de HTML ou JavaScript.

---

## ✨ Funcionalidades

- **Filtros dinâmicos** na sidebar: por cidade, faixa salarial e categoria salarial
- **KPIs em destaque**: total de funcionários, salário médio, máximo e mínimo — atualizados em tempo real conforme os filtros
- **Gráficos interativos** com Plotly: bar chart por cidade/categoria, histograma de distribuição salarial e linha de contratações por ano
- **Tabela interativa** com todos os dados filtrados
- **Pivot table** com salário médio cruzado por cidade e categoria
- **Upload de CSV**: substitui os dados de exemplo pelos dados do próprio usuário
- **Download de CSV**: exporta os dados filtrados com um clique

---

## 🖥️ Como rodar localmente

**Pré-requisitos:** Python 3.10+

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/dashboard-funcionarios.git
cd dashboard-funcionarios

# 2. Instale as dependências
pip install streamlit pandas numpy plotly

# 3. Execute o app
python -m streamlit run app.py
```

O app abrirá automaticamente em `http://localhost:8501`.

---

## 🗂️ Estrutura do projeto

```
dashboard-funcionarios/
├── app.py        # Aplicação principal
└── README.md     # Documentação
```

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| Python | Linguagem principal |
| Streamlit | Framework para a interface web |
| Pandas | Manipulação e análise de dados |
| NumPy | Geração de dados e operações numéricas |
| Plotly Express | Visualizações interativas |

---

## 📚 Contexto

Projeto desenvolvido como atividade prática da disciplina de **Inteligência Artificial / Análise de Dados** no curso de Análise e Desenvolvimento de Sistemas — **Centro Universitário UniFavip Wyden**.

O objetivo foi implementar um dashboard completo com Streamlit, cobrindo os três níveis de desafio propostos na aula:

- 🔵 **Fácil:** filtro `selectbox` por categoria salarial
- 🟡 **Médio:** substituição dos gráficos nativos por visualizações Plotly com cores e tooltips customizados
- 🔴 **Difícil:** upload de CSV pelo usuário substituindo os dados de exemplo, com aplicação dos mesmos filtros

---

## 👨‍💻 Autor

**Vinicius** — [github.com/seu-usuario](https://github.com/Viniciusmbbr)**
