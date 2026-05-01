## 📄 Lab 5 – Local Serverless Event-Driven Image Processing Pipeline

---

## 📌 Overview
This lab implements a **local serverless-style event-driven system** for image processing using Docker containers only (no cloud services).

The system simulates how real-world cloud-native pipelines work using:
- Event-driven architecture  
- Message passing (via Redis)  
- Microservices separation  
- Asynchronous processing  

---

## 🏗️ Architecture

The system consists of the following components:

- **Event Source** → Detects new images in `data/input`  
- **Event Router** → Receives events and routes them  
- **Image Processor** → Processes the image (resize / grayscale)  
- **Notifier** → Sends completion logs  
- **Redis** → Acts as the event broker  

---

## 📂 Project Structure

Lab5/

├── docker-compose.yml

├── data/

│ ├── input/

│ └── output/

├── event_source/

├── router/

├── functions/

│ ├── image_resizer/

│ └── notifier/

├── screenshots/

└── README.md


---

## ⚙️ How to Run

### 1️⃣ Build services
```
docker compose build
```

### 2️⃣ Run the system
```
docker compose up
```

### 3️⃣ Add an image
Place any image inside:
```
data/input/
```


The system will automatically:
- detect the image  
- process it  
- save output in `data/output/`  

---

## 📸 Screenshots

### 🔹 Running Containers
All services are up and running successfully.

![Running Containers](screenshots/01_containers_running.png)

---

### 🔹 Event Router Logs
Shows the event-driven pipeline flow from image upload to processing and notification.

![Event Logs](screenshots/02_event_router_logs.png)

---

### 🔹 Docker Build Process
All services are successfully built using Docker.

![Docker Build](screenshots/03_docker_build.png)

---

### 🔹 Output Image Result
Processed image generated successfully (before vs after).

![Output Result](screenshots/04_output_result.png)

---

## 🔍 Reflection

### ❓ What is event-driven architecture?
It is a design where services communicate through events instead of direct calls, making systems more scalable and loosely coupled.

---

### ❓ How does this simulate serverless?
Each component acts like an independent function triggered by events, similar to serverless functions (e.g., AWS Lambda), but running locally.

---

### ❓ Why use Redis?
Redis acts as a lightweight message broker to pass events between services efficiently.

---

### ❓ Benefits of this approach
- Decoupled services  
- Scalable design  
- Fault tolerance  
- Real-time processing  

---

## ✅ Conclusion
This lab demonstrates how modern cloud-native systems use event-driven architecture to process data asynchronously, even without using actual cloud services.

This implementation reflects real-world serverless pipelines used in modern cloud platforms, adapted to run locally using containerized services.
