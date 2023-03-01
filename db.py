import subprocess
import configparser
import os

def root_add(id_user):
    #создает навовый конфиг для подключения к wireguard
    if subprocess.call(["./newclient.sh", id_user]) == 0:
        return True
    return False


def get_client_list():
    call = subprocess.check_output("awk '/# BEGIN_PEER/ {print $3}' /etc/wireguard/wg0.conf", shell=True)
    client_list = call.decode('utf-8').split('\n')
    call = subprocess.check_output("awk '/AllowedIPs/ {print $3, $4}' /etc/wireguard/wg0.conf", shell=True)
    ip_list = call.decode('utf-8').split('\n')
    
    return [[client, ip_list[n]] for n , client in enumerate(client_list)]


def deactive_user_db(id_user):
    #удаеть конфиг клиента из wireguard и отмечает это в своей базе
    id_user = str(id_user)
    if subprocess.call(["./removeclient.sh", str(id_user)]) == 0:
        return True
    return False


def create_config(path='setting.ini', bot_token='', admin_id=''):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("setting")
    config.set("setting", "bot_token", f'{bot_token}')
    config.set("setting", "admin_id", f'{admin_id}')

    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path='setting.ini'):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        bot_token = str(input('Input telegram bot token: '))
        admin_id = str(input('Input telegram id admin'))
        create_config(path, bot_token, admin_id)

    config = configparser.ConfigParser()
    config.read(path)
    out = {}
    for key in config['setting']:
        out[key] = config['setting'][key]

    return out



if __name__ == "__main__":
    #add_in_db(34342322)
    get_client_list()
    pass

