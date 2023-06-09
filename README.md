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
| Etherscan API           | Offers a suite of APIs to access Ethereum blockchain data, including account information, transaction history, contract events, and token balances.    | JSON or CSV Response   |
| Chainlink API           | Provides access to decentralized oracle services, allowing smart contracts to retrieve real-world data from various sources and interact with off-chain systems. | JSON Response          |
| Infura API              | Offers a scalable and reliable API infrastructure that allows developers to connect to the Ethereum network without running their own Ethereum nodes.   | Varies based on method  |
| ArcherDAO API           | Offers a range of APIs for interacting with the ArcherDAO protocol, which provides gas-efficient and frontrunning-resistant transactions on Ethereum.     | JSON or CSV Response   |




