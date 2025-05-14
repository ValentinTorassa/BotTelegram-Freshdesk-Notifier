from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = '7672794559:AAHF0_VhsV5Ps-N9DmkNU6hiSfNNdT0MI2Q'
TELEGRAM_CHAT_ID = '-4756247251' 


@app.route('/ticket-creado', methods=['POST'])
def ticket_creado():
    data = request.get_json()

    ticket_id = data.get('ticket_id')
    subject = data.get('subject')
    ticket_url = data.get('ticket_url')
    status = data.get('status')
    priority = data.get('priority')

    agent_name = data.get('ticket', {}).get('agent', {}).get('name', 'No asignado')
    group_name = data.get('ticket', {}).get('group', {}).get('name', 'Sin grupo')
    contact_name = data.get('ticket', {}).get('contact', {}).get('name', 'Sin nombre')
    contact_email = data.get('ticket', {}).get('contact', {}).get('email', 'Sin email')

    message = f"""📬 *Nuevo Ticket en Freshdesk*\n
🎫 *ID:* {ticket_id}
📝 *Asunto:* {subject}
🔗 [Ver Ticket]({ticket_url})
⚙️ *Estado:* {status}
🚨 *Prioridad:* {priority}
👤 *Cliente:* {contact_name} ({contact_email})
👨‍💼 *Agente:* {agent_name}
👥 *Grupo:* {group_name}
"""
    return enviar_mensaje(message)


@app.route('/ticket-actualizado', methods=['POST'])
def ticket_actualizado():
    data = request.get_json()

    ticket_id = data.get('ticket_id')
    subject = data.get('subject')
    ticket_url = data.get('ticket_url')
    nuevo_estado = data.get('status')
    agente = data.get('ticket', {}).get('agent', {}).get('name', 'No asignado')
    contact_name = data.get('ticket', {}).get('contact', {}).get('name', 'Sin nombre')
    contact_email = data.get('ticket', {}).get('contact', {}).get('email', 'Sin email')

    message = f"""🔄 *Ticket actualizado en Freshdesk*\n
🎫 *ID:* {ticket_id}
📝 *Asunto:* {subject}
⚙️ *Nuevo Estado:* {nuevo_estado}
🔗 [Ver Ticket]({ticket_url})
👨‍💼 *Agente:* {agente}
👤 *Cliente:* {contact_name} ({contact_email})
"""
    return enviar_mensaje(message)

@app.route('/ticket-pendiente', methods=['POST'])
def ticket_pendiente():
    data = request.get_json()

    ticket_id = data.get('ticket_id')
    subject = data.get('subject')
    status = data.get('status')
    due_by = data.get('due_by')
    agente = data.get('ticket', {}).get('agent', {}).get('name', 'No asignado')
    contact_name = data.get('ticket', {}).get('contact', {}).get('name', 'Sin nombre')
    contact_email = data.get('ticket', {}).get('contact', {}).get('email', 'Sin email')

    message = f"""⏰ *Ticket pendiente de respuesta del agente*\n
🎫 *ID:* {ticket_id}
📝 *Asunto:* {subject}
📅 *Vence:* {due_by}
⚙️ *Estado:* {status}
👤 *Cliente:* {contact_name} ({contact_email})
👨‍💼 *Agente:* {agente}
"""
    return enviar_mensaje(message)


@app.route('/test', methods=['GET'])
def test_telegram():
    message = "🧪 *Prueba exitosa!* Este es un mensaje de test desde tu bot de Telegram."
    return enviar_mensaje(message)


def enviar_mensaje(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return 'Mensaje enviado con éxito', 200
    else:
        return f'Error al enviar mensaje: {response.text}', 500


if __name__ == '__main__':
    app.run(port=5000)



    #    - Agregar una acción de tipo "Webhook"
    #    - Método: POST
    #    - URL: https://LINKRENDER/ticket-pendiente
    #    - Encabezado (Header): 
    #         Content-Type: application/json
    #    - Cuerpo (Body del JSON):
    #
    #    {
    #      "ticket_id": "{{ticket.id}}",
    #      "subject": "{{ticket.subject}}",
    #      "status": "{{ticket.status}}",
    #      "due_by": "{{ticket.due_by}}",
    #      "ticket": {
    #        "agent": { "name": "{{ticket.agent.name}}" },
    #        "contact": {
    #          "name": "{{ticket.contact.name}}",
    #          "email": "{{ticket.contact.email}}"
    #        }
    #      }
    #    }