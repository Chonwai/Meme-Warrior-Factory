// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/IWarriorToken.sol";

/**
 * @title WarriorToken
 * @dev ERC20 token for each Meme Warrior
 */
contract WarriorToken is ERC20, ERC20Burnable, Ownable, IWarriorToken {
    // Mapping of addresses that are allowed to control the token (burn others' tokens)
    mapping(address => bool) private _controllers;
    
    // Events
    event ControllerSet(address indexed controller, bool status);
    
    constructor(
        string memory name,
        string memory symbol,
        address initialOwner,
        uint256 initialSupply
    ) ERC20(name, symbol) Ownable() {
        _transferOwnership(initialOwner);
        _mint(initialOwner, initialSupply * 10 ** decimals());
    }
    
    /**
     * @dev Modifier to restrict function access to controllers
     */
    modifier onlyController() {
        require(_controllers[msg.sender] || msg.sender == owner(), "Caller is not a controller");
        _;
    }
    
    /**
     * @dev Set or remove an address as a controller
     * @param controller The address to set as controller
     * @param status True to add, false to remove
     */
    function setController(address controller, bool status) external override onlyOwner {
        require(controller != address(0), "Controller cannot be zero address");
        _controllers[controller] = status;
        emit ControllerSet(controller, status);
    }
    
    /**
     * @dev Check if an address is a controller
     * @param account The address to check
     * @return True if the address is a controller
     */
    function isController(address account) external view override returns (bool) {
        return _controllers[account];
    }
    
    /**
     * @dev Mint additional tokens. Only callable by owner.
     * @param to Address to mint tokens to
     * @param amount Amount of tokens to mint
     */
    function mint(address to, uint256 amount) external override onlyOwner {
        _mint(to, amount);
    }
    
    /**
     * @dev Burns tokens from a specific account. Only callable by controllers.
     * @param account Address to burn tokens from
     * @param amount Amount of tokens to burn
     */
    function burnFrom(address account, uint256 amount) public override(ERC20Burnable, IWarriorToken) onlyController {
        _spendAllowance(account, _msgSender(), amount);
        _burn(account, amount);
    }
    
    /**
     * @dev Burns a specific amount of tokens.
     * Overrides both ERC20Burnable and IWarriorToken
     */
    function burn(uint256 amount) public virtual override(ERC20Burnable, IWarriorToken) {
        super.burn(amount);
    }
    
    /**
     * @dev Override decimals function
     */
    function decimals() public view virtual override(ERC20, IWarriorToken) returns (uint8) {
        return 18;
    }
} 