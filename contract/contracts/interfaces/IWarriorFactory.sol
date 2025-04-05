// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

/**
 * @title IWarriorFactory
 * @dev Interface for the WarriorFactory contract
 */
interface IWarriorFactory {
    /**
     * @dev Emitted when a new warrior is created
     */
    event WarriorCreated(uint256 indexed warriorId, address indexed creator, address tokenAddress);
    
    /**
     * @dev Emitted when a warrior is deployed to battle
     */
    event WarriorDeployed(uint256 indexed warriorId, uint256 amount);
    
    /**
     * @dev Emitted when a warrior is retired from battle
     */
    event WarriorRetired(uint256 indexed warriorId);
    
    /**
     * @dev Emitted when a battle ends
     */
    event BattleEnded(uint256 indexed winnerId, uint256 indexed loserId, uint256 burnedAmount);
    
    /**
     * @dev Create a new Meme Warrior token
     * @param _name Token name
     * @param _symbol Token symbol
     * @param _description Warrior description
     * @param _imageURI URI to the warrior image
     * @param _initialSupply Initial token supply
     * @return tokenId The ID of the created warrior
     */
    function createWarrior(
        string memory _name,
        string memory _symbol,
        string memory _description,
        string memory _imageURI,
        uint256 _initialSupply
    ) external payable returns (uint256);
    
    /**
     * @dev Deploy warrior to battle
     * @param _warriorId ID of the warrior to deploy
     * @param _amount Amount of tokens to deploy
     */
    function deployWarrior(uint256 _warriorId, uint256 _amount) external;
    
    /**
     * @dev End a battle and burn loser tokens
     * @param _winnerWarriorId ID of the winning warrior
     * @param _loserWarriorId ID of the losing warrior
     * @param _burnAmount Amount of loser tokens to burn
     */
    function endBattle(uint256 _winnerWarriorId, uint256 _loserWarriorId, uint256 _burnAmount) external;
    
    /**
     * @dev Retire a warrior from battle
     * @param _warriorId ID of the warrior to retire
     */
    function retireWarrior(uint256 _warriorId) external;
    
    /**
     * @dev Get warrior metadata
     * @param _warriorId ID of the warrior
     */
    function getWarrior(uint256 _warriorId) external view returns (
        string memory name,
        string memory description,
        string memory imageURI,
        uint256 created,
        address creator,
        bool active,
        address tokenAddress
    );
    
    /**
     * @dev Get a user's warriors
     * @param _user Address of the user
     */
    function getUserWarriors(address _user) external view returns (uint256[] memory);
    
    /**
     * @dev Set platform fee
     * @param _newFee New fee in basis points (100 = 1%)
     */
    function setPlatformFee(uint256 _newFee) external;
    
    /**
     * @dev Set fee collector address
     * @param _newCollector New fee collector address
     */
    function setFeeCollector(address _newCollector) external;
    
    /**
     * @dev Set battlefield wallet address
     * @param _newBattlefieldWallet New battlefield wallet address
     */
    function setBattlefieldWallet(address _newBattlefieldWallet) external;
} 