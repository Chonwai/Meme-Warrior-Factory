// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/IMemeWarriorsToken.sol";

/**
 * @title MemeWarriorsToken
 * @dev Main platform token for the MemeWarriors game
 */
contract MemeWarriorsToken is ERC20, ERC20Burnable, Ownable, IMemeWarriorsToken {
    constructor() ERC20("MemeWarriors", "MWAR") Ownable() {
        // Initial supply to contract deployer
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }

    /**
     * @dev Mint new tokens. Only callable by the contract owner.
     * @param to Address to mint tokens to
     * @param amount Amount of tokens to mint
     */
    function mint(address to, uint256 amount) public override onlyOwner {
        _mint(to, amount);
        emit Minted(to, amount);
    }

    /**
     * @dev Returns the number of decimals used by the token
     */
    function decimals() public view virtual override(ERC20, IMemeWarriorsToken) returns (uint8) {
        return 18;
    }

    /**
     * @dev Burns a specific amount of tokens.
     * Overrides both ERC20Burnable and IMemeWarriorsToken
     */
    function burn(uint256 amount) public virtual override(ERC20Burnable, IMemeWarriorsToken) {
        super.burn(amount);
    }

    /**
     * @dev Burns tokens from a specific account.
     * Overrides both ERC20Burnable and IMemeWarriorsToken
     */
    function burnFrom(address account, uint256 amount) public virtual override(ERC20Burnable, IMemeWarriorsToken) {
        super.burnFrom(account, amount);
    }
} 