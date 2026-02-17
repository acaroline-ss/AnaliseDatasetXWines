# chat.py
from flask import Blueprint, request, jsonify, render_template, session
import logging
from chat_logic import processar_pergunta
import uuid

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
def chat_page():
    """Página do chatbot - inicializa sessão"""
    # Gera um ID de conversa se não existir
    if 'conversation_id' not in session:
        session['conversation_id'] = str(uuid.uuid4())
        # Inicializa histórico vazio
        session['chat_history'] = []
    
    return render_template('chat.html')

@chat_bp.route('/api/chat', methods=['POST'])
def chat_api():
    """API do chatbot - mantém histórico na sessão"""
    try:
        data = request.json
        pergunta = data.get('pergunta', '')
        
        if not pergunta:
            return jsonify({'resposta': 'Por favor, faça uma pergunta!'})
        
        # Recupera histórico da sessão
        historico = session.get('chat_history', [])
        
        # Adiciona pergunta atual ao histórico
        historico.append({'role': 'user', 'content': pergunta})
        
        # Processa a pergunta COM o histórico
        resposta = processar_pergunta(pergunta, historico)
        
        # Adiciona resposta ao histórico
        historico.append({'role': 'assistant', 'content': resposta})
        
        # Mantém apenas as últimas 20 mensagens
        if len(historico) > 20:
            historico = historico[-20:]
        
        # Salva histórico na sessão
        session['chat_history'] = historico
        
        return jsonify({'resposta': resposta})
    
    except Exception as e:
        logging.error(f"Erro no chat: {str(e)}")
        return jsonify({'resposta': 'Desculpe, tive um problema. Pode repetir?'}), 500

@chat_bp.route('/api/chat/sugestoes', methods=['GET'])
def sugestoes():
    """Retorna sugestões de perguntas"""
    sugestoes = [
        "Que vinho tinto harmoniza com carne?",
        "Vinhos da região do Douro",
        "Recomende um vinho branco",
        "Vinhos com uva Cabernet Sauvignon",
        "Que prato combina com vinho do Porto?",
        "Qual a diferença entre Vinho do Porto e Vinho do Douro?",
        "Vinhos com mais de 14% álcool"
    ]
    return jsonify({'sugestoes': sugestoes})

@chat_bp.route('/api/chat/nova-conversa', methods=['POST'])
def nova_conversa():
    """Limpa o histórico da conversa atual"""
    session['chat_history'] = []
    return jsonify({'status': 'ok', 'mensagem': 'Nova conversa iniciada!'})