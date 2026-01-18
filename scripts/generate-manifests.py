#!/usr/bin/env python3
"""
Skrypt generujący manifesty Kubernetes/ArgoCD
"""
import os
import yaml
import sys
from datetime import datetime


def generate_deployment_manifest(app_name, image_tag, namespace='default', replicas=2):
    """Generuje manifest Deployment dla Kubernetes"""
    deployment = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': app_name,
            'namespace': namespace,
            'labels': {
                'app': app_name,
                'version': image_tag
            }
        },
        'spec': {
            'replicas': replicas,
            'selector': {
                'matchLabels': {
                    'app': app_name
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'app': app_name,
                        'version': image_tag
                    }
                },
                'spec': {
                    'containers': [{
                        'name': app_name,
                        'image': f'{app_name}:{image_tag}',
                        'ports': [{
                            'containerPort': 5000,
                            'protocol': 'TCP'
                        }],
                        'env': [
                            {'name': 'APP_VERSION', 'value': image_tag},
                            {'name': 'ENVIRONMENT', 'value': os.getenv('ENVIRONMENT', 'production')},
                            {'name': 'PORT', 'value': '5000'}
                        ],
                        'resources': {
                            'requests': {
                                'memory': '128Mi',
                                'cpu': '100m'
                            },
                            'limits': {
                                'memory': '256Mi',
                                'cpu': '500m'
                            }
                        },
                        'livenessProbe': {
                            'httpGet': {
                                'path': '/',
                                'port': 5000
                            },
                            'initialDelaySeconds': 30,
                            'periodSeconds': 10
                        },
                        'readinessProbe': {
                            'httpGet': {
                                'path': '/',
                                'port': 5000
                            },
                            'initialDelaySeconds': 5,
                            'periodSeconds': 5
                        }
                    }]
                }
            }
        }
    }
    return deployment


def generate_service_manifest(app_name, namespace='default'):
    """Generuje manifest Service dla Kubernetes"""
    service = {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {
            'name': f'{app_name}-service',
            'namespace': namespace,
            'labels': {
                'app': app_name
            }
        },
        'spec': {
            'type': 'ClusterIP',
            'ports': [{
                'port': 80,
                'targetPort': 5000,
                'protocol': 'TCP',
                'name': 'http'
            }],
            'selector': {
                'app': app_name
            }
        }
    }
    return service


def generate_ingress_manifest(app_name, host, namespace='default'):
    """Generuje manifest Ingress dla Kubernetes"""
    ingress = {
        'apiVersion': 'networking.k8s.io/v1',
        'kind': 'Ingress',
        'metadata': {
            'name': f'{app_name}-ingress',
            'namespace': namespace,
            'annotations': {
                'kubernetes.io/ingress.class': 'nginx',
                'cert-manager.io/cluster-issuer': 'letsencrypt-prod'
            }
        },
        'spec': {
            'tls': [{
                'hosts': [host],
                'secretName': f'{app_name}-tls'
            }],
            'rules': [{
                'host': host,
                'http': {
                    'paths': [{
                        'path': '/',
                        'pathType': 'Prefix',
                        'backend': {
                            'service': {
                                'name': f'{app_name}-service',
                                'port': {
                                    'number': 80
                                }
                            }
                        }
                    }]
                }
            }]
        }
    }
    return ingress


def generate_argocd_application(app_name, repo_url, path, namespace='argocd', target_namespace='default'):
    """Generuje manifest ArgoCD Application"""
    application = {
        'apiVersion': 'argoproj.io/v1alpha1',
        'kind': 'Application',
        'metadata': {
            'name': app_name,
            'namespace': namespace,
            'finalizers': ['resources-finalizer.argocd.argoproj.io']
        },
        'spec': {
            'project': 'default',
            'source': {
                'repoURL': repo_url,
                'targetRevision': 'HEAD',
                'path': path
            },
            'destination': {
                'server': 'https://kubernetes.default.svc',
                'namespace': target_namespace
            },
            'syncPolicy': {
                'automated': {
                    'prune': True,
                    'selfHeal': True
                },
                'syncOptions': [
                    'CreateNamespace=true'
                ]
            }
        }
    }
    return application


def main():
    """Główna funkcja generująca manifesty"""
    app_name = os.getenv('APP_NAME', 'devops-app')
    image_tag = os.getenv('IMAGE_TAG', 'latest')
    namespace = os.getenv('NAMESPACE', 'default')
    repo_url = os.getenv('REPO_URL', 'https://github.com/user/repo.git')
    manifests_path = os.getenv('MANIFESTS_PATH', 'manifests')
    host = os.getenv('INGRESS_HOST', f'{app_name}.example.com')
    
    # Tworzenie katalogu na manifesty
    os.makedirs(manifests_path, exist_ok=True)
    
    # Generowanie manifestów
    deployment = generate_deployment_manifest(app_name, image_tag, namespace)
    service = generate_service_manifest(app_name, namespace)
    ingress = generate_ingress_manifest(app_name, host, namespace)
    argocd_app = generate_argocd_application(app_name, repo_url, manifests_path, target_namespace=namespace)
    
    # Zapis manifestów do plików
    with open(f'{manifests_path}/deployment.yaml', 'w') as f:
        yaml.dump(deployment, f, default_flow_style=False, sort_keys=False)
    
    with open(f'{manifests_path}/service.yaml', 'w') as f:
        yaml.dump(service, f, default_flow_style=False, sort_keys=False)
    
    with open(f'{manifests_path}/ingress.yaml', 'w') as f:
        yaml.dump(ingress, f, default_flow_style=False, sort_keys=False)
    
    with open(f'{manifests_path}/argocd-application.yaml', 'w') as f:
        yaml.dump(argocd_app, f, default_flow_style=False, sort_keys=False)
    
    print(f"✓ Wygenerowano manifesty w katalogu {manifests_path}/")
    print(f"  - deployment.yaml")
    print(f"  - service.yaml")
    print(f"  - ingress.yaml")
    print(f"  - argocd-application.yaml")


if __name__ == '__main__':
    try:
        import yaml
    except ImportError:
        print("Błąd: Brak biblioteki PyYAML. Zainstaluj: pip install pyyaml")
        sys.exit(1)
    
    main()

