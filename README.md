# fixprinter
A pretty printer for decoding and displaying FIX protocol messages
in a human-readable format.

## Usage
```
$ ./fixprinter.py
usage: fixprinter.py [-h] [-f FILENAME] [--stdin] [--spec SPEC]

A pretty printer of fix messages using the quickfix library (Must specify
either --filename or --stdin)

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        a file containing fix messages to display
  --stdin               a file containing fix messages to display
  --spec SPEC           loads the provided XML specification (presumably from
                        the quickfix library) WARNING! The output will be
                        fairly useless without a spec
```

## Example
```
$ ./fixprinter.py --spec FIX44.xml --filename fix_message

Found FIX message at line 1: 8=FIX.4.4|9=247|35=s|34=5|49=sender|52=20060319-09:08:20.881|56=target|22=8|40=2|44=9|48=ABC|55=ABC|60=20060319-09:08:19|548=184214|549=2|550=0|552=2|54=1|453=2|448=8|447=D|452=4|448=AAA35777|447=D|452=3|38=9|54=2|453=2|448=8|447=D|452=4|448=aaa|447=D|452=3|38=9|10=056|

BeginString (8): FIX.4.4
BodyLength (9): 247
MsgSeqNum (34): 5
MsgType (35): NewOrderCross (s)
SenderCompID (49): sender
SendingTime (52): 20060319-09:08:20.881
TargetCompID (56): target
SecurityIDSource (22): EXCHANGE_SYMBOL (8)
OrdType (40): LIMIT (2)
Price (44): 9
SecurityID (48): ABC
Symbol (55): ABC
TransactTime (60): 20060319-09:08:19
CrossID (548): 184214
CrossType (549): CROSS_TRADE_WHICH_IS_EXECUTED_PARTIALLY_AND_THE_REST_IS_CANCELLED_ONE_SIDE_IS_FULLY_EXECUTED_THE_OTHER_SIDE_IS_PARTIALLY_EXECUTED_WITH_THE_REMAINDER_BEING_CANCELLED_THIS_IS_EQUIVALENT_TO_AN_IMMEDIATE_OR_CANCEL_ON_THE_OTHER_SIDE_NOTE_THE_CROSSPRIORITZATION (2)
CrossPrioritization (550): NONE (0)
NoSides (552): count = 2
  OrderQty (38): 9
  Side (54): BUY (1)
  NoPartyIDs (453): count = 2
    PartyIDSource (447): PROPRIETARY_CUSTOM_CODE (D)
    PartyID (448): 8
    PartyRole (452): CLEARING_FIRM (4)
    ----
    PartyIDSource (447): PROPRIETARY_CUSTOM_CODE (D)
    PartyID (448): AAA35777
    PartyRole (452): CLIENT_ID (3)
  ----
  OrderQty (38): 9
  Side (54): SELL (2)
  NoPartyIDs (453): count = 2
    PartyIDSource (447): PROPRIETARY_CUSTOM_CODE (D)
    PartyID (448): 8
    PartyRole (452): CLEARING_FIRM (4)
    ----
    PartyIDSource (447): PROPRIETARY_CUSTOM_CODE (D)
    PartyID (448): aaa
    PartyRole (452): CLIENT_ID (3)
CheckSum (10): 056
```
