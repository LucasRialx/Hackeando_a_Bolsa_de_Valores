# Importando as bibliotecas necessárias
from flask import Flask, render_template, request
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from io import StringIO
import logging

# Configurando o logging
logging.basicConfig(level=logging.INFO)

# Inicializando a aplicação Flask
app = Flask(__name__)

# Função para obter os dados do site Fundamentus e processar o DataFrame
def obter_dados_fundamentus():
    try:
        logging.info("Iniciando o driver do Chrome")
        # Inicializa o driver do Chrome
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        url = 'https://www.fundamentus.com.br/resultado.php'
        driver.get(url)

        # Localiza a tabela na página e extrai o HTML
        local_tabela = '/html/body/div[1]/div[2]/table'
        elemento = driver.find_element("xpath", local_tabela)
        html_tabela = elemento.get_attribute('outerHTML')
        driver.quit()

        # Lê a tabela HTML usando pandas e formata os números corretamente
        tabela = pd.read_html(StringIO(html_tabela), thousands='.', decimal=',')[0]

        # Define o índice do DataFrame como a coluna "Papel"
        tabela = tabela.set_index("Papel")

        # Lista de colunas relevantes
        colunas = [
            'Cotação', 'EV/EBIT', 'ROIC', 'Liq.2meses', 'Div.Yield', 'P/L', 'P/VP', 
            'PSR', 'P/Ativo', 'P/Cap.Giro', 'P/EBIT', 'P/Ativ Circ.Liq', 
            'EV/EBITDA', 'Mrg Ebit', 'Mrg. Líq.', 'Liq. Corr.', 'ROE', 
            'Patrim. Líq', 'Dív.Brut/ Patrim.', 'Cresc. Rec.5a'
        ]

        # Seleciona apenas as colunas que existem na tabela
        colunas_existentes = [col for col in colunas if col in tabela.columns]
        tabela = tabela[colunas_existentes]

        # Função para limpar e converter valores percentuais para float
        def limpar_percentual(valor):
            try:
                return float(valor.replace('%', '').replace('.', '').replace(',', '.'))
            except ValueError:
                return None

        # Aplica a função de limpeza nas colunas percentuais
        for col in ['ROIC', 'Div.Yield', 'Mrg Ebit', 'Mrg. Líq.']:
            if col in tabela.columns:
                tabela[col] = tabela[col].apply(limpar_percentual)

        # Remove linhas com valores nulos
        tabela = tabela.dropna()

        # Filtra a tabela para excluir empresas com baixa liquidez e valores negativos
        tabela = tabela[tabela['Liq.2meses'] > 1000000]
        tabela = tabela[tabela['EV/EBIT'] > 0]
        tabela = tabela[tabela['ROIC'] > 0]

        return tabela
    except Exception as e:
        logging.error(f"Erro ao obter dados do Fundamentus: {e}")
        return None

# Rota principal para exibir a interface e os resultados
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Obter o critério de ordenação selecionado pelo usuário
            criterio = request.form.get('criterio')
            tabela = obter_dados_fundamentus()

            if tabela is None:
                return render_template('index.html', error="Erro ao obter dados do Fundamentus")

            # Ordena a tabela de acordo com o critério selecionado
            if criterio == 'dividendos':
                resultado = tabela.sort_values(by='Div.Yield', ascending=False).head(10)
            elif criterio == 'roic':
                resultado = tabela.sort_values(by='ROIC', ascending=False).head(10)
            elif criterio == 'ev_ebit':
                resultado = tabela.sort_values(by='EV/EBIT', ascending=True).head(10)
            elif criterio == 'pl_pvp':
                resultado = tabela[(tabela['P/L'] < 15) & (tabela['P/VP'] < 1)].sort_values(by=['P/L', 'P/VP'], ascending=[True, True]).head(10)
            elif criterio == 'psr_mrgliq':
                resultado = tabela[(tabela['PSR'] < 2) & (tabela['Mrg. Líq.'] > 10)].sort_values(by=['PSR', 'Mrg. Líq.'], ascending=[True, False]).head(10)
            elif criterio == 'roe_roic':
                resultado = tabela.sort_values(by=['ROE', 'ROIC'], ascending=[False, False]).head(10)
            elif criterio == 'liqcorr_divbrutpatrim':
                resultado = tabela[(tabela['Liq. Corr.'] > 1) & (tabela['Dív.Brut/ Patrim.'] < 1)].sort_values(by=['Liq. Corr.', 'Dív.Brut/ Patrim.'], ascending=[False, True]).head(10)
            else:
                resultado = tabela.head(10)

            # Renderiza a página com os resultados
            return render_template('resultado.html', resultado=resultado)
        except Exception as e:
            logging.error(f"Erro ao processar a requisição: {e}")
            return render_template('index.html', error="Erro ao processar a requisição")
    else:
        # Renderiza a página inicial
        return render_template('index.html')

# Executa a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)
