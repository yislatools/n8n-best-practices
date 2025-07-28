# 🛠️ Configurações de Tools: API Omie

> **Arquivo de referência:** Configurações funcionais testadas e validadas  
> **Fonte:** Implementação real em produção (28/07/2025)  
> **Status:** ✅ 100% Funcional

## 📋 Tool: cadastra_conta

### Configuração Completa
```json
{
  "nodes": [
    {
      "parameters": {
        "toolDescription": "cadastra_conta: Executa cadastro completo de nova conta no CRM Omie com observações estruturadas",
        "method": "POST",
        "url": "https://app.omie.com.br/api/v1/crm/contas/",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\n  \"call\": \"IncluirConta\",\n  \"param\": [\n    {\n      \"identificacao\": {\n        \"cCodInt\": \"{{ $fromAI(\"cnpj_formatado\") }}\",\n        \"cNome\": \"{{ $fromAI(\"nome\") }}\",\n        \"cDoc\": \"{{ $fromAI(\"cnpj_formatado\") }}\",\n        \"cObs\": \"📋 DADOS DO PROJETO:\\n\\n🏢 Como conheceu: {{ $fromAI(\"como_conheceu\") }}\\n📐 Estimativa: {{ $fromAI(\"estimativa_projeto\") }}\\n🎨 Revestimento: {{ $fromAI(\"revestimento\") }}\\n⚖️ Carga: {{ $fromAI(\"especificacao_carga\") }}\\n🚚 Transporte: {{ $fromAI(\"transporte\") }}\\n👷 Mão de obra: {{ $fromAI(\"mao_obra\") }}\\n\\n📅 Data cadastro: {{ $fromAI(\"data_cadastro\") }}\"\n      },\n      \"endereco\": {\n        \"cCidade\": \"{{ $fromAI(\"cidade\") }}\",\n        \"cUF\": \"{{ $fromAI(\"estado\") }}\"\n      },\n      \"telefone_email\": {\n        \"cDDDTel\": \"{{ $fromAI(\"ddd\") }}\",\n        \"cNumTel\": \"{{ $fromAI(\"telefone\") }}\",\n        \"cEmail\": \"{{ $fromAI(\"email\") }}\"\n      }\n    }\n  ],\n  \"app_key\": \"SEU_APP_KEY\",\n  \"app_secret\": \"SEU_APP_SECRET\"\n}",
        "options": {}
      },
      "type": "n8n-nodes-base.httpRequestTool",
      "typeVersion": 4.2,
      "position": [-1840, 624],
      "id": "cadastra_conta_id",
      "name": "cadastra_conta",
      "alwaysOutputData": true,
      "retryOnFail": true,
      "maxTries": 3,
      "onError": "continueRegularOutput"
    }
  ]
}
```

### Campos Necessários no Agente
```javascript
// Campos básicos (obrigatórios)
nome: "Nome da Empresa Ltda"
cnpj_formatado: "11.222.333/0001-81"  
email: "contato@empresa.com"
cidade: "São Paulo"
estado: "SP"
ddd: "11"
telefone: "999887766"

// Campos para observações (opcionais)
como_conheceu: "Google"
estimativa_projeto: "500m² - altura 15cm"
revestimento: "Carpete modular"
especificacao_carga: "Distribuída 300kg/m²"
transporte: "Necessário"
mao_obra: "Necessária"
data_cadastro: "28/07/2025 14:30"
```

---

## 🔍 Tool: consulta_conta

### Versão Recomendada (ListarContas)
```json
{
  "nodes": [
    {
      "parameters": {
        "toolDescription": "consulta_conta: Verifica se CNPJ já existe na base CRM Omie antes do cadastro. Use apenas o CNPJ no formato XX.XXX.XXX/XXXX-XX. Retorna se a conta existe ou não.",
        "method": "POST",
        "url": "https://app.omie.com.br/api/v1/crm/contas/",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Content-Type",
              "value": "application/json"
            },
            {
              "name": "Accept",
              "value": "application/json"
            }
          ]
        },
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\n  \"call\": \"ListarContas\",\n  \"param\": [\n    {\n      \"pagina\": 1,\n      \"registros_por_pagina\": 1,\n      \"filtrar_por_documento\": \"{{ $fromAI(\"cnpj_formatado\") }}\"\n    }\n  ],\n  \"app_key\": \"SEU_APP_KEY\",\n  \"app_secret\": \"SEU_APP_SECRET\"\n}",
        "options": {}
      },
      "type": "n8n-nodes-base.httpRequestTool",
      "typeVersion": 4.2,
      "position": [-1712, 976],
      "id": "consulta_conta_id",
      "name": "consulta_conta",
      "retryOnFail": true,
      "maxTries": 3,
      "alwaysOutputData": true,
      "onError": "continueRegularOutput"
    }
  ]
}
```

### Versão Alternativa (VerificarConta)
```json
{
  "jsonBody": "={\n  \"call\": \"VerificarConta\",\n  \"param\": [\n    {\n      \"cDoc\": \"{{ $fromAI(\"cnpj_formatado\") }}\"\n    }\n  ],\n  \"app_key\": \"SEU_APP_KEY\",\n  \"app_secret\": \"SEU_APP_SECRET\"\n}"
}
```

---

## 👤 Tool: cadastra_contato

### Configuração Simplificada
```json
{
  "nodes": [
    {
      "parameters": {
        "toolDescription": "cadastra_contato: Cadastra contato vinculado à conta. Use após cadastrar a conta da empresa. Parâmetros: nome, cnpj, codigo_interno (para vincular à empresa).",
        "method": "POST",
        "url": "https://app.omie.com.br/api/v1/crm/contatos/",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\n  \"call\": \"IncluirContato\",\n  \"param\": [\n    {\n      \"identificacao\": {\n        \"cCodInt\": \"{{ $fromAI(\"cnpj_formatado\") }}\",\n        \"cNome\": \"{{ $fromAI(\"nome\") }}\",\n        \"cDoc\": \"{{ $fromAI(\"cnpj_formatado\") }}\"\n      }\n    }\n  ],\n  \"app_key\": \"SEU_APP_KEY\",\n  \"app_secret\": \"SEU_APP_SECRET\"\n}",
        "options": {}
      },
      "type": "n8n-nodes-base.httpRequestTool",
      "typeVersion": 4.2,
      "position": [-1616, 640],
      "id": "cadastra_contato_id",
      "name": "cadastra_contato",
      "retryOnFail": true,
      "maxTries": 3,
      "alwaysOutputData": true,
      "onError": "continueRegularOutput"
    }
  ]
}
```

---

## ⚙️ Configurações Globais

### Headers Recomendados
```json
"headerParameters": {
  "parameters": [
    {
      "name": "Content-Type",
      "value": "application/json"
    },
    {
      "name": "Accept", 
      "value": "application/json"
    }
  ]
}
```

### Configurações de Retry
```json
"retryOnFail": true,
"maxTries": 3,
"alwaysOutputData": true,
"onError": "continueRegularOutput"
```

---

## 🔐 Configuração de Credenciais

### Obtenção das Credenciais Omie
1. Acesse o painel da Omie
2. Vá em **Configurações** > **Integração**
3. Gere um novo **App Key** e **App Secret**
4. Configure os valores nas tools

### Variáveis de Ambiente (Recomendado)
```bash
OMIE_APP_KEY=sua_app_key_aqui
OMIE_APP_SECRET=seu_app_secret_aqui
```

---

## 📝 Exemplo de Uso Completo

### Sequência de Execução
```javascript
// 1. Consultar se CNPJ existe
consulta_conta({
  cnpj_formatado: "11.222.333/0001-81"
})

// 2. Se não existe, cadastrar empresa
cadastra_conta({
  nome: "Tech Solutions Ltda",
  cnpj_formatado: "11.222.333/0001-81",
  email: "contato@techsolutions.com",
  cidade: "São Paulo",
  estado: "SP",
  ddd: "11",
  telefone: "999887766",
  como_conheceu: "Google",
  estimativa_projeto: "500m² - altura 15cm",
  // ... outros campos
})

// 3. Se empresa cadastrada com sucesso, cadastrar contato
cadastra_contato({
  nome: "Tech Solutions Ltda",
  cnpj_formatado: "11.222.333/0001-81"
})
```

---

## 🚨 Pontos Críticos

### ✅ Fazer Sempre
- Usar formato `{{ $fromAI("campo") }}` para placeholders
- CNPJ sempre com máscara: `XX.XXX.XXX/XXXX-XX`
- Cadastrar empresa ANTES do contato
- Incluir `retryOnFail` e `onError`

### ❌ Nunca Fazer
- Usar formato `{campo}` (não funciona)
- CNPJ sem máscara para API Omie
- Cadastrar contato sem empresa
- Ignorar tratamento de erros

---

## 📊 Respostas Esperadas

### Sucesso - cadastra_conta
```json
{
  "nCod": 3512969548,
  "cCodInt": "11.222.333/0001-81",
  "cCodStatus": "0",
  "cDesStatus": "Conta cadastrada com sucesso!"
}
```

### Sucesso - consulta_conta
```json
{
  "conta_cadastro": [{
    "identificacao": {
      "cCodInt": "11.222.333/0001-81",
      "cNome": "Tech Solutions Ltda"
    }
  }]
}
```

### Erro Comum
```json
{
  "faultstring": "ERROR: O CNPJ ou CPF informado está inválido.",
  "faultcode": "SOAP-ENV:Client-206"
}
```

---

## 🏷️ Tags
`#omie-api` `#configuracao-tools` `#http-request-tool` `#cnpj` `#examples` `#producao`

---

*Configurações testadas e validadas em ambiente de produção - 28/07/2025*