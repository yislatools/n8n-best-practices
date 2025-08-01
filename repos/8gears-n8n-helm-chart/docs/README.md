# ☸️ N8N Helm Chart - Production Kubernetes Deployment

## 📊 METADADOS DO REPOSITÓRIO

**Repositório**: `8gears/n8n-helm-chart`  
**Status**: **PRODUCTION-READY DEPLOYMENT** - Kubernetes Enterprise  
**Chart Version**: **1.0.0** (Breaking Changes - Não backward compatible)  
**App Version**: N8N Latest Compatible  
**Maintainer**: 8gears + Community Contributors  
**Categoria**: L3_INFRASTRUCTURE (Peso Neural: 0.75)  

## 🚀 VISÃO GERAL

Helm chart maduro e confiável para deploy de N8N em Kubernetes, com suporte a scaling, alta disponibilidade, e configurações enterprise. Usado em produção por centenas de organizações mundialmente.

### **⚠️ AVISO IMPORTANTE - VERSÃO 1.0.0**
- **Breaking Changes** incluídos e não é backward compatible
- **Migração necessária** de versões anteriores
- **Revisão obrigatória** do migration guide antes de atualizar

### **REQUISITOS TÉCNICOS**
- **Helm**: >= 3.8
- **Kubernetes**: Versão suportada
- **Database**: PostgreSQL externo OU SQLite embarcado
- **Helmfile**: Opcional para gestão avançada

## 🏗️ ARQUITETURA DE COMPONENTES

### **ESTRUTURA MODULAR (5 SEÇÕES)**

**1. Global e Chart Values**
- Repository da imagem, tag, configurações globais
- Configurações que afetam todos os componentes

**2. Ingress Configuration**  
- Default: nginx (customizável para outros controllers)
- SSL/TLS, domínios, annotations customizadas

**3. Main N8N Application**
- Configuração principal + settings Kubernetes específicos
- Persistência, recursos, security contexts

**4. Worker Related Settings**
- Configurações para workers + Kubernetes específicos  
- Queue-mode para processamento distribuído

**5. Webhook Processing**
- Settings para webhook processing + Kubernetes específicos
- Separação de workloads para alta performance

## ⚙️ CONFIGURAÇÃO AVANÇADA

### **SISTEMA DE CONFIGURAÇÃO INTELIGENTE**

**Transformação Automática YAML → ENV:**
```yaml
main:
  config:
      n8n:
        encryption_key: "my_secret" # ==> N8N_ENCRYPTION_KEY=my_secret
      db:
        type: postgresdb # ==> DB_TYPE=postgresdb
        postgresdb:
          host: 192.168.0.52 # ==> DB_POSTGRESDB_HOST=192.168.0.52
      node:
        function_allow_builtin: "*" # ==> NODE_FUNCTION_ALLOW_BUILTIN="*"
```

**Flexibilidade Config vs Secret:**
- **config**: Variáveis não-sensíveis (ConfigMap)
- **secret**: Dados sensíveis (Secret)
- **Mistura livre** conforme necessidade de segurança

### **EXEMPLO CONFIGURAÇÃO TÍPICA**
```yaml
# Deployment pequeno com nodeport para testes locais
main:
  config:
    n8n:
      hide_usage_page: true
  secret:
    n8n:
      encryption_key: "<your-secure-encryption-key>"
  resources:
    limits:
      memory: 2048Mi
    requests:
      memory: 512Mi
  service:
    type: NodePort
    port: 5678
```

## 🚀 SCALING E ALTA DISPONIBILIDADE

### **QUEUE-MODE ENTERPRISE**

N8N oferece **queue-mode** onde workload é compartilhado entre múltiplas instâncias:
- **Shared load** sobre múltiplas instâncias
- **Alta disponibilidade limitada** (controller como SPOF)
- **Redis/Valkey** para coordenação de tarefas
- **BullMQ** para gerenciamento de filas

**Ativação Simples:**
```yaml
scaling:
  enabled: true
  worker:
    replicaCount: 3  # Múltiplos workers
```

**Redis Externo:**
```yaml
scaling:
  enabled: true
  redis:
    host: "redis-hostname"
    password: "redis-password-if-set"
```

**Webhook Dedicado:**
```yaml
scaling:
  webhook:
    enabled: true  # Instâncias dedicadas para webhooks
```

### **CONFIGURAÇÕES DE SCALING**

**Main Application:**
- **replicaCount**: Número de pods desejados
- **autoscaling**: HPA com CPU/Memory targets
- **resources**: Limites e requests configuráveis

**Worker Configuration:**
- **concurrency**: Jobs paralelos por worker (default: 10)
- **replicaCount**: Número de workers
- **deploymentStrategy**: Recreate ou RollingUpdate

**Webhook Processing:**
- **Separação de workload** para alta performance
- **Dedicated resources** para processamento webhook
- **Independent scaling** do main application

## 🔒 SEGURANÇA E HARDENING

### **SECURITY CONTEXTS**
```yaml
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000

securityContext:
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000
```

### **SERVICE ACCOUNTS**
- **Criação automática** de service accounts
- **Annotations customizáveis** para cloud integrations
- **RBAC compliance** com minimal permissions

### **SECRETS MANAGEMENT**
- **Kubernetes Secrets** para dados sensíveis
- **External secret management** suportado
- **Encryption keys** e database passwords protegidos

## 💾 PERSISTÊNCIA E STORAGE

### **OPÇÕES DE STORAGE**
```yaml
persistence:
  enabled: true
  type: dynamic  # dynamic, existing, emptyDir
  storageClass: "fast-ssd"  # ou "-" para default
  accessModes:
    - ReadWriteOnce
  size: 10Gi
  # existingClaim: my-pvc  # Para PVC existente
```

**Tipos Suportados:**
- **dynamic**: Dynamic Volume Provisioning
- **existing**: Usar PVC existente
- **emptyDir**: Storage temporário (não persistente)

### **BACKUP E RECOVERY**
- **PVC annotations** para políticas de backup
- **Volume snapshots** suportados
- **Cross-AZ replication** configurável

## 🌐 NETWORKING E INGRESS

### **INGRESS CONFIGURATION**
```yaml
ingress:
  enabled: true
  className: "nginx"  # ou traefik, etc.
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - host: n8n.company.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - hosts:
        - n8n.company.com
      secretName: n8n-tls-cert
```

### **SERVICE TYPES**
- **ClusterIP**: Acesso interno cluster
- **NodePort**: Acesso via porta específica
- **LoadBalancer**: Cloud load balancer
- **ExternalName**: Redirecionamento externo

## 🔧 CUSTOMIZAÇÕES AVANÇADAS

### **LIFECYCLE HOOKS**
```yaml
lifecycle:
  postStart:
    exec:
      command: ["/bin/sh", "-c", "apk add mysql-client"]
```

### **INIT CONTAINERS**
```yaml
initContainers:
  - name: init-data-dir
    image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
    command: ["/bin/sh", "-c", "mkdir -p /home/node/.n8n/"]
    volumeMounts:
      - name: data
        mountPath: /home/node/.n8n
```

### **EXTRA VOLUMES & MOUNTS**
```yaml
extraVolumes:
  - name: db-ca-cert
    secret:
      secretName: db-ca
      items:
        - key: ca.crt
          path: ca.crt

extraVolumeMounts:
  - name: db-ca-cert
    mountPath: /etc/ssl/certs/postgresql
    readOnly: true
```

## 🔍 MONITORING E OBSERVABILITY

### **HEALTH CHECKS**
```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /healthz
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10
```

### **METRICS E MONITORING**
- **Prometheus metrics** endpoints expostos
- **ServiceMonitor** CRDs suportados
- **Grafana dashboards** disponíveis
- **Alerting rules** pré-configuradas

## 📦 DEPLOYMENT STRATEGIES

### **ROLLING UPDATE**
```yaml
deploymentStrategy:
  type: RollingUpdate
  maxSurge: "50%"
  maxUnavailable: "50%"
```

### **RECREATE STRATEGY**
```yaml
deploymentStrategy:
  type: "Recreate"  # Para stateful applications
```

### **BLUE-GREEN DEPLOYMENT**
- **Suporte via Argo Rollouts**
- **Traffic splitting** configurável
- **Automated rollback** em caso de falha

## 🚀 INSTALAÇÃO E DEPLOYMENT

### **INSTALAÇÃO RÁPIDA**
```bash
# Via OCI Registry (Recomendado)
helm install my-n8n oci://8gears.container-registry.com/library/n8n --version 1.0.0

# Via Repository tradicional
helm repo add 8gears https://8gears.container-registry.com/library/
helm install my-n8n 8gears/n8n
```

### **CONFIGURAÇÃO CUSTOMIZADA**
```bash
# Com values file personalizado
helm install my-n8n 8gears/n8n -f my-values.yaml

# Com overrides inline
helm install my-n8n 8gears/n8n \
  --set main.config.n8n.encryption_key="my-key" \
  --set ingress.enabled=true
```

### **UPGRADE E MIGRAÇÃO**
```bash
# Backup antes do upgrade
kubectl create backup n8n-backup --from=my-n8n

# Upgrade para nova versão
helm upgrade my-n8n 8gears/n8n --version 1.0.0

# Rollback se necessário
helm rollback my-n8n 1
```

## 📊 CONFIGURAÇÕES DE EXEMPLO

### **DEVELOPMENT ENVIRONMENT**
```yaml
main:
  replicaCount: 1
  resources:
    limits:
      memory: 1Gi
    requests:
      memory: 512Mi
  service:
    type: NodePort
  persistence:
    enabled: false
    type: emptyDir
```

### **PRODUCTION ENVIRONMENT**
```yaml
main:
  replicaCount: 2
  resources:
    limits:
      cpu: 2000m
      memory: 4Gi
    requests:
      cpu: 1000m
      memory: 2Gi
  
scaling:
  enabled: true
  worker:
    replicaCount: 3
    concurrency: 15

ingress:
  enabled: true
  className: "nginx"
  tls:
    - hosts:
        - n8n.company.com
      secretName: n8n-tls

valkey:
  enabled: true
  architecture: standalone
```

### **HIGH AVAILABILITY SETUP**
```yaml
main:
  replicaCount: 3
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

scaling:
  enabled: true
  worker:
    replicaCount: 5
    autoscaling:
      enabled: true
      minReplicas: 3
      maxReplicas: 20
  
  webhook:
    enabled: true
    replicaCount: 2

valkey:
  enabled: true
  architecture: replication
  replica:
    replicaCount: 2
```

## 🎯 CASOS DE USO ESTRATÉGICOS

### **ENTERPRISE DEPLOYMENT**
- **Multi-tenant** com namespace isolation
- **RBAC integration** com Active Directory
- **Resource quotas** por department
- **Network policies** para security compliance

### **CI/CD AUTOMATION**
- **GitOps** com ArgoCD/Flux
- **Automated testing** de workflows
- **Blue-green deployments** para zero downtime
- **Canary releases** para rollouts seguros

### **DISASTER RECOVERY**
- **Multi-region deployments** para failover
- **Cross-cluster backups** automatizados
- **RTO/RPO compliance** para enterprise
- **Automated failover** com DNS switching

## 🔗 CONEXÕES NEURAIS

### **RELACIONAMENTOS IDENTIFICADOS**
- **Kubernetes Ecosystem** (integração nativa: 1.0)
- **Cloud Providers** (compatibilidade: 0.95)
- **CI/CD Tools** (GitOps ready: 0.90)
- **Monitoring Stack** (observability: 0.85)
- **Security Tools** (compliance: 0.80)

### **IMPACTO NO ECOSSISTEMA**
- **Production Standard** para N8N deployments
- **Enterprise Ready** com security hardening
- **Cloud Native** following Kubernetes best practices
- **Community Driven** com contribuições ativas

---

**🎯 CONCLUSÃO**: Helm chart **production-ready** que estabelece o **padrão de qualidade para deployments N8N enterprise**, oferecendo scaling, security e reliability necessários para ambientes críticos.