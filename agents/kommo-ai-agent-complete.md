# Agente IA CRM Kommo - Chat Conversacional

## 🤖 Overview

Agente IA completo para CRM Kommo com chat trigger, especializado em coleta conversacional de leads de energia solar. Integração direta via webhook com 3 tools HTTP para operações completas de CRM.

## 🏗️ Arquitetura

```
Webhook Chat Trigger → AI Agent Tool → 3 CRM Tools
    ↓                    ↓                ↓
 POST /kommo-crm     OpenAI GPT      [🔍 Buscar]
                                     [✅ Cadastrar]  
                                     [🔄 Atualizar]
```

## 🛠️ Componentes

### 1. **Chat Trigger - Kommo CRM**
- **Tipo**: `n8n-nodes-base.webhook`
- **Método**: POST
- **Path**: `/kommo-crm-agent`
- **Função**: Recebe mensagens de chat e inicia conversação

### 2. **Agente IA - CRM Kommo**
- **Tipo**: `@n8n/n8n-nodes-langchain.agentTool`
- **Modelo**: OpenAI (configurável)
- **Função**: Processamento conversacional inteligente
- **Iterações**: 10 máximo por conversa

### 3. **Tools CRM (3 Ferramentas)**

#### 🔍 **Buscar Cliente**
```json
{
  "method": "GET",
  "url": "https://n8nyisla.kommo.com/api/v4/leads",
  "query": "{{ $fromAI('termo_busca') }}",
  "function": "Evita duplicatas, busca por telefone/email"
}
```

#### ✅ **Cadastrar Cliente**
```json
{
  "method": "POST", 
  "url": "https://n8nyisla.kommo.com/api/v4/leads",
  "function": "Cria novos leads com todos os campos customizados"
}
```

#### 🔄 **Atualizar Cliente**
```json
{
  "method": "PATCH",
  "url": "https://n8nyisla.kommo.com/api/v4/leads/{{ $fromAI('lead_id') }}",
  "function": "Atualiza dados de leads existentes"
}
```

## 📊 Dados Coletados

### 🔹 **Dados Pessoais**
- `nome_contato`: Nome completo
- `whatsapp`: WhatsApp com DDD (11 dígitos)
- `email`: Email válido
- `estado`: Estado/localização

### 🔹 **Dados Comerciais**
- `tipo_interesse`: Tipo de interesse em energia solar
- `valor_conta`: Valor da conta de energia (R$)
- `distribuidora`: Distribuidora de energia
- `expectativa_ganhos`: Expectativa de ganhos
- `tempo_disponivel`: Tempo disponível para projeto

## 🧠 Comportamento do Agente

### **Personalidade**
- **Tom**: Profissional, acolhedor e eficiente
- **Expertise**: Demonstra conhecimento em energia solar
- **Abordagem**: Conversacional, nunca interrogatório

### **Fluxo de Conversação**
1. **Cumprimento** e identificação do interesse
2. **Busca cliente** existente (telefone/email)
3. **Coleta dados** faltantes de forma natural
4. **Confirma informações** antes de salvar
5. **Executa ação CRM** (cadastrar/atualizar)
6. **Confirma sucesso** e próximos passos

### **Validações Automáticas**
- WhatsApp: 11 dígitos com DDD
- Email: Formato válido (@domain.com)
- Valor conta: Somente números

## 🔗 Mapeamento de Campos

| Campo Workflow | Field ID | Descrição |
|----------------|----------|-----------|
| `whatsapp` | 1702010 | WhatsApp do cliente |
| `email` | 1702012 | Email do cliente |
| `estado` | 1702014 | Estado/localização |
| `tipo_interesse` | 1702016 | Tipo de interesse |
| `distribuidora` | 1702018 | Distribuidora de energia |
| `expectativa_ganhos` | 1702020 | Expectativa de ganhos |
| `tempo_disponivel` | 1702022 | Tempo disponível |

## 🚀 Implementação

### **1. Pré-requisitos**
```bash
# Credenciais necessárias
- OpenAI API Key (para AI Agent)
- Bearer Token Kommo (já configurado no workflow)
```

### **2. Importar Workflow**
1. Copie o JSON do agente completo
2. Importe no n8n
3. Configure credencial OpenAI
4. Ative o workflow

### **3. Configuração Chat Trigger**
```bash
# URL do webhook será:
https://seu-n8n-instance.com/webhook/kommo-crm-agent

# Método: POST
# Content-Type: application/json
```

### **4. Integração Frontend**
```javascript
// Exemplo de envio de mensagem para o agente
fetch('https://seu-n8n-instance.com/webhook/kommo-crm-agent', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: "Olá, tenho interesse em energia solar",
    user_id: "user123",
    chat_id: "chat456"
  })
});
```

## 📱 Exemplos de Conversação

### **Exemplo 1: Novo Cliente**
```
👤 User: Olá, tenho interesse em energia solar
🤖 Agent: Olá! Que ótimo saber do seu interesse em energia solar! Para te ajudar melhor, vou buscar se você já é nosso cliente. Pode me informar seu WhatsApp?

👤 User: (11) 99999-9999
🤖 Agent: [Busca cliente no CRM] Perfeito! Vejo que é nosso primeiro contato. Qual seu nome completo?

👤 User: João Silva
🤖 Agent: Prazer, João! E qual seu email?

[... conversa continua coletando todos os dados ...]

🤖 Agent: ✅ Perfeito! Cadastrei suas informações no nosso CRM. Em breve nossa equipe entrará em contato para apresentar a melhor solução em energia solar para você!
```

### **Exemplo 2: Cliente Existente**
```
👤 User: Quero atualizar meus dados
🤖 Agent: [Busca no CRM] Encontrei seu cadastro! O que gostaria de atualizar?

👤 User: Mudei de endereço, agora estou em SP
🤖 Agent: [Atualiza no CRM] ✅ Pronto! Atualizei seu estado para SP no nosso sistema.
```

## ✅ Status de Validação

**Status**: `VÁLIDO` ✅  
**Erros**: `0`  
**Warnings**: `7` (normais para AI workflows)  
**Expressões validadas**: `21`  
**Conexões AI tool**: `3 tools conectadas`

## 🔧 Troubleshooting

### **Problema: Agent não responde**
- Verificar credencial OpenAI configurada
- Verificar webhook ativo
- Verificar formato da mensagem de entrada

### **Problema: Erro nas tools CRM**
- Verificar Bearer token válido
- Verificar URLs do Kommo corretas
- Verificar field_ids correspondentes

### **Problema: Dados não salvam**
- Verificar se agente está coletando dados corretos
- Verificar mapeamento de campos
- Verificar status_id e pipeline_id válidos

## 📈 Monitoramento

### **KPIs do Agente**
- Taxa de conversão: leads coletados vs. conversas iniciadas
- Tempo médio de coleta: duração das conversas
- Qualidade dos dados: completude dos campos
- Taxa de erro: falhas nas operações CRM

### **Logs Importantes**
- Execuções do workflow
- Retries das tools HTTP
- Responses do agente IA
- Errors de validação

## 🔄 Evolução e Melhorias

### **Próximas Features**
- [ ] Integração com WhatsApp Business
- [ ] Chat memory para conversas contínuas
- [ ] Qualificação automática de leads
- [ ] Agendamento de reuniões
- [ ] Envio de propostas automáticas

### **Otimizações**
- [ ] Cache de dados para clientes recorrentes
- [ ] Templates de resposta dinâmicos
- [ ] Integração com outros CRMs
- [ ] Analytics avançados de conversação

---

**Versão**: 1.0 - Agente AI Conversacional  
**Autor**: Sistema n8n-mcp especializado  
**Data**: 2025-09-06  
**Repo**: [yislatools/n8n-best-practices](https://github.com/yislatools/n8n-best-practices)
