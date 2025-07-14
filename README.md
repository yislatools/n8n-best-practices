# n8n – Boas Práticas Enterprise

[![n8n version](https://img.shields.io/badge/n8n-1.100%2B-blue)](https://n8n.io)
[![Enterprise](https://img.shields.io/badge/Enterprise-Ready-green)](https://github.com/yislatools/n8n-best-practices)
[![Maintained](https://img.shields.io/badge/Maintained-YISLA-orange)](https://github.com/yislatools)

Repositório curado de padrões arquiteturais, naming, segurança e escalabilidade para workflows n8n em ambientes de produção Enterprise.

> **Mantido por**: YISLA  
> **Última revisão**: 2025-07-14  
> **Versão n8n**: 1.100.1+  

## 📋 **Índice**

### 🏗️ **Arquitetura & Padrões**
- [📝 Convenções de Nomenclatura](./naming_conventions.md)
- [⚡ Tratamento de Erros](./error_handling.md)
- [🔄 Versionamento & CI/CD](./versioning_ci_cd.md)

### 🔒 **Segurança & Escalabilidade**
- [🛡️ Hardening de Segurança](./security_hardening.md)
- [📊 Observabilidade & Scaling](./observability_scaling.md)

---

## 🎯 **Objetivos**

Este repositório fornece:

✅ **Padrões de nomenclatura** consistentes para workflows, nodes e variáveis  
✅ **Estratégias de error handling** robustas para ambientes críticos  
✅ **Pipelines CI/CD** automatizados para deploy seguro  
✅ **Configurações de segurança** para compliance empresarial  
✅ **Métricas e observabilidade** para operação em produção  

---

## 🚀 **Quick Start**

### **Infraestrutura Recomendada**
```yaml
VPS Specs:
  Memory: 4+ GB
  CPU: 2+ AMD vCPUs
  Disk: 80+ GB SSD
  OS: Ubuntu 22.04+

Stack:
  - n8n: 1.100.1+
  - Redis: 8.0.2+
  - PostgreSQL: 17.5+
  - Docker: Latest
```

### **Aplicação Rápida**
1. **Clone este repositório**
2. **Revise as convenções** em `naming_conventions.md`
3. **Implemente error handling** seguindo `error_handling.md`
4. **Configure CI/CD** conforme `versioning_ci_cd.md`
5. **Aplique hardening** usando `security_hardening.md`
6. **Monitore performance** com `observability_scaling.md`

---

## 📚 **Guias Detalhados**

### 📝 **[Convenções de Nomenclatura](./naming_conventions.md)**
Padrões uniformes para naming de workflows, nodes, variáveis e estrutura organizacional por domínio (CRM, Finance, Marketing, System).

**Principais tópicos:**
- Padrões de naming por tipo de elemento
- Organização hierárquica de workflows
- Templates de documentação
- Validação automatizada

### ⚡ **[Tratamento de Erros](./error_handling.md)**
Estratégias robustas para garantir alta disponibilidade e recuperação automática em ambientes críticos.

**Principais tópicos:**
- Retry logic com backoff exponencial
- Circuit breaker pattern
- Dead Letter Queue (DLQ)
- Saga pattern para transações distribuídas
- Templates de workflows resilientes

### 🔄 **[Versionamento & CI/CD](./versioning_ci_cd.md)**
Pipelines automatizados para deploy seguro e gestão de workflows em múltiplos ambientes.

**Principais tópicos:**
- Git Flow simplificado
- Scripts de export/import automatizados
- GitHub Actions workflows
- Blue-green deployment
- Quality gates e validação

### 🛡️ **[Hardening de Segurança](./security_hardening.md)**
Implementação de camadas robustas de segurança para proteger workflows Enterprise contra ameaças.

**Principais tópicos:**
- SAML/OIDC authentication
- Role-Based Access Control (RBAC)
- Encryption at rest e in transit
- Network security (Firewall, VPN, TLS)
- Compliance (SOC2, GDPR)
- Security monitoring

### 📊 **[Observabilidade & Scaling](./observability_scaling.md)**
Monitoramento completo, métricas de performance e estratégias de escalabilidade para alta disponibilidade.

**Principais tópicos:**
- Prometheus metrics customizados
- Grafana dashboards operacionais
- Alerting rules e SLA monitoring
- Horizontal scaling com queue mode
- Kubernetes deployment com HPA
- Health checks abrangentes

---

## 🛠️ **Ferramentas e Scripts**

### **Automação de Workflows**
- `export-workflows.js` - Export automático via n8n API
- `import-workflows.js` - Deploy automatizado de workflows
- `validate-workflows.js` - Validação estrutural e de naming

### **Monitoramento**
- `n8n-metrics-exporter.js` - Métricas customizadas para Prometheus
- `health-check.js` - Monitoramento de saúde multi-camada
- `sla-monitor.js` - Calculadora de SLA automatizada

### **Segurança**
- `security-audit.js` - Scripts de auditoria de segurança
- `credential-rotation.js` - Rotação automática de credenciais
- `compliance-checker.js` - Verificação de compliance

---

## 🏢 **Ambientes Enterprise**

### **Desenvolvimento**
- Workflows isolados por feature branch
- Validação automatizada no commit
- Sandbox environment para testes

### **Staging**
- Réplica do ambiente de produção
- Testes de integração automatizados
- Validação de performance

### **Produção**
- Alta disponibilidade com load balancing
- Monitoramento 24/7 com alertas
- Backup automatizado e disaster recovery

---

## 📈 **Métricas e KPIs**

### **Performance**
- Tempo de execução de workflows (P50, P95, P99)
- Taxa de throughput (execuções/minuto)
- Utilização de recursos (CPU, Memory, Queue)

### **Confiabilidade**
- Uptime (SLA 99.9%)
- Taxa de erro (< 1%)
- Tempo de recuperação (MTTR < 5min)

### **Segurança**
- Tentativas de login falhadas
- Acessos suspeitos detectados
- Compliance score (> 95%)

---

## 🤝 **Contribuições**

Contribuições são bem-vindas! Por favor:

1. **Fork** o repositório
2. **Crie uma branch** (`feature/nova-pratica`)
3. **Documente mudanças** seguindo os padrões existentes
4. **Teste** as implementações
5. **Envie um Pull Request**

### **Guidelines para Contribuição**
- Siga as convenções de nomenclatura estabelecidas
- Inclua documentação detalhada
- Adicione exemplos práticos
- Teste em ambiente Enterprise

---

## 🆘 **Suporte e Comunidade**

### **Documentação**
- [n8n Official Docs](https://docs.n8n.io/)
- [n8n Community](https://community.n8n.io/)
- [n8n GitHub](https://github.com/n8n-io/n8n)

### **Issues e Feedback**
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yislatools/n8n-best-practices/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/yislatools/n8n-best-practices/discussions)
- 📧 **Suporte Direto**: [yislatools.ai@gmail.com](mailto:yislatools.ai@gmail.com)

---

## 📄 **Licença**

Este projeto está licenciado sob a [MIT License](LICENSE) - veja o arquivo LICENSE para detalhes.

---

## 🏆 **Reconhecimentos**

### **Baseado em**
- Experiência real de implementações Enterprise
- Best practices da comunidade n8n
- Padrões de DevOps e SRE
- Frameworks de segurança corporativa

### **Agradecimentos**
- Comunidade n8n pelo suporte contínuo
- Equipe YISLA pelos insights técnicos
- Colaboradores que testaram em produção

---

## 🔮 **Roadmap**

### **Q3 2025**
- [ ] Templates de workflows por vertical (E-commerce, SaaS, Healthcare)
- [ ] Integração com mais ferramentas de monitoring
- [ ] Guides de migração para n8n Cloud

### **Q4 2025**
- [ ] Automation testing frameworks
- [ ] Performance benchmarking tools
- [ ] Multi-cloud deployment guides

---

**⭐ Se este repositório foi útil, considere dar uma estrela!**

---

> **Mantido com ❤️ por [YISLA](https://github.com/yislatools) | Última atualização: 2025-07-14**