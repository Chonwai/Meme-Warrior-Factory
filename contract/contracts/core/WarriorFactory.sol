// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "../tokens/WarriorToken.sol";
import "../interfaces/IWarriorFactory.sol";
import "../interfaces/IWarriorToken.sol";

/**
 * @title WarriorFactory
 * @dev Contract for creating Meme Warrior tokens
 */
contract WarriorFactory is Ownable, IWarriorFactory {
    using Counters for Counters.Counter;
    
    Counters.Counter private _tokenIdCounter;
    
    // Platform fee percentage (in basis points, 100 = 1%)
    uint256 public platformFee = 500; // 5% initially
    
    // Address where platform fees are collected
    address public feeCollector;
    
    // Address of the battlefield (system wallet)
    address public battlefieldWallet;
    
    // Mapping from warrior ID to its metadata
    mapping(uint256 => WarriorMetadata) private _warriors;
    
    // Mapping from warrior ID to its token contract
    mapping(uint256 => address) private _warriorTokens;
    
    // Mapping of user's created warriors
    mapping(address => uint256[]) private _userWarriors;
    
    // Active warriors in battle
    mapping(uint256 => bool) private _activeWarriors;
    
    // Events
    event WarriorCreated(uint256 indexed warriorId, address indexed creator, address tokenAddress);
    event WarriorDeployed(uint256 indexed warriorId, uint256 amount);
    event WarriorRetired(uint256 indexed warriorId);
    event BattleEnded(uint256 indexed winnerId, uint256 indexed loserId, uint256 burnedAmount);
    
    struct WarriorMetadata {
        string name;
        string description;
        string imageURI;
        uint256 created;    // timestamp
        address creator;    // creator's address
        bool active;        // active status
    }
    
    modifier onlyBattlefield() {
        require(msg.sender == battlefieldWallet, "Caller is not the battlefield");
        _;
    }
    
    constructor() Ownable(msg.sender) {
        feeCollector = msg.sender;
        battlefieldWallet = msg.sender; // Default to owner, should be updated
    }
    
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
    ) external payable override returns (uint256) {
        require(_initialSupply > 0, "Initial supply must be positive");
        require(bytes(_name).length > 0, "Name cannot be empty");
        require(bytes(_symbol).length > 0, "Symbol cannot be empty");
        
        // Calculate platform fee
        uint256 fee = (msg.value * platformFee) / 10000;
        
        // Collect platform fee
        if (fee > 0) {
            payable(feeCollector).transfer(fee);
        }
        
        // Refund excess payment
        if (msg.value > fee) {
            payable(msg.sender).transfer(msg.value - fee);
        }
        
        // Create new warrior token
        WarriorToken newToken = new WarriorToken(_name, _symbol, address(this), _initialSupply);
        
        // Set the warrior factory and battlefield as authorized controllers
        newToken.setController(address(this), true);
        newToken.setController(battlefieldWallet, true);
        
        // Calculate token amounts (50% to creator, 50% to battlefield)
        uint256 halfSupply = _initialSupply / 2;
        uint256 battlefieldAmount = halfSupply * 10 ** newToken.decimals();
        uint256 creatorAmount = (_initialSupply - halfSupply) * 10 ** newToken.decimals();
        
        // Distribute tokens
        newToken.transfer(msg.sender, creatorAmount); // 50% to creator
        newToken.transfer(battlefieldWallet, battlefieldAmount); // 50% to battlefield
        
        // Increment and get the new token ID
        _tokenIdCounter.increment();
        uint256 warriorId = _tokenIdCounter.current();
        
        // Store warrior metadata
        _warriors[warriorId] = WarriorMetadata({
            name: _name,
            description: _description,
            imageURI: _imageURI,
            created: block.timestamp,
            creator: msg.sender,
            active: true
        });
        
        // Map warrior ID to token contract
        _warriorTokens[warriorId] = address(newToken);
        
        // Add to user's warriors
        _userWarriors[msg.sender].push(warriorId);
        
        emit WarriorCreated(warriorId, msg.sender, address(newToken));
        
        return warriorId;
    }
    
    /**
     * @dev Deploy warrior to battle
     * @param _warriorId ID of the warrior to deploy
     * @param _amount Amount of tokens to deploy
     */
    function deployWarrior(uint256 _warriorId, uint256 _amount) external override {
        require(_warriorTokens[_warriorId] != address(0), "Warrior does not exist");
        require(_warriors[_warriorId].active, "Warrior is not active");
        require(_amount > 0, "Amount must be positive");
        
        IWarriorToken token = IWarriorToken(_warriorTokens[_warriorId]);
        
        // Transfer tokens from user to battlefield wallet
        require(token.transferFrom(msg.sender, battlefieldWallet, _amount), "Transfer failed");
        
        // Mark warrior as active in battle
        _activeWarriors[_warriorId] = true;
        
        emit WarriorDeployed(_warriorId, _amount);
    }
    
    /**
     * @dev End a battle and burn loser tokens
     * @param _winnerWarriorId ID of the winning warrior
     * @param _loserWarriorId ID of the losing warrior
     * @param _burnAmount Amount of loser tokens to burn
     */
    function endBattle(uint256 _winnerWarriorId, uint256 _loserWarriorId, uint256 _burnAmount) external override onlyBattlefield {
        require(_warriorTokens[_winnerWarriorId] != address(0), "Winner warrior does not exist");
        require(_warriorTokens[_loserWarriorId] != address(0), "Loser warrior does not exist");
        require(_activeWarriors[_winnerWarriorId], "Winner warrior not in battle");
        require(_activeWarriors[_loserWarriorId], "Loser warrior not in battle");
        require(_burnAmount > 0, "Burn amount must be positive");
        
        // Get losing warrior token
        IWarriorToken loserToken = IWarriorToken(_warriorTokens[_loserWarriorId]);
        
        // Battlefield must have enough tokens to burn
        require(loserToken.balanceOf(battlefieldWallet) >= _burnAmount, "Not enough tokens to burn");
        
        // Burn tokens from the battlefield wallet
        loserToken.burnFrom(battlefieldWallet, _burnAmount);
        
        emit BattleEnded(_winnerWarriorId, _loserWarriorId, _burnAmount);
    }
    
    /**
     * @dev Retire a warrior from battle
     * @param _warriorId ID of the warrior to retire
     */
    function retireWarrior(uint256 _warriorId) external override {
        require(_warriorTokens[_warriorId] != address(0), "Warrior does not exist");
        require(_warriors[_warriorId].creator == msg.sender || owner() == msg.sender, "Not creator or owner");
        
        // Mark warrior as inactive
        _warriors[_warriorId].active = false;
        _activeWarriors[_warriorId] = false;
        
        emit WarriorRetired(_warriorId);
    }
    
    /**
     * @dev Get warrior metadata
     * @param _warriorId ID of the warrior
     */
    function getWarrior(uint256 _warriorId) external view override returns (
        string memory name,
        string memory description,
        string memory imageURI,
        uint256 created,
        address creator,
        bool active,
        address tokenAddress
    ) {
        require(_warriorTokens[_warriorId] != address(0), "Warrior does not exist");
        
        WarriorMetadata storage warrior = _warriors[_warriorId];
        
        return (
            warrior.name,
            warrior.description,
            warrior.imageURI,
            warrior.created,
            warrior.creator,
            warrior.active,
            _warriorTokens[_warriorId]
        );
    }
    
    /**
     * @dev Get a user's warriors
     * @param _user Address of the user
     */
    function getUserWarriors(address _user) external view override returns (uint256[] memory) {
        return _userWarriors[_user];
    }
    
    /**
     * @dev Set platform fee
     * @param _newFee New fee in basis points (100 = 1%)
     */
    function setPlatformFee(uint256 _newFee) external override onlyOwner {
        require(_newFee <= 1000, "Fee cannot exceed 10%");
        platformFee = _newFee;
    }
    
    /**
     * @dev Set fee collector address
     * @param _newCollector New fee collector address
     */
    function setFeeCollector(address _newCollector) external override onlyOwner {
        require(_newCollector != address(0), "Cannot set zero address");
        feeCollector = _newCollector;
    }
    
    /**
     * @dev Set battlefield wallet address
     * @param _newBattlefieldWallet New battlefield wallet address
     */
    function setBattlefieldWallet(address _newBattlefieldWallet) external override onlyOwner {
        require(_newBattlefieldWallet != address(0), "Cannot set zero address");
        battlefieldWallet = _newBattlefieldWallet;
    }
} 