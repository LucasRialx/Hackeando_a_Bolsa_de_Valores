# Hackeando a Bolsa de Valores

Este projeto é uma aplicação web criada com Flask para listar e visualizar ações da Bolsa de Valores com base em critérios específicos. A aplicação usa Selenium para raspar dados do site Fundamentus e exibe os resultados em uma interface web.

## Funcionalidades

- **Obter dados do Fundamentus**: Raspa os dados da tabela de resultados do site Fundamentus.
- **Filtragem de dados**: Filtra e processa os dados conforme critérios selecionados pelo usuário.
- **Exibição de resultados**: Exibe os resultados filtrados em uma tabela interativa na página web.

## Tecnologias Utilizadas

- **Flask**: Framework web usado para construir a aplicação.
- **Selenium**: Biblioteca usada para automação de navegação web e raspagem de dados.
- **Pandas**: Biblioteca usada para manipulação e análise de dados.
- **Materialize**: Framework de CSS usado para estilização da interface web.
- **HTML/CSS**: Linguagens usadas para a estrutura e estilização da interface.

## Pré-requisitos

- Python 3.6+
- Virtualenv (recomendado)

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/hackeando-a-bolsa-de-valores.git
    cd hackeando-a-bolsa-de-valores
    ```

2. Crie e ative um ambiente virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Execute a aplicação Flask:

    ```bash
    flask run
    ```

2. Abra o navegador e vá para `http://127.0.0.1:5000/`.

3. Selecione um critério e clique em "Buscar" para visualizar a listagem de ações.

## Estrutura do Projeto

hackeando-a-bolsa-de-valores/
├── static/
│ └── wallpaper_I.jpg

├── templates/
│ ├── index.html
│ └── resultado.html

├── app.py
├── requirements.txt
└── README.md


- `static/`: Diretório para arquivos estáticos como imagens.
- `templates/`: Diretório para arquivos HTML.
- `app.py`: Script principal da aplicação Flask.
- `requirements.txt`: Arquivo contendo as dependências do projeto.
- `README.md`: Documentação do projeto.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma nova branch: `git checkout -b minha-nova-funcionalidade`
3. Faça suas alterações e commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Envie para o repositório remoto: `git push origin minha-nova-funcionalidade`
5. Abra um pull request.

## Futuras Atualizações

Estamos trabalhando em diversas melhorias para tornar o aplicativo ainda mais útil e eficiente. Confira algumas das atualizações planejadas:

- ** Campo de Consulta Focado em Fundos Imobiliários**: Adicionaremos uma nova fonte de consulta especificamente voltada para fundos imobiliários, permitindo uma análise mais abrangente e detalhada.

- **Bot de Compra e Venda de Ações através do MetaTrader5**: Implementaremos um bot para automação das operações de compra e venda de ações usando a plataforma MetaTrader5, visando facilitar a execução das transações e otimizar a estratégia de investimento.

- **Suporte Web**: Estamos planejando adicionar suporte para acesso e gerenciamento do aplicativo através de uma interface web, proporcionando maior flexibilidade e conveniência para os usuários.

Fique atento às atualizações para mais detalhes sobre o progresso e a implementação dessas novas funcionalidades!


## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.


## Autor
Lucas Rial
