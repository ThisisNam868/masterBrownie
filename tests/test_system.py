import random as rand
import math
import brownie

def test_system_s1(CSToken, RewardsDistribution, Donation, accounts):
    # 1. Deploy Contracts
    citiSci = CSToken.deploy(accounts[1], 100 *10**18, {'from': accounts[0]})
    reward = RewardsDistribution.deploy(citiSci.address, {'from': accounts[0]})
    donation = Donation.deploy(citiSci.address, {'from': accounts[0]})
    print("CSToken Contract was deployed to:", citiSci.address)
    print("RewardDistribution Contract was deployed to:", reward.address)
    print("Donation Contract was deployed to:", reward.address)
    print(100 *10**18, "CSTokens were minted to account 1")
    print("total Supply: ", citiSci.totalSupply())

    # 2. Randomized Consumers add Rewards and Donation Requests
    consumer_list = []
    rewards_dict = {}
    donations_dict = {}
    for _ in range(2):
        randConsumer = math.floor(rand.uniform(1,9))
        rew_price = math.floor(rand.uniform(1,10)) *10**18
        reward.addReward(accounts[randConsumer], "reward A",  rew_price, 10, "https://name1.access.com", "Description for reward A", {'from': accounts[randConsumer]})
        consumer_list.append(randConsumer)
        rewards_dict[randConsumer] = rew_price
        print(f"Reward A with Price of {rew_price} added to the list by Account {randConsumer} ({accounts[randConsumer]})")

        don_price = math.floor(rand.uniform(1, 500 *10**18))
        donation.addDonation(accounts[randConsumer], "Donation Request B", don_price, f"description of Donation Request B", {'from': accounts[randConsumer]})
        donations_dict[randConsumer] = don_price
        print(f"Donation Request B with budget of {don_price} added to the list by Account {randConsumer} ({accounts[randConsumer]})")


    # 3. Random Bids on Donation Requests and their Persistence
    producer_list = []
    for _ in range(3):
        randProducer = math.floor(rand.uniform(1,9))
        while randProducer in consumer_list:
            randProducer = math.floor(rand.uniform(1,9))
        producer_list.append(randProducer)
        
        randConsumerToPersist = rand.choice(list(consumer_list))
        randDonationPrice = math.floor(rand.uniform(0, donations_dict[randConsumerToPersist]))
        donation.bidOnDonationRequest(accounts[randConsumerToPersist], "Donation Request B", randDonationPrice, {'from': accounts[randProducer]})
        print(f"Producer {randProducer} ({accounts[randProducer]}) bid {randDonationPrice} CSToken on Donation Request B of Consumer {randConsumerToPersist} ({accounts[randConsumerToPersist]})")
        donation.persistDonation(accounts[randConsumerToPersist], "Donation Request B", reward, [(accounts[randProducer], randDonationPrice)], {'from': accounts[randConsumerToPersist]})
        donations_dict[randConsumerToPersist] -= randDonationPrice
        print(f"Consumer {randConsumerToPersist} ({accounts[randConsumerToPersist]}) persisted the bid of Producer {randProducer} ({accounts[randProducer]}) on Donation Request B and minted {randDonationPrice} CSTokens")

    # 4. Prdoucers buy a Reward
    randProducer = math.floor(rand.uniform(1,9))
    while randProducer not in producer_list:
        randProducer = math.floor(rand.uniform(1,9))
    
    randConsumerToBuy = rand.choice(list(consumer_list))
    try:
        citiSci.approve(reward.address, 9999999999 *10**18, {'from': accounts[randProducer]})
        reward.buyReward(accounts[randConsumerToBuy], "reward A", {'from': accounts[randProducer]})
        print(f"Producer {randProducer} ({accounts[randProducer]}) bought Reward A of Consumer {randConsumerToBuy} ({accounts[randConsumerToBuy]})")
    except brownie.exceptions.VirtualMachineError:
        print(f"Producer {randProducer} ({accounts[randProducer]}) could not buy Reward A of Consumer {randConsumerToBuy} ({accounts[randConsumerToBuy]})")
        print(f"Balance of Producer {randProducer}: ", citiSci.balanceOf(accounts[randProducer]))
        print(f"Price of Reward {randConsumerToBuy}: ", rewards_dict[randConsumerToBuy])
