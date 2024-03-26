from aptos_sdk.async_client import RestClient
from fake_useragent import UserAgent
from ecdsa.curves import Ed25519
from core.constants import *
from utils.log import log
import json as js
import hashlib
import struct
import hmac


class PublicKey25519:
    def __init__(self, private_key):
        self.private_key = private_key

    def __bytes__(self):
        sk = Ed25519.SigningKey(self.private_key)
        return '\x00' + sk.get_verifying_key().to_bytes()


class AptosClient(RestClient):
    node_url = "https://fullnode.mainnet.aptoslabs.com/v1"

    def __init__(self):
        super().__init__(AptosClient.node_url)

        self.BIP39_PBKDF2_ROUNDS = 2048
        self.BIP39_SALT_MODIFIER = "mnemonic"
        self.BIP32_PRIVDEV = 0x80000000
        self.BIP32_SEED_ED25519 = b'ed25519 seed'
        self.APTOS_DERIVATION_PATH = "m/44'/637'/0'/0'/0'"
        self.ua = UserAgent()

    async def check_eligibility(self, session, wallet, credential, retry=1):
        try:
            session.headers.update({"User-Agent": self.ua.random})
            json = {
                "operationName": QUERIES["Cred"]["name"],
                "variables": {
                    "id": credential["id"],
                    "eligibleAddress": str(wallet.address())
                },
                "query": QUERIES["Cred"]["query"]
            }
            response = await session.post(url=GALXE_API_URL, json=json)

            if js.loads(response.text)["data"]["credential"]["eligible"] == 1:
                log.success(f'{wallet.address()} | {credential["name"]} | Check eligibility | Attempt {retry}/3 | '
                            f'Wallet is eligible')
                return True

            else:
                log.warning(f'{wallet.address()} | {credential["name"]} | Check eligibility | Attempt {retry}/3 | '
                            f'Wallet is not eligible')
                return False

        except Exception as error:
            log.error(f'{wallet} | {credential["name"]} | Check eligibility | Attempt {retry}/3 | '
                      f'Error: {error}')
            retry += 1

            if retry > 3:
                log.critical(f'{wallet.address()} | {credential["name"]} | Check eligibility | '
                             f'Wallet failed after 3 retries')
                return False

            return await self.check_eligibility(session, wallet, credential, retry)

    def mnemonic_to_bip39seed(self, mnemonic, passphrase):
        mnemonic = bytes(mnemonic, 'utf8')
        salt = bytes(self.BIP39_SALT_MODIFIER + passphrase, 'utf8')

        return hashlib.pbkdf2_hmac('sha512', mnemonic, salt, self.BIP39_PBKDF2_ROUNDS)

    def derive_bip32childkey(self, parent_key, parent_chain_code, i):
        assert len(parent_key) == 32
        assert len(parent_chain_code) == 32

        k = parent_chain_code

        if (i & self.BIP32_PRIVDEV) != 0:
            key = b'\x00' + parent_key

        else:
            key = bytes(PublicKey25519(parent_key))

        d = key + struct.pack('>L', i)
        h = hmac.new(k, d, hashlib.sha512).digest()
        key, chain_code = h[:32], h[32:]

        return key, chain_code

    def mnemonic_to_private_key(self, mnemonic, passphrase=""):
        derivation_path = self.parse_derivation_path()
        bip39seed = self.mnemonic_to_bip39seed(mnemonic, passphrase)
        master_private_key, master_chain_code = self.bip39seed_to_bip32masternode(
            bip39seed)
        private_key, chain_code = master_private_key, master_chain_code

        for i in derivation_path:
            private_key, chain_code = self.derive_bip32childkey(
                private_key, chain_code, i)

        return "0x" + private_key.hex()

    def bip39seed_to_bip32masternode(self, seed):
        h = hmac.new(self.BIP32_SEED_ED25519, seed, hashlib.sha512).digest()
        key, chain_code = h[:32], h[32:]

        return key, chain_code

    def parse_derivation_path(self):
        path = []

        if self.APTOS_DERIVATION_PATH[0:2] != 'm/':
            raise ValueError(
                "Can't recognize derivation path. It should look like \"m/44'/chaincode/change'/index\".")

        for i in self.APTOS_DERIVATION_PATH.lstrip('m/').split('/'):
            if "'" in i:
                path.append(self.BIP32_PRIVDEV + int(i[:-1]))

            else:
                path.append(int(i))

        return path
