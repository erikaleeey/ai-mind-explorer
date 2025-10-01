docker-compose -f docker/docker-compose-test.yml up -d neo4j-test      
docker-compose -f docker/docker-compose-test.yml up -d  

cd backend
source venv/bin/activate
pip install -r requirements.txt
docker start neo4j-ai-mind-explorer 
python -m uvicorn main:app --reload

cd ../frontend
npm install 


issues
docker daemon not running:  open /Applications/Docker.app