# FastAPI 
FastAPI application that provides two endpoints for interacting with Weaviate: one for pushing data to Weaviate (/push_data_to_weaviate) and another for searching data (/search_data). Here's a brief summary of your code:

Data Format: You have a list of dictionaries (json_sets) representing pairs of questions and answers in English and Hindi.

FastAPI App: You've created a FastAPI application (app), and you define two endpoints:


Endpoints
```base
Push Data to Weaviate: POST /push_data_to_weaviate

Pushes data to Weaviate.
Update Data in Weaviate: POST /update_data_to_weaviate

Updates data in Weaviate.
Search Data in Weaviate: POST /search_data

Searches data in Weaviate based on a question and number.
Delete Data in Weaviate: POST /delete_data

Deletes a Weaviate class.

```
### Getting Started

   1. Clone the UI-Testing branch of this repository:
      ```bash
      git clone https://github.com/madgicaltechdom/jayant-sinha-chatbot

   2. Install the other requirements by running:
      
      Install requirements
      
      ```bash
      pip install -r requirements.txt
        sudo apt install uvicorn

      ```
Or
```bash
pip install python-dotenv
pip install sentence_transformers~=2.2.2
pip install torch==1.9.0
pip install weaviate-client
pip install uvicorn
```

### Project Structure
- Run the command:
    ```bash
         uvicorn app:app --reload

    ```

# Deploying to AWS EC2
Log into your AWS account and create an EC2 instance (t2.micro), using the latest stable Ubuntu Linux AMI.

SSH into the instance and run these commands to update the software repository and install our dependencies.
```bash
sudo apt-get update
sudo apt install -y python3-pip nginx
```
Clone the FastAPI server app (or create your main.py in Python).
```bash
      git clone https://github.com/madgicaltechdom/jayant-sinha-chatbot
```
Add the FastAPI configuration to NGINX's folder. Create a file called fastapi_nginx (like the one in this repository).
```bash
sudo vim /etc/nginx/sites-enabled/fastapi_nginx
```
And put this config into the file (replace the IP address with your EC2 instance's public IP):

```bash
Explain
server {
    listen 80;   
    server_name <YOUR_EC2_IP>;    
    location / {        
        proxy_pass http://127.0.0.1:8000;    
    }
}
```
Start NGINX.

```bash
sudo service nginx restart
Start FastAPI.
```
```bash
python3 -m uvicorn app:app

```
Update EC2 security-group settings for your instance to allow HTTP traffic to port 80.

Now when you visit your public IP of the instance, you should be able to access your API.


    
