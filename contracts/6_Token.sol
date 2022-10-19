// SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

import "../OpenZeppelin/openzeppelin-contracts@4.7.3/contracts/token/ERC20/ERC20.sol";
import "../OpenZeppelin/openzeppelin-contracts@4.7.3/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "../OpenZeppelin/openzeppelin-contracts@4.7.3/contracts/access/Ownable.sol";

contract CSToken is ERC20, ERC20Burnable {
    mapping(address => uint) public registered; 

    event mintedSuccess (address receiver, uint256 amount);
    event deleteRegisterSuccess(address consumer);
    event addRegisterSuccess(address consumer);

    constructor(address receiver, uint256 amount) ERC20("CSToken", "CST"){
        _mint(receiver, amount);
    }

    function getRegistered (address consumer) external view returns (bool) {
        if (registered[consumer] != 0){
            return true;
        } else {
            return false;
        }
    }

    function mint(address originalCaller, address to, uint256 amount) external  returns (uint256) {
        require(registered[originalCaller] != 0, "Only registered Consumers can mint Tokens");
        _mint(to, amount);

        emit mintedSuccess(to, amount);
        return amount;
    }

    function _transfer(address from, address to, uint256 value) internal override {
        if (registered[to] != 0){
            burnFrom(from, value);
            return;
        }
        super._transfer(from, to, value);
    }

    function addRegistered(address newReg) external {
        registered[newReg] = block.timestamp;

        emit addRegisterSuccess(newReg);
    }

    function deleteRegistered(address newReg) external {
        registered[newReg] = 0;

        emit deleteRegisterSuccess(newReg);
    } 
}
