//SPDX-License-Identifier: MIT
pragma solidity 0.8.4;

import "./6_Token.sol";
import "./4_Reward.sol";

contract Donation {
    
    struct DonationRequest{
        address consumer;
        string name;
        uint256 budget;
        string description;
    }

    struct receivedDonation {
        address producer;
        uint256 bid;
    }

    CSToken private _token;
    DonationRequest[] private _donations;
    mapping (address => uint256) private _mintedPerAddress;
    mapping (address => mapping (string => mapping ( uint256 => address[]))) private _biddings;
    uint constant MINTLIMIT = 1000 * 10**18;

    event donationAddedSuccess(address consumer, string name, uint256 budget, string description);
    event donationPersistSuccess(address producer, address consumer, string name, uint256 minted);
    event deleteDonationSuccess(address consumer, string name);
    event biddingRequestSuccess(address consumer, string name, address bidder, uint256 budget);



    constructor (CSToken token) {
        _token = token;
    }


    function getDonation (address consumer_, string memory name_) external view returns (DonationRequest memory){
        require (keccak256(abi.encodePacked(name_)) != keccak256(abi.encodePacked("")), "Name must not be empty");
        for (uint256 i = 0; i < _donations.length; i++) {
            if (_donations[i].consumer == consumer_ && keccak256(abi.encodePacked(_donations[i].name)) == keccak256(abi.encodePacked(name_))) {
                return _donations[i];
            }
        }
        revert('Donation Request Not Found.');
    }

    function getDonations () external view returns (DonationRequest[] memory) {
        return _donations;
    }

    function getMintedPerAddress (address find_) external view returns (uint) {
        return _mintedPerAddress[find_];
    }

    function getMintLeft (address consumer_) public view returns (uint) {
        // calculate individual MintingCap
        uint timeDiffDays = (block.timestamp - _token.registered(consumer_)) / 60 / 60 / 24 ;
        // +1 to enable minting for the first day
        uint maxMint = ((timeDiffDays / 30) + 1) * MINTLIMIT;
        uint mintLeft = maxMint - _mintedPerAddress[consumer_];
        return mintLeft;
    }


    function addDonation(address consumer_, string memory name_, uint256 budget_, string memory description_) external {
        require (keccak256(abi.encodePacked(name_)) != keccak256(abi.encodePacked("")), "Name must not be empty");
        require (msg.sender == consumer_, "Only the consumer can add a donation himself");
        require (_token.registered(msg.sender) != 0, "Msg.Sender must be a registered Consumer");
        
        uint mintLeft = getMintLeft(consumer_);
        require(mintLeft >= budget_, "Address has not enough MintingCap left for this donationRequest");

        // check if donation already exists and update it
        bool wasReplaced = false;
        for (uint256 i = 0; i < _donations.length; i++) {
            if (_donations[i].consumer == consumer_ && keccak256(abi.encodePacked(_donations[i].name)) == keccak256(abi.encodePacked(name_))) {
                deleteDonation(consumer_, name_);
                _donations.push(DonationRequest(consumer_, name_, budget_, description_));
                wasReplaced = true;
                break;
            }
        }
        if (!wasReplaced){
            _donations.push(DonationRequest(consumer_, name_, budget_, description_));
        }
        
        _mintedPerAddress[consumer_] = _mintedPerAddress[consumer_] + budget_;

        emit donationAddedSuccess(consumer_, name_, budget_, description_);
    }

    function deleteDonation (address consumer_, string memory name_) public {
        require (keccak256(abi.encodePacked(name_)) != keccak256(abi.encodePacked("")), "Name must not be empty");
        require (msg.sender == consumer_, "Only the consumer can delete the donation");
        
        for (uint256 i = 0; i < _donations.length; i++) {
            if (_donations[i].consumer == consumer_ && keccak256(abi.encodePacked(_donations[i].name)) == keccak256(abi.encodePacked(name_))) {
                _mintedPerAddress[consumer_] -= _donations[i].budget;
                _donations[i] = _donations[_donations.length-1];
                _donations.pop();

                emit deleteDonationSuccess(consumer_, name_);
                return;
            }
        }
        revert('Donation Request Not Found.');
    }


    function bidOnDonationRequest(address consumer_, string memory name_, uint256 bid_) external {
        require (keccak256(abi.encodePacked(name_)) != keccak256(abi.encodePacked("")), "Name must not be empty");
        require (msg.sender != consumer_, "You can't bid on your own donation request");
        require (bid_ > 0, "The bid must be greater than 0");   

        uint256 donationPrice = 0;
        bool hasRequest = false;
        for (uint256 i = 0; i < _donations.length; i++) {
            if (_donations[i].consumer == consumer_ && keccak256(abi.encodePacked(_donations[i].name)) == keccak256(abi.encodePacked(name_))) {
                donationPrice = _donations[i].budget;
                hasRequest = true;
                break;
            }
        }
        require (hasRequest, "The donation request doesn't exist");
        require (bid_ <= donationPrice, "The bid must be equal or lower than the donation budget");
        
        _biddings[consumer_][name_][bid_].push(msg.sender);
        emit biddingRequestSuccess(consumer_, name_, msg.sender, bid_);
    } 


    function persistDonation(address consumer_, string memory name_, address rewardSmartContractAddress, receivedDonation[] memory toPersist_) external {
        require (keccak256(abi.encodePacked(name_)) != keccak256(abi.encodePacked("")), "Name must not be empty");
        require (msg.sender == consumer_, "Only the consumer can persist a donation");
        require (toPersist_.length > 0, "You must persist at least one donation");
        require (_token.registered(msg.sender) != 0, "Msg.Sender must be a registered Consumer");
        
        bool wasFound;
        uint256 i = 0;
        for (; i < _donations.length; i++) {
            if (_donations[i].consumer == consumer_ && keccak256(abi.encodePacked(_donations[i].name)) == keccak256(abi.encodePacked(name_))) {
                wasFound = true;
                break;
            }
        }
        if (!wasFound){
            revert('DonationRequest not Found');
        }

        //check if producer has a bid on this donation request
        for (uint256 j = 0; j < toPersist_.length; j++) {
            bool inBiddings = false;
            for (uint256 k = 0; k < _biddings[consumer_][name_][toPersist_[j].bid].length; k++) {
                if (_biddings[consumer_][name_][toPersist_[j].bid][k] == toPersist_[j].producer) {
                    inBiddings = true;
                    break;                
                }
            }
            require (inBiddings, "The producer must have bid on this donation request");
        }

        //sort all donations by bid with bubble sort
        for (uint256 j = 0; j < toPersist_.length; j++) {
            for (uint256 k = j+1; k < toPersist_.length; k++) {
                if (toPersist_[j].bid > toPersist_[k].bid) {
                    receivedDonation memory temp = toPersist_[j];
                    toPersist_[j] = toPersist_[k];
                    toPersist_[k] = temp;
                }
            }
        }

        //check if bids are in ascending order
        for (uint256 j = 0; j < toPersist_.length-1; j++) {
            if (toPersist_[j].bid > toPersist_[j+1].bid) {
                revert('The bids must be in ascending order');
            }
        }
        
        //mint the bids as long as the budget is not exceeded
        uint256 oldSupply = _token.totalSupply();
        // to avoid dividing by 0
        if (oldSupply == 0) {
            oldSupply++;
        }
        for (uint256 j = 0; j < toPersist_.length; j++) {
            if (_donations[i].budget <= toPersist_[j].bid) {
                _token.mint(msg.sender, toPersist_[j].producer, _donations[i].budget);
                _donations[i].budget = 0;
                emit donationPersistSuccess(toPersist_[j].producer, consumer_, name_, _donations[i].budget);
                deleteDonation(consumer_, name_);
                break;
            }
            _token.mint(msg.sender, toPersist_[j].producer, toPersist_[j].bid);
            _donations[i].budget -= toPersist_[j].bid;
            
            emit donationPersistSuccess(toPersist_[j].producer, consumer_, name_, toPersist_[j].bid);
        }
        
        // Dreisatz - multiply by 100 for .2 floating precision 
        uint256 inflationRate = ( (_token.totalSupply() * 100 * 100) / oldSupply ) - 10000; 
        RewardsDistribution reward = RewardsDistribution(rewardSmartContractAddress);
        reward.increaseInflation(inflationRate);
    
    }
}