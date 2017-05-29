import requests
import socket
import select
import time

# Setup functions for discovering and authenticating your Auroras
# For instructions or bug reports, please visit
# https://github.com/software-2/nanoleaf

def find_auroras(seek_time: float = 30):
    """
    Returns a list of the IP addresses of all Auroras found on the network
    
    Discovery will take about 30 seconds by default.
    If your Auroras are not found, try increasing the seek time to 90 seconds.
    """
    SSDP_IP = "239.255.255.250"
    SSDP_PORT = 1900
    SSDP_MX = 3
    SSDP_ST = "nanoleaf_aurora:light"

    req = ['M-SEARCH * HTTP/1.1',
           'HOST: ' + SSDP_IP + ':' + str(SSDP_PORT),
           'MAN: "ssdp:discover"',
           'ST: ' + SSDP_ST,
           'MX: ' + str(SSDP_MX)]
    req = '\r\n'.join(req).encode('utf-8')

    auroraLocations = []
    def checkIfNewAurora(response):
        if not SSDP_ST in response:
            return
        for line in response.split("\n"):
            if "Location:" in line:
                newLocation = line.replace("Location:", "").strip() \
                                  .replace("http://", "") \
                                  .replace(":16021", "")
                if not newLocation in auroraLocations:
                    auroraLocations.append(newLocation)
                    print("New Aurora found at " + newLocation)
                return

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, SSDP_MX)
    sock.bind((socket.gethostname(), 9090))
    sock.sendto(req, (SSDP_IP, SSDP_PORT))
    sock.setblocking(False)

    timeout = time.time() + seek_time
    print("Starting discovery. This will continue for " + str(seek_time) + " seconds.")
    while time.time() < timeout:
        try:
            ready = select.select([sock], [], [], 5)
            if ready[0]:
                response = sock.recv(1024).decode("utf-8")
                checkIfNewAurora(response)
        except socket.error as err:
            print("Socket error while discovering SSDP devices!")
            print(err)
            print("If you are sure your network connection is working, please post an issue on the GitHub page: https://github.com/software-2/nanoleaf/issues")
            print("Please include as much information as possible, including your OS, how your computer is connected to your network, etc.")
            sock.close()
            break

    if len(auroraLocations) == 0:
        print("Discovery complete, but no Auroras found!")
        return auroraLocations
    print("Discovery complete! Found " + str(len(auroraLocations)) + " Auroras.")
    return auroraLocations

def generate_auth_token(self, ipAddress: str):
    '''
    Generates an auth token for the Aurora at the given IP address. 
    
    You must first press and hold the power button on the Aurora for about 5-7 seconds, until the white LED flashes briefly.
    '''
    url = "http://" + ipAddress + ":16021/api/v1/new"
    r = requests.post(url)
    if r.status_code == 200:
        print("Auth token for "  + ipAddress + " successfully generated!   " + str(r.json()))
        return r.json()['auth_token']
    if r.status_code == 401:
        print("Not Authorized! I don't even know how this happens. Please post an issue on the GitHub page: https://github.com/software-2/nanoleaf/issues")
    if r.status_code == 403:
        print("Forbidden! Press and hold the power button for 5-7 seconds first! (Light will begin flashing)")
    if r.status_code == 422:
        print("Unprocessable Entity! I'm blaming your network on this one.")
    return None