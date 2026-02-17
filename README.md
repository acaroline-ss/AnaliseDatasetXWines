# Sistema de Análise de Vinhos: Do Dataset à Web com Chatbot IA 🤖🍷

Pipeline de dados que transforma um dataset de vinhos numa base de dados relacional em SQL, integrada a uma aplicação web em Flask, permitindo analisar as informações e navegar por todo o catálogo de forma estruturada — **tudo isso com um chatbot inteligente que responde em linguagem natural a perguntas sobre os dados do catálogo!**

## Objetivo

Converter dados brutos num sistema navegável e estruturado, permitindo análise integrada e exploração interativa de informação enológica através de uma arquitetura web orientada a dados. **O chatbot com IA torna a experiência ainda mais rica e interativa.**

## Visão Geral

Este projeto apresenta uma solução end-to-end que transforma um dataset de vinhos numa aplicação web interativa e totalmente navegável. A aplicação resulta de uma análise detalhada do dataset X-Wines, seguida da modelação estruturada da informação e da implementação de uma arquitetura orientada a dados.

Mais do que uma interface visual, o sistema reflete um processo completo de engenharia de dados: compreensão do domínio, modelação Entidade–Relacionamento, conversão para modelo relacional normalizado, povoamento das tabelas, construção de interrogações SQL e integração com uma aplicação web.

É fortemente aconselhada a leitura do relatório em PDF `analise_sistemas_web.pdf`, onde é descrito todo o processo, incluindo:

*   Descrição do universo da base de dados
*   Identificação dos requisitos funcionais
*   Modelação Entidade–Relacionamento
*   Criação do modelo relacional em 3ª Forma Normal
*   Povoamento das tabelas a partir do dataset X-Wines
*   Tratamento de atributos multivalorados (castas, harmonizações e anos de colheita)
*   Construção das tabelas associativas
*   Interrogações SQL para análise de dados
*   Arquitetura completa da aplicação web

Este documento demonstra que a aplicação não é apenas um conjunto de páginas interativas, mas o resultado de uma análise minuciosa do dataset e da aplicação integrada de várias competências técnicas.

## Aplicação Web

A aplicação foi desenvolvida em Flask e permite explorar todos os dados do dataset de forma estruturada e interligada.

**Principais características:**

*   Página inicial com acesso às tabelas e interrogações SQL
*   Barra de pesquisa global para vinhos, castas e regiões
*   Navegação entre múltiplas páginas (vinhos, vinícolas, países, regiões, uvas, pratos e anos de colheita)
*   Página de vinhos com listagem completa do catálogo
*   Páginas de detalhe para cada entidade, com informação específica e ligações dinâmicas para entidades relacionadas
*   **🤖 Chatbot integrado** disponível em todas as páginas através de um botão flutuante

**Para cada entidade são apresentados:**

* Os respetivos atributos, bem como ligações dinâmicas para entidades relacionadas, permitindo a navegação cruzada por todo o sistema.
* A informação inclui características específicas do domínio (como propriedades enológicas, relações geográficas, associações com castas, harmonizações gastronómicas e anos de colheita), garantindo uma representação completa e interligada dos dados.
* A aplicação mantém uma estrutura consistente entre vinhos, vinícolas, países, regiões, uvas, pratos e vintages, assegurando uma experiência uniforme de exploração da informação.

Todos os dados do dataset foram aproveitados de forma inteligente, sendo distribuídos por entidades normalizadas e apresentados através de relações explícitas, o que garante consistência, rastreabilidade e exploração completa da informação.

## 🤖 Chatbot Inteligente com IA

O chatbot foi desenvolvido para funcionar com diferentes provedores de IA, sendo que por padrão está configurado para usar a API da **Groq**.

**Características do chatbot:**
- **Memória de conversa**: O bot lembra do contexto das perguntas anteriores
- **Busca em tempo real**: Consulta o banco SQLite para respostas precisas baseadas nos dados reais
- **Respostas personalizadas**: Age como um sommelier digital especialista

**Exemplos de perguntas que o chatbot responde:**
- "Vinhos da região do Douro"
- "Vinhos tintos com mais de 14% álcool"
- "Vinhos com uva Cabernet Sauvignon"
- "Que prato combina com vinho do Porto?"

## Exemplo da Aplicação

### Página Inicial
Visão geral da aplicação, com navegação entre entidades e acesso à pesquisa.

![Página inicial](/app/static/screenshots/home.png)

### Chatbot AI 
Assistente virtual especialista em vinhos, acessível em todas as páginas.

![Chatbot](/app/static/screenshots/sommelier.png)

### Lista de Vinhos
Listagem completa dos vinhos disponíveis no catálogo.

![Lista de vinhos](/app/static/screenshots/wines.png)

### Detalhe de um Vinho
Página de detalhe com informação específica e ligações para entidades relacionadas.

![Detalhe do vinho](/app/static/screenshots/wine_detail.png)

### Castas (Uvas)
Página dedicada às castas, permitindo navegação cruzada com os vinhos associados.

![Castas](/app/static/screenshots/uvas.png)

### Pesquisa
Resultados da pesquisa integrada na aplicação.

![Resultados da pesquisa](/app/static/screenshots/lupa.png)

### Interrogações SQL
Exemplo de interrogação SQL executada diretamente a partir da interface web.

![Interrogações SQL](/app/static/screenshots/sql_query.png)

## Competências Demonstradas

*   Análise de dados
*   Modelação Entidade–Relacionamento
*   Arquitetura de bases de dados relacionais
*   SQL (criação de esquema, povoamento e consultas)
*   Normalização (3ª Forma Normal)
*   Python para processamento de dados
*   Desenvolvimento web com Flask
*   **Integração de IA com API Groq**
*   **Engenharia de prompt para respostas contextuais**
*   **Memória de conversa em chatbots**
*   Integração entre backend, base de dados e frontend
*   Organização de projeto e documentação técnica

## Stack Tecnológica

*   Python
*   Flask
*   SQLite
*   SQL
*   HTML / CSS
*   JavaScript (vanilla, sem Node.js)
*   **Groq API** (ou OpenAI/Claude/Gemini como alternativa)

## 🚀 Como Executar Localmente

### Pré-requisitos

*   Python 
*   pip (gerenciador de pacotes Python)

### Passos

1.  **Clonar o repositório**
    ```bash
    git clone https://github.com/acaroline-ss/AnaliseDatasetXWines.git
    cd AnaliseDatasetXWines
    ```

2.  **(Opcional) Criar ambiente virtual**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    # ou
    venv\Scripts\activate  # Windows
    ```

3.  **Instalar dependências Python**
    ```bash
    pip install flask groq python-dotenv
    ```

4.  **Configurar o caminho do banco de dados**

    O caminho para o arquivo `wines.db` é configurado em **dois arquivos**, ajustando para o caminho real no seu computador:

    **No `app/db.py`:**
    ```python
    DB_FILE = '/caminho/COMPLETO/ate/seu/projeto/wines.db'  # 🔧 AJUSTE PARA SEU COMPUTADOR!
    ```

    **No `app/chat_logic.py`:**
    ```python
    DB_PATH = '/caminho/COMPLETO/ate/seu/projeto/wines.db'  # 🔧 AJUSTE PARA SEU COMPUTADOR!
    ```

    **Exemplos de caminhos reais:**
    - **Mac/Linux:** `/Users/joao/Documents/AnaliseDatasetXWines/wines.db`
    - **Windows:** `C:\\Users\\joao\\Documents\\AnaliseDatasetXWines\\wines.db`

    > ⚠️ **Importante**: Use o **mesmo caminho** nos dois arquivos!

5.  **Configurar a chave da API do chatbot**
    
    **Opção A: Usar Groq (Recomendado)**
    
    No arquivo `app/chat_logic.py`, substitua pela sua chave da Groq:
    ```python
    client = Groq(
        api_key="cole-sua-chave-do-groq-aqui"  # 🔐 Obtenha em console.groq.com
    )
    ```

    **Opção B: Usar outro provedor (OpenAI, Claude, Gemini, etc.)**
    
    Se preferir usar outra API, você precisará:
    
    1. **Alterar a importação** no início do arquivo:
        ```python
        # Para OpenAI
        from openai import OpenAI
        client = OpenAI(api_key="sua-chave-openai")
        
        # Para Anthropic (Claude)
        from anthropic import Anthropic
        client = Anthropic(api_key="sua-chave-anthropic")
        
        # Para Google Gemini
        import google.generativeai as genai
        genai.configure(api_key="sua-chave-gemini")
        model = genai.GenerativeModel('gemini-pro')
        ```
    
    2. **Ajustar a função `perguntar_groq`** (em `chat_logic.py`) para o formato de chamada da API escolhida
    
    3. **Instalar a biblioteca da API escolhida**:
        ```bash
        pip install openai      # para OpenAI
        pip install anthropic   # para Claude
        pip install google-generativeai  # para Gemini
        ```

    > 💡 **Dica**: Independente da API escolhida, lembre-se de **nunca compartilhar suas chaves publicamente**. Em produção, use variáveis de ambiente.

6.  **(Opcional) Configurar chave secreta do Flask**
    
    No arquivo `app/app.py`, configure a chave secreta como achar mais conveniente:
    ```python
    APP.config['SECRET_KEY'] = 'chave-para-desenvolvimento-local'  # OK para testes
    ```

7.  **Executar o servidor**
    
    Dentro da pasta `app/`:
    ```bash
    cd app
    python3 server.py
    ```

8.  **Acessar no navegador**
    
    Após iniciar o servidor, abra o navegador e use um dos links abaixo:
    ```
    http://127.0.0.1:9000
    http://localhost:9000
    ```

A partir da página inicial é possível navegar por todas as entidades (Wines, Wineries, Regions, Countries, Grapes, Dishes e Vintages), pelas interrogações SQL implementadas e **experimentar o chatbot interativo** clicando no botão flutuante 🍷.
