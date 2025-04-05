// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title IMemeWarriorsToken
 * @dev Interface for the MemeWarriorsToken contract
 */
interface IMemeWarriorsToken is IERC20 {
    /**
     * @dev Emitted when tokens are minted
     */
    event Minted(address indexed to, uint256 amount);
    
    /**
     * @dev Mint new tokens. Only callable by the contract owner.
     * @param to Address to mint tokens to
     * @param amount Amount of tokens to mint
     */
    function mint(address to, uint256 amount) external;
    
    /**
     * @dev Burns a specific amount of the caller's tokens
     * @param amount Amount of tokens to burn
     */
    function burn(uint256 amount) external;
    
    /**
     * @dev Burns tokens from a specific account
     * @param account Address to burn tokens from
     * @param amount Amount of tokens to burn
     */
    function burnFrom(address account, uint256 amount) external;
    
    /**
     * @dev Returns the number of decimals used by the token
     */
    function decimals() external view returns (uint8);
} 