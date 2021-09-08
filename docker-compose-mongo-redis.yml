version: '3'

services:

  redis_db_sdk:
    container_name: redis_db_sdk
    image: redis:6-buster
    restart: unless-stopped
    ports:
      - '6379:6379'
    
  mongo_db_sdk:
    container_name: mongo_db_sdk
    image: mongo:4.2-bionic
    restart: unless-stopped
    volumes:
      - 'mongodata:/data/database'  
    ports:
      - '27017:27017'
    environment:
      - 'MONGO_DATABASE_NAME=${MONGO_DATABASE_NAME}'
      - 'MONGO_CONNECTION_STRING=${MONGO_CONNECTION_STRING}'
  

  mongo_express_sdk:
    container_name: mongo_express_sdk
    image: mongo-express
    restart: unless-stopped
    ports:
      - '8081:8081'
    environment:
      ME_CONFIG_MONGODB_SERVER: mongo_db_sdk
    depends_on: 
      - mongo_db_sdk



volumes:
  mongodata: null