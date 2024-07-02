# Orchestration and Container Management with Kubernetes

## Container Orchestrator
I'd choose to use managed EKS and Argo over managing my own cluster for a few key reasons. Firstly, using EKS saves me from the operational complexities of setting up and maintaining my own Kubernetes control plane. This allows me to focus more on application development and deployment. Secondly, Argo, being a cloud-native workflow engine, integrates seamlessly with Kubernetes. It's designed for microservices-based workflows and has strong support for CI/CD pipelines, which makes it a more efficient and streamlined choice compared to Airflow.

## Step 0: Docker images
Even before instantiating EKS cluster, I'd create the necessary Dockerfiles for running specific python scripts. Each Docker image would be used in containers called by Argo. These Docker images should be registered on private container respoitory like AWS ECR, as they could be referenced and used later on.

### Step 1: Confiure EKS cluster
In AWS, EKS is the managed Kubernetes cluster service. We must configure a pool that will have the Argo client and other containers running, that will be always running. And also configure pools that will scale up and down according to what Argo orchestrates, called workers-pool for example. Depending on different workloads, we might need different pools with different min and max pod configuration.

### Step 2: Configure Argo on own pool
Argo is the kubernetes orchestrator that will trigger the creation of new container/pods as needed. The created pods will run specific tasks depending on their role, e.eg reading from db, running python script, writing to db, etc. For each role, there should be an specific Docker image to be retrieved from ECR.

### Step 3: Configure Postgres
Although I would not do this in a prod environment (due to Kubernetes not being designed for data persistence), there are no constraints on provisioning a container for running Postgres DB in this dev environment. Ideally, I'd use a managed DB service like RDS or amange my own EC2 for it.

### Step 4: Submit Argo Workflow definition
Similarly to Airflow's DAG definition, Argo has yaml configuration for defining Workflows. Each Workflow is very similar to Airflow DAG, except that it is the most suitable for working with Kubernetes due to inherent support parallelization over different pods, unlike Airflow. I'd write the Workflow definition - defining images to use etc.- and submit it to run on defined schedule.


## Logging and monitoring with Prometheus or Grafana
The big picture would be to integrate ArgoCD to our working repository - GitOps tool - and Helm Charts - Kubernetes ready-to-use application definitions - for both Prometheus and Grafana.
We would need to configure manifests for both - manifests are yaml declaration files - in our working repository.
ArgoCD seems to streamline the entire monitoring process by deploying Prometheus and Grafana to Kubernetes. Prometheus allows more robust metrics, and Grafana is the viz tool to monitor these metrics.

To be honest, I have never worked with these tools together, so I'll limit my answer to this more broad and general response. A more detailed answer could be provided if given more time.
