from logging import INFO
from smartcard.scard import *
from smartcard.System import readers
from smartcard.util import toHexString, toBytes
import smartcard.util
from model.device_model import CARD_RESPONSE_CODE
from util import logger
import os
log = logger.get_logger("device")

def prepare_cmd(InsType=None, p1=0x00, p2=0x00, Lc=None, dataIn=0x00):
    """
    This function prepare transamit command
    """
    log.debug("prepare_cmd() : start")
    CLA = 0xFF
    COMMAND = [CLA]
    INS_SWITCHER = {
        "GETDATA": 0xCA,
        "LOADKEY": 0x82,
        "AUTH": 0x86,
        "READBINARY": 0xB0,
        "MFCREAD": 0xB1,
        "UPDATEBINARY": 0xD6,
        "MFCWRITE": 0xD7
    }

    INS = INS_SWITCHER.get(InsType, None)

    if INS == None:
        log.error("prepare_cmd() : command empty failed")
        return -1

    COMMAND.append(INS)
    COMMAND.append(p1)
    COMMAND.append(p2)
    if Lc == None:
        COMMAND.append(dataIn)
    else:

        if InsType == "READBINARY":
            COMMAND.append(Lc)
        else:
            if len(dataIn) != Lc:
                log.error("prepare_cmd() : data input isn't match data length")
                return -1
            COMMAND.append(Lc)
            arrValue = []

            if type(dataIn) == str:
                arrValue = bytes(dataIn, 'utf-8')
            if type(dataIn) == list:
                arrValue = dataIn

            for byte in arrValue:
                COMMAND.append(byte)

    log.debug(
        f"prepare_cmd() : {toHexString(COMMAND, smartcard.util.HEX)}")
    return COMMAND

class Device:
    """
    Device for Read/Write Card
    """
    hcard = ""
    dwActiveProtocol = ""
    cardKeyType = ""
    cardKeyIndex = 0
    # updateCardFileName = ""

    def __init__(self):
        log.debug("__init__")
        self.deviceLists = readers()

    def get_device_list(self):
        """
        this function return reader list
        """
        return self.deviceLists
    
    def send_cmd(self, cmd):
        hresult, response = SCardTransmit(Device.hcard, Device.dwActiveProtocol, cmd)
        if hresult != SCARD_S_SUCCESS:
            log.error(
                f"send_cmd() : Failed to transmit: {SCardGetErrorMessage(hresult)}")
        else:
            log.info(
                f"send_cmd() : get  << {toHexString(response)}")

        return response
    
    def auth_block_index(self, blockIndex=None):
        
        log.info(f"auth_block_index() : authen block index ({blockIndex})")
    
        inputBytes = toBytes("0100"+format(blockIndex, '02X') +
                             Device.cardKeyType+format(Device.cardKeyIndex, '02X'))

        commandAuth = prepare_cmd(InsType="AUTH", Lc=len(inputBytes), dataIn=inputBytes)

        return self.send_cmd(commandAuth)

    def read_binary_data_block(self, blockIndex=None):
        result = ""
        result = self.auth_block_index(blockIndex)
        resultCode = int.from_bytes(result, byteorder='little')
        log.debug(f"read_binary_data_block() : result code = {resultCode}")
        if resultCode != CARD_RESPONSE_CODE.SUCCESS:
            log.error(f"read_binary_data_block() : auth {blockIndex} failed {CARD_RESPONSE_CODE(resultCode).name}")
            return "read_binary_data_block() : error"

        commandRead = prepare_cmd(InsType="READBINARY", p1=0x00, p2=blockIndex, Lc=0x10)

        data = self.send_cmd(commandRead)
        if len(data) == 2:
            log.error(f"read_binary_data_block() : auth {blockIndex} get error")
            return data
        else:
            checkResult = data[-2:-1]
            checkResultCode = int.from_bytes(checkResult, byteorder='little')
            if checkResultCode != CARD_RESPONSE_CODE.SUCCESS:
                log.error(f"read_binary_data_block() : read data {blockIndex} failed {checkResultCode}")
                return checkResultCode
            # remove last 2 bytes
            del data[-2:]
            # print(toHexString(commandRead))
            return data
    
    def load_auth_key(self):
        """
        The LOAD KEY instruction
        """
        log.debug("load_auth_key() : start")
        KEYA_DEFAULT = prepare_cmd(InsType="LOADKEY", p2=0x00, Lc=0x06, dataIn=toBytes("FF FF FF FF FF FF"))

        if KEYA_DEFAULT == -1:
            log.error("load_auth_key() : set key default failed")
            return -1
        
        LOAD_KEYA = prepare_cmd(InsType="LOADKEY", p2=0x01, Lc=0x06, dataIn=toBytes("FF FF FF FF FF FF"))

        if LOAD_KEYA == -1:
            log.error("load_auth_key() : set authen KeyA failed")
            return -1
        
        commandLists = [KEYA_DEFAULT, LOAD_KEYA]
        
        # commandLists = [KEYA_DEFAULT]

        for index, COMMAND in enumerate(commandLists):
            log.info(f"load_auth_key() : excute {index} send >> {toHexString(COMMAND)}")
            hresult, response = SCardTransmit(Device.hcard, Device.dwActiveProtocol, COMMAND)
            log.debug(f"load_auth_key() : result = {hresult} , response = {response}")
            if hresult != SCARD_S_SUCCESS:
                log.error(f"load_auth_key() : Failed to transmit: {SCardGetErrorMessage(hresult)}")
            else:
                log.info(f"load_auth_key() : get  << {toHexString(response)}")

        log.info("load_auth_key() : done")
        return 0

    
    def read_uuid(self):
        """
        read UID
            return 6 bytes
            0 - 3 bytes is UID
            4 is sw1
            5 is sw2
        """
        log.debug("read_uuid() : start")
        uid = ""
        COMMAND = prepare_cmd(InsType="GETDATA")
        hresult, response = SCardTransmit(Device.hcard, Device.dwActiveProtocol, COMMAND)
        log.debug(f"read_uuid() : result = {hresult} , response = {response}")
        if hresult != SCARD_S_SUCCESS:
            log.error(f"Failed to transmit: {SCardGetErrorMessage(hresult)}")
        else:
            # get a result
            uid += "uuid: " + toHexString(response, smartcard.util.HEX)
            log.info(f"read_uuid() : {uid}")
        return uid
    
    def read_info(self, KeyType="A", KeyIndex=1):
        """
        this function read info
        """
        strByteKeyType = ""
        if KeyType == "A":
            strByteKeyType = "60"
        elif KeyType == "B":
            strByteKeyType = "61" 
        Device.cardKeyIndex = KeyIndex
        Device.cardKeyType = strByteKeyType
        """
        start read block 4-63 skipt 4 block and block key
        """
        data = []
        blockValue = self.read_binary_data_block(12)
        
        data = blockValue
        
        return data
        
        # data = []
        # for blockDataIndex in range(4, 30):
        #     blockValue = []
        #     if (blockDataIndex +1) % 4 != 0:
        #         blockValue = self.read_binary_data_block(blockDataIndex)
        #         log.debug(f"read_info() : blockIndex = {blockDataIndex} , value = {blockValue}")
        #         """
        #         expected list [D0 .. D16] ,  [D0 .. D16]
        #         """
        #         data.append(blockValue)
        # return 0
        
        
    
    def write_tag_info(self,value):
        log.info(f"write_tag_info() : start write data with value = {value}") 
        blockIndex = 12
        #  def writeDataToCard(self, blockIndex: int, data: list, typeUpdate: str):
        #     """
        # wirte Smart Card 16 bytes
        # """
        result = ""
        dataUpdate = []
        Device.cardKeyIndex = 1
        Device.cardKeyType = "60"
        
        result = self.auth_block_index(blockIndex)
        log.debug(f"write_tag_info() : result = {result}")
        resultCode = int.from_bytes(result, byteorder='little')
        log.debug(f"write_tag_info() : result code = {resultCode}")
        
        if resultCode != CARD_RESPONSE_CODE.SUCCESS:
            log.error(
                f"write_tag_info() : auth {blockIndex} failed {CARD_RESPONSE_CODE(resultCode).name}")
            return (-1)

        # if typeUpdate == "MFCWRITE":
        #     dataUpdate = data[0:4]
        # else:
        #     dataUpdate = data
        
        # dataUpdate = b'000102030405060708090A0B0C0D0E0F'
        # dataUpdate = int(value).to_bytes(16, 'little')
        
        #dataUpdate = value.zfill(16)
        dataUpdate = value.ljust(16, '0')
        
        log.debug(f"write_tag_info() : data update = {dataUpdate}")
        
        commandWrite = prepare_cmd( InsType="UPDATEBINARY", p1=0x00, p2=blockIndex, Lc=len(dataUpdate),dataIn=dataUpdate)

        result = self.send_cmd(commandWrite)
        
        resultCode = int.from_bytes(result, byteorder='little')
                
        log.debug(f"write_tag_info() : result code write data  = {resultCode}")
        
        return resultCode
    
    def polling_write_tag(self, value):
        log.info("polling_write_tag() : start")
        strOut = ""
        readTagInfo = ""
        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        hresult, readers = SCardListReaders(hcontext, [])
        readerstates = []
        for i in range(len(readers)):
            readerstates += [(readers[i], SCARD_STATE_UNAWARE)]
        # current status
        hresult, newstates = SCardGetStatusChange(hcontext, 0, readerstates)
        log.info("----- Please insert or remove a card ------------")
        # waiitng change a status
        hresult, newstates = SCardGetStatusChange(hcontext, INFINITE, newstates)
        
        eventStateStr = ""
        for i in newstates:
            reader, eventstate, atr = i
            if (eventstate & SCARD_STATE_PRESENT):
                eventStateStr = "Card Present"
                ###############################################
                try:
                    hresult, Device.hcard, Device.dwActiveProtocol = SCardConnect(hcontext, reader, SCARD_SHARE_SHARED,
                                                                                SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
                    if hresult != SCARD_S_SUCCESS:
                        raise Exception('Unable to connect: ' + SCardGetErrorMessage(hresult))

                    try:
                        uuidInfo = self.read_uuid()
                        if uuidInfo:
                            # load key to device
                            self.load_auth_key()
                            # strOut += uuidInfo
                    finally:
                        """
                        update tag info
                        """
                        # log.info
                        log.debug(f"polling_write_tag() : write a data = {value}")
                        res = self.write_tag_info(value)
                        log.debug(f"polling_write_tag() : result = {res}")
                        
                        strOut += str(res)
                        
                        hresult = SCardDisconnect(Device.hcard, SCARD_UNPOWER_CARD)
                        if hresult != SCARD_S_SUCCESS:
                            raise Exception('Failed to disconnect: ' + SCardGetErrorMessage(hresult))

                finally:
                    hresult = SCardReleaseContext(hcontext)
                    if hresult != SCARD_S_SUCCESS:
                        raise Exception('Failed to release context: ' + SCardGetErrorMessage(hresult))

            if eventstate & SCARD_STATE_ATRMATCH:
                # "Card Found"
                eventStateStr = "Card Found"
            if eventstate & SCARD_STATE_UNAWARE:
                # "State unware"
                eventStateStr = "State Unware"
            if eventstate & SCARD_STATE_IGNORE:
                # "Ignore reader"
                eventStateStr = "Ignore Reader"
            if eventstate & SCARD_STATE_UNAVAILABLE:
                # "Reader unavailable"
                eventStateStr = "Reader Unavailable"
            if eventstate & SCARD_STATE_EMPTY:
                # "Reader empty" is mean Card Removed
                eventStateStr = "Reader Empty"
            if eventstate & SCARD_STATE_EXCLUSIVE:
                # "Card allocated for exclusive use by another application"
                eventStateStr = "Card Allocated"
            if eventstate & SCARD_STATE_INUSE:
                # "Card in used by another application but can be shared"
                eventStateStr = "Card Busy"
            if eventstate & SCARD_STATE_MUTE:
                # "Card is mute"
                eventStateStr = "Card Mute"
            # if eventstate & SCARD_STATE_CHANGED:
            #     strOut += "State changed"
            if eventstate & SCARD_STATE_UNKNOWN:
                # "State unknowned"
                eventStateStr = "State Unknown"

        log.debug(eventStateStr)
        log.debug(strOut)

        return strOut, eventStateStr

    
    def polling_card_detected(self):
        log.info("polling_card_detected() : start")
        strOut = ""
        readTagInfo = ""
        hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        hresult, readers = SCardListReaders(hcontext, [])
        readerstates = []
        for i in range(len(readers)):
            readerstates += [(readers[i], SCARD_STATE_UNAWARE)]
        # current status
        hresult, newstates = SCardGetStatusChange(hcontext, 0, readerstates)
        log.info("----- Please insert or remove a card ------------")
        # waiitng change a status
        hresult, newstates = SCardGetStatusChange(hcontext, INFINITE, newstates)
        
        eventStateStr = ""
        for i in newstates:
            reader, eventstate, atr = i
            if (eventstate & SCARD_STATE_PRESENT):
                eventStateStr = "Card Present"
                ###############################################
                try:
                    hresult, Device.hcard, Device.dwActiveProtocol = SCardConnect(hcontext, reader, SCARD_SHARE_SHARED,
                                                                                SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
                    if hresult != SCARD_S_SUCCESS:
                        raise Exception('Unable to connect: ' + SCardGetErrorMessage(hresult))

                    try:
                        uuidInfo = self.read_uuid()
                        if uuidInfo:
                            # load key to device
                            self.load_auth_key()
                            # strOut += uuidInfo
                    finally:
                        """
                        enquiry card and update card Image
                        """
                        # log.info
                        tagInfo = self.read_info()
                        log.debug(f"read_info() : get a data = {tagInfo} type = {type(tagInfo)}")
                        outStr = ''.join(chr(number) for number in tagInfo)
                        
                        
                        # log.debug(f"read_info() : type = {type(bytes(tagInfo))}")
                        # byteorder is big where MSB is at start
                        # int_val = int.from_bytes( bytes(tagInfo), "little")
                        #log.debug(f"read_info() : int value = {int_val}")
                        strOut += outStr
                        
                        hresult = SCardDisconnect(Device.hcard, SCARD_UNPOWER_CARD)
                        if hresult != SCARD_S_SUCCESS:
                            raise Exception('Failed to disconnect: ' + SCardGetErrorMessage(hresult))

                finally:
                    hresult = SCardReleaseContext(hcontext)
                    if hresult != SCARD_S_SUCCESS:
                        raise Exception('Failed to release context: ' + SCardGetErrorMessage(hresult))

            if eventstate & SCARD_STATE_ATRMATCH:
                # "Card Found"
                eventStateStr = "Card Found"
            if eventstate & SCARD_STATE_UNAWARE:
                # "State unware"
                eventStateStr = "State Unware"
            if eventstate & SCARD_STATE_IGNORE:
                # "Ignore reader"
                eventStateStr = "Ignore Reader"
            if eventstate & SCARD_STATE_UNAVAILABLE:
                # "Reader unavailable"
                eventStateStr = "Reader Unavailable"
            if eventstate & SCARD_STATE_EMPTY:
                # "Reader empty" is mean Card Removed
                eventStateStr = "Reader Empty"
            if eventstate & SCARD_STATE_EXCLUSIVE:
                # "Card allocated for exclusive use by another application"
                eventStateStr = "Card Allocated"
            if eventstate & SCARD_STATE_INUSE:
                # "Card in used by another application but can be shared"
                eventStateStr = "Card Busy"
            if eventstate & SCARD_STATE_MUTE:
                # "Card is mute"
                eventStateStr = "Card Mute"
            # if eventstate & SCARD_STATE_CHANGED:
            #     strOut += "State changed"
            if eventstate & SCARD_STATE_UNKNOWN:
                # "State unknowned"
                eventStateStr = "State Unknown"

        log.debug(eventStateStr)
        log.debug(strOut)

        return strOut, eventStateStr