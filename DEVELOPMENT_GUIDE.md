# Deployment Guide

## Prerequisites:
- Azure account with AKS permissions
- GitHub account
- Docker installed on your local machine
- kubectl installed on your local machine
- Azure CLI installed on your local machine

## Set up GitHub Container Registry:
1. In your GitHub account, go to **Settings > Developer settings > Personal access tokens**
2. Generate a new token with `read:packages` and `write:packages` permissions
3. Save this token securely

## Build and push your Docker image:
1. Login to GitHub Container Registry:
   ```sh
   echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
   ```
2. Build your Docker image:
   ```sh
   docker build -t ghcr.io/USERNAME/rag-backend:latest .
   ```
3. Push the image:
   ```sh
   docker push ghcr.io/USERNAME/rag-backend:latest
   ```

## Set up AKS:
1. Login to Azure CLI:
   ```sh
   az login
   ```
2. Create a resource group:
   ```sh
   az group create --name myResourceGroup --location eastus
   ```
3. Create AKS cluster:
   ```sh
   az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 3 --enable-addons monitoring --generate-ssh-keys
   ```
4. Get credentials for kubectl:
   ```sh
   az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
   ```

## Create Kubernetes Secret:
1. Create a file named `rag-secrets.yaml`:
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: rag-secrets
   type: Opaque
   stringData:
     PG_DATABASE_URL: "your-database-url"
     SECRET_KEY: "your-secret-key"
     ALGORITHM: "HS256"
     ACCESS_TOKEN_EXPIRE_MINUTES: "30"
     AWS_ACCESS_KEY_ID: "your-aws-access-key"
     AWS_SECRET_ACCESS_KEY: "your-aws-secret-key"
     S3_BUCKET_NAME: "your-s3-bucket-name"
     PINECONE_API_KEY: "your-pinecone-api-key"
     UNSTRUCTURED_API_KEY: "your-unstructured-api-key"
     GOOGLE_API_KEY: "your-google-api-key"
   ```
2. Apply the secret:
   ```sh
   kubectl apply -f rag-secrets.yaml
   ```

## Deploy your application:
1. Apply the deployment:
   ```sh
   kubectl apply -f deployment.yaml
   ```
2. Apply the service:
   ```sh
   kubectl apply -f service.yaml
   ```

## Check the deployment:
1. Check pods:
   ```sh
   kubectl get pods
   ```
2. Check service:
   ```sh
   kubectl get services
   ```

## Access your application:
1. Get the external IP of your LoadBalancer service:
   ```sh
   kubectl get services
   ```
2. Use this IP to access your application: `https://<EXTERNAL-IP>`

## Monitoring and logging:
- You can use Azure Monitor and Log Analytics, which are integrated with AKS

## Scaling:
- To scale your deployment:
  ```sh
  kubectl scale deployment rag-backend --replicas=5
  ```