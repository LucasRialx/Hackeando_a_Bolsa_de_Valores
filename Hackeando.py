from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from io import StringIO
import logging

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Alterar para uma chave secreta real

# Configurações do LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock database
users = {
    'admin@admin.com': {'password': generate_password_hash('KeyMaster')},

}

class User(UserMixin):
    def __init__(self, email):
        self.id = email

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in users else None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)
        if user and check_password_hash(user['password'], password):
            login_user(User(email))
            return redirect(url_for('index'))
        else:
            return 'Credenciais inválidas', 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        try:
            criterio = request.form.get('criterio')
            tabela = obter_dados_fundamentus()

            if tabela is None or tabela.empty:
                return render_template('resultado.html', error="Erro ao obter dados do Fundamentus", resultado=None)

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

            return render_template('resultado.html', resultado=resultado)
        except Exception as e:
            logging.error(f"Erro ao processar a requisição: {e}")
            return render_template('resultado.html', error="Erro ao processar a requisição", resultado=None)
    else:
        return render_template('index.html')

# Função para obter os dados do Fundamentus e processar o DataFrame
def obter_dados_fundamentus():
    try:
        logging.info("Iniciando o driver do Chrome")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        url = 'https://www.fundamentus.com.br/resultado.php'
        driver.get(url)
        local_tabela = '/html/body/div[1]/div[2]/table'
        elemento = driver.find_element("xpath", local_tabela)
        html_tabela = elemento.get_attribute('outerHTML')
        driver.quit()
        tabela = pd.read_html(StringIO(html_tabela), thousands='.', decimal=',')[0]
        tabela = tabela.set_index("Papel")
        colunas = [
            'Cotação', 'EV/EBIT', 'ROIC', 'Liq.2meses', 'Div.Yield', 'P/L', 'P/VP', 
            'PSR', 'P/Ativo', 'P/Cap.Giro', 'P/EBIT', 'P/Ativ Circ.Liq', 
            'EV/EBITDA', 'Mrg Ebit', 'Mrg. Líq.', 'Liq. Corr.', 'ROE', 
            'Patrim. Líq', 'Dív.Brut/ Patrim.', 'Cresc. Rec.5a'
        ]
        colunas_existentes = [col for col in colunas if col in tabela.columns]
        tabela = tabela[colunas_existentes]
        def limpar_percentual(valor):
            try:
                return float(valor.replace('%', '').replace('.', '').replace(',', '.'))
            except ValueError:
                return None
        for col in ['ROIC', 'Div.Yield', 'Mrg Ebit', 'Mrg. Líq.']:
            if col in tabela.columns:
                tabela[col] = tabela[col].apply(limpar_percentual)
        tabela = tabela.dropna()
        tabela = tabela[tabela['Liq.2meses'] > 1000000]
        tabela = tabela[tabela['EV/EBIT'] > 0]
        tabela = tabela[tabela['ROIC'] > 0]
        return tabela
    except Exception as e:
        logging.error(f"Erro ao obter dados do Fundamentus: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
