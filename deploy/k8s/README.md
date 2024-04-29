#### Prerequisite 
1. K8s cluster 
2. kubectl configured 

#### Steps to Deploy Pebblo Server on k8s cluster
```
kubectl apply -f config.yaml
kubectl apply -f pvc.yaml 
kubectl apply -f deploy.yaml 
kubectl apply -f service.yaml 
```

#### Port forwading 
```
kubectl port-forward <pod-name>  <host-port>:<remote-port>
example - kubectl port-forward pebblo-api-cc9ffcf6d-ffjkc  8080:8000
```

Browse the local UI on http://localhost:<host-port>

example - http://localhost:8080

#### Run the sample RAG application

https://github.com/daxa-ai/pebblo/tree/main/pebblo_safeloader/langchain/acme-corp-rag 
