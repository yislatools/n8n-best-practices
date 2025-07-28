# 📚 n8n Best Practices - Índice Atualizado

> **Repositório:** Melhores práticas, configurações e soluções para n8n  
> **Mantido por:** yislatools  
> **Última atualização:** 28/07/2025

## 🆕 Adições Recentes

### 28/07/2025 - Solução Completa: HTTP Request Tools + API Omie
- ✅ **[Caso Prático Completo](casos-praticos/omie-api-http-request-tools.md)** - Resolução de erro de placeholders + integração Omie
- ✅ **[Configurações de Tools](configuracoes/tools/omie-api-tools.md)** - Tools funcionais testadas e validadas  
- ✅ **[Guia de Troubleshooting](troubleshooting/http-request-tools-ai-agents.md)** - Debug e resolução de problemas

**Highlights:**
- Migração de `{placeholder}` para `{{ $fromAI("campo") }}`
- Formatação correta de CNPJ para API Omie
- Observações estruturadas com emojis
- Fluxo empresa + contato automatizado
- Arquitetura simplificada vs complexa

---

## 📂 Estrutura do Repositório

### 📋 Casos Práticos
- **[Omie API + HTTP Request Tools](casos-praticos/omie-api-http-request-tools.md)** ⭐ *Novo*
  - Resolução completa de erros de placeholders
  - Integração CRM com validações
  - De arquitetura complexa para simples

### 🛠️ Configurações
#### Tools
- **[API Omie Tools](configuracoes/tools/omie-api-tools.md)** ⭐ *Novo*
  - cadastra_conta, consulta_conta, cadastra_contato
  - Configurações testadas em produção
  - Campos necessários e formatos

### 🚨 Troubleshooting  
- **[HTTP Request Tools + AI Agents](troubleshooting/http-request-tools-ai-agents.md)** ⭐ *Novo*
  - Problemas mais comuns e soluções
  - Debugging passo a passo
  - Métricas e alertas

### 📖 Guias e Tutoriais
- *[Área em desenvolvimento]*

### 🔧 Utilitários
- *[Área em desenvolvimento]*

### 📐 Arquiteturas
- *[Área em desenvolvimento]*

---

## 🎯 Por Categoria

### 🤖 AI Agents
- [Configuração com HTTP Request Tools](casos-praticos/omie-api-http-request-tools.md#configurações-funcionais)
- [Troubleshooting AI Agents](troubleshooting/http-request-tools-ai-agents.md)
- [Uso correto de placeholders](troubleshooting/http-request-tools-ai-agents.md#1-❌-placeholders-não-substituídos)

### 🌐 Integrações API
- [API Omie - Caso completo](casos-praticos/omie-api-http-request-tools.md)
- [Configurações Omie](configuracoes/tools/omie-api-tools.md)
- [Validação de CNPJ](casos-praticos/omie-api-http-request-tools.md#2-formatação-de-cnpj-para-api-omie)

### 🔧 HTTP Request Tools
- [Configuração correta de placeholders](troubleshooting/http-request-tools-ai-agents.md#1-❌-placeholders-não-substituídos)
- [Tools funcionais para Omie](configuracoes/tools/omie-api-tools.md)
- [Debugging de tools](troubleshooting/http-request-tools-ai-agents.md#🔧-debugging-passo-a-passo)

### 📝 Melhores Práticas
- [Simplicidade vs Complexidade](casos-praticos/omie-api-http-request-tools.md#4-simplicidade-sobre-complexidade)
- [Tratamento de erros](casos-praticos/omie-api-http-request-tools.md#3-tratamento-de-erros)
- [Sequência de cadastro](casos-praticos/omie-api-http-request-tools.md#2-sequência-de-cadastro)

---

## 🏷️ Tags Principais

### Por Tecnologia
- `#omie-api` - Integração com CRM Omie
- `#http-request-tool` - Tools de requisição HTTP
- `#ai-agents` - Agentes de IA
- `#placeholders` - Substituição de variáveis
- `#cnpj` - Validação e formatação

### Por Tipo
- `#caso-pratico` - Implementações reais
- `#configuracao` - Arquivos de configuração
- `#troubleshooting` - Resolução de problemas  
- `#debugging` - Técnicas de debug
- `#producao` - Soluções em produção

### Por Nível
- `#iniciante` - Conceitos básicos
- `#intermediario` - Implementações práticas
- `#avancado` - Arquiteturas complexas

---

## 📊 Estatísticas do Repositório

### Conteúdo Disponível
- **3 casos práticos** detalhados
- **1 conjunto** de configurações testadas
- **1 guia** completo de troubleshooting
- **100% focado** em soluções reais

### Casos de Uso Cobertos
- ✅ Integração CRM (Omie)
- ✅ Automação de cadastro
- ✅ AI Agents com tools
- ✅ Validação de dados
- ✅ Tratamento de erros

### Problemas Resolvidos
- ✅ Placeholders não substituídos
- ✅ Erros de validação CNPJ
- ✅ Tools que não retornam dados
- ✅ Sequência de execução
- ✅ Debugging complexo

---

## 🚀 Como Usar Este Repositório

### 1. **Precisa resolver um problema?**
- Comece pelo [Troubleshooting](troubleshooting/)
- Busque por sintomas similares
- Siga o checklist de debugging

### 2. **Quer implementar algo novo?**
- Veja os [Casos Práticos](casos-praticos/)
- Use as [Configurações](configuracoes/) como base
- Adapte para seu contexto

### 3. **Busca por referência rápida?**
- Use as tags para filtrar conteúdo
- Consulte configurações funcionais
- Copie exemplos testados

---

## 🤝 Contribuição

### Como Contribuir
1. **Relate problemas** encontrados
2. **Compartilhe soluções** que funcionaram
3. **Documente casos reais** de implementação
4. **Sugira melhorias** nas configurações

### Padrões de Documentação
- **Casos práticos:** Problema → Solução → Resultado
- **Configurações:** Exemplo funcional + comentários
- **Troubleshooting:** Sintoma → Diagnóstico → Correção

---

## 📞 Contato

- **Repositório:** [yislatools/n8n-best-practices](https://github.com/yislatools/n8n-best-practices)
- **Issues:** Para reportar problemas ou sugestões
- **Discussions:** Para dúvidas e discussões técnicas

---

## 📈 Roadmap

### Próximas Adições Planejadas
- [ ] Casos práticos com outras APIs brasileiras
- [ ] Configurações para automação de marketing
- [ ] Guias de performance e otimização
- [ ] Templates de workflows comuns
- [ ] Integrações com bancos de dados

### Em Desenvolvimento
- [ ] Seção de utilitários (validações, formatações)
- [ ] Arquiteturas de referência
- [ ] Guias de segurança
- [ ] Monitoramento e alertas

---

*Repositório mantido pela comunidade n8n brasileiro - Sempre em evolução! 🇧🇷*