// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title IWarriorToken
 * @dev Interface for the WarriorToken contract
 */
interface IWarriorToken is IERC20 {
    /**
     * @dev Set or remove an address as a controller
     * @param controller The address to set as controller
     * @param status True to add, false to remove
     */
    function setController(address controller, bool status) external;
    
    /**
     * @dev Check if an address is a controller
     * @param account The address to check
     * @return True if the address is a controller
     */
    function isController(address account) external view returns (bool);
    
    /**
     * @dev Mint additional tokens. Only callable by owner.
     * @param to Address to mint tokens to
     * @param amount Amount of tokens to mint
     */
    function mint(address to, uint256 amount) external;
    
    /**
     * @dev Burns tokens from a specific account. Only callable by controllers.
     * @param account Address to burn tokens from
     * @param amount Amount of tokens to burn
     */
    function burnFrom(address account, uint256 amount) external;
    
    /**
     * @dev Burns a specific amount of the caller's tokens
     * @param amount Amount of tokens to burn
     */
    function burn(uint256 amount) external;
    
    /**
     * @dev Returns the number of decimals used by the token
     */
    function decimals() external view returns (uint8);
} 