# Sistema de Análise de Vinhos: Do Dataset à Web 

Pipeline de dados que transforma um dataset de vinhos numa base de dados relacional em SQL, integrada a uma aplicação web em Flask, permitindo analisar as informações e navegar por todo o catálogo de forma estruturada.

## Objetivo

Converter dados brutos num sistema navegável e estruturado, permitindo análise integrada e exploração interativa de informação enológica através de uma arquitetura web orientada a dados.

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

**Para cada entidade são apresentados:**

* Os respetivos atributos, bem como ligações dinâmicas para entidades relacionadas, permitindo a navegação cruzada por todo o sistema.
* A informação inclui características específicas do domínio (como propriedades enológicas, relações geográficas, associações com castas, harmonizações gastronómicas e anos de colheita), garantindo uma representação completa e interligada dos dados.
* A aplicação mantém uma estrutura consistente entre vinhos, vinícolas, países, regiões, uvas, pratos e vintages, assegurando uma experiência uniforme de exploração da informação.

Todos os dados do dataset foram aproveitados de forma inteligente, sendo distribuídos por entidades normalizadas e apresentados através de relações explícitas, o que garante consistência, rastreabilidade e exploração completa da informação.

Adicionalmente, a aplicação disponibiliza páginas dedicadas às interrogações SQL, permitindo executar consultas analíticas diretamente a partir da interface web.

## Competências Demonstradas

*   Análise de dados
*   Modelação Entidade–Relacionamento
*   Arquitetura de bases de dados relacionais
*   SQL (criação de esquema, povoamento e consultas)
*   Normalização (3ª Forma Normal)
*   Python para processamento de dados
*   Desenvolvimento web com Flask
*   Integração entre backend, base de dados e frontend
*   Organização de projeto e documentação técnica

## Stack Tecnológica

*   Python
*   Flask
*   SQLite
*   SQL
*   HTML / CSS

## Como Executar Localmente

### Pré-requisitos

*   Python 3
*   pip

### Passos

1.  **(Opcional)** Criar ambiente virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  Instalar dependências:
    ```bash
    pip install flask
    ```

3.  **Configuração da base de dados**
    No ficheiro `db.py`, confirma o caminho para a base de dados:
    ```python
    DB_FILE = "wines.db"
    ```

4.  **Executar o servidor**
    Dentro da pasta `app/`, executa:
    ```bash
    python3 server.py
    ```

5.  **Aceder à aplicação**
    *   http://127.0.0.1:9000
    *   http://localhost:9000

A partir da página inicial é possível navegar por todas as entidades (Wines, Wineries, Regions, Countries, Grapes, Dishes e Vintages), bem como pelas interrogações SQL implementadas.

## Base de Dados

A base de dados é construída a partir do ficheiro CSV `X-Wines` utilizando:

*   Tabela intermédia (staging)
*   Scripts Python para decomposição de listas (castas, harmonizações e vintages)
*   Criação de tabelas associativas para relações N:M

O modelo encontra-se normalizado em **3ª Forma Normal**, garantindo integridade referencial, atomicidade e ausência de redundâncias.
