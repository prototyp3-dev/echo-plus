from os import environ
import sys
import logging
import requests
import traceback
import json
import sqlite3
from eth_abi import encode
from shapely.geometry import shape, Point
import numpy as np
import cv2
from Cryptodome.Hash import SHA256
import base64
import base58
from protobuf_models import unixfs_pb2, merkle_dag_pb2

DAPP_RELAY_ADDRESS = "0xF5DE34d6BbC0446E2a45719E718efEbaaE179daE".lower()
ETHER_PORTAL_ADDRESS = "0xFfdbe43d4c855BF7e0f105c400A50857f53AB044".lower()
ERC20_PORTAL_ADDRESS = "0x9C21AEb2093C32DDbC53eEF24B873BDCd1aDa1DB".lower()
ERC721_PORTAL_ADDRESS = "0x237F8DD094C0e47f4236f12b4Fa01d6Dae89fb87".lower()

# b'Y\xda*\x98N\x16Z\xe4H|\x99\xe5\xd1\xdc\xa7\xe0L\x8a\x990\x1b\xe6\xbc\t)2\xcb]\x7f\x03Cx'
ERC20_TRANSFER_HEADER = b'Y\xda*\x98N\x16Z\xe4H|\x99\xe5\xd1\xdc\xa7\xe0L\x8a\x990\x1b\xe6\xbc\t)2\xcb]\x7f\x03Cx'
# b'd\xd9\xdeE\xe7\xdb\x1c\n|\xb7\x96\n\xd2Q\x07\xa67\x9bj\xb8[0DO:\x8drHW\xc1\xacx'
ERC721_TRANSFER_HEADER = b'd\xd9\xdeE\xe7\xdb\x1c\n|\xb7\x96\n\xd2Q\x07\xa67\x9bj\xb8[0DO:\x8drHW\xc1\xacx'
# print(Web3.keccak(b"Ether_Transfer"))
ETHER_TRANSFER_HEADER = b'\xf2X\xe0\xfc9\xd3Z\xbd}\x83\x93\xdc\xfe~\x1c\xf8\xc7E\xdd\xca8\xaeA\xd4Q\xd0\xc5Z\xc5\xf2\xc4\xce'

# print(Web3.keccak(b"transfer(address,uint256)")) -> will be called as [token_address].transfer([address receiver],[uint256 amount])
ERC20_TRANSFER_FUNCTION_SELECTOR = b'\xa9\x05\x9c\xbb*\xb0\x9e\xb2\x19X?JY\xa5\xd0b:\xde4m\x96+\xcdNF\xb1\x1d\xa0G\xc9\x04\x9b'[:4]
# print(Web3.keccak(b"safeTransferFrom(address,address,uint256)")) -> will be called as [nft_address].safeTransferFrom([address sender],[address receiver],[uint256 id])
ERC721_SAFETRANSFER_FUNCTION_SELECTOR = b'B\x84.\x0e\xb3\x88W\xa7w[Nsd\xb2w]\xf72Pt\xd0\x88\xe7\xfb9Y\x0c\xd6(\x11\x84\xed'[:4]
# print(Web3.keccak(b"withdrawEther(address,uint256)")) -> will be called as [rollups_address].withdrawEther(address,uint256)
ETHER_WITHDRAWAL_FUNCTION_SELECTOR = b'R/h\x15\xd7\xe9\xa0\xcazPV\x96G]\xe7q\x9bDY\\0\x96\xa6\x83~\xe8g\xf0>\r\xce\xb3'[:4]

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

###
# Aux Functions 

def str2hex(string):
    """
    Encode a string as an hex string
    """
    return binary2hex(str2binary(string))

def str2binary(string):
    """
    Encode a string as an binary string
    """
    return string.encode("utf-8")

def binary2hex(binary):
    """
    Encode a binary as an hex string
    """
    return "0x" + binary.hex()

def hex2binary(hexstr):
    """
    Decodes a hex string into a regular byte string
    """
    return bytes.fromhex(hexstr[2:])

def hex2str(hexstr):
    """
    Decodes a hex string into a regular string
    """
    return hex2binary(hexstr).decode("utf-8")


def send_voucher(voucher):
    send_post("voucher",voucher)

def send_notice(notice):
    send_post("notice",notice)

def send_report(report):
    send_post("report",report)

def send_exception(exception):
    send_post("exception",exception)

def send_post(endpoint,json_data):
    response = requests.post(rollup_server + f"/{endpoint}", json=json_data)
    logger.info(f"/{endpoint}: Received response status {response.status_code} body {response.content}")

def check_point_in_fence(fence, latitude, longitude):
    # shapely
    fence = json.loads(fence)
    y = shape(fence)
    x = Point(longitude, latitude)
    return y.contains(x)

def process_sql_statement(statement):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(statement)
    result = cur.fetchall()
    con.commit()
    con.close()
    return result

def process_image(image):
    b64str = image
    png = base64.decodebytes(b64str)
    nparr = np.frombuffer(png,np.uint8)
    img = cv2.imdecode(nparr,cv2.IMREAD_UNCHANGED)
    (rows, cols) = img.shape[:2]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 15, 1)
    rotated = cv2.warpAffine(img, M, (cols, rows))
    rotated_png = cv2.imencode('.png',rotated)
    data_encode = np.array(rotated_png[1])
    # gaussian = cv2.GaussianBlur(rotated, (9, 9), 0)
    # gaussian_png = cv2.imencode('.png',gaussian)
    # data_encode = np.array(gaussian_png[1])
    byte_encode = data_encode.tobytes()
    b64out = base64.b64encode(byte_encode)
    return b64out

def mint_erc721_with_uri_from_image(msg_sender,erc721_to_mint,mint_header,b64out):
    pngout = base64.decodebytes(b64out)

    unixf = unixfs_pb2.Data()
    unixf.Type = 2 # file
    unixf.Data = pngout
    unixf.filesize = len(unixf.Data)

    mdag = merkle_dag_pb2.MerkleNode()
    mdag.Data = unixf.SerializeToString()

    data = mdag.SerializeToString()

    h = SHA256.new()
    h.update(data)
    sha256_code = "12"
    size = hex(h.digest_size)[2:]
    digest = h.hexdigest()
    combined = f"{sha256_code}{size}{digest}"
    multihash = base58.b58encode(bytes.fromhex(combined))
    tokenURI = multihash.decode('utf-8') # it is not the ipfs unixfs 'file' hash

    mint_erc721_with_string(msg_sender,erc721_to_mint,mint_header,tokenURI)
    
def mint_erc721_with_string(msg_sender,erc721_to_mint,mint_header,string):
    mint_header = clean_header(mint_header)
    data = encode(['address', 'string'], [msg_sender,string])
    payload = f"0x{(mint_header+data).hex()}"
    voucher = {"destination": erc721_to_mint , "payload": payload}
    logger.info(f"voucher {voucher}")
    send_voucher(voucher)
    
    send_notice({"payload": str2hex(str(f"Emmited voucher to mint ERC721 {erc721_to_mint} with the content {string}"))})

def mint_erc721_no_data(msg_sender,erc721_to_mint,mint_header):
    mint_header = clean_header(mint_header)
    data = encode(['address'], [msg_sender])
    payload = f"0x{(mint_header+data).hex()}"
    voucher = {"destination": erc721_to_mint , "payload": payload}
    logger.info(f"voucher {voucher}")
    send_voucher(voucher)
    
    send_notice({"payload": str2hex(str(f"Emmited voucher to mint ERC721 {erc721_to_mint}"))})

def clean_header(mint_header):
    if mint_header[:2] == "0x":
        mint_header = mint_header[2:]
    mint_header = bytes.fromhex(mint_header)
    return mint_header

###
# handlers

def handle_advance(data):
    logger.info(f"Received advance request data")
    logger.info(data)
    status = "accept"
    payload = None
    sender = data["metadata"]["msg_sender"].lower()
    try:
        payload = data["payload"]

        # Check whether an input was sent by the relay
        if sender == DAPP_RELAY_ADDRESS:
            logger.info(f"Received advance from dapp relay")
            global rollup_address
            rollup_address = payload
            send_report({"payload": str2hex(f"Set rollup_address {rollup_address}")})
        elif sender in [ETHER_PORTAL_ADDRESS,ERC20_PORTAL_ADDRESS,ERC721_PORTAL_ADDRESS]:
            logger.info(f"Received advance from portal")
            # or was sent by the Portals, which is where deposits must come from
            handle_tx(sender,payload)
        else:
            payload = hex2str(payload)
            logger.info(f"Received str {payload}")
            if payload == "exception":
                status = "reject"
                exception = {"payload": str2hex(str(payload))}
                send_exception(exception)
                sys.exit(1)
            elif payload == "reject":
                status = "reject"
                report = {"payload": str2hex(str(payload))}
                send_report(report)
            elif payload == "report":
                report = {"payload": str2hex(str(payload))}
                send_report(report)
            elif payload[0:7] == "voucher":
                payload = f"{payload}"
                voucher = json.loads(payload[7:])
                send_voucher(voucher)
            elif payload == "notice":
                notice = {"payload": str2hex(str(payload))}
                send_notice(notice)
            else:
                try:
                    logger.info(f"Trying to decode json")
                    # try json data
                    json_data = json.loads(payload)
                    # check geo data
                    if json_data.get("fence") and json_data.get("latitude") and json_data.get("longitude"):
                        latitude = json_data["latitude"]
                        longitude = json_data["longitude"]
                        # logger.info(f"Received geo request lat,long({latitude},{longitude})")
                        # payload = f"{check_point_in_fence(latitude, longitude)}"
                        fence = json_data["fence"]
                        logger.info(f"Received geo request fence ({fence}) lat,long({latitude},{longitude})")
                        payload = f"{check_point_in_fence(fence, latitude, longitude)}"
                    # check sql
                    elif json_data.get("sql"):
                        sql_statement = json_data["sql"]
                        logger.info(f"Received sql statement ({sql_statement})")
                        payload = f"{process_sql_statement(sql_statement)}"
                    elif json_data.get("array"):
                        logger.info(f"Received array to sort ({json_data['array']})")
                        a = np.array(json_data["array"])
                        payload = f"{np.sort(a)}"
                    elif json_data.get("image"):
                        b64out = process_image(json_data["image"].encode("utf-8"))
                        payload = f"{b64out}"
                        if json_data.get("erc721_to_mint") and json_data.get("selector"):
                            mint_erc721_with_uri_from_image(sender,json_data["erc721_to_mint"],json_data["selector"],b64out)
                    elif json_data.get("erc721_to_mint") and json_data.get("selector"):
                        logger.info(f"Received mint request to ({json_data['erc721_to_mint']})")
                        if json_data.get("string"):
                            mint_erc721_with_string(sender,json_data["erc721_to_mint"],json_data["selector"],json_data["string"])
                        else:
                            mint_erc721_no_data(sender,json_data["erc721_to_mint"],json_data["selector"])
                    else:
                        raise Exception('Not supported json operation')
                except Exception as e2:
                    msg = f"Not valid json: {e2}"
                    traceback.print_exc()
                    logger.info(msg)
    except Exception as e:
        status = "reject"
        msg = f"Error: {e}"
        traceback.print_exc()
        logger.error(msg)
        send_report({"payload": str2hex(msg)})

    if not payload:
        payload = data["payload"]
    else:
        payload = str2hex(str(payload))
    notice = {"payload": payload}
    send_notice(notice)

    logger.info(f"Notice payload was {payload}")
    return status

def handle_tx(sender,payload):
    binary = hex2binary(payload)
    voucher = None

    if sender == ERC20_PORTAL_ADDRESS:
        logger.info(f"Received ERC20 deposit")

        ret = binary[:1]
        token_address = binary2hex(binary[1:21])
        depositor = binary2hex(binary[21:41])
        amount = int.from_bytes(binary[41:73], "big")
        deposit_data = binary[73:]

        # Function to be called in voucher [token_address].transfer([address receiver],[uint256 amount])
        receiver = depositor
        data = encode(['address', 'uint256'], [receiver,amount])
        voucher_payload = binary2hex(ERC20_TRANSFER_FUNCTION_SELECTOR + data)
        voucher = {"destination": token_address, "payload": voucher_payload}

    elif sender == ERC721_PORTAL_ADDRESS:
        logger.info(f"Received ERC721 deposit")

        token_address = binary2hex(binary[:20])
        depositor = binary2hex(binary[20:40])
        token_id = int.from_bytes(binary[40:72], "big")
        deposit_data = binary[72:]

        # send deposited erc721 back to depositor
        if rollup_address is not None:
            # Function to be called in voucher [token_address].transfer([address sender],[address receiver],[uint256 id])
            receiver = depositor
            data = encode(['address', 'address', 'uint256'], [sender,receiver,token_id])
            voucher_payload = binary2hex(ERC721_SAFETRANSFER_FUNCTION_SELECTOR + data)
            voucher = {"destination": token_address, "payload": voucher_payload}

    elif sender == ETHER_PORTAL_ADDRESS:
        logger.info(f"Received Ether deposit ({rollup_address})")
        depositor = binary2hex(binary[:20])
        amount = int.from_bytes(binary[20:52], "big")
        deposit_data = binary[52:]

        logger.info(f"Received Ether deposit ({depositor}) ({amount}) ({deposit_data})")
        # send deposited ether back to depositoramount
        if rollup_address is not None:
            # Function to be called in voucher [rollups_address].withdrawEther([address sender],[uint256 amount])
            receiver = depositor
            data = encode(['address', 'uint256'], [receiver,amount])
            voucher_payload = binary2hex(ETHER_WITHDRAWAL_FUNCTION_SELECTOR + data)
            voucher = {"destination": rollup_address, "payload": voucher_payload}
            logger.info(f"Received Ether deposit ({voucher})")

    else:
        pass

    if voucher:
        send_voucher(voucher)
        logger.info(f"Voucher was {voucher}")

def handle_inspect(request):
    data = request["data"]
    logger.info(f"Received inspect request {data}")
    logger.info("Adding report")
    report = {"payload": data["payload"]}
    send_report(report)
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}
rollup_address = None

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])