'''
Сделано Mizogg Tools для помощи в поиске биткойнов. Удачи и счастливой охоты Miz_Tools_ice_RU.py Версия 1

Using iceland2k14 secp256k1 https://github.com/iceland2k14/secp256k1  fastest Python Libary

https://mizogg.co.uk
'''
import requests, codecs, hashlib, ecdsa, bip32utils, binascii
from bit.base58 import b58decode_check
from bit.utils import bytes_to_hex
import secp256k1 as ice
from mnemonic import Mnemonic


def get_balance(addr):
    contents = requests.get('https://sochain.com/api/v2/get_address_balance/BTC/' + addr, timeout=10)
    res = contents.json()
    response = (contents.content)
    balance = dict(res['data'])['confirmed_balance']
    return balance

class BrainWallet:

    @staticmethod
    def generate_address_from_passphrase(passphrase):
        private_key = str(hashlib.sha256(
            passphrase.encode('utf-8')).hexdigest())
        address =  BrainWallet.generate_address_from_private_key(private_key)
        return private_key, address

    @staticmethod
    def generate_address_from_private_key(private_key):
        public_key = BrainWallet.__private_to_public(private_key)
        address = BrainWallet.__public_to_address(public_key)
        return address

    @staticmethod
    def __private_to_public(private_key):
        private_key_bytes = codecs.decode(private_key, 'hex')
        # Get ECDSA public key
        key = ecdsa.SigningKey.from_string(
            private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
        key_bytes = key.to_string()
        key_hex = codecs.encode(key_bytes, 'hex')
        # Add bitcoin byte
        bitcoin_byte = b'04'
        public_key = bitcoin_byte + key_hex
        return public_key

    @staticmethod
    def __public_to_address(public_key):
        public_key_bytes = codecs.decode(public_key, 'hex')
        # Run SHA256 for the public key
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        # Run ripemd160 for the SHA256
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
        # Add network byte
        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(
            network_bitcoin_public_key, 'hex')
        # Double SHA256 to get checksum
        sha256_nbpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_nbpk_digest = sha256_nbpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
        checksum = sha256_2_hex[:8]
        # Concatenate public key and checksum to get the address
        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
        wallet = BrainWallet.base58(address_hex)
        return wallet

    @staticmethod
    def base58(address_hex):
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        b58_string = ''
        # Get the number of leading zeros and convert hex to decimal
        leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
        # Convert hex to decimal
        address_int = int(address_hex, 16)
        # Append digits to the start of string
        while address_int > 0:
            digit = address_int % 58
            digit_char = alphabet[digit]
            b58_string = digit_char + b58_string
            address_int //= 58
        # Add '1' for each 2 leading zeros
        ones = leading_zeros // 2
        for one in range(ones):
            b58_string = '1' + b58_string
        return b58_string

def data_wallet():
    for child in range(0,20):
        bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
        bip32_child_key_obj = bip32_root_key_obj.ChildKey(
            44 + bip32utils.BIP32_HARDEN
        ).ChildKey(
            0 + bip32utils.BIP32_HARDEN
        ).ChildKey(
            0 + bip32utils.BIP32_HARDEN
        ).ChildKey(0).ChildKey(child)
        data.append({
                'bip32_root_key': bip32_root_key_obj.ExtendedKey(),
                'bip32_extended_private_key': bip32_child_key_obj.ExtendedKey(),
                'path': f"m/44'/0'/0'/0/{child}",
                'address': bip32_child_key_obj.Address(),
                'publickey': binascii.hexlify(bip32_child_key_obj.PublicKey()).decode(),
                'privatekey': bip32_child_key_obj.WalletImportFormat(),
            })

prompt= '''
    ************************ Главное меню Mizogg's Tools **********************************
    *                                                                                     *
    *  Вариант 1. Биткойн-адрес с проверкой баланса                          =  1         *
    *  Вариант 2. Биткойн-адрес на HASH160                                   =  2         *
    *  Вариант 3. HASH160 на биткойн-адрес (не работает)                     =  3         *
    *  Вариант 4. Мозговой кошелек Биткойн с проверкой баланса               =  4         *
    *  Вариант 5. Шестнадцатеричный код в десятичный (HEX 2 DEC)             =  5         *
    *  Вариант 6. Десятичный в шестнадцатеричный (DEC 2 HEX)                 =  6         *
    *  Вариант 7. Шестнадцатеричный адрес в биткойн с проверкой баланса      =  7         *
    *  Вариант 8. Десятичный адрес в биткойн с проверкой баланса             =  8         *
    *  Вариант 9. Мнемонические слова для биткойн-адреса с проверкой баланса =  9         *
    *                                                                                     *
    ************ Главное меню Mizogg's Tools Using iceland2k14 secp256k1 ******************

Введите свой выбор здесь Enter 1-9 : 
'''


while True:
    data = []
    start=int(input(prompt))
    if start == 1:
        print ('Инструмент проверки баланса адреса')
        addr = str(input('Введите здесь свой биткойн-адрес : '))
        print ('\nBitcoin Address = ', addr, '    Balance = ', get_balance(addr), ' BTC')
    elif start == 2:
        print ('Адрес для инструмента HASH160')
        addr = str(input('Введите здесь свой биткойн-адрес : '))
        hash160=b58decode_check(addr)
        address_hash160 = bytes_to_hex(hash160)[2:]
        print ('\nBitcoin Address = ', addr, '\nTo HASH160 = ', address_hash160)
    elif start == 3:
        print ('Инструмент HASH160 для биткойн-адреса')
        hash160 =(str(input('Введите свой HASH160 здесь : ')))
        print ('Скоро не работает')
    elif start == 4:
        print ('Мозговой кошелек Биткойн Адрес Инструмент')    
        passphrase = (input("Введите пароль ЗДЕСЬ : "))
        wallet = BrainWallet()
        private_key, addr = wallet.generate_address_from_passphrase(passphrase)
        print('\nPassphrase     = ',passphrase)
        print('Private Key      = ',private_key)
        print('Bitcoin Address  = ', addr, '    Balance = ', get_balance(addr), ' BTC')
    elif start == 5:
        print('Шестнадцатеричный в десятичный инструмент')
        HEX = str(input('Введите свой шестнадцатеричный HEX здесь : '))
        dec = int(HEX, 16)
        print('\nHexadecimal = ',HEX, '\nTo Decimal = ', dec)
    elif start == 6:
        print('Десятичный в шестнадцатеричный инструмент')
        dec = int(input('Введите свой десятичный DEC здесь : '))
        HEX = "%064x" % dec
        print('\nDecimal = ', dec, '\nTo Hexadecimal = ', HEX)
    elif start == 7:
        print('Инструмент преобразования шестнадцатеричного адреса в биткойн')
        HEX=str(input("Шестнадцатеричный HEX ->  "))
        dec = int(HEX, 16)
        wifc = ice.btc_pvk_to_wif(HEX)
        wifu = ice.btc_pvk_to_wif(HEX, False)
        caddr = ice.privatekey_to_address(0, True, dec) #Compressed
        uaddr = ice.privatekey_to_address(0, False, dec)  #Uncompressed
        p2sh = ice.privatekey_to_address(1, True, dec) #p2sh
        bech32 = ice.privatekey_to_address(2, True, dec)  #bech32
        query = {caddr}|{uaddr}|{p2sh}|{bech32}
        request = requests.get("https://blockchain.info/multiaddr?active=" + ','.join(query), timeout=10)
        try:
            request = request.json()
            print('PrivateKey (hex) : ', HEX)
            print('PrivateKey (dec) : ', dec)
            print('PrivateKey (wif) Compressed   : ', wifc)
            print('PrivateKey (wif) UnCompressed : ', wifu)
            print('Bitcoin Address Compressed   = ', caddr, '    Balance = ', get_balance(caddr), ' BTC')
            print('Bitcoin Address UnCompressed = ', uaddr, '    Balance = ', get_balance(uaddr), ' BTC')
            print('Bitcoin Address p2sh         = ', p2sh, '    Balance = ', get_balance(p2sh), ' BTC')
            print('Bitcoin Address Bc1  bech32  = ', bech32, '    Balance = ', get_balance(bech32), ' BTC')
            for row in request["addresses"]:
                print(row)
        except:
            pass
    elif start == 8:
        print('Инструмент преобразования десятичного адреса в биткойн')
        dec=int(input('Десятичный Dec (Максимум 115792089237316195423570985008687907852837564279074904382605163141518161494336 ) ->  '))
        HEX = "%064x" % dec  
        wifc = ice.btc_pvk_to_wif(HEX)
        wifu = ice.btc_pvk_to_wif(HEX, False)
        caddr = ice.privatekey_to_address(0, True, dec) #Compressed
        uaddr = ice.privatekey_to_address(0, False, dec)  #Uncompressed
        p2sh = ice.privatekey_to_address(1, True, dec) #p2sh
        bech32 = ice.privatekey_to_address(2, True, dec)  #bech32
        query = {caddr}|{uaddr}|{p2sh}|{bech32}
        request = requests.get("https://blockchain.info/multiaddr?active=" + ','.join(query), timeout=10)
        try:
            request = request.json()
            print('PrivateKey (hex) : ', HEX)
            print('PrivateKey (dec) : ', dec)
            print('PrivateKey (wif) Compressed   : ', wifc)
            print('PrivateKey (wif) UnCompressed : ', wifu)
            print('Bitcoin Address Compressed   = ', caddr, '    Balance = ', get_balance(caddr), ' BTC')
            print('Bitcoin Address UnCompressed = ', uaddr, '    Balance = ', get_balance(uaddr), ' BTC')
            print('Bitcoin Address p2sh         = ', p2sh, '    Balance = ', get_balance(p2sh), ' BTC')
            print('Bitcoin Address Bc1  bech32  = ', bech32, '    Balance = ', get_balance(bech32), ' BTC')
            for row in request["addresses"]:
                print(row)
        except:
            pass
    elif start == 9:
        print('Мнемоника 12/15/18/21/24 Words to Bitcoin Address Tool')
        wordlist = str(input('Введите свои мнемонические слова = '))
        mnemo = Mnemonic("english")
        mnemonic_words = wordlist
        seed = mnemo.to_seed(mnemonic_words, passphrase="")
        data_wallet()
        for target_wallet in data:
            print('\nmnemonic_words  : ', mnemonic_words, '\nDerivation Path : ', target_wallet['path'], '\nBitcoin Address : ', target_wallet['address'], ' Balance = ', get_balance(target_wallet['address']), ' BTC', '\nPrivatekey WIF  : ', target_wallet['privatekey'])
      
    else:
        print("WRONG NUMBER!!! MUST CHOSE 1 - 9 ")
        break