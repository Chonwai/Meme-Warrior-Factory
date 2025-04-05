// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "../interfaces/IMemeWarriorsToken.sol";
import "../interfaces/IMemeWarriorsReward.sol";

/**
 * @title MemeWarriorsReward
 * @dev Reward system for the MemeWarriors game
 */
contract MemeWarriorsReward is IMemeWarriorsReward {
    IMemeWarriorsToken public token;
    address public owner;
    
    // Track battles and votes
    mapping(uint256 => Battle) public battles;
    mapping(address => mapping(uint256 => uint256)) public userVotes; // user -> battleId -> teamId
    mapping(uint256 => mapping(uint256 => uint256)) public teamVotes; // battleId -> teamId -> votes
    
    uint256 public battleCounter = 0;
    
    // Events
    event BattleCreated(uint256 indexed battleId, uint256 team1Id, uint256 team2Id, uint256 startTime, uint256 endTime);
    event VoteCast(address indexed user, uint256 indexed battleId, uint256 teamId);
    event BattleEnded(uint256 indexed battleId, uint256 winningTeamId);
    event RewardDistributed(address indexed user, uint256 indexed battleId, uint256 amount);
    
    struct Battle {
        uint256 team1Id;
        uint256 team2Id;
        uint256 startTime;
        uint256 endTime;
        uint256 winningTeamId;
        bool isEnded;
        uint256 totalVotes;
        uint256 rewardPool;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }
    
    constructor(address _tokenAddress) {
        token = IMemeWarriorsToken(_tokenAddress);
        owner = msg.sender;
    }
    
    /**
     * @dev Create a new battle between two teams
     * @param _team1Id ID of the first team
     * @param _team2Id ID of the second team
     * @param _startTime Start time of the battle
     * @param _duration Duration of the battle in seconds
     * @param _rewardPool Initial reward pool for the battle
     */
    function createBattle(
        uint256 _team1Id,
        uint256 _team2Id,
        uint256 _startTime,
        uint256 _duration,
        uint256 _rewardPool
    ) external override onlyOwner {
        require(_team1Id != _team2Id, "Teams must be different");
        require(_startTime > block.timestamp, "Start time must be in the future");
        require(_duration > 0, "Duration must be positive");
        require(_rewardPool > 0, "Reward pool must be positive");
        
        // Transfer tokens from owner to contract for rewards
        require(token.transferFrom(msg.sender, address(this), _rewardPool), "Failed to transfer reward tokens");
        
        uint256 battleId = battleCounter++;
        battles[battleId] = Battle({
            team1Id: _team1Id,
            team2Id: _team2Id,
            startTime: _startTime,
            endTime: _startTime + _duration,
            winningTeamId: 0,
            isEnded: false,
            totalVotes: 0,
            rewardPool: _rewardPool
        });
        
        emit BattleCreated(battleId, _team1Id, _team2Id, _startTime, _startTime + _duration);
    }
    
    /**
     * @dev Cast a vote for a team in a battle
     * @param _battleId ID of the battle
     * @param _teamId ID of the team to vote for
     */
    function voteForTeam(uint256 _battleId, uint256 _teamId) external override {
        Battle storage battle = battles[_battleId];
        
        require(!battle.isEnded, "Battle has ended");
        require(block.timestamp >= battle.startTime, "Battle has not started");
        require(block.timestamp < battle.endTime, "Battle has ended");
        require(_teamId == battle.team1Id || _teamId == battle.team2Id, "Invalid team");
        require(userVotes[msg.sender][_battleId] == 0, "Already voted");
        
        userVotes[msg.sender][_battleId] = _teamId;
        teamVotes[_battleId][_teamId]++;
        battles[_battleId].totalVotes++;
        
        emit VoteCast(msg.sender, _battleId, _teamId);
    }
    
    /**
     * @dev End a battle and set the winning team
     * @param _battleId ID of the battle
     * @param _winningTeamId ID of the winning team
     */
    function endBattle(uint256 _battleId, uint256 _winningTeamId) external override onlyOwner {
        Battle storage battle = battles[_battleId];
        
        require(!battle.isEnded, "Battle already ended");
        require(block.timestamp >= battle.endTime, "Battle not yet ended");
        require(_winningTeamId == battle.team1Id || _winningTeamId == battle.team2Id, "Invalid winning team");
        
        battle.winningTeamId = _winningTeamId;
        battle.isEnded = true;
        
        emit BattleEnded(_battleId, _winningTeamId);
    }
    
    /**
     * @dev Claim rewards for correct votes
     * @param _battleId ID of the battle to claim rewards for
     */
    function claimReward(uint256 _battleId) external override {
        Battle storage battle = battles[_battleId];
        
        require(battle.isEnded, "Battle not ended");
        require(userVotes[msg.sender][_battleId] == battle.winningTeamId, "Did not vote for winning team");
        
        // Calculate reward based on proportion of correct votes
        uint256 correctVotes = teamVotes[_battleId][battle.winningTeamId];
        uint256 reward = battle.rewardPool / correctVotes;
        
        // Reset user vote to prevent multiple claims
        userVotes[msg.sender][_battleId] = 0;
        
        // Transfer reward to user
        require(token.transfer(msg.sender, reward), "Failed to transfer reward");
        
        emit RewardDistributed(msg.sender, _battleId, reward);
    }
    
    /**
     * @dev Get battle details
     * @param _battleId ID of the battle
     */
    function getBattle(uint256 _battleId) external view override returns (
        uint256 team1Id,
        uint256 team2Id,
        uint256 startTime,
        uint256 endTime,
        uint256 winningTeamId,
        bool isEnded,
        uint256 totalVotes,
        uint256 rewardPool
    ) {
        Battle storage battle = battles[_battleId];
        return (
            battle.team1Id,
            battle.team2Id,
            battle.startTime,
            battle.endTime,
            battle.winningTeamId,
            battle.isEnded,
            battle.totalVotes,
            battle.rewardPool
        );
    }
    
    /**
     * @dev Change the token address (in case of upgrades)
     * @param _newTokenAddress Address of the new token contract
     */
    function setTokenAddress(address _newTokenAddress) external override onlyOwner {
        token = IMemeWarriorsToken(_newTokenAddress);
    }
} 