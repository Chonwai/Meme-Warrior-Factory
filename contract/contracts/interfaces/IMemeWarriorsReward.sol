// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

/**
 * @title IMemeWarriorsReward
 * @dev Interface for the MemeWarriorsReward contract
 */
interface IMemeWarriorsReward {
    /**
     * @dev Emitted when a new battle is created
     */
    event BattleCreated(uint256 indexed battleId, uint256 team1Id, uint256 team2Id, uint256 startTime, uint256 endTime);
    
    /**
     * @dev Emitted when a user casts a vote
     */
    event VoteCast(address indexed user, uint256 indexed battleId, uint256 teamId);
    
    /**
     * @dev Emitted when a battle is ended
     */
    event BattleEnded(uint256 indexed battleId, uint256 winningTeamId);
    
    /**
     * @dev Emitted when a user claims rewards
     */
    event RewardDistributed(address indexed user, uint256 indexed battleId, uint256 amount);
    
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
    ) external;
    
    /**
     * @dev Cast a vote for a team in a battle
     * @param _battleId ID of the battle
     * @param _teamId ID of the team to vote for
     */
    function voteForTeam(uint256 _battleId, uint256 _teamId) external;
    
    /**
     * @dev End a battle and set the winning team
     * @param _battleId ID of the battle
     * @param _winningTeamId ID of the winning team
     */
    function endBattle(uint256 _battleId, uint256 _winningTeamId) external;
    
    /**
     * @dev Claim rewards for correct votes
     * @param _battleId ID of the battle to claim rewards for
     */
    function claimReward(uint256 _battleId) external;
    
    /**
     * @dev Get battle details
     * @param _battleId ID of the battle
     */
    function getBattle(uint256 _battleId) external view returns (
        uint256 team1Id,
        uint256 team2Id,
        uint256 startTime,
        uint256 endTime,
        uint256 winningTeamId,
        bool isEnded,
        uint256 totalVotes,
        uint256 rewardPool
    );
    
    /**
     * @dev Change the token address (in case of upgrades)
     * @param _newTokenAddress Address of the new token contract
     */
    function setTokenAddress(address _newTokenAddress) external;
} 