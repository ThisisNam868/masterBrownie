def test_upload_u1(CSToken, RewardsDistribution, accounts):
    # 1. deploy the contract with initial mint
    citiSci = CSToken.deploy(accounts[1], 100 *10**18, {'from': accounts[0]})
    reward = RewardsDistribution.deploy(citiSci.address, {'from': accounts[0]})
    print("CSToken Contract was deployed to:", citiSci.address)
    print("RewardDistribution Contract was deployed to:", reward.address)
    print(100 *10**18, "CSTokens were minted to account 1")
    print("total Supply: ", citiSci.totalSupply())

    # 2. Different Accounts add rewards to the list
    reward.addReward(accounts[1], "reward A", 11 *10**18, 1, "https://name1.access.com", "Description for reward Item 1", {'from': accounts[1]})
    reward.addReward(accounts[1], "reward B", 11 *10**18, 1, "https://name1.access.com", "Description for reward Item 2", {'from': accounts[1]})
    reward.addReward(accounts[2], "reward C", 22 *10**18, 2, "https://name1.access.com", "Description for reward Item 3", {'from': accounts[2]})
    print("Account 1", accounts[1], "added", reward.getReward(accounts[1], "reward A")["name"] ,"to the list")
    print("Account 1", accounts[1], "added", reward.getReward(accounts[1], "reward B")["name"] ,"to the list")
    print("Account 2", accounts[2], "added", reward.getReward(accounts[2], "reward C")["name"] ,"to the list")
    print("Is Account 1 registered as consumer?", citiSci.registered(accounts[1]))
    print("Is Account 2 registered as consumer?", citiSci.registered(accounts[2]))
    print("show all rewards")
    rewards = reward.getRewards()
    counter = 1
    for i in rewards:
        print(counter, "-", i[0],i[1])	
        counter += 1

    # 3. Delete Rewards and check Registered Status
    reward.deleteReward(accounts[1], "reward A", {'from': accounts[1]})
    print("reward A by Account 1 is deleted")
    print("Is Account 1 registered as consumer?", citiSci.getRegistered(accounts[1]))
    reward.deleteReward(accounts[1], "reward B", {'from': accounts[1]})
    print("name2 by consumer 1 is deleted")
    print("Is", accounts[1], "registered as consumer?", citiSci.getRegistered(accounts[1]))

    assert citiSci.getRegistered(accounts[1]) == False


def test_upload_u2(CSToken, RewardsDistribution, Donation, accounts):
    # 1. Deploy Contracts
    citiSci = CSToken.deploy(accounts[1], 100 *10**18, {'from': accounts[0]})
    reward = RewardsDistribution.deploy(citiSci.address, {'from': accounts[0]})
    donation = Donation.deploy(citiSci.address, {'from': accounts[0]})
    print("CSToken Contract was deployed to:", citiSci.address)
    print("RewardDistribution Contract was deployed to:", reward.address)
    print("Donation Contract was deployed to:", reward.address)
    print(100 *10**18, "CSTokens were minted to account 1")
    print("total Supply: ", citiSci.totalSupply())

    # 2. Adding Reward and Donation Request to the list
    reward.addReward(accounts[1], "reward A", 11 *10**18, 101, "https://name1.access.com", "Description for reward A", {'from': accounts[1]})
    print("Reward A added to the list by", accounts[1])
    donation.addDonation(accounts[1], "donation request B", 12 *10**18, "descrption of donation request B", {'from': accounts[1]})
    print(f"Donation Request B added to the list. Budget {donation.getDonation(accounts[1], 'donation request B')['budget']} - by Account 1 ({accounts[1]})")

    assert donation.getDonation(accounts[1], "donation request B")["budget"] == 12 *10**18


def test_reward_u3_single(CSToken, RewardsDistribution, accounts):
    # 1. Deploy Contracts
    citiSci = CSToken.deploy(accounts[1], 100 *10**18, {'from': accounts[0]})
    reward = RewardsDistribution.deploy(citiSci.address, {'from': accounts[0]})
    print("CSToken Contract was deployed to:", citiSci.address)
    print("RewardDistribution Contract was deployed to:", reward.address)
    print(100 *10**18, "CSTokens were minted to account 1")
    print("total Supply: ", citiSci.totalSupply())

    # 2. Different Accounts add rewards to the list
    print("Gas Used for addReward after 1 execution", reward.addReward(accounts[1], "reward A", 11, 2, "https://name1.access.com", "Description for reward Item 1", {'from': accounts[1]}).gas_used)


def test_reward_u3_hundred(CSToken, RewardsDistribution, accounts):
    # 1. Deploy Contracts
    citiSci = CSToken.deploy(accounts[1], 100 *10**18, {'from': accounts[0]})
    reward = RewardsDistribution.deploy(citiSci.address, {'from': accounts[0]})
    print("CSToken Contract was deployed to:", citiSci.address)
    print("RewardDistribution Contract was deployed to:", reward.address)
    print(100 *10**18, "CSTokens were minted to account 1")
    print("total Supply: ", citiSci.totalSupply())

    # 2. Different Accounts add rewards to the list
    for i in range(1, 100):
        print(reward.addReward(accounts[1], "name"+str(i), 11, 2, "https://name2.access.com", "Description for reward Item 1", {'from': accounts[1]}).gas_used)
