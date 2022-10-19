import brownie


def test_buy_b1(CSToken, RewardsDistribution, accounts):
    # 1. deploy the contract with initial mint
    citiSci = CSToken.deploy(accounts[1], 100 *10**18, {'from': accounts[0]})
    reward = RewardsDistribution.deploy(citiSci.address, {'from': accounts[0]})
    print("CSToken Contract was deployed to:", citiSci.address)
    print("RewardDistribution Contract was deployed to:", reward.address)
    print(100 *10**18, "CSTokens were minted to account 1")
    print("total Supply: ", citiSci.totalSupply())

    # 2. Account 2 adds Reward
    reward.addReward(accounts[2], "reward A", 11 *10**18, 1, "https://name1.access.com", "Description for reward A", {'from': accounts[2]})
    print(f"Reward A added with (amount=1) to the list by Account 2 ({accounts[2]})")

    # 3. Account 1 buys reward A
    citiSci.approve(reward.address, 9999999999999 *10**18, {'from': accounts[1]})
    reward.buyReward(accounts[2], "reward A", {'from': accounts[1]})
    print(f"Reward A bought by Account 1 ({accounts[1]}) from Account 2 ({accounts[2]})")
    with brownie.reverts():
        print(reward.getReward(accounts[2], "name A")['price'])
    print("Reward A is not available anymore")


def test_buy_b2(CSToken, RewardsDistribution, accounts):
    # 1. deploy the contract with initial mint
    citiSci = CSToken.deploy(accounts[1], 100 *10**18, {'from': accounts[0]})
    reward = RewardsDistribution.deploy(citiSci.address, {'from': accounts[0]})
    print("CSToken Contract was deployed to:", citiSci.address)
    print("RewardDistribution Contract was deployed to:", reward.address)
    print(100 *10**18, "CSTokens were minted to account 1")
    print("total Supply: ", citiSci.totalSupply())

    # 2. Adding 11 rewards
    reward.addReward(accounts[2], "name2", 22, 99, "https://name1.access.com", "Description for reward Item 2", {'from': accounts[2]})
    reward.addReward(accounts[3], "name3", 11, 101, "https://name2.access.com", "Description for reward Item 1", {'from': accounts[3]})
    citiSci.approve(reward.address, 9999999999999, {'from': accounts[1]})
    index = 0
    for i in range(0,23):
        print("run: ", index)
        print("The Price of Reward 2 is:", reward.getReward(accounts[2], "name2")['price'], "(demand:", reward.getReward(accounts[2], "name2")['demand'], ")")
        print("The Price of Reward 3 is:", reward.getReward(accounts[3], "name3")['price'], "(demand:", reward.getReward(accounts[3], "name3")['demand'], ")")
        reward.buyReward(accounts[2], "name2", {'from': accounts[1]})
        index = index + 1