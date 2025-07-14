# 📝 Convenções de Nomenclatura

> **Objetivo**: Padronizar naming para melhorar legibilidade, manutenibilidade e colaboração em workflows n8n Enterprise.

---

## 🎯 **Princípios Fundamentais**

✅ **Clareza**: Nomes auto-explicativos  
✅ **Consistência**: Padrões uniformes em todo o projeto  
✅ **Brevidade**: Máximo 50 caracteres quando possível  
✅ **Contexto**: Incluir domínio/propósito quando relevante  

---

## 📊 **Tabela de Padrões**

| **Elemento** | **Padrão** | **Exemplo** | **Observações** |
|--------------|------------|-------------|----------------|
| **Workflow** | `{domínio}-{ação}` | `crm-syncContacts` | Kebab-case, domínio em minúsculo |
| **Node Set** | `set_{contexto}` | `set_preparePayload` | Snake_case, verbo descritivo |
| **Node HTTP** | `api_{serviço}_{ação}` | `api_salesforce_getLeads` | Identificar serviço externo |
| **Node IF** | `check_{condição}` | `check_hasEmail` | Condição boolean clara |
| **Node Switch** | `route_{critério}` | `route_byStatus` | Critério de roteamento |
| **Variável Global** | `UPPER_SNAKE` | `ACCESS_TOKEN` | Constantes em maiúsculo |
| **Expressão** | `camelCase` | `$json.firstName` | Propriedades JSON |
| **Webhook** | `webhook_{evento}` | `webhook_orderCreated` | Evento disparador |
| **Sub-Workflow** | `sub_{processo}` | `sub_validateUser` | Processo encapsulado |

---

## 🏗️ **Estrutura de Workflows**

### **📁 Organização por Domínio**
```text
Workflows/
├── 📊 CRM/
│   ├── crm-syncContacts
│   ├── crm-updateLeads
│   └── crm-generateReports
├── 💰 Finance/
│   ├── finance-processPayments
│   ├── finance-reconcileBanks
│   └── finance-invoiceGeneration
├── 📧 Marketing/
│   ├── marketing-emailCampaigns
│   ├── marketing-leadScoring
│   └── marketing-analyticsReports
└── 🔧 System/
    ├── system-healthCheck
    ├── system-backupData
    └── system-logRotation
```

### **🏷️ Tags Padronizadas**
```yaml
Tags de Ambiente:
  - env:dev
  - env:staging
  - env:prod

Tags de Criticidade:
  - critical
  - important
  - routine

Tags de Domínio:
  - domain:crm
  - domain:finance
  - domain:marketing
  - domain:system

Tags de Funcionalidade:
  - sync
  - webhook
  - scheduled
  - manual
```

---

## 🔗 **Padrões de Conexões**

### **Node Names Descritivos**
```javascript
// ✅ BOM
"HTTP Request - Get Salesforce Contacts"
"Set - Prepare Contact Payload"
"Postgres - Insert Contact Record"
"IF - Check Email Exists"

// ❌ RUIM
"HTTP Request"
"Set"
"Postgres"
"IF"
```

### **Outputs Nomeados**
```javascript
// ✅ Switch Node Outputs
Outputs: {
  "active": "Active Users",
  "inactive": "Inactive Users",
  "pending": "Pending Approval"
}

// ✅ IF Node Outputs
Outputs: {
  "true": "Valid Email",
  "false": "Invalid Email"
}
```

---

## 🗂️ **Convenções de Credenciais**

| **Tipo** | **Padrão** | **Exemplo** |
|----------|------------|-------------|
| **API Keys** | `{serviço}_API_KEY` | `SALESFORCE_API_KEY` |
| **Database** | `{db}_{env}_CONN` | `POSTGRES_PROD_CONN` |
| **OAuth** | `{serviço}_OAUTH` | `GOOGLE_OAUTH` |
| **Webhook** | `{app}_WEBHOOK_SECRET` | `STRIPE_WEBHOOK_SECRET` |

---

## 📝 **Template de Documentação**

### **Workflow Header Comment**
```markdown
/**
 * WORKFLOW: crm-syncContacts
 * DESCRIPTION: Sincroniza contatos entre Salesforce e PostgreSQL
 * TRIGGER: Webhook (Salesforce Contact Created/Updated)
 * FREQUENCY: Real-time
 * DEPENDENCIES: Salesforce API, PostgreSQL
 * OWNER: YISLA
 * LAST_UPDATED: 2025-07-14
 */
```

### **Node Documentation**
```markdown
// Node Notes Template
PURPOSE: [O que este node faz]
INPUT: [Dados esperados]
OUTPUT: [Dados produzidos]
ERROR_HANDLING: [Como tratar falhas]
DEPENDENCIES: [Serviços/APIs necessários]
```

---

## ✅ **Checklist de Validação**

- [ ] Nome do workflow segue padrão `{domínio}-{ação}`
- [ ] Todos os nodes têm nomes descritivos
- [ ] Variáveis seguem convenção apropriada
- [ ] Tags aplicadas corretamente
- [ ] Credenciais nomeadas consistentemente
- [ ] Documentação adicionada nos headers
- [ ] Outputs nomeados quando aplicável

---

## 🔍 **Ferramentas de Validação**

### **Regex para Validação**
```javascript
// Workflow Name Validation
const workflowPattern = /^[a-z]+(-[a-zA-Z]+)+$/;

// Node Name Validation
const nodePattern = /^[A-Z][a-zA-Z\s-]+$/;

// Variable Validation
const globalVarPattern = /^[A-Z][A-Z0-9_]*$/;
const localVarPattern = /^[a-z][a-zA-Z0-9]*$/;
```

### **Linting Script**
```bash
#!/bin/bash
# validate-workflows.sh
# Valida nomenclatura em exports JSON

for file in workflows/*.json; do
    echo "Validating: $file"
    # Implementar validações regex
done
```

---

**📚 Próximo**: [⚡ Tratamento de Erros](./error_handling.md)