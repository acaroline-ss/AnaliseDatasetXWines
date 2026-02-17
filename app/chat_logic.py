# chat_logic.py 
import logging
import sqlite3
import re
from groq import Groq

# ===== CONFIGURAÇÃO DA API =====
# O chatbot usa a API Groq (gratuita) por padrão.
# Para usar, você precisa de uma chave de API:
# 1. Crie uma conta em https://console.groq.com
# 2. Gere sua chave de API
# 3. Substitua abaixo ou defina como variável de ambiente
#
# 🔑 IMPORTANTE: Nunca compartilhe sua chave públicamente!
#    Em produção, use variáveis de ambiente:
#    export GROQ_API_KEY="sua-chave-aqui"

# Coloque sua chave diretamente (apenas para testes locais)
client = Groq(
    api_key="cole-sua-chave-do-groq-aqui"  # 🔐 Substitua pela sua chave
)

# Para usar outra API (OpenAI, Claude, Gemini, etc), 
# você precisa:
# 1. Trocar a importação no início do arquivo
# 2. Trocar a configuração do client acima
# 3. Ajustar a chamada na função perguntar_groq

# ===== CONFIGURAÇÃO DO BANCO DE DADOS =====
# Ajuste este caminho para a localização do seu arquivo wines.db
# Exemplos:
# - Mac/Linux: '/caminho/para/seu/projeto/wines.db'
# - Windows: 'C:\\caminho\\para\\seu\\projeto\\wines.db'

DB_PATH = '/caminho/para/seu/projeto-bd/wines.db'  # 🔧 ALTERE PARA SEU CAMINHO!

def limpar_texto(texto):
    """Remove colchetes e aspas dos textos"""
    if not texto:
        return ""
    texto = str(texto)
    texto = re.sub(r'[\[\]\'"]', '', texto)
    return texto.strip()

def buscar_dados_especificos(pergunta):
    """Busca dados no banco baseado na pergunta"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    pergunta_lower = pergunta.lower()
    dados_encontrados = []
    
    # FASE 1: BUSCAS ESPECÍFICAS (prioridade máxima)
    
    # 1. Se mencionar REGIÃO
    regioes = ['douro', 'alentejo', 'verde', 'porto', 'gaucha', 'serra']
    for regiao in regioes:
        if regiao in pergunta_lower:
            cursor.execute("""
                SELECT w.WineName, w.Type, r.RegionName
                FROM Wine w
                JOIN Region r ON w.RegionID = r.RegionID
                WHERE LOWER(r.RegionName) LIKE ?
                ORDER BY w.WineName
                LIMIT 15
            """, (f'%{regiao}%',))
            resultados = cursor.fetchall()
            if resultados:
                dados_encontrados.append((f"🍷 VINHOS DA REGIÃO {regiao.upper()}:", resultados, True))
                conn.close()
                return dados_encontrados
    
    # 2. Se mencionar UVA
    uvas = ['cabernet', 'merlot', 'sauvignon', 'chardonnay', 'touriga', 'syrah', 'pinot', 'moscatel']
    for uva in uvas:
        if uva in pergunta_lower:
            cursor.execute("""
                SELECT w.WineName, w.Type, g.GrapeName
                FROM Wine w
                JOIN WineGrape wg ON w.WineID = wg.WineID
                JOIN Grape g ON wg.GrapeID = g.GrapeID
                WHERE LOWER(g.GrapeName) LIKE ?
                ORDER BY w.WineName
                LIMIT 15
            """, (f'%{uva}%',))
            resultados = cursor.fetchall()
            if resultados:
                dados_encontrados.append((f"🍇 VINHOS COM UVA {uva.upper()}:", resultados, True))
                conn.close()
                return dados_encontrados
    
    # 3. Se mencionar PAÍS
    paises = {
        'portugal': 'Portugal', 'português': 'Portugal', 'portuguesa': 'Portugal',
        'brasil': 'Brazil', 'brasileiro': 'Brazil',
        'espanha': 'Spain', 'espanhol': 'Spain',
        'frança': 'France', 'frances': 'France',
        'itália': 'Italy', 'italia': 'Italy', 'italiano': 'Italy'
    }
    for chave, valor in paises.items():
        if chave in pergunta_lower:
            cursor.execute("""
                SELECT w.WineName, w.Type, c.CountryName, r.RegionName
                FROM Wine w
                JOIN Region r ON w.RegionID = r.RegionID
                JOIN Country c ON r.CountryCode = c.Code
                WHERE LOWER(c.CountryName) LIKE ?
                ORDER BY w.WineName
                LIMIT 15
            """, (f'%{valor}%',))
            resultados = cursor.fetchall()
            if resultados:
                dados_encontrados.append((f"🌎 VINHOS DE {valor.upper()}:", resultados, True))
                conn.close()
                return dados_encontrados
    
    # 4. Se mencionar HARMONIZAÇÃO
    pratos = {
        'carne': 'Beef', 'bife': 'Beef', 'vaca': 'Beef',
        'porco': 'Pork', 'leitão': 'Pork',
        'peixe': 'Fish', 'bacalhau': 'Codfish',
        'queijo': 'Cheese', 'massa': 'Pasta', 'pizza': 'Pizza'
    }
    for chave, valor in pratos.items():
        if chave in pergunta_lower:
            cursor.execute("""
                SELECT w.WineName, w.Type, d.DishName
                FROM Wine w
                JOIN WineDish wd ON w.WineID = wd.WineID
                JOIN Dish d ON wd.DishID = d.DishID
                WHERE LOWER(d.DishName) LIKE ?
                ORDER BY w.WineName
                LIMIT 15
            """, (f'%{valor}%',))
            resultados = cursor.fetchall()
            if resultados:
                dados_encontrados.append((f"🍽️ VINHOS QUE HARMONIZAM COM {chave.upper()}:", resultados, True))
                conn.close()
                return dados_encontrados
    
    # 5. Se mencionar TIPO
    if 'tinto' in pergunta_lower:
        cursor.execute("""
            SELECT WineName, Type, ABV FROM Wine 
            WHERE Type='Red' 
            ORDER BY WineName 
            LIMIT 20
        """)
        tintos = cursor.fetchall()
        if tintos:
            dados_encontrados.append(("🍷 VINHOS TINTOS:", tintos, True))
            conn.close()
            return dados_encontrados
    
    if 'branco' in pergunta_lower:
        cursor.execute("""
            SELECT WineName, Type, ABV FROM Wine 
            WHERE Type='White' 
            ORDER BY WineName 
            LIMIT 20
        """)
        brancos = cursor.fetchall()
        if brancos:
            dados_encontrados.append(("🥂 VINHOS BRANCOS:", brancos, True))
            conn.close()
            return dados_encontrados
    
    if 'rose' in pergunta_lower or 'rosé' in pergunta_lower:
        cursor.execute("""
            SELECT WineName, Type, ABV FROM Wine 
            WHERE Type='Rosé' 
            ORDER BY WineName 
            LIMIT 20
        """)
        roses = cursor.fetchall()
        if roses:
            dados_encontrados.append(("🌸 VINHOS ROSÉ:", roses, True))
            conn.close()
            return dados_encontrados
    
    # 6. Se mencionar ÁLCOOL
    if 'álcool' in pergunta_lower or 'alcoólico' in pergunta_lower or 'graduação' in pergunta_lower:
        cursor.execute("""
            SELECT WineName, Type, ABV FROM Wine 
            WHERE ABV > 14.0 AND ABV IS NOT NULL 
            ORDER BY ABV DESC 
            LIMIT 15
        """)
        alto_teor = cursor.fetchall()
        if alto_teor:
            dados_encontrados.append(("🍷 VINHOS COM MAIS DE 14% ÁLCOOL:", alto_teor, True))
            conn.close()
            return dados_encontrados
    
    # FASE 2: Se não achou nada específico, busca geral
    cursor.execute("""
        SELECT WineName, Type FROM Wine 
        ORDER BY WineName 
        LIMIT 20
    """)
    gerais = cursor.fetchall()
    if gerais:
        dados_encontrados.append(("📌 CATÁLOGO DE VINHOS:", gerais, False))
    
    conn.close()
    return dados_encontrados

def perguntar_groq(pergunta, dados, historico=None):

    """Envia para o Groq com contexto da conversa anterior"""
    
    # Monta o contexto com os dados encontrados 
    contexto_dados = "DADOS DO CATÁLOGO DE VINHOS:\n\n"

    if dados and len(dados) > 0:
        for titulo, itens, is_especifico in dados:
            contexto_dados += f"{titulo}\n"
            for item in itens[:15]:  # Mostra até 15 vinhos
                nome = limpar_texto(item[0])
                
                # CASO 1: Tem ABV (posição 2)
                if len(item) >= 3 and item[2] is not None:
                    abv = item[2]
                    if len(item) >= 2 and item[1]:
                        tipo = limpar_texto(item[1])
                        contexto_dados += f"  • {nome} ({tipo}) - {abv}% álcool\n"
                    else:
                        contexto_dados += f"  • {nome} - {abv}% álcool\n"
                
                # CASO 2: Não tem ABV mas tem tipo
                elif len(item) >= 2 and item[1]:
                    tipo = limpar_texto(item[1])
                    contexto_dados += f"  • {nome} ({tipo})\n"
                
                # CASO 3: Só nome
                else:
                    contexto_dados += f"  • {nome}\n"
            contexto_dados += "\n"
    else:
        contexto_dados += "Nenhum dado encontrado no catálogo para esta consulta.\n\n"
    
    # Monta o histórico da conversa (se existir)
    contexto_historico = ""
    if historico and len(historico) > 0:
        contexto_historico = "HISTÓRICO DA CONVERSA ATUAL:\n"
        for msg in historico[-10:]:  
            papel = "Cliente" if msg['role'] == 'user' else "Sommelier"
            contexto_historico += f"{papel}: {msg['content']}\n"
        contexto_historico += "\n"
    
    prompt = f"""{contexto_dados}

{contexto_historico}

PERGUNTA ATUAL DO CLIENTE: {pergunta}

Você é um sommelier digital especialista em vinhos.

⚠️ **LEIA A PERGUNTA COM ATENÇÃO ANTES DE RESPONDER**

A pergunta do cliente é: "{pergunta}"

**IDENTIFIQUE O TIPO DE PERGUNTA:**

🔍 Se a pergunta for sobre **PRATOS, COMIDAS, HARMONIZAÇÃO** (ex: "que prato combina", "o que comer com", "harmoniza com"):
   → Responda APENAS sobre sugestões de comidas e harmonização
   → NÃO liste vinhos (a menos que seja para exemplificar)
   → Ex: "O Vinho do Porto harmoniza perfeitamente com queijos azuis, chocolates amargos e sobremesas à base de frutos secos."

🍷 Se a pergunta for sobre **VINHOS** (ex: "quais vinhos", "me mostre vinhos", "lista de vinhos"):
   → Liste os vinhos encontrados no catálogo
   → Siga o formato elegante com descrições

🌍 Se a pergunta for sobre **REGIÕES** (ex: "vinhos da região"):
   → Liste vinhos daquela região

**SUA RESPOSTA DEVE SER EXCLUSIVAMENTE SOBRE O QUE FOI PERGUNTADO.**

⚠️ INSTRUÇÃO CRÍTICA - LEIA COM ATENÇÃO ⚠️

Os dados do catálogo ACIMA são a ÚNICA fonte de verdade.
Você DEVE usar EXCLUSIVAMENTE estes dados para responder.

Se um valor numérico (como porcentagem de álcool) aparecer nos dados, você DEVE usar esse valor exato.
Por exemplo, se os dados dizem "50.0% álcool", você deve dizer "50.0%" e NUNCA inventar outro valor. E falar a porcentagem de alcool 
apenas quando a pergunta explicitamente tiver haver com isso, caso contrário não precisa colocar esse informação na resposta.

REGRAS ABSOLUTAS - NÃO VIOLAR:
1. NÃO alucine - use APENAS os dados fornecidos acima
2. NÃO invente vinhos, produtores, safras ou informações
3. Se os dados acima estiverem vazios, diga que não encontrou
4. NÃO associe vinhos a vinícolas sem confirmação nos dados
5. Quando não souber, diga: "Não encontrei essa informação no meu catálogo"
6. Seja 100% fiel aos dados do catálogo

🎯 **SUA MISSÃO:**
Responda EXATAMENTE o que foi perguntado. Se a pergunta for sobre harmonização (pratos, comidas), foque APENAS em sugestões de harmonização. Se for sobre vinhos, liste vinhos. Se for sobre regiões, fale de regiões.

📋 **EXEMPLOS DE RESPOSTAS CORRETAS:**

Cliente: "Que prato combina com vinho do Porto?"
Resposta correta: Deve falar de PRATOS (queijos, sobremesas, chocolates) que harmonizam com Porto.

Cliente: "Vinhos da região do Douro"  
Resposta correta: Deve listar VINHOS da região do Douro.

Cliente: "Vinhos com uva Cabernet"
Resposta correta: Deve listar VINHOS feitos com uva Cabernet.


DIRETRIZES DE RESPOSTA:
🎯 **Tom e Estilo:**
• Seja caloroso e profissional, como um sommelier de restaurante estrelado
• Use linguagem refinada mas acessível
• Transmita paixão pelos vinhos

📋 **Formatação:**
• Use **negrito** para nomes de vinhos e destaques
• Use *itálico* para termos técnicos (terroir, assemblage, etc)
• Use • para listas de vinhos
• Separe seções com linhas em branco
• Use emojis com parcimônia e elegância: 🍷 🥂 🍇 🌍

🗂️ **Estrutura ideal:**
1. Comece com uma saudação ou reconhecimento da pergunta
2. Apresente os vinhos encontrados de forma organizada
3. Para cada vinho, mencione nome (negrito) e características
4. Se houver muitos, agrupe por categoria
5. **NÃO use "Recomendação do sommelier" como um título separado** - em vez disso, a resposta COMO UM TODO deve soar como uma recomendação pessoal sua
6. **TERMINE A RESPOSTA DE FORMA NATURAL, SEM PERGUNTAS ADICIONAIS.** Apenas conclua o raciocínio e pare.

🚫 **EVITE:**
• "Recomendação do sommelier:" (título separado)
• Frases genéricas como "Qualquer um desses é uma excelente escolha"
• Finalizações que não se conectam com o assunto
* NÃO faça perguntas no final.** A resposta deve ser completa em si mesma.

✅ **PREFIRA:**
• Uma resposta fluida que já é a recomendação em si
• Finalizações específicas como:
  - "Para carnes mais intensas, o *Douro Tinto* seria minha escolha pessoal. Gostaria de conhecer outras opções da mesma região?"
  - "O *Flor de Crasto* tem uma elegância que surpreende. Quer explorar vinhos com perfil semelhante?"
  - "Fiquei especialmente impressionado com o *Meandro Douro* pela relação qualidade-preço. Posso sugerir outras safras?"

🎯 **SUA RESPOSTA DEVE:**
• Ser coerente com o que já foi discutido
• Avançar a conversa, não repetir
• Parecer que você LEMBRA do que foi falado


Resposta:"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Você é um sommelier especialista em vinhos. "
                "Você é extremamente honesto e NUNCA inventa informações que não estão nos dados fornecidos. "
                "REGRAS TÉCNICAS OBRIGATÓRIAS:"
                "• Vinhos TINTOS: podem ter notas de frutas vermelhas (cereja, framboesa, morango)"
                "• Vinhos BRANCOS: têm notas de frutas brancas (pêra, maçã, pêssego) ou cítricas (limão, laranja)"
                "• 🚫 NUNCA associe a vinhos brancos - isso é um erro técnico grave"
                "• 🚫 NÃO repita informações - cada vinho deve ter uma descrição única"

                "Se você não tiver informações específicas sobre o perfil de um vinho nos dados fornecidos, limite-se a mencionar sua existência sem inventar notas de degustação."
                "SUAS CARACTERÍSTICAS:"
                "• Você LEMBRA de tudo que foi discutido na conversa"
                "• Você usa o histórico para dar continuidade natural"
                "• Você NUNCA repete informações já fornecidas"
                "• Você entende pronomes e referências (esse, aquele, dessa região)"
                "• Suas respostas são personalizadas com base no contexto"
                "Exemplo: Se antes falou de vinhos do Douro e agora perguntam e os tintos?, você sabe que é da mesma região."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"Erro no Groq: {e}")
        return formatar_resposta_simples(dados)

def formatar_resposta_simples(dados):
    """Resposta simples sem IA (fallback)"""
    resposta = "🍷 **VINHOS ENCONTRADOS:**\n\n"
    
    for titulo, itens, is_especifico in dados:
        resposta += f"**{titulo}**\n"
        resposta += "─" * 30 + "\n"
        
        for item in itens[:10]:
            nome = limpar_texto(item[0])
            if len(item) > 2 and item[2]:
                extra = limpar_texto(item[2])
                resposta += f"• {nome} ({extra})\n"
            elif len(item) > 1 and item[1]:
                tipo = limpar_texto(item[1])
                resposta += f"• {nome} ({tipo})\n"
            else:
                resposta += f"• {nome}\n"
        
        resposta += "\n"
    
    return resposta

def processar_pergunta(pergunta, historico=None):
    """Função principal - AGORA RECEBE HISTÓRICO"""
    
    logging.info(f"🔍 Pergunta: {pergunta}")
    
    # PASSO 1: Busca dados específicos no banco
    dados = buscar_dados_especificos(pergunta)
    
    # PASSO 2: Se encontrou dados, retorna resposta com contexto
    if dados:
        return perguntar_groq(pergunta, dados, historico)
    
    # PASSO 3: Se não encontrou nada, mensagem amigável
    return "Não encontrei vinhos específicos para sua pergunta. Pode reformular ou perguntar sobre vinhos tintos, região do Douro, ou uvas específicas?"