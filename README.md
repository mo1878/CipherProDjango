## CipherPro
CipherPro 0 is the First Iteration of the MEV bot.

### Project Setup
The project will be split into two parts:

- API Interaction Layer (Data Collection)
- Web3 and Crypto Layer (Transaction Logic)

### API Interaction Layer

This layer will handle the logic of data collection from the various API's endpoints required to power the Web3 Layer.

#### The APIs required:

| API                     | Description                                                                                                                                     | Data Type              |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|------------------------|
| Ethereum JSON-RPC API   | Provides a remote procedure call (RPC) interface to interact with Ethereum nodes, allowing developers to query blockchain data and execute transactions. | JSON-RPC Response      |
| Flashbots API           | Enables users to submit bundles of transactions directly to miners to improve transaction execution strategies and mitigate the impact of front-running. | JSON-RPC Request       |
| Etherscan API           | **Offers a suite of APIs to access Ethereum blockchain data, including account information, transaction history, contract events, and token balances.**    | JSON or CSV Response   |
| Chainlink API           | **Provides access to decentralized oracle services, allowing smart contracts to retrieve real-world data from various sources and interact with off-chain systems.** | JSON Response          |
| Infura API              | Offers a scalable and reliable API infrastructure that allows developers to connect to the Ethereum network without running their own Ethereum nodes.   | Varies based on method  |
| ArcherDAO API           | Offers a range of APIs for interacting with the ArcherDAO protocol, which provides gas-efficient and frontrunning-resistant transactions on Ethereum.     | JSON or CSV Response   |

# System Design

## Components
  Backend (Django) - This part of the system is responsible for connecting to the API, retrieving the real-time data and sending it to the front end.
  Frontend (Vanilla JS) - Renders the data received from the back end updates the UI in real-time

## Flow of Information 



### API Methodology

- There are multiple ways to connect to an API and extract data from it.
- The traditional method is using the **request-response model**:
  - This is where a server OR a client sends a request to an API endpoint.
  - Once the endpoint recieves request, it'll send a response back confirming whether the request was processed successfully or not.
  - This method is usually sufficient to power applications, however it is not ideal for real-time data streaming
- The other method is to establish something called a **WebSocket** connection.
  - This method establishes a bidirectional connection between two nodes i.e. a Client - Server **OR** a Server - API.
  - This connection can be established and can stay open for as long as required or until it is terminated.
  - This can allow real-time data streaming from endpoints that tolerate WebSocket connections.


For this project it is obvious to me that it will require real-time data streaming OR close to real-time data streaming.
Furthermore, as there will be multiple API endpoint connections, I will be implementing Asynchronous functions such that multiple API calls can be made in parallel and are non-blocking. 

# Websockets + Django Channels

- We'll open up a connection on the client side using Websockets
- We will use Django channels on the server side to send and recieve requests back to the client

## 4 Steps To do Successfully

  1. Configure ASGI
  2. Build out Consumers
  3. Deal with routing to those consumers
  4. JS Websocket API to initiate the handshake and create a connection between the client and the server


## Django Backend + React Front End

  - The backend of the application will be in Django 
  - The Front End of the application will be in React
  - The back-end ASGI server is connected to the react front end through the websocket connection created by my django consumer.
  - This will allow me to do some processing on the client side where there is a heavy dependency on web3 javascript libraries.
  - Therefore the django back end is being used as a websocket api route to the INFURA API

## Next Steps

  - The next steps in this are as follows:
    - Decipher the input to the Router contract - Retrieve the transaction slippage through this
    - Get the Router contract ABI (Metadata) in order to decipher the inputs to the contract.
    - Output the relevant data from the pending transaction itself.
    - Connect to the chainlink API for real-time gas prices.


  - Etherscan API for cross referencing addresses when monitoring other transactions AND for checking whether or not our transactions have gone through.
  - Chainlink API for real time stream of Gas prices but can also be extracted from etherscan.
  


