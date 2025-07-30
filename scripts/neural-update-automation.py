#!/usr/bin/env python3
"""
Neural Repository Update Automation Script
Automatiza atualizações da estrutura neural de repositórios n8n
"""

import json
import requests
import datetime
from pathlib import Path
from typing import Dict, List, Any

class NeuralRepoUpdater:
    """
    Automatiza atualizações do sistema neural de repositórios
    """
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.indices_path = self.base_path / "_repo_indices"
        self.repos_path = self.base_path / "repos"
        
    def fetch_npmjs_stats(self, package_name: str) -> Dict[str, Any]:
        """
        Busca estatísticas atualizadas do npmjs.com
        """
        try:
            # NPM API para downloads
            downloads_url = f"https://api.npmjs.org/downloads/point/last-month/{package_name}"
            response = requests.get(downloads_url)
            
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"Erro ao buscar stats NPM para {package_name}: {e}")
            return {}
    
    def fetch_github_stats(self, repo_path: str) -> Dict[str, Any]:
        """
        Busca estatísticas do GitHub (stars, forks, etc.)
        """
        try:
            # GitHub API pública
            api_url = f"https://api.github.com/repos/{repo_path}"
            response = requests.get(api_url)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "stars": data.get("stargazers_count", 0),
                    "forks": data.get("forks_count", 0),
                    "last_updated": data.get("updated_at", ""),
                    "language": data.get("language", ""),
                    "size": data.get("size", 0)
                }
            return {}
        except Exception as e:
            print(f"Erro ao buscar stats GitHub para {repo_path}: {e}")
            return {}
    
    def update_repository_registry(self):
        """
        Atualiza o registry de repositórios com dados mais recentes
        """
        registry_file = self.indices_path / "repository-registry.json"
        
        if not registry_file.exists():
            print("❌ Registry não encontrado")
            return
            
        with open(registry_file, 'r') as f:
            registry = json.load(f)
        
        print("🔄 Atualizando repository registry...")
        
        # Repositórios com packages NPM conhecidos
        npm_packages = {
            "oriondesign2015-n8n-nodes-evolution-api": "n8n-nodes-evolution-api",
            "restyler-awesome-n8n": None,  # Não é um package
            "n8n-io-n8n-core": None  # Core do n8n
        }
        
        # GitHub repositories
        github_repos = {
            "oriondesign2015-n8n-nodes-evolution-api": "oriondesign2015/n8n-nodes-evolution-api",
            "restyler-awesome-n8n": "restyler/awesome-n8n",
            "n8n-io-n8n-core": "n8n-io/n8n",
            "n8n-io-n8n-docs": "n8n-io/n8n-docs",
            "8gears-n8n-helm-chart": "8gears/n8n-helm-chart"
        }
        
        for repo_id, repo_data in registry["repositories"].items():
            repo_name = repo_data["name"]
            
            # Atualizar stats NPM se aplicável
            npm_package = npm_packages.get(repo_name)
            if npm_package:
                npm_stats = self.fetch_npmjs_stats(npm_package)
                if npm_stats:
                    repo_data["npm_stats"] = {
                        "monthly_downloads": npm_stats.get("downloads", 0),
                        "last_updated": datetime.datetime.now().isoformat()
                    }
                    print(f"  ✅ NPM stats atualizados para {repo_name}")
            
            # Atualizar stats GitHub se aplicável  
            github_repo = github_repos.get(repo_name)
            if github_repo:
                github_stats = self.fetch_github_stats(github_repo)
                if github_stats:
                    repo_data["github_stats"] = github_stats
                    print(f"  ✅ GitHub stats atualizados para {repo_name}")
        
        # Atualizar metadata geral
        registry["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
        registry["metadata"]["auto_update_version"] = "1.1.0"
        
        # Salvar registry atualizado
        with open(registry_file, 'w') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        
        print("✅ Repository registry atualizado com sucesso")
    
    def update_evolution_tracking(self):
        """
        Atualiza métricas de evolução do ecossistema
        """
        tracking_file = self.indices_path / "evolution-tracking.json"
        
        if not tracking_file.exists():
            print("❌ Evolution tracking não encontrado")
            return
            
        with open(tracking_file, 'r') as f:
            tracking = json.load(f)
        
        print("📈 Atualizando evolution tracking...")
        
        # Buscar stats atualizados do Evolution API
        evolution_stats = self.fetch_npmjs_stats("n8n-nodes-evolution-api")
        
        if evolution_stats:
            current_downloads = evolution_stats.get("downloads", 0)
            
            # Atualizar métricas baseline
            tracking["ecosystem_evolution"]["baseline_snapshot"]["date"] = datetime.date.today().isoformat()
            tracking["ecosystem_evolution"]["growth_metrics"]["repository_weights"]["repo_001_evolution_api"]["monthly_downloads"] = current_downloads
            
            # Adicionar snapshot histórico
            if "historical_snapshots" not in tracking:
                tracking["historical_snapshots"] = []
            
            tracking["historical_snapshots"].append({
                "date": datetime.date.today().isoformat(),
                "evolution_api_downloads": current_downloads,
                "auto_updated": True
            })
            
            print(f"  ✅ Evolution API: {current_downloads:,} downloads/mês")
        
        # Atualizar timestamp
        tracking["tracking_metadata"]["last_auto_update"] = datetime.datetime.now().isoformat()
        
        # Salvar tracking atualizado
        with open(tracking_file, 'w') as f:
            json.dump(tracking, f, indent=2, ensure_ascii=False)
        
        print("✅ Evolution tracking atualizado com sucesso")
    
    def generate_update_report(self) -> Dict[str, Any]:
        """
        Gera relatório das atualizações realizadas
        """
        report = {
            "update_timestamp": datetime.datetime.now().isoformat(),
            "script_version": "1.0.0",
            "updates_performed": [],
            "metrics_snapshot": {},
            "next_update_recommended": (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat()
        }
        
        # Carregar registry para métricas
        registry_file = self.indices_path / "repository-registry.json"
        if registry_file.exists():
            with open(registry_file, 'r') as f:
                registry = json.load(f)
                
                # Extrair métricas chave
                for repo_id, repo_data in registry["repositories"].items():
                    if "npm_stats" in repo_data:
                        report["metrics_snapshot"][repo_data["name"]] = {
                            "downloads": repo_data["npm_stats"]["monthly_downloads"],
                            "neural_weight": repo_data["neural_weight"]
                        }
        
        # Salvar relatório
        report_file = self.indices_path / f"update-report-{datetime.date.today().isoformat()}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def run_full_update(self):
        """
        Executa atualização completa do sistema neural
        """
        print("🧠 Iniciando atualização neural completa...")
        print("=" * 50)
        
        try:
            # 1. Atualizar repository registry
            self.update_repository_registry()
            
            # 2. Atualizar evolution tracking  
            self.update_evolution_tracking()
            
            # 3. Gerar relatório
            report = self.generate_update_report()
            
            print("=" * 50)
            print("✅ Atualização neural concluída com sucesso!")
            print(f"📊 Relatório salvo: update-report-{datetime.date.today().isoformat()}.json")
            
            return report
            
        except Exception as e:
            print(f"❌ Erro durante atualização: {e}")
            return None


def main():
    """
    Função principal do script
    """
    # Detectar se está rodando no contexto correto
    current_path = Path.cwd()
    
    # Procurar pelo diretório _repo_indices
    if not (current_path / "_repo_indices").exists():
        print("❌ Erro: Execute este script a partir do diretório raiz do repositório")
        print("   Certifique-se de que _repo_indices/ existe")
        return
    
    # Inicializar updater
    updater = NeuralRepoUpdater(str(current_path))
    
    # Executar atualização
    report = updater.run_full_update()
    
    if report:
        print("\\n📈 Métricas atualizadas:")
        for repo, metrics in report["metrics_snapshot"].items():
            if metrics.get("downloads", 0) > 0:
                print(f"  • {repo}: {metrics['downloads']:,} downloads/mês")


if __name__ == "__main__":
    main()
