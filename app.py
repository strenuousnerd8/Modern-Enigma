from flask import Flask, render_template, url_for, request
import json
from AES_code import AES
from ECC_code import ECC
import converter
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/result',methods=['POST', 'GET'])

def result():
    output = request.form.to_dict()
    input_file = output["name"]
    file_type = input_file.split(".")[1]
    multimedia_data = converter.fileToBase64("test_files/" + input_file)
    displayer = multimedia_data[0:100]
    aes_key = 57811460909138771071931939740208549692
    # Encrypt  AES_key with ECC public key
    ecc_obj_AESkey = ECC.ECC()
    private_key = 59450895769729158456103083586342075745962357150281762902433455229297926354304
    public_key = ecc_obj_AESkey.gen_pubKey(private_key)
    (C1_aesKey, C2_aesKey) = ecc_obj_AESkey.encryption(public_key, str(aes_key))
    # Encrypt the multimedia_data with AES algorithm
    print(aes_key)
    aes = AES.AES(aes_key)
    encrypted_multimedia = aes.encryptBigData(multimedia_data)
    print(encrypted_multimedia)
    data_for_ecc = converter.makeSingleString(encrypted_multimedia)
    print(data_for_ecc)
    # Encrypt the encrypted_multimedia with ECC
    ecc = ECC.ECC()
    (C1_multimedia, C2_multimedia) = ecc.encryption(public_key, data_for_ecc)
    cipher = {
        "file_type": file_type,
        "C1_aesKey": C1_aesKey,
        "C2_aesKey": C2_aesKey,
        "C1_multimedia": C1_multimedia,
        "C2_multimedia": C2_multimedia,
        "private_key": private_key
    }
    with open('cipher.json', 'w') as fp:
        json.dump(cipher, fp)
    print('Encryption Done ')
    return render_template('index.html', name = encrypted_multimedia, display = displayer, aesdisp = aes_key, eccdisp = data_for_ecc)


@app.route('/decrypt',methods=['POST', 'GET'])
def decrypt():
    with open('cipher.json') as f:
        data = json.load(f)
    C1_aesKey = data["C1_aesKey"]
    C2_aesKey = data["C2_aesKey"]
    private_key = data["private_key"]
    file_type = data["file_type"]
    # Decrypt with ECC to get the AES key
    ecc_AESkey = ECC.ECC()
    decryptedAESkey = ecc_AESkey.decryption(C1_aesKey, C2_aesKey, private_key)
    C1_multimedia = data["C1_multimedia"]
    C2_multimedia = data["C2_multimedia"]
    # Decrypt the data with ECC
    ecc_obj = ECC.ECC()
    encrypted_multimedia = ecc_obj.decryption(C1_multimedia, C2_multimedia, private_key)
    clean_data_list = converter.makeListFromString(encrypted_multimedia)
    # Decrypt with AES
    aes_obj = AES.AES(int(decryptedAESkey))
    decrypted_multimedia = aes_obj.decryptBigData(clean_data_list)
    # Decode from Base64 to the corresponding fileToBase64
    output_file = "Decrypted_file."+file_type
    converter.base64ToFile(decrypted_multimedia, output_file)
    dec_result = "Decryption Done and file saved in project folder with name Decrypted_file."
    return render_template('index.html', decout = dec_result)

if __name__ == "__main__":
    app.run(debug=True)
