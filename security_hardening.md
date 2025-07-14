# 🛡️ Hardening de Segurança

> **Objetivo**: Implementar camadas robustas de segurança para proteger workflows n8n Enterprise contra ameaças e garantir compliance com padrões de segurança corporativa.

---

## 🎯 **Framework de Segurança**

### **Princípios Fundamentais**
✅ **Defense in Depth**: Múltiplas camadas de proteção  
✅ **Least Privilege**: Acesso mínimo necessário  
✅ **Zero Trust**: Verificação contínua de identidade  
✅ **Data Classification**: Proteção baseada em sensibilidade  
✅ **Audit Trail**: Rastreabilidade completa de ações  

### **Níveis de Segurança**
```text
┌─────────────────────────────────────────────────────┐
│                 COMPLIANCE                      │ ← SOC2, GDPR, ISO27001
├─────────────────────────────────────────────────────┤
│               APPLICATION                       │ ← n8n Configuration
├─────────────────────────────────────────────────────┤
│                 NETWORK                         │ ← Firewall, VPN, TLS
├─────────────────────────────────────────────────────┤
│                INFRASTRUCTURE                   │ ← OS, Docker, K8s
└─────────────────────────────────────────────────────┘
```

---

## 🔐 **Autenticação e Autorização**

### **SAML 2.0 / OIDC Configuration**
```yaml
# docker-compose.yml - n8n with SAML
version: '3.8'
services:
  n8n:
    image: n8nio/n8n:latest
    environment:
      # SAML Configuration
      N8N_SAML_ENABLED: 'true'
      N8N_SAML_METADATA_URL: 'https://your-idp.com/metadata'
      N8N_SAML_ENTITY_ID: 'n8n-production'
      N8N_SAML_RETURN_URL: 'https://n8n.yourdomain.com/rest/sso/saml'
      
      # Security Headers
      N8N_SECURITY_AUDIT_ENABLED: 'true'
      N8N_LOG_LEVEL: 'info'
      
      # Session Security
      N8N_SESSION_SECURE: 'true'
      N8N_SESSION_SAME_SITE: 'strict'
      N8N_SESSION_MAX_AGE: '3600' # 1 hour
      
      # CORS
      N8N_CORS_ORIGIN: 'https://yourdomain.com'
      
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - n8n_network
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
```

### **Role-Based Access Control (RBAC)**
```javascript
// User Roles Configuration
const roles = {
  "admin": {
    "permissions": [
      "workflow:create",
      "workflow:read", 
      "workflow:update",
      "workflow:delete",
      "workflow:execute",
      "credential:manage",
      "user:manage",
      "audit:view"
    ]
  },
  "developer": {
    "permissions": [
      "workflow:create",
      "workflow:read",
      "workflow:update", 
      "workflow:execute",
      "credential:use"
    ]
  },
  "operator": {
    "permissions": [
      "workflow:read",
      "workflow:execute",
      "credential:use"
    ]
  },
  "viewer": {
    "permissions": [
      "workflow:read",
      "execution:view"
    ]
  }
};

// Permission Check Middleware
function checkPermission(required_permission) {
  return (req, res, next) => {
    const userRole = req.user.role;
    const userPermissions = roles[userRole]?.permissions || [];
    
    if (userPermissions.includes(required_permission)) {
      next();
    } else {
      res.status(403).json({ error: 'Insufficient permissions' });
    }
  };
}
```

---

## 🔒 **Gestão de Credenciais**

### **Credential Encryption**
```bash
# Environment Variables for Encryption
N8N_ENCRYPTION_KEY="$(openssl rand -base64 32)"
N8N_USER_MANAGEMENT_JWT_SECRET="$(openssl rand -base64 64)"
N8N_AUTH_EXCLUDE_ENDPOINTS="/healthz,/metrics"

# Credential Rotation Policy
CREDENTIAL_ROTATION_DAYS=90
CREDENTIAL_AUDIT_ENABLED=true
CREDENTIAL_BACKUP_ENCRYPTED=true
```

### **External Secret Management**
```yaml
# HashiCorp Vault Integration
apiVersion: v1
kind: Secret
metadata:
  name: n8n-vault-config
type: Opaque
data:
  vault-token: <base64-encoded-token>
  vault-url: <base64-encoded-url>

---
# Vault Secret Store
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.yourdomain.com"
      path: "secret"
      version: "v2"
      auth:
        tokenSecretRef:
          name: "vault-token"
          key: "token"

---
# External Secret
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: n8n-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: n8n-secrets
    creationPolicy: Owner
  data:
  - secretKey: salesforce-api-key
    remoteRef:
      key: n8n/salesforce
      property: api_key
```

### **Credential Security Patterns**
```javascript
// Node: Set - Secure Credential Usage
{
  "credentials": {
    "type": "vault",
    "path": "secret/n8n/{{ $json.environment }}/{{ $json.service }}",
    "field": "api_key",
    "ttl": 3600 // 1 hour TTL
  },
  "request": {
    "headers": {
      "Authorization": "Bearer {{ $credentials.api_key }}",
      "X-Request-ID": "{{ $json.requestId }}",
      "X-Environment": "{{ $json.environment }}"
    }
  },
  "audit": {
    "action": "credential_accessed",
    "credential_type": "{{ $credentials.type }}",
    "user": "{{ $user.email }}",
    "timestamp": "{{ new Date().toISOString() }}"
  }
}
```

---

## 🌐 **Network Security**

### **Reverse Proxy Configuration (Nginx)**
```nginx
# /etc/nginx/sites-available/n8n-secure
server {
    listen 443 ssl http2;
    server_name n8n.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/ssl/certs/n8n.crt;
    ssl_certificate_key /etc/ssl/private/n8n.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' wss:; frame-ancestors 'self';" always;
    
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/m;
    
    # API Rate Limiting
    location /rest/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://n8n:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Login Rate Limiting
    location /rest/login {
        limit_req zone=login burst=5 nodelay;
        proxy_pass http://n8n:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # WebSocket Support
    location /socket.io/ {
        proxy_pass http://n8n:5678;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Default Location
    location / {
        proxy_pass http://n8n:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Security.txt
    location = /.well-known/security.txt {
        return 200 "Contact: security@yourdomain.com\nExpires: 2025-12-31T23:59:59.000Z";
        add_header Content-Type text/plain;
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name n8n.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### **Firewall Rules (UFW)**
```bash
#!/bin/bash
# firewall-setup.sh

# Reset firewall
ufw --force reset

# Default policies
ufw default deny incoming
ufw default allow outgoing

# SSH (restrict to management network)
ufw allow from 10.0.0.0/24 to any port 22

# HTTP/HTTPS (public)
ufw allow 80/tcp
ufw allow 443/tcp

# n8n (internal only)
ufw allow from 10.0.0.0/24 to any port 5678

# PostgreSQL (internal only)
ufw allow from 10.0.0.0/24 to any port 5432

# Redis (internal only)
ufw allow from 10.0.0.0/24 to any port 6379

# Monitoring (management network)
ufw allow from 10.0.0.0/24 to any port 9090  # Prometheus
ufw allow from 10.0.0.0/24 to any port 3000  # Grafana

# Rate limiting for SSH
ufw limit ssh

# Enable firewall
ufw enable

# Log configuration
ufw logging medium
```

---

## 🗃️ **Data Protection**

### **Database Security**
```sql
-- PostgreSQL Security Configuration
-- Create dedicated database user
CREATE USER n8n_app WITH PASSWORD 'strong_random_password';

-- Create database with restricted permissions
CREATE DATABASE n8n_production OWNER n8n_app;

-- Revoke public schema privileges
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO n8n_app;

-- Grant specific permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO n8n_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO n8n_app;

-- Row Level Security for multi-tenancy
ALTER TABLE workflow_entity ENABLE ROW LEVEL SECURITY;

CREATE POLICY workflow_isolation ON workflow_entity
  FOR ALL TO n8n_app
  USING (owner_id = current_setting('app.user_id')::uuid);

-- Audit table
CREATE TABLE security_audit (
    id SERIAL PRIMARY KEY,
    user_id UUID,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(255),
    ip_address INET,
    user_agent TEXT,
    success BOOLEAN DEFAULT true,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for performance
CREATE INDEX idx_security_audit_user_id ON security_audit(user_id);
CREATE INDEX idx_security_audit_created_at ON security_audit(created_at);
```

### **Data Encryption at Rest**
```yaml
# PostgreSQL with encryption
version: '3.8'
services:
  postgres:
    image: postgres:17-alpine
    environment:
      POSTGRES_DB: n8n_production
      POSTGRES_USER: n8n_app
      POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
      # Enable encryption
      POSTGRES_INITDB_ARGS: "--auth-host=md5 --auth-local=md5"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgresql.conf:/etc/postgresql/postgresql.conf
    command: >
      postgres
      -c ssl=on
      -c ssl_cert_file=/etc/ssl/certs/postgres.crt
      -c ssl_key_file=/etc/ssl/private/postgres.key
      -c log_statement=all
      -c log_connections=on
      -c log_disconnections=on
    secrets:
      - postgres_password
    networks:
      - backend

secrets:
  postgres_password:
    file: ./secrets/postgres_password.txt

volumes:
  postgres_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /encrypted/postgres-data
```

### **Backup Security**
```bash
#!/bin/bash
# secure-backup.sh

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/secure/backups"
ENCRYPTION_KEY_FILE="/secure/keys/backup.key"
S3_BUCKET="your-encrypted-backup-bucket"

# Create encrypted backup
pg_dump -h localhost -U n8n_app n8n_production | \
  gzip | \
  openssl enc -aes-256-cbc -salt -in - -out "${BACKUP_DIR}/n8n_backup_${BACKUP_DATE}.sql.gz.enc" -pass file:${ENCRYPTION_KEY_FILE}

# Create workflow export backup
curl -X GET "http://localhost:5678/rest/workflows" \
  -H "Authorization: Bearer ${N8N_API_TOKEN}" | \
  jq '.' | \
  gzip | \
  openssl enc -aes-256-cbc -salt -in - -out "${BACKUP_DIR}/workflows_${BACKUP_DATE}.json.gz.enc" -pass file:${ENCRYPTION_KEY_FILE}

# Upload to S3 with server-side encryption
aws s3 cp "${BACKUP_DIR}/n8n_backup_${BACKUP_DATE}.sql.gz.enc" \
  "s3://${S3_BUCKET}/database/" \
  --server-side-encryption AES256

aws s3 cp "${BACKUP_DIR}/workflows_${BACKUP_DATE}.json.gz.enc" \
  "s3://${S3_BUCKET}/workflows/" \
  --server-side-encryption AES256

# Clean local backups older than 7 days
find "${BACKUP_DIR}" -name "*.enc" -mtime +7 -delete

# Audit log
echo "$(date): Backup completed - ${BACKUP_DATE}" >> /var/log/n8n-backup.log
```

---

## 📊 **Security Monitoring**

### **Security Event Workflow**
```json
{
  "name": "security-monitoring",
  "active": true,
  "nodes": [
    {
      "id": "webhook",
      "name": "Security Event Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "security-events",
        "httpMethod": "POST",
        "authentication": "headerAuth"
      }
    },
    {
      "id": "classify",
      "name": "Classify Event Severity",
      "type": "n8n-nodes-base.switch",
      "parameters": {
        "dataType": "string",
        "value1": "{{ $json.event_type }}",
        "rules": {
          "values": [
            {
              "conditions": {
                "string": [
                  {
                    "value1": "{{ $json.event_type }}",
                    "operation": "equal",
                    "value2": "failed_login"
                  }
                ]
              },
              "renameOutput": "Low Priority"
            },
            {
              "conditions": {
                "string": [
                  {
                    "value1": "{{ $json.event_type }}",
                    "operation": "equal",
                    "value2": "privilege_escalation"
                  }
                ]
              },
              "renameOutput": "High Priority"
            },
            {
              "conditions": {
                "string": [
                  {
                    "value1": "{{ $json.event_type }}",
                    "operation": "equal",
                    "value2": "data_exfiltration"
                  }
                ]
              },
              "renameOutput": "Critical"
            }
          ]
        }
      }
    },
    {
      "id": "store-event",
      "name": "Store Security Event",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "insert",
        "table": "security_audit",
        "columns": [
          "user_id",
          "action",
          "resource_type",
          "resource_id",
          "ip_address",
          "user_agent",
          "success",
          "error_message"
        ]
      }
    },
    {
      "id": "alert-high",
      "name": "Alert High Priority",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#security-alerts",
        "text": "🚨 High Priority Security Event",
        "blocks": [
          {
            "type": "header",
            "text": {
              "type": "plain_text",
              "text": "🚨 Security Alert"
            }
          },
          {
            "type": "section",
            "fields": [
              {
                "type": "mrkdwn",
                "text": "*Event:* {{ $json.event_type }}"
              },
              {
                "type": "mrkdwn",
                "text": "*User:* {{ $json.user_id }}"
              },
              {
                "type": "mrkdwn",
                "text": "*IP:* {{ $json.ip_address }}"
              },
              {
                "type": "mrkdwn",
                "text": "*Time:* {{ $json.timestamp }}"
              }
            ]
          }
        ]
      }
    }
  ],
  "connections": {
    "webhook": {
      "main": [
        [
          {
            "node": "classify",
            "type": "main",
            "index": 0
          },
          {
            "node": "store-event",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "classify": {
      "main": [
        [],
        [
          {
            "node": "alert-high",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "alert-high",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

### **SIEM Integration**
```javascript
// security-siem-forwarder.js
const syslog = require('syslog-client');
const client = syslog.createClient('siem.yourdomain.com', {
  port: 514,
  transport: syslog.Transport.Tcp,
  facility: syslog.Facility.Local0
});

function forwardSecurityEvent(event) {
  const message = {
    timestamp: new Date().toISOString(),
    source: 'n8n',
    severity: mapSeverity(event.type),
    user: event.user_id,
    action: event.action,
    resource: event.resource_type,
    ip: event.ip_address,
    success: event.success,
    details: event.details
  };
  
  client.log(JSON.stringify(message), {
    severity: mapSeverity(event.type)
  });
}

function mapSeverity(eventType) {
  const severityMap = {
    'failed_login': syslog.Severity.Warning,
    'privilege_escalation': syslog.Severity.Error,
    'data_exfiltration': syslog.Severity.Critical,
    'workflow_modified': syslog.Severity.Notice,
    'credential_accessed': syslog.Severity.Informational
  };
  
  return severityMap[eventType] || syslog.Severity.Notice;
}

module.exports = { forwardSecurityEvent };
```

---

## 🔍 **Security Compliance**

### **SOC 2 Controls**
```yaml
# Security Control Matrix
controls:
  CC1.1: # Control Environment
    description: "Organization demonstrates commitment to integrity and ethical values"
    implementation:
      - Security policy documented
      - Code of conduct established
      - Background checks for privileged users
    evidence:
      - Security policy document
      - Training records
      - Background check records
  
  CC2.1: # Communication and Information
    description: "Organization obtains/generates relevant quality information"
    implementation:
      - Security metrics dashboard
      - Incident response procedures
      - Regular security assessments
    evidence:
      - Security dashboard screenshots
      - Incident response playbooks
      - Assessment reports
  
  CC6.1: # Logical Access
    description: "Organization implements logical access security controls"
    implementation:
      - Multi-factor authentication
      - Role-based access control
      - Regular access reviews
    evidence:
      - MFA configuration
      - RBAC documentation
      - Access review reports
```

### **GDPR Compliance**
```javascript
// Data Protection Workflow
const gdprWorkflow = {
  "name": "gdpr-data-protection",
  "nodes": [
    {
      "name": "Data Subject Request",
      "type": "webhook",
      "parameters": {
        "path": "gdpr/data-request",
        "authentication": "required"
      }
    },
    {
      "name": "Validate Request",
      "type": "function",
      "parameters": {
        "functionCode": `
          // Validate GDPR request
          const request = $input.all()[0].json;
          
          const validTypes = ['access', 'rectification', 'erasure', 'portability'];
          if (!validTypes.includes(request.type)) {
            throw new Error('Invalid request type');
          }
          
          // Verify identity
          if (!request.identity_verification || !request.data_subject_id) {
            throw new Error('Identity verification required');
          }
          
          return {
            request_id: generateUUID(),
            type: request.type,
            data_subject_id: request.data_subject_id,
            status: 'validated',
            received_at: new Date().toISOString()
          };
        `
      }
    },
    {
      "name": "Process Data Request",
      "type": "switch",
      "parameters": {
        "dataType": "string",
        "value1": "{{ $json.type }}",
        "rules": {
          "values": [
            {
              "conditions": { "equal": "access" },
              "renameOutput": "Data Access"
            },
            {
              "conditions": { "equal": "erasure" },
              "renameOutput": "Data Deletion"
            }
          ]
        }
      }
    }
  ]
};
```

---

## ✅ **Security Checklist**

### **Infrastructure Security**
- [ ] TLS 1.2+ encryption for all communications
- [ ] Strong cipher suites configured
- [ ] Firewall rules implemented and tested
- [ ] VPN access for administrative tasks
- [ ] Regular security patches applied
- [ ] Intrusion detection system configured

### **Application Security**
- [ ] SAML/OIDC authentication implemented
- [ ] Role-based access control configured
- [ ] Session management secured
- [ ] Input validation implemented
- [ ] SQL injection protection enabled
- [ ] XSS protection configured

### **Data Security**
- [ ] Database encryption at rest enabled
- [ ] Credential encryption configured
- [ ] Backup encryption implemented
- [ ] Data retention policies defined
- [ ] PII data classification completed
- [ ] GDPR compliance measures implemented

### **Monitoring & Compliance**
- [ ] Security event logging enabled
- [ ] SIEM integration configured
- [ ] Security metrics dashboard created
- [ ] Incident response procedures documented
- [ ] Regular penetration testing scheduled
- [ ] Compliance audit trail maintained

---

**📚 Próximo**: [📊 Observabilidade & Scaling](./observability_scaling.md)