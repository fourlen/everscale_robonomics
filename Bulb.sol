pragma ton-solidity >= 0.35.0;
pragma AbiHeader expire;


contract Bulb {

    bool public isTurnedOn = false;

    constructor() public {
        require(tvm.pubkey() != 0, 101);
        require(msg.pubkey() == tvm.pubkey(), 102);
        tvm.accept();
    }

    function turnOnOff() public returns (bool success) {
        tvm.accept();
        if (isTurnedOn) {
            isTurnedOn = false;
        }
        else {
            isTurnedOn = true;
        }
        return true;
    }
}