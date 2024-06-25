from enum import IntEnum

class CARD_RESPONSE_CODE(IntEnum):
    DEFAULT_ERRROR = -1             # default error
    SUCCESS = 144                   # 90 00 SUCCESS
    ERROR = 25344                   # 63 00 General Error
    WRONGLENGTH = 26368             # 67 00 Wrong Length
    CLA_NOT_MATCH = 26624           # 68 00 CLA byte is not correct
    # error for GENERAL AUTHENTICATE
    CRYPTO1_AUTH_FAILED = 27010     # 69 82 CRYPTO1 authentication failed
    ERR = 99
    UNKNOW = 0