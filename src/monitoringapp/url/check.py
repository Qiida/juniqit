import subprocess


def ping(serverName):
    return str(subprocess.run(['ping', serverName], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout)


if __name__ == '__main__':
    print(ping(serverName="www.google.de"))
