# 📊 Observabilidade & Scaling

> **Objetivo**: Implementar monitoramento completo, métricas de performance e estratégias de escalabilidade para garantir alta disponibilidade e crescimento sustentável de workflows n8n Enterprise.

---

## 🎯 **Framework de Observabilidade**

### **Três Pilares da Observabilidade**
```text
┌─────────────────────────────────────────────────────┐
│                  METRICS                        │ ← Prometheus, Grafana
├─────────────────────────────────────────────────────┤
│                   LOGS                          │ ← ELK Stack, Fluentd
├─────────────────────────────────────────────────────┤
│                  TRACES                         │ ← Jaeger, Zipkin
└─────────────────────────────────────────────────────┘
```

### **Níveis de Monitoramento**
✅ **Infrastructure**: CPU, Memory, Disk, Network  
✅ **Application**: n8n specific metrics, workflow performance  
✅ **Business**: KPIs, SLAs, user experience  
✅ **Security**: Failed logins, suspicious activities  
✅ **Cost**: Resource utilization, optimization opportunities  

---

## 📈 **Métricas e Monitoramento**

### **Prometheus Configuration**
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "n8n_alerts.yml"
  - "infrastructure_alerts.yml"

scrape_configs:
  # n8n Metrics
  - job_name: 'n8n'
    static_configs:
      - targets: ['n8n:5678']
    metrics_path: '/metrics'
    scrape_interval: 30s
    
  # Node Exporter (System Metrics)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
    
  # PostgreSQL Exporter
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
    
  # Redis Exporter
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
    
  # Nginx Exporter
  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx-exporter:9113']

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

### **n8n Custom Metrics Exporter**
```javascript
// n8n-metrics-exporter.js
const express = require('express');
const prometheus = require('prom-client');
const axios = require('axios');

class N8nMetricsExporter {
  constructor(n8nUrl, n8nToken) {
    this.n8nUrl = n8nUrl;
    this.n8nToken = n8nToken;
    this.app = express();
    this.setupMetrics();
    this.setupRoutes();
  }

  setupMetrics() {
    // Default metrics
    prometheus.collectDefaultMetrics();

    // Custom n8n metrics
    this.workflowExecutionsTotal = new prometheus.Counter({
      name: 'n8n_workflow_executions_total',
      help: 'Total number of workflow executions',
      labelNames: ['workflow_id', 'workflow_name', 'status']
    });

    this.workflowExecutionDuration = new prometheus.Histogram({
      name: 'n8n_workflow_execution_duration_seconds',
      help: 'Workflow execution duration in seconds',
      labelNames: ['workflow_id', 'workflow_name'],
      buckets: [0.1, 0.5, 1, 2, 5, 10, 30, 60, 120, 300]
    });

    this.activeWorkflows = new prometheus.Gauge({
      name: 'n8n_active_workflows_count',
      help: 'Number of active workflows',
      labelNames: ['environment']
    });

    this.queueSize = new prometheus.Gauge({
      name: 'n8n_queue_size',
      help: 'Current queue size',
      labelNames: ['queue_type']
    });

    this.nodeExecutionsTotal = new prometheus.Counter({
      name: 'n8n_node_executions_total',
      help: 'Total number of node executions',
      labelNames: ['node_type', 'status']
    });

    this.credentialUsage = new prometheus.Counter({
      name: 'n8n_credential_usage_total',
      help: 'Total credential usage count',
      labelNames: ['credential_type']
    });

    this.webhookRequests = new prometheus.Counter({
      name: 'n8n_webhook_requests_total',
      help: 'Total webhook requests',
      labelNames: ['workflow_id', 'status_code']
    });

    this.errorRate = new prometheus.Gauge({
      name: 'n8n_error_rate',
      help: 'Error rate percentage',
      labelNames: ['workflow_id', 'time_window']
    });
  }

  setupRoutes() {
    this.app.get('/metrics', async (req, res) => {
      try {
        await this.collectN8nMetrics();
        res.set('Content-Type', prometheus.register.contentType);
        res.end(prometheus.register.metrics());
      } catch (error) {
        res.status(500).send(error.message);
      }
    });

    this.app.get('/health', (req, res) => {
      res.json({ status: 'healthy', timestamp: new Date().toISOString() });
    });
  }

  async collectN8nMetrics() {
    try {
      // Get workflow statistics
      const workflowsResp = await axios.get(`${this.n8nUrl}/rest/workflows`, {
        headers: { Authorization: `Bearer ${this.n8nToken}` }
      });
      
      const activeCount = workflowsResp.data.data.filter(w => w.active).length;
      this.activeWorkflows.set({ environment: process.env.ENVIRONMENT || 'production' }, activeCount);

      // Get recent executions
      const executionsResp = await axios.get(`${this.n8nUrl}/rest/executions`, {
        headers: { Authorization: `Bearer ${this.n8nToken}` },
        params: { limit: 100 }
      });

      // Process execution metrics
      for (const execution of executionsResp.data.data) {
        const labels = {
          workflow_id: execution.workflowId,
          workflow_name: execution.workflowData?.name || 'unknown',
          status: execution.finished ? 'success' : execution.stoppedAt ? 'failed' : 'running'
        };

        this.workflowExecutionsTotal.inc(labels);

        if (execution.startedAt && execution.stoppedAt) {
          const duration = (new Date(execution.stoppedAt) - new Date(execution.startedAt)) / 1000;
          this.workflowExecutionDuration.observe(
            { workflow_id: execution.workflowId, workflow_name: labels.workflow_name },
            duration
          );
        }
      }

      // Queue metrics (if using queue mode)
      if (process.env.EXECUTIONS_MODE === 'queue') {
        const queueStats = await this.getQueueStats();
        this.queueSize.set({ queue_type: 'main' }, queueStats.waiting);
        this.queueSize.set({ queue_type: 'active' }, queueStats.active);
      }

    } catch (error) {
      console.error('Error collecting n8n metrics:', error.message);
    }
  }

  async getQueueStats() {
    // Implementação real com Redis
    const Redis = require('redis');
    const redis = Redis.createClient({
      host: process.env.REDIS_HOST || 'localhost',
      port: process.env.REDIS_PORT || 6379
    });

    try {
      const waiting = await redis.llen('bull:n8n:waiting');
      const active = await redis.llen('bull:n8n:active');
      const failed = await redis.llen('bull:n8n:failed');
      
      return { waiting, active, failed };
    } catch (error) {
      console.error('Redis connection error:', error);
      return { waiting: 0, active: 0, failed: 0 };
    }
  }

  start(port = 9090) {
    this.app.listen(port, () => {
      console.log(`n8n Metrics Exporter running on port ${port}`);
    });
  }
}

// Execução
if (require.main === module) {
  const exporter = new N8nMetricsExporter(
    process.env.N8N_BASE_URL,
    process.env.N8N_API_TOKEN
  );
  exporter.start();
}

module.exports = N8nMetricsExporter;
```

### **Alerting Rules (n8n_alerts.yml)**
```yaml
groups:
  - name: n8n_alerts
    rules:
      # High Error Rate
      - alert: N8nHighErrorRate
        expr: (rate(n8n_workflow_executions_total{status="failed"}[5m]) / rate(n8n_workflow_executions_total[5m])) > 0.1
        for: 2m
        labels:
          severity: warning
          service: n8n
        annotations:
          summary: "High error rate detected in n8n workflows"
          description: "Error rate is {{ $value | humanizePercentage }} for workflow {{ $labels.workflow_name }}"

      # Long Running Workflow
      - alert: N8nLongRunningWorkflow
        expr: increase(n8n_workflow_execution_duration_seconds_bucket{le="300"}[5m]) == 0 and increase(n8n_workflow_execution_duration_seconds_count[5m]) > 0
        for: 5m
        labels:
          severity: warning
          service: n8n
        annotations:
          summary: "Workflow execution taking longer than expected"
          description: "Workflow {{ $labels.workflow_name }} has been running for more than 5 minutes"

      # Queue Buildup
      - alert: N8nQueueBuildup
        expr: n8n_queue_size{queue_type="main"} > 50
        for: 1m
        labels:
          severity: critical
          service: n8n
        annotations:
          summary: "n8n queue buildup detected"
          description: "Queue size is {{ $value }} jobs, indicating potential bottleneck"

      # No Active Workflows
      - alert: N8nNoActiveWorkflows
        expr: n8n_active_workflows_count == 0
        for: 1m
        labels:
          severity: critical
          service: n8n
        annotations:
          summary: "No active workflows detected"
          description: "All workflows appear to be inactive, check n8n instance health"

      # High Memory Usage
      - alert: N8nHighMemoryUsage
        expr: (process_resident_memory_bytes / 1024 / 1024) > 1024
        for: 5m
        labels:
          severity: warning
          service: n8n
        annotations:
          summary: "n8n instance using high memory"
          description: "Memory usage is {{ $value }}MB, consider scaling or optimization"
```

---

## 📊 **Grafana Dashboards**

### **n8n Operations Dashboard**
```json
{
  "dashboard": {
    "id": null,
    "title": "n8n Operations Dashboard",
    "tags": ["n8n", "operations"],
    "timezone": "UTC",
    "panels": [
      {
        "id": 1,
        "title": "Workflow Executions Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(n8n_workflow_executions_total[5m])",
            "legendFormat": "{{ workflow_name }}"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "reqps",
            "thresholds": {
              "steps": [
                { "color": "green", "value": null },
                { "color": "yellow", "value": 10 },
                { "color": "red", "value": 50 }
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Error Rate by Workflow",
        "type": "timeseries",
        "targets": [
          {
            "expr": "rate(n8n_workflow_executions_total{status=\"failed\"}[5m]) / rate(n8n_workflow_executions_total[5m])",
            "legendFormat": "{{ workflow_name }}"
          }
        ]
      },
      {
        "id": 3,
        "title": "Execution Duration Percentiles",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, rate(n8n_workflow_execution_duration_seconds_bucket[5m]))",
            "legendFormat": "p50"
          },
          {
            "expr": "histogram_quantile(0.95, rate(n8n_workflow_execution_duration_seconds_bucket[5m]))",
            "legendFormat": "p95"
          },
          {
            "expr": "histogram_quantile(0.99, rate(n8n_workflow_execution_duration_seconds_bucket[5m]))",
            "legendFormat": "p99"
          }
        ]
      },
      {
        "id": 4,
        "title": "Queue Size",
        "type": "timeseries",
        "targets": [
          {
            "expr": "n8n_queue_size",
            "legendFormat": "{{ queue_type }}"
          }
        ]
      },
      {
        "id": 5,
        "title": "Node Execution by Type",
        "type": "piechart",
        "targets": [
          {
            "expr": "increase(n8n_node_executions_total[1h])",
            "legendFormat": "{{ node_type }}"
          }
        ]
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "30s"
  }
}
```

### **Infrastructure Dashboard**
```json
{
  "dashboard": {
    "title": "n8n Infrastructure Monitoring",
    "panels": [
      {
        "title": "CPU Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "{{ instance }}"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
            "legendFormat": "{{ instance }}"
          }
        ]
      },
      {
        "title": "Disk Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "100 - ((node_filesystem_avail_bytes{mountpoint=\"/\"} / node_filesystem_size_bytes{mountpoint=\"/\"}) * 100)",
            "legendFormat": "{{ instance }}"
          }
        ]
      },
      {
        "title": "Network I/O",
        "type": "timeseries",
        "targets": [
          {
            "expr": "rate(node_network_receive_bytes_total[5m])",
            "legendFormat": "{{ device }} - RX"
          },
          {
            "expr": "rate(node_network_transmit_bytes_total[5m])",
            "legendFormat": "{{ device }} - TX"
          }
        ]
      }
    ]
  }
}
```

---

## 🚀 **Estratégias de Scaling**

### **Horizontal Scaling com Queue Mode**
```yaml
# docker-compose-scaled.yml
version: '3.8'
services:
  # Main n8n instance (coordinator)
  n8n-main:
    image: n8nio/n8n:latest
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_PORT: 5432
      DB_POSTGRESDB_DATABASE: n8n
      DB_POSTGRESDB_USER: n8n
      DB_POSTGRESDB_PASSWORD: ${POSTGRES_PASSWORD}
      
      # Queue Mode Configuration
      EXECUTIONS_MODE: queue
      QUEUE_BULL_REDIS_HOST: redis
      QUEUE_BULL_REDIS_PORT: 6379
      QUEUE_BULL_REDIS_PASSWORD: ${REDIS_PASSWORD}
      
      # Main instance specific
      N8N_BASIC_AUTH_ACTIVE: true
      N8N_BASIC_AUTH_USER: ${N8N_USER}
      N8N_BASIC_AUTH_PASSWORD: ${N8N_PASSWORD}
      
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - n8n_network
    depends_on:
      - postgres
      - redis

  # Worker instances
  n8n-worker-1:
    image: n8nio/n8n:latest
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_PORT: 5432
      DB_POSTGRESDB_DATABASE: n8n
      DB_POSTGRESDB_USER: n8n
      DB_POSTGRESDB_PASSWORD: ${POSTGRES_PASSWORD}
      
      # Worker Configuration
      EXECUTIONS_MODE: queue
      QUEUE_BULL_REDIS_HOST: redis
      QUEUE_BULL_REDIS_PORT: 6379
      QUEUE_BULL_REDIS_PASSWORD: ${REDIS_PASSWORD}
      
      # Worker specific settings
      N8N_DISABLE_UI: true
      WEBHOOK_URL: http://n8n-main:5678/
      
    command: n8n worker
    networks:
      - n8n_network
    depends_on:
      - redis
      - postgres
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 2G
          cpus: '1.0'

  # Redis for queue
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - n8n_network
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'

  # PostgreSQL
  postgres:
    image: postgres:17-alpine
    environment:
      POSTGRES_DB: n8n
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - n8n_network

volumes:
  n8n_data:
  redis_data:
  postgres_data:

networks:
  n8n_network:
    driver: bridge
```

### **Kubernetes Deployment with HPA**
```yaml
# k8s/n8n-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: n8n-main
  namespace: n8n
spec:
  replicas: 1
  selector:
    matchLabels:
      app: n8n-main
  template:
    metadata:
      labels:
        app: n8n-main
    spec:
      containers:
      - name: n8n
        image: n8nio/n8n:latest
        ports:
        - containerPort: 5678
        env:
        - name: EXECUTIONS_MODE
          value: "queue"
        - name: QUEUE_BULL_REDIS_HOST
          value: "redis"
        - name: DB_TYPE
          value: "postgresdb"
        - name: DB_POSTGRESDB_HOST
          value: "postgres"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 5678
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /healthz
            port: 5678
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: n8n-worker
  namespace: n8n
spec:
  replicas: 3
  selector:
    matchLabels:
      app: n8n-worker
  template:
    metadata:
      labels:
        app: n8n-worker
    spec:
      containers:
      - name: n8n-worker
        image: n8nio/n8n:latest
        command: ["n8n", "worker"]
        env:
        - name: EXECUTIONS_MODE
          value: "queue"
        - name: QUEUE_BULL_REDIS_HOST
          value: "redis"
        - name: N8N_DISABLE_UI
          value: "true"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"

---
# HorizontalPodAutoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: n8n-worker-hpa
  namespace: n8n
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: n8n-worker
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: n8n_queue_size
      target:
        type: AverageValue
        averageValue: "10"
```

---

## 📋 **Logging Strategy**

### **Structured Logging Configuration**
```yaml
# fluentd/fluent.conf
<source>
  @type tail
  path /var/log/n8n/*.log
  pos_file /var/log/fluentd/n8n.log.pos
  tag n8n.*
  format json
  time_format %Y-%m-%dT%H:%M:%S.%L%z
</source>

<filter n8n.**>
  @type parser
  key_name message
  reserve_data true
  <parse>
    @type json
  </parse>
</filter>

<filter n8n.**>
  @type record_transformer
  <record>
    hostname "#{Socket.gethostname}"
    environment "#{ENV['ENVIRONMENT']}"
    service "n8n"
    timestamp ${time}
  </record>
</filter>

# Send to Elasticsearch
<match n8n.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  index_name n8n-logs
  type_name _doc
  logstash_format true
  logstash_prefix n8n
  logstash_dateformat %Y.%m.%d
  include_tag_key true
  tag_key @log_name
  flush_interval 1s
</match>
```

### **Custom n8n Logging Middleware**
```javascript
// logging-middleware.js
const winston = require('winston');
const { ElasticsearchTransport } = require('winston-elasticsearch');

class N8nLogger {
  constructor() {
    this.logger = winston.createLogger({
      level: process.env.LOG_LEVEL || 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
      ),
      defaultMeta: {
        service: 'n8n',
        environment: process.env.ENVIRONMENT || 'production',
        instance: process.env.HOSTNAME || 'unknown'
      },
      transports: [
        new winston.transports.Console(),
        new winston.transports.File({ 
          filename: '/var/log/n8n/error.log', 
          level: 'error' 
        }),
        new winston.transports.File({ 
          filename: '/var/log/n8n/combined.log' 
        }),
        new ElasticsearchTransport({
          level: 'info',
          clientOpts: {
            node: process.env.ELASTICSEARCH_URL || 'http://elasticsearch:9200'
          },
          index: 'n8n-logs'
        })
      ]
    });
  }

  logWorkflowExecution(workflowId, executionId, event, data = {}) {
    this.logger.info('Workflow execution event', {
      type: 'workflow_execution',
      workflow_id: workflowId,
      execution_id: executionId,
      event: event,
      ...data
    });
  }

  logSecurityEvent(event, userId, details = {}) {
    this.logger.warn('Security event', {
      type: 'security',
      event: event,
      user_id: userId,
      ...details
    });
  }

  logPerformanceMetric(metric, value, labels = {}) {
    this.logger.info('Performance metric', {
      type: 'performance',
      metric: metric,
      value: value,
      ...labels
    });
  }

  logError(error, context = {}) {
    this.logger.error('Application error', {
      type: 'error',
      error: error.message,
      stack: error.stack,
      ...context
    });
  }
}

module.exports = new N8nLogger();
```

---

## 💡 **Performance Optimization**

### **Database Optimization**
```sql
-- PostgreSQL Performance Tuning
-- Execution data cleanup
CREATE OR REPLACE FUNCTION cleanup_old_executions()
RETURNS void AS $$
BEGIN
    -- Delete executions older than 30 days
    DELETE FROM execution_entity 
    WHERE "startedAt" < NOW() - INTERVAL '30 days'
    AND finished = true;
    
    -- Delete error executions older than 7 days
    DELETE FROM execution_entity 
    WHERE "startedAt" < NOW() - INTERVAL '7 days'
    AND finished = true 
    AND "stoppedAt" IS NOT NULL
    AND data::text LIKE '%"error"%';
    
    -- Vacuum tables
    VACUUM ANALYZE execution_entity;
    VACUUM ANALYZE workflow_entity;
END;
$$ LANGUAGE plpgsql;

-- Schedule cleanup (requires pg_cron extension)
SELECT cron.schedule('cleanup-executions', '0 2 * * *', 'SELECT cleanup_old_executions();');

-- Indexes for performance
CREATE INDEX CONCURRENTLY idx_execution_workflow_started 
ON execution_entity (workflowId, "startedAt") 
WHERE finished = true;

CREATE INDEX CONCURRENTLY idx_execution_status_started 
ON execution_entity ("stoppedAt", finished, "startedAt") 
WHERE "stoppedAt" IS NOT NULL;

-- Partial index for active executions
CREATE INDEX CONCURRENTLY idx_execution_active 
ON execution_entity (workflowId, "startedAt") 
WHERE finished = false;
```

### **Redis Queue Optimization**
```javascript
// queue-optimization.js
const Queue = require('bull');

class OptimizedQueue {
  constructor(redisConfig) {
    this.queue = new Queue('n8n execution', {
      redis: redisConfig,
      defaultJobOptions: {
        removeOnComplete: 100,  // Keep only last 100 completed jobs
        removeOnFail: 50,       // Keep only last 50 failed jobs
        attempts: 3,            // Retry failed jobs 3 times
        backoff: {
          type: 'exponential',
          delay: 2000
        }
      },
      settings: {
        stalledInterval: 30000,   // Check for stalled jobs every 30s
        maxStalledCount: 1        // Max times a job can be stalled
      }
    });

    this.setupProcessors();
    this.setupEvents();
  }

  setupProcessors() {
    // Process high priority jobs first
    this.queue.process('high-priority', 5, async (job) => {
      return this.executeWorkflow(job.data);
    });

    // Normal priority jobs
    this.queue.process('normal', 10, async (job) => {
      return this.executeWorkflow(job.data);
    });

    // Low priority batch jobs
    this.queue.process('low-priority', 2, async (job) => {
      return this.executeWorkflow(job.data);
    });
  }

  setupEvents() {
    this.queue.on('completed', (job, result) => {
      logger.info('Job completed', {
        job_id: job.id,
        workflow_id: job.data.workflowId,
        duration: Date.now() - job.timestamp
      });
    });

    this.queue.on('failed', (job, err) => {
      logger.error('Job failed', {
        job_id: job.id,
        workflow_id: job.data.workflowId,
        error: err.message,
        attempts: job.attemptsMade
      });
    });

    this.queue.on('stalled', (job) => {
      logger.warn('Job stalled', {
        job_id: job.id,
        workflow_id: job.data.workflowId
      });
    });
  }

  async addJob(workflowData, priority = 'normal') {
    const jobOptions = {
      priority: this.getPriorityValue(priority),
      delay: priority === 'low-priority' ? 5000 : 0  // Delay low priority jobs
    };

    return this.queue.add(priority, workflowData, jobOptions);
  }

  getPriorityValue(priority) {
    const priorities = {
      'high-priority': 100,
      'normal': 50,
      'low-priority': 10
    };
    return priorities[priority] || 50;
  }

  async executeWorkflow(data) {
    // Workflow execution logic here
    // This would integrate with n8n's execution engine
    const startTime = Date.now();
    
    try {
      // Execute workflow
      const result = await this.runWorkflow(data);
      
      // Log performance metrics
      const duration = Date.now() - startTime;
      logger.logPerformanceMetric('workflow_execution_duration', duration, {
        workflow_id: data.workflowId
      });
      
      return result;
    } catch (error) {
      logger.logError(error, {
        workflow_id: data.workflowId,
        execution_context: 'queue_worker'
      });
      throw error;
    }
  }
}
```

---

## 🔍 **Health Checks & SRE**

### **Comprehensive Health Check**
```javascript
// health-check.js
const axios = require('axios');
const Redis = require('redis');
const { Pool } = require('pg');

class HealthChecker {
  constructor(config) {
    this.config = config;
    this.redis = Redis.createClient(config.redis);
    this.postgres = new Pool(config.postgres);
  }

  async checkOverallHealth() {
    const checks = {
      timestamp: new Date().toISOString(),
      status: 'healthy',
      checks: {}
    };

    try {
      // Check n8n API
      checks.checks.n8n_api = await this.checkN8nAPI();
      
      // Check database
      checks.checks.database = await this.checkDatabase();
      
      // Check Redis
      checks.checks.redis = await this.checkRedis();
      
      // Check queue
      checks.checks.queue = await this.checkQueue();
      
      // Check disk space
      checks.checks.disk_space = await this.checkDiskSpace();
      
      // Check memory usage
      checks.checks.memory = await this.checkMemory();
      
      // Determine overall status
      const failedChecks = Object.values(checks.checks).filter(check => check.status !== 'healthy');
      if (failedChecks.length > 0) {
        checks.status = failedChecks.some(check => check.critical) ? 'critical' : 'degraded';
      }
      
    } catch (error) {
      checks.status = 'critical';
      checks.error = error.message;
    }

    return checks;
  }

  async checkN8nAPI() {
    try {
      const start = Date.now();
      const response = await axios.get(`${this.config.n8n.url}/healthz`, {
        timeout: 5000
      });
      const responseTime = Date.now() - start;

      return {
        status: response.status === 200 ? 'healthy' : 'unhealthy',
        response_time_ms: responseTime,
        critical: true
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message,
        critical: true
      };
    }
  }

  async checkDatabase() {
    try {
      const start = Date.now();
      const result = await this.postgres.query('SELECT 1');
      const responseTime = Date.now() - start;

      // Check connection pool
      const poolStatus = {
        total: this.postgres.totalCount,
        idle: this.postgres.idleCount,
        waiting: this.postgres.waitingCount
      };

      return {
        status: 'healthy',
        response_time_ms: responseTime,
        pool_status: poolStatus,
        critical: true
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message,
        critical: true
      };
    }
  }

  async checkRedis() {
    try {
      const start = Date.now();
      await this.redis.ping();
      const responseTime = Date.now() - start;

      // Get Redis info
      const info = await this.redis.info('memory');
      const memoryUsage = this.parseRedisInfo(info, 'used_memory_human');

      return {
        status: 'healthy',
        response_time_ms: responseTime,
        memory_usage: memoryUsage,
        critical: true
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message,
        critical: true
      };
    }
  }

  async checkQueue() {
    try {
      const queueStats = {
        waiting: await this.redis.llen('bull:n8n:waiting'),
        active: await this.redis.llen('bull:n8n:active'),
        completed: await this.redis.llen('bull:n8n:completed'),
        failed: await this.redis.llen('bull:n8n:failed')
      };

      const status = queueStats.waiting > 100 ? 'degraded' : 'healthy';

      return {
        status: status,
        queue_stats: queueStats,
        critical: false
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message,
        critical: false
      };
    }
  }

  async checkDiskSpace() {
    const fs = require('fs');
    const { promisify } = require('util');
    const statvfs = promisify(fs.statvfs || fs.statSync);

    try {
      const stats = await statvfs('/');
      const free = stats.bavail * stats.frsize;
      const total = stats.blocks * stats.frsize;
      const used = total - free;
      const usagePercent = (used / total) * 100;

      const status = usagePercent > 90 ? 'critical' : usagePercent > 80 ? 'degraded' : 'healthy';

      return {
        status: status,
        usage_percent: Math.round(usagePercent),
        free_bytes: free,
        total_bytes: total,
        critical: usagePercent > 95
      };
    } catch (error) {
      return {
        status: 'unknown',
        error: error.message,
        critical: false
      };
    }
  }

  async checkMemory() {
    const used = process.memoryUsage();
    const totalMem = require('os').totalmem();
    const freeMem = require('os').freemem();
    const usagePercent = ((totalMem - freeMem) / totalMem) * 100;

    const status = usagePercent > 90 ? 'critical' : usagePercent > 80 ? 'degraded' : 'healthy';

    return {
      status: status,
      usage_percent: Math.round(usagePercent),
      process_memory: {
        rss: Math.round(used.rss / 1024 / 1024),
        heap_used: Math.round(used.heapUsed / 1024 / 1024),
        heap_total: Math.round(used.heapTotal / 1024 / 1024)
      },
      critical: usagePercent > 95
    };
  }

  parseRedisInfo(info, key) {
    const lines = info.split('\r\n');
    const line = lines.find(l => l.startsWith(key));
    return line ? line.split(':')[1] : null;
  }
}

module.exports = HealthChecker;
```

### **SLA Monitoring**
```javascript
// sla-monitor.js
class SLAMonitor {
  constructor() {
    this.slaTargets = {
      availability: 99.9,        // 99.9% uptime
      response_time: 2000,       // 2 seconds
      error_rate: 1,             // 1% error rate
      queue_processing: 30000    // 30 seconds queue processing
    };
  }

  async calculateSLA(timeRange = '24h') {
    const metrics = await this.gatherMetrics(timeRange);
    
    return {
      period: timeRange,
      calculated_at: new Date().toISOString(),
      sla_status: {
        availability: this.calculateAvailability(metrics),
        response_time: this.calculateResponseTime(metrics),
        error_rate: this.calculateErrorRate(metrics),
        queue_processing: this.calculateQueueSLA(metrics)
      },
      overall_sla: this.calculateOverallSLA(metrics)
    };
  }

  calculateAvailability(metrics) {
    const uptime = metrics.uptime_seconds;
    const totalTime = metrics.period_seconds;
    const availability = (uptime / totalTime) * 100;
    
    return {
      current: availability,
      target: this.slaTargets.availability,
      status: availability >= this.slaTargets.availability ? 'met' : 'violated',
      violation_minutes: availability < this.slaTargets.availability 
        ? Math.round((totalTime - uptime) / 60) 
        : 0
    };
  }

  calculateResponseTime(metrics) {
    const p95ResponseTime = metrics.response_time_p95;
    
    return {
      current: p95ResponseTime,
      target: this.slaTargets.response_time,
      status: p95ResponseTime <= this.slaTargets.response_time ? 'met' : 'violated',
      violation_percentage: p95ResponseTime > this.slaTargets.response_time 
        ? Math.round(((p95ResponseTime - this.slaTargets.response_time) / this.slaTargets.response_time) * 100)
        : 0
    };
  }

  calculateErrorRate(metrics) {
    const errorRate = (metrics.failed_requests / metrics.total_requests) * 100;
    
    return {
      current: errorRate,
      target: this.slaTargets.error_rate,
      status: errorRate <= this.slaTargets.error_rate ? 'met' : 'violated',
      violation_count: errorRate > this.slaTargets.error_rate 
        ? metrics.failed_requests 
        : 0
    };
  }

  async gatherMetrics(timeRange) {
    // Implementation would query Prometheus/database for actual metrics
    // This is a simplified example
    return {
      period_seconds: 86400, // 24 hours
      uptime_seconds: 86350,  // ~10 minutes downtime
      total_requests: 10000,
      failed_requests: 50,
      response_time_p95: 1800,
      queue_processing_p95: 25000
    };
  }
}
```

---

## ✅ **Checklist de Observabilidade**

### **Métricas & Monitoramento**
- [ ] Prometheus configurado e coletando métricas
- [ ] Grafana dashboards criados e funcionais
- [ ] Alerting rules definidas e testadas
- [ ] Custom metrics exporter implementado
- [ ] SLA monitoring configurado
- [ ] Performance baselines estabelecidas

### **Logging & Debugging**
- [ ] Structured logging implementado
- [ ] Log aggregation configurado (ELK/Fluentd)
- [ ] Log retention policies definidas
- [ ] Debug workflows documentados
- [ ] Error tracking configurado
- [ ] Security logging habilitado

### **Scaling & Performance**
- [ ] Queue mode configurado
- [ ] Horizontal scaling testado
- [ ] HPA configurado (Kubernetes)
- [ ] Database optimization aplicada
- [ ] Resource limits configurados
- [ ] Load testing realizado

### **Health & Reliability**
- [ ] Health checks implementados
- [ ] Circuit breakers configurados
- [ ] Backup e recovery testados
- [ ] Disaster recovery plan criado
- [ ] Incident response procedures documentados
- [ ] Regular maintenance schedule estabelecido

---

**🎯 Conclusão**: Este framework de observabilidade e scaling fornece uma base sólida para operar n8n em escala Enterprise, garantindo alta disponibilidade, performance otimizada e capacidade de crescimento sustentável.

---

**📚 Referências**:
- [📝 Convenções de Nomenclatura](./naming_conventions.md)
- [⚡ Tratamento de Erros](./error_handling.md)  
- [🔄 Versionamento & CI/CD](./versioning_ci_cd.md)
- [🛡️ Hardening de Segurança](./security_hardening.md)