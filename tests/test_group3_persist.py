import brownie

def test_persist_p1(CSToken, RewardsDistribution, Donation, accounts):
    # 1. Deploy Contracts
    citiSci = CSToken.deploy(accounts[1], 100 *10**18, {'from': accounts[0]})
    reward = RewardsDistribution.deploy(citiSci.address, {'from': accounts[0]})
    donation = Donation.deploy(citiSci.address, {'from': accounts[0]})
    print("CSToken Contract was deployed to:", citiSci.address)
    print("RewardDistribution Contract was deployed to:", reward.address)
    print("Donation Contract was deployed to:", reward.address)
    print(100 *10**18, "CSTokens were minted to account 1")
    print("total Supply: ", citiSci.totalSupply())

    # 2. Add Reward and Donation Request
    reward.addReward(accounts[1], "reward A", 11 *10**18, 101, "https://name1.access.com", "Description for reward A", {'from': accounts[1]})
    print(f"Reward A added to the list by Account 1 ({accounts[1]})")
    donation.addDonation(accounts[1], "donation request B", 100 *10**18, "description of donation request B", {'from': accounts[1]})
    print(f"Donation Request B added to the list by Account 1 ({accounts[1]})")
    
    # 3. Add Bid to Donation Request and Persist that Bid
    bid = 10 *10**18
    donation.bidOnDonationRequest(accounts[1], "donation request B", bid, {'from': accounts[2]})
    print(f"Account 2 ({accounts[2]}) bid on Donation Request A for {bid} CSTokens")
    donation.persistDonation(accounts[1], "donation request B", reward, [(accounts[2], bid)], {'from': accounts[1]})
    print(f"Persisted Donation by Account 2 ({accounts[2]}) with mint of {bid} CSTokens")
    print("Balance of 2: ", citiSci.balanceOf(accounts[2]))
    print("Total Supply:", citiSci.totalSupply())

    assert  citiSci.balanceOf(accounts[2]) == bid


def test_persist_p2(CSToken, RewardsDistribution, Donation, accounts):
    # 1. Deploy Contracts
    citiSci = CSToken.deploy(accounts[1], 100 *10**18, {'from': accounts[0]})
    reward = RewardsDistribution.deploy(citiSci.address, {'from': accounts[0]})
    donation = Donation.deploy(citiSci.address, {'from': accounts[0]})
    print("CSToken Contract was deployed to:", citiSci.address)
    print("RewardDistribution Contract was deployed to:", reward.address)
    print("Donation Contract was deployed to:", reward.address)
    print(100 *10**18, "CSTokens were minted to account 1")
    print("total Supply: ", citiSci.totalSupply())

    # 2. Add Reward and Donation Request
    reward.addReward(accounts[1], "reward A", 11 *10**18, 101, "https://name1.access.com", "Description for reward A", {'from': accounts[1]})
    print(f"Reward A added to the list by Account 1 ({accounts[1]})")
    donation.addDonation(accounts[1], "donation request B", 100 *10**18, "description of donation request B", {'from': accounts[1]})
    print(f"Donation Request B added to the list by Account 1 ({accounts[1]})")

    #3. Add Bid to Donation Request
    bid = 10 *10**18
    donation.bidOnDonationRequest(accounts[1], "donation request B", bid, {'from': accounts[2]})
    print(f"Account 2 ({accounts[2]}) bid on Donation Request A for {bid} CSTokens")
    
    # 4. Delete Reward and Persist that Bid
    reward.deleteReward(accounts[1], "reward A", {'from': accounts[1]})
    print("reward A by Account 1 is deleted")
    print("Is Account 1 registered as consumer?", citiSci.getRegistered(accounts[1]))
    with brownie.reverts():
        donation.persistDonation(accounts[1], "donation request B", reward, [(accounts[2], bid)], {'from': accounts[1]})
    print("Donation Persist was successfully stopped, because Account 1 is no longer a registered consumer")

    assert citiSci.getRegistered(accounts[1]) == False
    

def test_persist_p3(CSToken, RewardsDistribution, Donation, accounts):
    # 1. Deploy Contracts
    citiSci = CSToken.deploy(accounts[1], 100 *10**18, {'from': accounts[0]})
    reward = RewardsDistribution.deploy(citiSci.address, {'from': accounts[0]})
    donation = Donation.deploy(citiSci.address, {'from': accounts[0]})
    print("CSToken Contract was deployed to:", citiSci.address)
    print("RewardDistribution Contract was deployed to:", reward.address)
    print("Donation Contract was deployed to:", reward.address)
    print(100 *10**18, "CSTokens were minted to account 1")
    print("total Supply: ", citiSci.totalSupply())

    # 2. Add Reward and Donation Request
    reward.addReward(accounts[1], "reward A", 11 *10**18, 101, "https://name1.access.com", "Description for reward A", {'from': accounts[1]})
    print(f"Reward A added to the list by Account 1 ({accounts[1]})")
    donation.addDonation(accounts[1], "donation request B", 100 *10**18, "description of donation request B", {'from': accounts[1]})
    print(f"Donation Request B added to the list by Account 1 ({accounts[1]})")

    #3. Add Bid to Donation Request
    bid = 1 *10**18
    donation.bidOnDonationRequest(accounts[1], "donation request B", bid, {'from': accounts[2]})
    print(f"Account 2 ({accounts[2]}) bid on Donation Request A for {bid} CSTokens")

    # 4. persist and view reward price 20 times
    counter = 1
    for _ in range(1,20):
        print(f"Run: {counter}")
        print(f"The price of reward A is {reward.getReward(accounts[1],'reward A')['price']}")
        donation.persistDonation(accounts[1], "donation request B", reward, [(accounts[2], bid)], {'from': accounts[1]})
        print(f"Donation Request B persisted and mints {bid} CSToken to Account 2 ({accounts[2]})")
        print("Balance of Account 2: ", citiSci.balanceOf(accounts[2]))
        print("Total Supply:", citiSci.totalSupply())
        counter += 1


def test_persist_p4(CSToken, RewardsDistribution, Donation, accounts):
    # 1. Deploy Contracts
    citiSci = CSToken.deploy(accounts[1], 100 *10**18, {'from': accounts[0]})
    reward = RewardsDistribution.deploy(citiSci.address, {'from': accounts[0]})
    donation = Donation.deploy(citiSci.address, {'from': accounts[0]})
    print("CSToken Contract was deployed to:", citiSci.address)
    print("RewardDistribution Contract was deployed to:", reward.address)
    print("Donation Contract was deployed to:", reward.address)
    print(100 *10**18, "CSTokens were minted to account 1")
    print("total Supply: ", citiSci.totalSupply())

    # 2. Account 1 checks his Minting Limit
    reward.addReward(accounts[1], "reward R1", 11 *10**18, 101, "https://name1.access.com", "Description for reward R1", {'from': accounts[1]})
    print(f"Reward R1 added to the list by Account 1 ({accounts[1]})")
    donation.addDonation(accounts[1], "donation request B", 100 *10**18, "description of donation request D1", {'from': accounts[1]})
    print(f"Donation Request D1 added to the list by Account 1 ({accounts[1]})")
    print("Account 1 has a minting limit of: ", donation.getMintLeft(accounts[1]))

    # 3. Account 2 adds Donation Requests until he reaches his minting limit
    counterA2 = 1
    reward.addReward(accounts[2], f"reward R2{counterA2}", 11 *10**18, 101, "https://name2.access.com", f"Description for reward R2{counterA2}", {'from': accounts[2]})
    print(f"Reward R2 added to the list by Account 2 ({accounts[1]})")
    for i in range(3):
        donation.addDonation(accounts[2], f"donation request D2{counterA2}", 300 *10**18, f"description of donation request D2{counterA2}", {'from': accounts[2]})
        print("Account 2 has reached his minting limit")
        print(f"Donation Request D2{counterA2} added to the list by Account 2 ({accounts[2]})")
        print("Account 2 has a minting limit of: ", donation.getMintLeft(accounts[2]))
        counterA2 += 1
    with brownie.reverts():
        donation.addDonation(accounts[2], f"donation request D2{counterA2}", 300 *10**18, f"description of donation request D2{counterA2}", {'from': accounts[2]})
    print("Account 2 has reached his minting limit")

    # 4. Account 3 adds, persists and deletes Donation Requests to show retreived Minting Limit when requests get deleted
    reward.addReward(accounts[3], "reward R3", 11 *10**18, 101, "https://name3.access.com", "Description for reward R3", {'from': accounts[3]})
    print(f"Reward R3 added to the list by Account 3 ({accounts[3]})")
    for _ in range(2):
        donation.addDonation(accounts[3], "donation request D3", 600 *10**18, "description of donation request D3", {'from': accounts[3]})
        print(f"Donation Request D3 added to the list by Account 3 ({accounts[3]})")
        donation.bidOnDonationRequest(accounts[3], "donation request D3", 400 *10**18, {'from': accounts[4]})
        print(f"Account 4 ({accounts[4]}) bid on Donation Request D3 for {400 *10**18} CSTokens")
        donation.persistDonation(accounts[3], "donation request D3", reward, [(accounts[4], 400 *10**18)], {'from': accounts[3]})
        print(f"Donation Request D3 persisted and mints {400 *10**18} CSToken to Account 4 ({accounts[4]})")
        print("Balance of Account 4: ", citiSci.balanceOf(accounts[4]))
        donation.deleteDonation(accounts[3], "donation request D3", {'from': accounts[3]})
