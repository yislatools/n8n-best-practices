# ⚡ Tratamento de Erros

> **Objetivo**: Implementar estratégias robustas de error handling para garantir alta disponibilidade e recuperação automática em workflows n8n Enterprise.

---

## 🎯 **Princípios de Error Handling**

✅ **Fail Fast**: Detectar e reportar erros rapidamente  
✅ **Graceful Degradation**: Manter funcionalidades essenciais mesmo com falhas parciais  
✅ **Retry Logic**: Tentar novamente operações que podem ser temporárias  
✅ **Dead Letter Queue**: Preservar dados que falharam para análise posterior  
✅ **Observabilidade**: Logging detalhado para debugging  

---

## 🔄 **Estratégias de Retry**

### **1. Retry Incremental com Backoff**
```javascript
// Node: Set - Configure Retry Logic
{
  "retryCount": 0,
  "maxRetries": 5,
  "baseDelay": 1000, // 1 segundo
  "backoffMultiplier": 2,
  "currentDelay": "{{ $json.baseDelay * Math.pow($json.backoffMultiplier, $json.retryCount) }}"
}

// Node: IF - Check Retry Condition
{{ $json.retryCount < $json.maxRetries }}

// Node: Wait - Dynamic Delay
{{ $json.currentDelay }}

// Node: Set - Increment Counter
{
  "retryCount": "{{ $json.retryCount + 1 }}",
  "lastError": "{{ $json.error?.message || 'Unknown error' }}",
  "timestamp": "{{ new Date().toISOString() }}"
}
```

### **2. Circuit Breaker Pattern**
```javascript
// Global Variable: CIRCUIT_BREAKER_STATE
{
  "salesforce_api": {
    "state": "CLOSED", // CLOSED, OPEN, HALF_OPEN
    "failureCount": 0,
    "failureThreshold": 5,
    "timeout": 30000, // 30 segundos
    "lastFailureTime": null
  }
}

// Node: IF - Check Circuit State
{{
  const circuitState = $vars.CIRCUIT_BREAKER_STATE.salesforce_api;
  
  if (circuitState.state === 'OPEN') {
    const timeSinceFailure = Date.now() - circuitState.lastFailureTime;
    if (timeSinceFailure > circuitState.timeout) {
      circuitState.state = 'HALF_OPEN';
      return true; // Try request
    }
    return false; // Skip request
  }
  
  return true; // CLOSED or HALF_OPEN
}}
```

---

## 🏗️ **Padrões Arquiteturais**

### **1. Try/Catch Sub-Workflow**
```yaml
Main Workflow:
  - Node: "Execute Workflow - Process Data"
    Settings:
      Workflow: "sub_processDataSafely"
      Error Handling: "Continue on Error"
  
  - Node: "IF - Check Execution Success"
    Expression: "{{ $json.success === true }}"
  
  - Node: "Set - Log Success" (True branch)
  
  - Node: "Execute Workflow - Handle Error" (False branch)
    Settings:
      Workflow: "sub_handleProcessingError"

Sub-Workflow (sub_processDataSafely):
  - Try: Process data normally
  - Catch: Return { "success": false, "error": error_details }
```

### **2. Saga Pattern para Transações Distribuídas**
```javascript
// Node: Set - Define Saga Steps
{
  "sagaId": "{{ $json.transactionId }}",
  "steps": [
    {
      "action": "createOrder",
      "compensate": "cancelOrder",
      "status": "pending"
    },
    {
      "action": "reserveInventory",
      "compensate": "releaseInventory",
      "status": "pending"
    },
    {
      "action": "processPayment",
      "compensate": "refundPayment",
      "status": "pending"
    }
  ],
  "currentStep": 0,
  "rollbackRequired": false
}

// Compensation Logic
// Node: Function - Execute Compensation
const saga = $json;
for (let i = saga.currentStep - 1; i >= 0; i--) {
  const step = saga.steps[i];
  if (step.status === 'completed') {
    // Execute compensation action
    await executeCompensation(step.compensate, step.data);
    step.status = 'compensated';
  }
}
```

---

## 📮 **Dead Letter Queue (DLQ)**

### **Estrutura da Tabela DLQ**
```sql
CREATE TABLE failed_jobs (
    id SERIAL PRIMARY KEY,
    workflow_id VARCHAR(255) NOT NULL,
    execution_id VARCHAR(255) NOT NULL,
    node_name VARCHAR(255) NOT NULL,
    error_message TEXT NOT NULL,
    error_stack TEXT,
    input_data JSONB NOT NULL,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    next_retry_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'failed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_failed_jobs_status ON failed_jobs(status);
CREATE INDEX idx_failed_jobs_next_retry ON failed_jobs(next_retry_at);
```

### **Node: Postgres - Insert Failed Job**
```sql
INSERT INTO failed_jobs (
    workflow_id,
    execution_id,
    node_name,
    error_message,
    error_stack,
    input_data,
    retry_count,
    max_retries,
    next_retry_at
) VALUES (
    '{{ $json.workflowId }}',
    '{{ $json.executionId }}',
    '{{ $json.nodeName }}',
    '{{ $json.error.message }}',
    '{{ $json.error.stack }}',
    '{{ JSON.stringify($json.inputData) }}',
    {{ $json.retryCount || 0 }},
    {{ $json.maxRetries || 3 }},
    NOW() + INTERVAL '{{ $json.retryDelayMinutes || 5 }} minutes'
);
```

---

## 📊 **Monitoring e Alertas**

### **Estrutura de Logs**
```javascript
// Node: Set - Structured Error Log
{
  "timestamp": "{{ new Date().toISOString() }}",
  "level": "ERROR",
  "workflowId": "{{ $workflow.id }}",
  "executionId": "{{ $execution.id }}",
  "nodeName": "{{ $node.name }}",
  "errorType": "{{ $json.error?.name || 'UnknownError' }}",
  "errorMessage": "{{ $json.error?.message }}",
  "errorCode": "{{ $json.error?.code }}",
  "httpStatus": "{{ $json.error?.response?.status }}",
  "inputData": "{{ JSON.stringify($input.all()) }}",
  "context": {
    "userId": "{{ $json.userId }}",
    "sessionId": "{{ $json.sessionId }}",
    "environment": "{{ $vars.ENVIRONMENT }}"
  },
  "stack": "{{ $json.error?.stack }}"
}
```

### **Alertas Slack/Teams**
```javascript
// Node: Set - Prepare Alert Payload
{
  "text": "🚨 n8n Workflow Error",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🚨 Workflow Execution Failed"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Workflow:* {{ $json.workflowName }}"
        },
        {
          "type": "mrkdwn",
          "text": "*Error:* {{ $json.error.message }}"
        },
        {
          "type": "mrkdwn",
          "text": "*Time:* {{ new Date().toLocaleString() }}"
        },
        {
          "type": "mrkdwn",
          "text": "*Execution ID:* {{ $execution.id }}"
        }
      ]
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "View Execution"
          },
          "url": "{{ $vars.N8N_BASE_URL }}/workflow/{{ $workflow.id }}/executions/{{ $execution.id }}"
        }
      ]
    }
  ]
}
```

---

## 🔧 **Templates de Error Handling**

### **Template 1: API Call com Retry**
```yaml
Workflow: "template_apiCallWithRetry"
Nodes:
  1. "Set - Initialize Retry State"
  2. "HTTP Request - API Call"
     Continue on Error: true
  3. "IF - Check Success"
     True: "Set - Success Response"
     False: "IF - Check Retry Limit"
       True: "Wait - Retry Delay" → "Set - Increment Counter" → (loop back to HTTP)
       False: "Set - Final Failure" → "Postgres - Log to DLQ"
```

### **Template 2: Database Transaction**
```yaml
Workflow: "template_databaseTransaction"
Nodes:
  1. "Postgres - BEGIN TRANSACTION"
  2. "Postgres - Insert Record A"
     On Error: "Postgres - ROLLBACK" → "Set - Log Error"
  3. "Postgres - Insert Record B"
     On Error: "Postgres - ROLLBACK" → "Set - Log Error"
  4. "Postgres - COMMIT TRANSACTION"
  5. "Set - Success Response"
```

---

## 📈 **Métricas de Error Handling**

### **KPIs Essenciais**
```sql
-- Error Rate por Workflow
SELECT 
    workflow_id,
    COUNT(*) as total_errors,
    COUNT(*) / (SELECT COUNT(*) FROM executions WHERE workflow_id = failed_jobs.workflow_id) * 100 as error_rate
FROM failed_jobs 
WHERE created_at >= NOW() - INTERVAL '24 hours'
GROUP BY workflow_id
ORDER BY error_rate DESC;

-- Recovery Rate
SELECT 
    DATE(created_at) as date,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed,
    COUNT(CASE WHEN status = 'recovered' THEN 1 END) as recovered,
    COUNT(CASE WHEN status = 'recovered' THEN 1 END) * 100.0 / COUNT(*) as recovery_rate
FROM failed_jobs
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

---

## ✅ **Checklist de Implementação**

### **Workflow Level**
- [ ] Error handling configurado em todos os nodes críticos
- [ ] Retry logic implementado onde apropriado
- [ ] Dead letter queue configurado
- [ ] Logs estruturados adicionados
- [ ] Alertas configurados para falhas críticas

### **Infrastructure Level**
- [ ] Tabela `failed_jobs` criada
- [ ] Workflow de retry automático implementado
- [ ] Dashboard de monitoramento configurado
- [ ] Alertas Slack/Teams testados
- [ ] Métricas de error rate coletadas

---

**📚 Próximo**: [🔄 Versionamento & CI/CD](./versioning_ci_cd.md)