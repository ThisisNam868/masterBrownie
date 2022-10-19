import random as rand
import math

def test_currency_c1(CSToken, accounts):    
    FACTOR = 100
    randomNum =  rand.random()

    # 1. deploy the contract with initial mint to Account 1
    randomMint =  math.floor(randomNum * FACTOR * FACTOR * 10**18)
    print("random amount to mint on deploy: ", randomMint)
    citiSci = CSToken.deploy(accounts[1], randomMint, {'from': accounts[0]})
    print("CSToken Contract was deployed to:", citiSci.address)
    print(randomMint, "CSTokens were minted to", accounts[0])
    print("balance of Account 1: ", citiSci.balanceOf(accounts[1]))
    print("total Supply: ", citiSci.totalSupply())
    oldSupply = citiSci.totalSupply()

    # 2. transfer tokens from accounts[0] to accounts[1] - show that balances are updated
    randomSend = math.floor(rand.uniform(0, randomNum) * FACTOR * 10**18)
    print("random amount to send: ", randomSend)
    citiSci.transfer(accounts[2], randomSend, {'from': accounts[1]})
    print(randomSend, "CSTokens were sent from", accounts[1], "to", accounts[2])
    print("Balance of Account 1: ", citiSci.balanceOf(accounts[1]))
    print("Balance of Account 2: ", citiSci.balanceOf(accounts[2]))
    print("total Supply: ", citiSci.totalSupply())

    assert oldSupply == citiSci.totalSupply()
    
    # 3. transfer tokens from accounts[1] to accounts[2] - show that totalSupply is decremented because of burn
    citiSci.addRegistered(accounts[3], {'from': accounts[3]})
    print("Account 3 was added to the list of registered consumers")
    randomSend = math.floor(rand.uniform(0, randomNum) * FACTOR * 10**18)
    print("random amount to send: ", randomSend)
    citiSci.approve(accounts[1], 9999999999999 * 10**18, {'from': accounts[1]})
    citiSci.transfer(accounts[3], randomSend, {'from': accounts[1]})
    print(randomSend, "Token were sent from", accounts[1], "to", accounts[3])
    print("Balance of Account 1: ", citiSci.balanceOf(accounts[1]))
    print("Balance of Account 3: ", citiSci.balanceOf(accounts[3]))
    print("total Supply: ", citiSci.totalSupply())

    assert citiSci.totalSupply() == oldSupply - randomSend