# ENTIDADE NEURAL: N8N Core Platform

## METADADOS NEURAIS

```yaml
Categoria: Core Platform Architecture
Tipo: Framework/Engine
Força_Sináptica: 1.0 (Critical Core)
Última_Atualização: 2025-08-01
Status: Active Development
```

## IDENTIFICAÇÃO TÉCNICA

```yaml
Repositório: n8n-io/n8n
URL: https://github.com/n8n-io/n8n
Versão_Atual: 1.105.0
Licença: Fair-code (Sustainable Use License)
Arquitetura: Monorepo TypeScript
Package_Manager: pnpm@10.12.1
Node_Requirements: ">=22.16"
```

## ARQUITETURA MODULAR

### **Core Packages Structure**
```yaml
Core_Engine:
  - packages/core: Engine de execução principal
  - packages/workflow: Definições e processamento de workflows
  - packages/cli: Interface linha de comando e server

Frontend_Stack:
  - packages/frontend: Interface web (Vue.js)
  - packages/@n8n/design-system: Sistema de design
  - packages/@n8n/codemirror-lang: Editor de código integrado

Node_System:
  - packages/nodes-base: Nodes oficiais base
  - packages/@n8n/nodes-langchain: Integração AI/LangChain
  - packages/node-dev: Ferramentas desenvolvimento de nodes

Infrastructure:
  - packages/@n8n/backend-common: Utilitários backend compartilhados
  - packages/@n8n/db: Abstração banco de dados
  - packages/@n8n/api-types: Tipagens API compartilhadas
  - packages/@n8n/config: Sistema de configuração

Developer_Tools:
  - packages/@n8n/create-node: CLI para criação de nodes
  - packages/@n8n/node-cli: Ferramentas de desenvolvimento
  - packages/@n8n/extension-sdk: SDK para extensões
  - packages/testing: Utilitários de teste

Enterprise_Features:
  - packages/@n8n/ai-workflow-builder.ee: Builder AI (Enterprise)
  - packages/@n8n/permissions: Sistema de permissões
  - packages/@n8n/task-runner: Executor de tarefas distribuído
```

## PADRÕES ARQUITETURAIS IDENTIFICADOS

### **1. Monorepo Pattern**
```typescript
// Estrutura hierárquica com workspaces
{
  "name": "n8n-monorepo",
  "private": true,
  "packageManager": "pnpm@10.12.1",
  "workspaces": ["packages/*", "packages/@n8n/*"]
}
```

### **2. Modular Plugin Architecture**
```yaml
Node_Registration:
  - Dynamic loading de nodes
  - TypeScript-first development
  - Credential separation patterns
  - Operation-based node design

Extension_Points:
  - Custom nodes via @n8n/create-node
  - Frontend extensions
  - Database connectors
  - Task runners distribuídos
```

### **3. TypeScript-First Development**
```yaml
Type_Safety:
  - Shared types via @n8n/api-types
  - Strict TypeScript configuration
  - Runtime type validation
  - Schema-to-Type generation (@n8n/json-schema-to-zod)
```

### **4. Fair-Code Licensing Model**
```yaml
License_Structure:
  - Core: Sustainable Use License (fair-code)
  - Enterprise: n8n Enterprise License
  - Community: Open source contributions
  - Self-Hosting: Permitido sem restrições
```

## TECNOLOGIAS E DEPENDÊNCIAS CORE

### **Backend Stack**
```yaml
Runtime: Node.js >=22.16
Language: TypeScript
Package_Manager: pnpm (workspaces)
Database: Multi-DB support (SQLite, PostgreSQL, MySQL)
Task_Queue: Bull (Redis-based)
API: Express.js based
WebSocket: Socket.io para real-time
```

### **Frontend Stack**
```yaml
Framework: Vue.js 3 + TypeScript
Build: Vite
State: Pinia
UI: Custom design system (@n8n/design-system)
Editor: CodeMirror 6 (@n8n/codemirror-lang)
Testing: Vitest + Playwright
```

### **Development Tools**
```yaml
Monorepo: Turbo (build orchestration)
Linting: Biome (@biomejs/biome)
Testing: Jest + Vitest + Playwright
Formatting: Biome formatter
Git_Hooks: Lefthook
Bundle_Analysis: Bundlemon
```

### **AI Integration**
```yaml
LangChain: @n8n/nodes-langchain
AI_Workflow_Builder: Enterprise feature
Vector_Stores: Múltiplos providers
LLM_Support: OpenAI, Anthropic, local models
```

## PADRÕES DE DESENVOLVIMENTO

### **1. Node Development Pattern**
```typescript
// Estrutura padrão de um node
export class ExampleNode implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Example Node',
    name: 'exampleNode',
    group: ['transform'],
    version: 1,
    properties: [...],
    credentials: [...]
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    // Lógica de execução
  }
}
```

### **2. Credential Management**
```yaml
Pattern: Separated credential definitions
Security: Encrypted storage
Reusability: Shared across multiple nodes
OAuth: Built-in OAuth2 flows (@n8n/client-oauth2)
```

### **3. Testing Patterns**
```yaml
Unit_Tests: Jest para lógica de negócio
Integration_Tests: Supertest para APIs
E2E_Tests: Playwright para workflow completo
Performance_Tests: @n8n/benchmark
```

### **4. Build & Deploy Patterns**
```yaml
Build_System: Turbo para orchestração
Docker: Multi-stage builds
Kubernetes: Helm charts disponíveis
Monitoring: Health checks integrados
```

## CONEXÕES NEURAIS MAPEADAS

### **Strong Dependencies (0.8-1.0)**
```yaml
Core_Workflows: n8n-core ↔ n8n-workflow (1.0)
Node_System: n8n-core ↔ nodes-base (1.0)
Database: n8n-core ↔ @n8n/db (0.9)
API_Types: backend ↔ @n8n/api-types (0.9)
Frontend_Backend: editor-ui ↔ cli (0.8)
```

### **Medium Dependencies (0.5-0.7)**
```yaml
AI_Integration: core ↔ nodes-langchain (0.7)
Extensions: core ↔ extension-sdk (0.6)
Development: core ↔ create-node (0.6)
Testing: core ↔ testing-utils (0.5)
```

### **Evolution Patterns**
```yaml
Version_Strategy: Semantic versioning
Release_Cycle: Regular releases
Breaking_Changes: Migration guides
Community_Input: RFC process para mudanças major
```

## INSIGHTS ESTRATÉGICOS

### **Forças Técnicas**
- **Arquitetura Modular**: Facilita desenvolvimento e manutenção
- **TypeScript-First**: Type safety e developer experience
- **Fair-Code**: Balança open source com sustentabilidade
- **AI-Ready**: Nativo para workflows de IA moderna
- **Enterprise Features**: Escalabilidade para uso corporativo

### **Padrões Emergentes**
- **Task Runners**: Execução distribuída
- **AI Workflow Builder**: Automação de criação de workflows
- **Extension SDK**: Ecosystem de terceiros
- **Multi-Database**: Flexibilidade de deploy

### **Oportunidades de Melhoria**
- **Performance**: Otimização de execução de workflows
- **Developer Experience**: Tooling para node development
- **Documentation**: Padrões de desenvolvimento
- **Testing**: Coverage e patterns padronizados

## RECOMENDAÇÕES TÉCNICAS

### **Para Node Developers**
1. **Seguir TypeScript-first**: Usar tipagens strictas
2. **Modular Design**: Separar lógica em funções pequenas
3. **Error Handling**: Implementar error handling robusto
4. **Testing**: Unit tests para toda lógica de negócio
5. **Documentation**: JSDoc para todas as funções públicas

### **Para Arquitetos**
1. **Plugin Architecture**: Leverage extension points
2. **Scalability**: Usar task runners para workloads pesados
3. **Security**: Implementar credential management apropriado
4. **Monitoring**: Health checks e observabilidade
5. **Database**: Escolher DB apropriado para scale

### **Para DevOps**
1. **Container-First**: Usar imagens Docker oficiais
2. **Environment Variables**: Configuração via env vars
3. **Secrets Management**: Não hardcodar credentials
4. **Backup Strategy**: Backup regular do banco de dados
5. **Monitoring**: Prometheus metrics disponíveis

---

**Última Análise**: 2025-08-01 23:30 UTC  
**Próxima Revisão**: Quando houver release major  
**Arquitetura**: Validada contra v1.105.0
