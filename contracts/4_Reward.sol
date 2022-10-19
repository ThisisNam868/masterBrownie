//SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

import "./6_Token.sol";

contract RewardsDistribution {
    
    struct Reward {
        address consumer;
        string name;
        uint256 price;
        uint256 amount;
        string accessUrl;
        string description;
        uint256 demand;
    }

    CSToken private _token;
    Reward[] private _rewards;
    mapping(address => Reward[]) private buyers;
    uint256 private _counterExecs = 0;

    event rewardAddedSuccess(address consumer, string name, uint256 price, uint256 amount, string description);
    event deleteRewardSuccess(address consumer, string name);
    event rewardBuySuccess(address provider, address consumer, string rewardName, uint256 rewardPrice, string rewardUrl);


    constructor (CSToken token) {
        _token = token;
    }

    function getReward (address consumer_, string memory name_) external view returns (Reward memory){
        for (uint256 i = 0; i < _rewards.length; i++) {
            if (_rewards[i].consumer == consumer_ && keccak256(abi.encodePacked(_rewards[i].name)) == keccak256(abi.encodePacked(name_))) {
                return _rewards[i];
            }
        }
        revert('Reward not found.');
    }

    function getRewards () external view returns (Reward[] memory) {
        return _rewards;
    }

    function getbuyer (address buyer) external view returns (Reward[] memory) {
        return buyers[buyer];
    }


    function addReward(address consumer_, string memory name_, uint256 price_, uint256 amount_, string memory accessUrl_, string memory description_) external returns (bool) {
        require (keccak256(abi.encodePacked(name_)) != keccak256(abi.encodePacked("")), "Name must not be empty");
        require (msg.sender == consumer_, "Only the provider can add a reward");
        require (amount_ > 0, "Amount must be greater than 0");

        bool wasReplaced = false;
        for (uint256 i = 0; i < _rewards.length; i++) {
            if (_rewards[i].consumer == consumer_ && keccak256(abi.encodePacked(_rewards[i].name)) == keccak256(abi.encodePacked(name_))) {
                _rewards[i] = Reward(consumer_, name_, price_, amount_, accessUrl_, description_, 0);
                wasReplaced = true;
                break;
            }
        }

        if (!wasReplaced){
            _rewards.push(Reward(consumer_, name_, price_, amount_, accessUrl_, description_, 0));

        }

        // register as Consumer
        _token.addRegistered(consumer_);

        emit rewardAddedSuccess(consumer_, name_, price_, amount_, description_);
        return true;
    }

    function deleteReward (address consumer_, string memory name_) external {
        require (keccak256(abi.encodePacked(name_)) != keccak256(abi.encodePacked("")), "Name must not be empty");
        require (msg.sender == consumer_, "Only the provider can delete the reward");
        
        for (uint256 i = 0; i < _rewards.length; i++) {
            if (_rewards[i].consumer == consumer_ && keccak256(abi.encodePacked(_rewards[i].name)) == keccak256(abi.encodePacked(name_))) {
                _rewards[i] = _rewards[_rewards.length-1];
                _rewards.pop();

                if (!hasConsumerActiveRewards(consumer_)){
                    _token.deleteRegistered(consumer_);
                }

                emit deleteRewardSuccess(consumer_, name_);
                return;
            }
        }
        revert('Reward not found.');
    }

    function hasConsumerActiveRewards (address consumer_) internal view returns (bool) {
        for (uint256 i = 0; i < _rewards.length; i++) {
            if (_rewards[i].consumer == consumer_) {
                return true;
            }
        }
        return false;
    }


    function buyReward(address consumer_, string memory name_) external {
        require (keccak256(abi.encodePacked(name_)) != keccak256(abi.encodePacked("")), "Name must not be empty");
        
        Reward memory reward;
        bool wasFound;
        uint256 i = 0;
        for (; i < _rewards.length; i++) {
            if (_rewards[i].consumer == consumer_ && keccak256(abi.encodePacked(_rewards[i].name)) == keccak256(abi.encodePacked(name_))) {
                reward = _rewards[i];
                wasFound = true;
                break;
            }
        }
        if (!wasFound){
            revert('Requested Reward not Found');
        }

        uint256 oldBalance = _token.balanceOf(msg.sender);
        uint256 oldSupply = _token.totalSupply();
        if (oldSupply == 0){
            oldSupply++;
        }
        _token.transferFrom(msg.sender, consumer_, reward.price);
        require(_token.balanceOf(msg.sender) == oldBalance - reward.price, "Not the correct Reward price was deducted from balance"); 

        // adjust Inflation because of burning Tokens
        uint256 inflationRate = 10000 - ( (_token.totalSupply() * 100 * 100) / oldSupply ); 
        decreaseInflation(inflationRate);

        // save buyer in adress List
        buyers[msg.sender].push(reward);

        // emit rewardURL in an event
        emit rewardBuySuccess(msg.sender, reward.consumer, reward.name, reward.price, reward.accessUrl);

        // decrese amount
        // increase demand
        _rewards[i].demand++;
        _rewards[i].amount--;
        if (_rewards[i].amount == 0){
            _rewards[i] = _rewards[_rewards.length-1];
            _rewards.pop();

            if (!hasConsumerActiveRewards(consumer_)){
                _token.deleteRegistered(consumer_);
            }
        }
        
        // dynamic Pricing
        _counterExecs++;
        if (_counterExecs == 10){
            for (uint j = 0; j < _rewards.length; j++) {
                _rewards[j].price = dynamicPrice(_rewards[j].price, _rewards[j].demand);
                _rewards[j].demand = 0;
            }
        }
    }

    function dynamicPrice (uint256 price, uint256 demand) internal pure returns (uint256) {
        if (demand == 0){
            return price * 90 / 100;
        }
        return (price + (price * demand / 10)); 
    }

    function increaseInflation(uint256 inflationRate) public {
        for (uint i = 0; i < _rewards.length; i++) {
            // /10000 - um den Faktor aus Donation wieder rückgängig zu machen; /100 - um auf decimal Stelle (Dreisatz) zu kommen
            _rewards[i].price = _rewards[i].price + ( (_rewards[i].price * inflationRate) / 10000 );
        }
    }

    function decreaseInflation(uint256 inflationRate) public {
        for (uint i = 0; i < _rewards.length; i++) {
            // /10000 - um den Faktor aus Donation wieder rückgängig zu machen; /100 - um auf decimal Stelle (Dreisatz) zu kommen
            _rewards[i].price = _rewards[i].price - ( (_rewards[i].price * inflationRate) / 10000 );
        }
    }

}