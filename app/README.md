# Sistema de Análise de Vinhos: Do Dataset à Web com Chatbot IA 🤖🍷

Pipeline de dados que transforma um dataset de vinhos numa base de dados relacional em SQL, integrada a uma aplicação web em Flask, permitindo analisar as informações e navegar por todo o catálogo de forma estruturada — **tudo isso com um chatbot inteligente que responde em linguagem natural a perguntas sobre os dados do catálogo!** 🤖🍷

## Objetivo

Converter dados brutos num sistema navegável e estruturado, permitindo análise integrada e exploração interativa de informação enológica através de uma arquitetura web orientada a dados.

## ✨ Principais Funcionalidades

### 🖥️ Site Principal
- Catálogo completo de vinhos com páginas detalhadas
- Busca por vinhos, regiões, uvas e pratos
- 10 consultas analíticas predefinidas (Q1 a Q10)
- Navegação entre entidades relacionadas

### 🤖 Chatbot Inteligente com IA
- **Tecnologia**: API Groq com modelo `llama-3.1-8b-instant` 
- **Memória de conversa**: O bot lembra do contexto das perguntas anteriores
- **Busca em tempo real**: Consulta o banco SQLite para respostas precisas baseadas nos dados reais
- **Respostas personalizadas**: Age como um sommelier digital especialista

#### 📊 Exemplos de perguntas que o chatbot responde:
- "Vinhos da região do Douro"
- "Vinhos tintos com mais de 14% álcool"
- "Vinhos com uva Cabernet Sauvignon"
- "Que prato combina com vinho do Porto?"
- "Qual a diferença entre Vinho do Porto e Vinho do Douro?"
- "Recomende um vinho para harmonizar com carne"

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
*   **🤖 Chatbot integrado** 

**Para cada entidade são apresentados:**

* Os respetivos atributos, bem como ligações dinâmicas para entidades relacionadas, permitindo a navegação cruzada por todo o sistema.
* A informação inclui características específicas do domínio (como propriedades enológicas, relações geográficas, associações com castas, harmonizações gastronómicas e anos de colheita), garantindo uma representação completa e interligada dos dados.
* A aplicação mantém uma estrutura consistente entre vinhos, vinícolas, países, regiões, uvas, pratos e vintages, assegurando uma experiência uniforme de exploração da informação.

Todos os dados do dataset foram aproveitados de forma inteligente, sendo distribuídos por entidades normalizadas e apresentados através de relações explícitas, o que garante consistência, rastreabilidade e exploração completa da informação.

## Exemplo da Aplicação

### Página Inicial
Visão geral da aplicação, com navegação entre entidades e acesso à pesquisa.

![Página inicial](app/static/screenshots/home.png)

### Lista de Vinhos
Listagem completa dos vinhos disponíveis no catálogo.

![Lista de vinhos](app/static/screenshots/wines.png)

### Detalhe de um Vinho
Página de detalhe com informação específica e ligações para entidades relacionadas.

![Detalhe do vinho](app/static/screenshots/wine_detail.png)

### 🤖 Chatbot Interativo
Assistente virtual especialista em vinhos, acessível em todas as páginas.

![Chatbot](app/static/screenshots/chatbot.png) *(adicione um screenshot do chatbot)*

### Castas (Uvas)
Página dedicada às castas, permitindo navegação cruzada com os vinhos associados.

![Castas](app/static/screenshots/uvas.png)

### Pesquisa
Resultados da pesquisa integrada na aplicação.

![Resultados da pesquisa](app/static/screenshots/lupa.png)

### Interrogações SQL
Exemplo de interrogação SQL executada diretamente a partir da interface web.

![Interrogações SQL](app/static/screenshots/sql_query.png)

## 🛠️ Competências Demonstradas

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
*   Organização de projeto e documentação técnica

## 📚 Stack Tecnológica

*   Python
*   Flask
*   SQLite
*   SQL
*   HTML / CSS
*   **Groq API (IA)**
*   **JavaScript (frontend do chat)**

## 🚀 Como Executar Localmente

### Pré-requisitos

*   Python 3
*   pip
*   Conta gratuita na [Groq](https://console.groq.com) (para a chave da API)

### Passos

1.  **(Opcional)** Criar ambiente virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  Instalar dependências:
    ```bash
    pip install flask groq
    ```

3.  **Configuração da base de dados**
    No ficheiro `app/db.py`, confirma o caminho para a base de dados:
    ```python
    DB_FILE = "/caminho/para/seu/projeto-bd/wines.db"
    ```

4.  **Configuração da API do Chatbot**
    No ficheiro `app/chat_logic.py`, substitua pela sua chave da Groq:
    ```python
    client = Groq(api_key="cole-sua-chave-do-groq-aqui")
    ```
    > 🔑 Obtenha sua chave gratuita em [console.groq.com](https://console.groq.com)

5.  **Executar o servidor**
    Dentro da pasta `app/`, executa:
    ```bash
    python3 server.py
    ```

6.  **Aceder à aplicação**
    *   http://127.0.0.1:9000
    *   http://localhost:9000

A partir da página inicial é possível navegar por todas as entidades (Wines, Wineries, Regions, Countries, Grapes, Dishes e Vintages), pelas interrogações SQL implementadas e **experimentar o chatbot interativo** clicando no botão flutuante 🍷.

## 🤖 Como usar o Chatbot

O chatbot está disponível em **todas as páginas** através de um botão flutuante. Basta clicar e fazer perguntas em linguagem natural sobre:

- **Vinhos por região**: "Vinhos da região do Douro"
- **Vinhos por tipo**: "Vinhos tintos", "Vinhos brancos"
- **Vinhos por uva**: "Vinhos com uva Cabernet Sauvignon"
- **Harmonização**: "Que vinho combina com carne?"
- **Teor alcoólico**: "Vinhos com mais de 14% álcool"
- **Comparações**: "Diferença entre Vinho do Porto e Vinho do Douro"

O bot mantém o contexto da conversa, permitindo perguntas de seguimento como "e os tintos dessa região?" ou "algum deles harmoniza com queijo?".

## 🗄️ Base de Dados

A base de dados é construída a partir do ficheiro CSV `X-Wines` utilizando:

*   Tabela intermédia (staging)
*   Scripts Python para decomposição de listas (castas, harmonizações e vintages)
*   Criação de tabelas associativas para relações N:M

O modelo encontra-se normalizado em **3ª Forma Normal**, garantindo integridade referencial, atomicidade e ausência de redundâncias.
