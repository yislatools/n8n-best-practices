# 🚨 Troubleshooting: HTTP Request Tools + AI Agents

> **Guia de resolução:** Problemas comuns e soluções testadas  
> **Baseado em:** Casos reais de debugging e implementação  
> **Atualizado:** 28/07/2025

## 🔍 Problemas Mais Comuns

### 1. ❌ Placeholders Não Substituídos

**Erro Típico:**
```
"O endereço de e-mail '{email}' deve ter a senha '@'"
```

**Causa:** Formato incorreto de placeholders

**❌ Formato Incorreto:**
```json
{
  "cEmail": "{email}",
  "cNome": "{nome_empresa}"
}
```

**✅ Formato Correto:**
```json
{
  "cEmail": "{{ $fromAI(\"email\") }}",
  "cNome": "{{ $fromAI(\"nome_empresa\") }}"
}
```

**Checklist de Verificação:**
- [ ] Usar `{{ $fromAI("campo") }}` ao invés de `{campo}`
- [ ] Aspas duplas escapadas: `\"campo\"`
- [ ] Nome do campo coincide com o usado no agente
- [ ] Tool configurada como AI Tool no workflow

---

### 2. ❌ Tool Não Retorna Dados / Erro Silencioso

**Sintomas:**
- Workflow executa mas tool não retorna nada
- "Error in sub-node" sem detalhes
- Timeout da execução

**Possíveis Causas e Soluções:**

#### A. Tool Description Missing
```json
// ❌ Sem descrição
{
  "parameters": {
    "method": "POST",
    // ... outros parâmetros
  }
}

// ✅ Com descrição adequada
{
  "parameters": {
    "toolDescription": "cadastra_conta: Executa cadastro de conta. Parâmetros: nome, email, cnpj",
    "method": "POST",
    // ... outros parâmetros
  }
}
```

#### B. Parâmetros Mal Configurados
```json
// ❌ Formato de webhook
"cDoc": "{{ $json.body.event.cDoc }}"

// ✅ Formato AI Agent
"cDoc": "{{ $fromAI(\"cnpj_formatado\") }}"
```

#### C. Headers Faltando
```json
"sendHeaders": true,
"headerParameters": {
  "parameters": [
    {
      "name": "Content-Type",
      "value": "application/json"
    }
  ]
}
```

---

### 3. ❌ Erro de Validação da API Externa

**Exemplo - API Omie:**
```
"ERROR: O CNPJ ou CPF informado está inválido"
```

**Diagnóstico e Solução:**

#### A. Verificar Formato de Dados
```javascript
// Para CNPJ Omie - usar com máscara
"cnpj_formatado": "11.222.333/0001-81"  // ✅ Correto
"cnpj_limpo": "11222333000181"          // ❌ Incorreto para Omie
```

#### B. Validar Campos Obrigatórios
- Verificar documentação da API
- Testar com dados válidos conhecidos
- Usar Postman/Insomnia para teste isolado

#### C. Credenciais e Autenticação
```json
{
  "app_key": "sua_app_key_valida",
  "app_secret": "seu_app_secret_valido"
}
```

---

### 4. ❌ Agente Não Chama a Tool

**Sintomas:**
- Agente responde texto mas não executa tool
- Tool aparece conectada mas não é usada

**Soluções:**

#### A. Tool Description Clara
```json
"toolDescription": "cadastra_conta: Executa cadastro. Use quando cliente confirmar dados. Parâmetros: nome, email, cnpj"
```

#### B. Instruções Específicas no Prompt
```markdown
## Instruções para Tools

Quando todos os dados estiverem coletados:
1. Confirme com o cliente
2. Use a tool cadastra_conta com os parâmetros:
   - nome: valor_real_coletado
   - email: valor_real_coletado
   - cnpj: valor_real_coletado
```

#### C. Conexão Correta no Workflow
```
AI Agent → (ai_tool) → HTTP Request Tool
```

---

### 5. ❌ Dados Perdidos Entre Execuções

**Problema:** Agente "esquece" dados coletados

**Soluções:**

#### A. Configurar Memória
```json
{
  "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
  "parameters": {
    "sessionIdType": "customKey",
    "sessionKey": "=1",
    "contextWindowLength": 30
  }
}
```

#### B. Instruções de Persistência no Prompt
```markdown
**IMPORTANTE:** Mantenha TODOS os dados coletados em memória durante toda a conversa:
- nome: [valor]
- email: [valor]
- cnpj: [valor]
```

---

## 🔧 Debugging Passo a Passo

### Checklist de Debugging

#### 1. Verificação de Configuração
- [ ] Tool description presente e clara
- [ ] Parâmetros usando `{{ $fromAI("campo") }}`
- [ ] Headers corretos (Content-Type, Accept)
- [ ] Retry configurado (retryOnFail: true)
- [ ] Error handling (onError: continueRegularOutput)

#### 2. Teste de Conectividade
- [ ] Credentials da API válidas
- [ ] URL da API correta
- [ ] Método HTTP correto (POST/GET)
- [ ] Payload da API bem formado

#### 3. Validação de Dados
- [ ] Campos obrigatórios presentes
- [ ] Formatos corretos (CNPJ, email, telefone)
- [ ] Valores não-nulos nos campos críticos
- [ ] Encoding correto (UTF-8)

#### 4. Fluxo do Agente
- [ ] Tool conectada como ai_tool
- [ ] Prompt com instruções claras
- [ ] Memória configurada (se necessário)
- [ ] Sequência lógica de execução

---

## 📝 Logs de Debug Úteis

### Logs no Prompt do Agente
```markdown
Antes de chamar a tool, confirme internamente:
- Nome coletado: [nome]
- Email coletado: [email] 
- CNPJ coletado: [cnpj]
- Todos os campos obrigatórios: [sim/não]
```

### Logs na Tool (JSON Body)
```json
{
  "debug_info": {
    "timestamp": "{{ new Date().toISOString() }}",
    "nome_recebido": "{{ $fromAI(\"nome\") }}",
    "email_recebido": "{{ $fromAI(\"email\") }}"
  },
  // ... resto do payload
}
```

---

## 🛠️ Ferramentas de Debug

### 1. Postman/Insomnia
- Teste a API isoladamente
- Valide formato do payload
- Verifique headers e autenticação

### 2. Console do n8n
- Monitore execuções em tempo real
- Verifique logs de erro detalhados
- Analise dados entre nodes

### 3. Debug Mode
```json
{
  "options": {
    "debug": true,
    "verbose": true
  }
}
```

---

## 🚨 Cenários de Erro Complexos

### Erro Intermitente
**Sintoma:** Funciona às vezes, falha outras

**Possíveis Causas:**
- Rate limiting da API
- Dados inconsistentes do usuário
- Timeout de rede

**Soluções:**
```json
{
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 1000,
  "timeout": 30000
}
```

### Erro de Encoding
**Sintoma:** Caracteres especiais corrompidos

**Solução:**
```json
"headerParameters": {
  "parameters": [
    {
      "name": "Content-Type",
      "value": "application/json; charset=utf-8"
    }
  ]
}
```

### Erro de Sequência
**Sintoma:** Tools executam fora de ordem

**Solução:**
```markdown
**Sequência Obrigatória:**
1. SEMPRE execute consulta_conta PRIMEIRO
2. APENAS se sucesso, execute cadastra_conta
3. APENAS se conta ok, execute cadastra_contato
```

---

## 📊 Métricas de Sucesso

### KPIs para Monitorar
- **Taxa de sucesso:** >95% das execuções
- **Tempo de resposta:** <30 segundos
- **Taxa de retry:** <10% das execuções
- **Erros de validação:** <5% das tentativas

### Alertas Recomendados
- Falha consecutiva de 3+ execuções
- Timeout de mais de 60 segundos
- Taxa de erro acima de 20%
- Dados corrompidos ou nulos

---

## 🎯 Casos de Teste

### Teste Básico
```javascript
// Dados válidos mínimos
{
  "nome": "Empresa Teste Ltda",
  "email": "teste@empresa.com",
  "cnpj": "11.222.333/0001-81"
}
```

### Teste de Borda
```javascript
// Dados limítrofes
{
  "nome": "Empresa Com Nome Muito Longo Ltda Ltda Ltda",
  "email": "email-com-varios-pontos.e.hifens@sub.dominio.empresa.com.br",
  "cnpj": "99.999.999/0001-99"
}
```

### Teste de Erro
```javascript
// Dados inválidos (para testar tratamento)
{
  "nome": "",
  "email": "email_invalido",
  "cnpj": "123.456.789/0001-00"  // CNPJ inválido
}
```

---

## 🏷️ Tags
`#troubleshooting` `#http-request-tool` `#ai-agents` `#debugging` `#error-handling` `#validation`

---

*Guia baseado em casos reais e soluções testadas - 28/07/2025*