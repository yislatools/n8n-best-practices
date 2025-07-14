# 🔄 Versionamento & CI/CD

> **Objetivo**: Implementar pipelines automatizados para versionamento, deploy e gestão de workflows n8n em múltiplos ambientes Enterprise.

---

## 🎯 **Estratégia de Branching**

### **Git Flow Simplificado**
```text
┌──────────────────────────────────────────────────┐
│                    main                         │ ← Produção
├──────────────────────────────────────────────────┤
│                  staging                        │ ← Homologação
├──────────────────────────────────────────────────┤
│                    dev                          │ ← Desenvolvimento
├──────────────────────────────────────────────────┤
│              feature/crm-sync                   │ ← Features
└──────────────────────────────────────────────────┘
```

### **Política de Branches**
- **`main`**: Código de produção, protegido, deploy automático
- **`staging`**: Testes de homologação, validação QA
- **`dev`**: Integração contínua, testes automatizados
- **`feature/*`**: Desenvolvimento de funcionalidades
- **`hotfix/*`**: Correções urgentes de produção

---

## 📦 **Estrutura de Repositório**

```text
n8n-workflows/
├── 📁 workflows/
│   ├── 📁 crm/
│   │   ├── crm-syncContacts.json
│   │   ├── crm-updateLeads.json
│   │   └── metadata.json
│   ├── 📁 finance/
│   │   ├── finance-processPayments.json
│   │   └── metadata.json
│   └── 📁 system/
│       └── system-healthCheck.json
├── 📁 credentials/
│   ├── dev.env
│   ├── staging.env
│   └── prod.env
├── 📁 scripts/
│   ├── export-workflows.js
│   ├── import-workflows.js
│   └── validate-workflows.js
├── 📁 .github/
│   └── 📁 workflows/
│       ├── deploy-dev.yml
│       ├── deploy-staging.yml
│       └── deploy-prod.yml
├── docker-compose.yml
└── README.md
```

---

## 🤖 **Scripts de Automação**

### **Export de Workflows (export-workflows.js)**
```javascript
#!/usr/bin/env node
const axios = require('axios');
const fs = require('fs');
const path = require('path');

class N8nExporter {
  constructor(baseUrl, email, password) {
    this.baseUrl = baseUrl;
    this.email = email;
    this.password = password;
    this.token = null;
  }

  async authenticate() {
    try {
      const response = await axios.post(`${this.baseUrl}/rest/login`, {
        email: this.email,
        password: this.password
      });
      this.token = response.data.data.token;
      console.log('✅ Authenticated successfully');
    } catch (error) {
      console.error('❌ Authentication failed:', error.message);
      process.exit(1);
    }
  }

  async exportWorkflows() {
    if (!this.token) await this.authenticate();
    
    try {
      const response = await axios.get(`${this.baseUrl}/rest/workflows`, {
        headers: { Authorization: `Bearer ${this.token}` }
      });
      
      const workflows = response.data.data;
      console.log(`📥 Found ${workflows.length} workflows`);
      
      for (const workflow of workflows) {
        await this.saveWorkflow(workflow);
      }
      
      console.log('✅ Export completed successfully');
    } catch (error) {
      console.error('❌ Export failed:', error.message);
      process.exit(1);
    }
  }

  async saveWorkflow(workflow) {
    const category = this.getWorkflowCategory(workflow.name);
    const dirPath = path.join(__dirname, '..', 'workflows', category);
    
    // Criar diretório se não existir
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
    }
    
    // Salvar workflow
    const filename = `${workflow.name}.json`;
    const filepath = path.join(dirPath, filename);
    
    const exportData = {
      name: workflow.name,
      nodes: workflow.nodes,
      connections: workflow.connections,
      active: workflow.active,
      settings: workflow.settings,
      tags: workflow.tags,
      updatedAt: new Date().toISOString(),
      version: this.getVersion(workflow)
    };
    
    fs.writeFileSync(filepath, JSON.stringify(exportData, null, 2));
    console.log(`💾 Saved: ${filename}`);
  }

  getWorkflowCategory(name) {
    if (name.startsWith('crm-')) return 'crm';
    if (name.startsWith('finance-')) return 'finance';
    if (name.startsWith('marketing-')) return 'marketing';
    if (name.startsWith('system-')) return 'system';
    return 'misc';
  }

  getVersion(workflow) {
    // Gerar versão baseada em hash do conteúdo
    const crypto = require('crypto');
    const content = JSON.stringify({
      nodes: workflow.nodes,
      connections: workflow.connections
    });
    return crypto.createHash('sha256').update(content).digest('hex').substring(0, 8);
  }
}

// Execução
if (require.main === module) {
  const exporter = new N8nExporter(
    process.env.N8N_BASE_URL,
    process.env.N8N_EMAIL,
    process.env.N8N_PASSWORD
  );
  
  exporter.exportWorkflows().catch(console.error);
}

module.exports = N8nExporter;
```

### **Import de Workflows (import-workflows.js)**
```javascript
#!/usr/bin/env node
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const glob = require('glob');

class N8nImporter {
  constructor(baseUrl, email, password) {
    this.baseUrl = baseUrl;
    this.email = email;
    this.password = password;
    this.token = null;
  }

  async authenticate() {
    try {
      const response = await axios.post(`${this.baseUrl}/rest/login`, {
        email: this.email,
        password: this.password
      });
      this.token = response.data.data.token;
      console.log('✅ Authenticated successfully');
    } catch (error) {
      console.error('❌ Authentication failed:', error.message);
      process.exit(1);
    }
  }

  async importWorkflows() {
    if (!this.token) await this.authenticate();
    
    const workflowFiles = glob.sync('./workflows/**/*.json');
    console.log(`📤 Found ${workflowFiles.length} workflow files`);
    
    for (const filepath of workflowFiles) {
      await this.importWorkflow(filepath);
    }
    
    console.log('✅ Import completed successfully');
  }

  async importWorkflow(filepath) {
    try {
      const workflowData = JSON.parse(fs.readFileSync(filepath, 'utf8'));
      
      // Verificar se workflow já existe
      const existingWorkflow = await this.getWorkflowByName(workflowData.name);
      
      if (existingWorkflow) {
        await this.updateWorkflow(existingWorkflow.id, workflowData);
        console.log(`🔄 Updated: ${workflowData.name}`);
      } else {
        await this.createWorkflow(workflowData);
        console.log(`✨ Created: ${workflowData.name}`);
      }
    } catch (error) {
      console.error(`❌ Failed to import ${filepath}:`, error.message);
    }
  }

  async getWorkflowByName(name) {
    try {
      const response = await axios.get(`${this.baseUrl}/rest/workflows`, {
        headers: { Authorization: `Bearer ${this.token}` }
      });
      
      return response.data.data.find(w => w.name === name);
    } catch (error) {
      console.error('Error fetching workflows:', error.message);
      return null;
    }
  }

  async createWorkflow(workflowData) {
    await axios.post(`${this.baseUrl}/rest/workflows`, workflowData, {
      headers: { Authorization: `Bearer ${this.token}` }
    });
  }

  async updateWorkflow(id, workflowData) {
    await axios.put(`${this.baseUrl}/rest/workflows/${id}`, workflowData, {
      headers: { Authorization: `Bearer ${this.token}` }
    });
  }
}

// Execução
if (require.main === module) {
  const importer = new N8nImporter(
    process.env.N8N_BASE_URL,
    process.env.N8N_EMAIL,
    process.env.N8N_PASSWORD
  );
  
  importer.importWorkflows().catch(console.error);
}

module.exports = N8nImporter;
```

---

## 🚀 **GitHub Actions Workflows**

### **Deploy Development (.github/workflows/deploy-dev.yml)**
```yaml
name: Deploy to Development

on:
  push:
    branches: [ dev ]
  pull_request:
    branches: [ dev ]

env:
  NODE_VERSION: '18'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Validate workflows
        run: node scripts/validate-workflows.js

      - name: Lint JSON files
        run: |
          find workflows -name '*.json' -exec node -c {} \;

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/dev'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Deploy to Development
        env:
          N8N_BASE_URL: ${{ secrets.N8N_DEV_BASE_URL }}
          N8N_EMAIL: ${{ secrets.N8N_DEV_EMAIL }}
          N8N_PASSWORD: ${{ secrets.N8N_DEV_PASSWORD }}
        run: |
          node scripts/import-workflows.js

      - name: Run smoke tests
        env:
          N8N_BASE_URL: ${{ secrets.N8N_DEV_BASE_URL }}
        run: |
          node scripts/smoke-tests.js

      - name: Notify Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          channel: '#n8n-deployments'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### **Deploy Production (.github/workflows/deploy-prod.yml)**
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

env:
  NODE_VERSION: '18'

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Create full backup
        env:
          N8N_BASE_URL: ${{ secrets.N8N_PROD_BASE_URL }}
          N8N_EMAIL: ${{ secrets.N8N_PROD_EMAIL }}
          N8N_PASSWORD: ${{ secrets.N8N_PROD_PASSWORD }}
        run: |
          mkdir -p backups/prod/$(date +%Y%m%d-%H%M%S)
          node scripts/export-workflows.js
          tar -czf backups/prod-backup-$(date +%Y%m%d-%H%M%S).tar.gz backups/prod/$(date +%Y%m%d-%H%M%S)/

      - name: Deploy to Production
        env:
          N8N_BASE_URL: ${{ secrets.N8N_PROD_BASE_URL }}
          N8N_EMAIL: ${{ secrets.N8N_PROD_EMAIL }}
          N8N_PASSWORD: ${{ secrets.N8N_PROD_PASSWORD }}
        run: |
          node scripts/import-workflows.js

      - name: Health check
        env:
          N8N_BASE_URL: ${{ secrets.N8N_PROD_BASE_URL }}
        run: |
          node scripts/health-check.js

      - name: Create GitHub Release
        if: startsWith(github.ref, 'refs/tags/v')
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false
```

---

## 🔍 **Scripts de Validação**

### **Validation Script (validate-workflows.js)**
```javascript
#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const glob = require('glob');

class WorkflowValidator {
  constructor() {
    this.errors = [];
    this.warnings = [];
  }

  validate() {
    console.log('🔍 Starting workflow validation...');
    
    const workflowFiles = glob.sync('./workflows/**/*.json');
    
    for (const filepath of workflowFiles) {
      this.validateWorkflow(filepath);
    }
    
    this.printResults();
    
    if (this.errors.length > 0) {
      process.exit(1);
    }
  }

  validateWorkflow(filepath) {
    try {
      const content = fs.readFileSync(filepath, 'utf8');
      const workflow = JSON.parse(content);
      
      this.validateStructure(workflow, filepath);
      this.validateNaming(workflow, filepath);
      this.validateNodes(workflow, filepath);
      this.validateConnections(workflow, filepath);
      
    } catch (error) {
      this.errors.push(`${filepath}: Invalid JSON - ${error.message}`);
    }
  }

  validateStructure(workflow, filepath) {
    const requiredFields = ['name', 'nodes', 'connections'];
    
    for (const field of requiredFields) {
      if (!workflow[field]) {
        this.errors.push(`${filepath}: Missing required field '${field}'`);
      }
    }
  }

  validateNaming(workflow, filepath) {
    // Validar nome do workflow
    const namePattern = /^[a-z]+(-[a-zA-Z]+)+$/;
    if (!namePattern.test(workflow.name)) {
      this.errors.push(`${filepath}: Workflow name '${workflow.name}' doesn't follow naming convention`);
    }
    
    // Validar nome do arquivo
    const expectedFilename = `${workflow.name}.json`;
    const actualFilename = path.basename(filepath);
    if (expectedFilename !== actualFilename) {
      this.errors.push(`${filepath}: Filename should be '${expectedFilename}'`);
    }
  }

  validateNodes(workflow, filepath) {
    if (!Array.isArray(workflow.nodes)) {
      this.errors.push(`${filepath}: 'nodes' must be an array`);
      return;
    }

    const nodeIds = new Set();
    
    for (const node of workflow.nodes) {
      // Verificar campos obrigatórios
      if (!node.id || !node.name || !node.type) {
        this.errors.push(`${filepath}: Node missing required fields (id, name, type)`);
        continue;
      }
      
      // Verificar IDs únicos
      if (nodeIds.has(node.id)) {
        this.errors.push(`${filepath}: Duplicate node ID '${node.id}'`);
      }
      nodeIds.add(node.id);
      
      // Validar nome do node
      if (node.name.trim() !== node.name || node.name.length === 0) {
        this.warnings.push(`${filepath}: Node '${node.id}' has empty or whitespace name`);
      }
    }
  }

  validateConnections(workflow, filepath) {
    if (typeof workflow.connections !== 'object') {
      this.errors.push(`${filepath}: 'connections' must be an object`);
      return;
    }

    const nodeIds = new Set(workflow.nodes.map(n => n.id));
    
    for (const [sourceId, outputs] of Object.entries(workflow.connections)) {
      if (!nodeIds.has(sourceId)) {
        this.errors.push(`${filepath}: Connection references non-existent source node '${sourceId}'`);
      }
      
      if (typeof outputs !== 'object') continue;
      
      for (const [outputIndex, connections] of Object.entries(outputs)) {
        if (!Array.isArray(connections)) continue;
        
        for (const connection of connections) {
          if (!connection.node || !nodeIds.has(connection.node)) {
            this.errors.push(`${filepath}: Connection references non-existent target node '${connection.node}'`);
          }
        }
      }
    }
  }

  printResults() {
    console.log('\n📊 Validation Results:');
    console.log(`✅ Errors: ${this.errors.length}`);
    console.log(`⚠️  Warnings: ${this.warnings.length}`);
    
    if (this.errors.length > 0) {
      console.log('\n❌ Errors:');
      this.errors.forEach(error => console.log(`  ${error}`));
    }
    
    if (this.warnings.length > 0) {
      console.log('\n⚠️  Warnings:');
      this.warnings.forEach(warning => console.log(`  ${warning}`));
    }
    
    if (this.errors.length === 0 && this.warnings.length === 0) {
      console.log('\n🎉 All workflows are valid!');
    }
  }
}

// Execução
if (require.main === module) {
  const validator = new WorkflowValidator();
  validator.validate();
}

module.exports = WorkflowValidator;
```

---

## ✅ **Checklist de CI/CD**

### **Repository Setup**
- [ ] Estrutura de diretórios criada
- [ ] Scripts de export/import implementados
- [ ] Scripts de validação configurados
- [ ] GitHub Actions workflows criados
- [ ] Secrets configurados no GitHub

### **Environment Configuration**
- [ ] Ambientes dev/staging/prod configurados
- [ ] Credenciais separadas por ambiente
- [ ] Backup automático implementado
- [ ] Health checks configurados
- [ ] Alertas de deploy configurados

### **Quality Gates**
- [ ] Validação de JSON implementada
- [ ] Testes de smoke criados
- [ ] Code review obrigatório
- [ ] Proteção de branch main ativada

---

**📚 Próximo**: [🛡️ Hardening de Segurança](./security_hardening.md)