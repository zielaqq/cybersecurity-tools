# network_info.py
import socket
import platform
import subprocess
import re


def print_banner():
    print("\n" + "=" * 60)
    print("🌐  NETWORK INFORMATION TOOL  🌐")
    print("    By Hubert Zieliński")
    print("=" * 60 + "\n")


def get_local_ip():
    """Pobiera lokalny adres IP"""
    try:
        # Tworzymy tymczasowe połączenie
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Nie można ustalić"


def get_public_ip():
    """Próbuje uzyskać publiczny IP (uproszczone)"""
    try:
        # Używamy socket do sprawdzenia nazwy hosta
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "Nie można ustalić"


def get_hostname():
    """Pobiera nazwę hosta"""
    return socket.gethostname()


def get_default_gateway():
    """Pobiera bramę domyślną (tylko Windows)"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            output = result.stdout

            # Szukamy Default Gateway
            match = re.search(r'Default Gateway.*: ([\d.]+)', output)
            if match:
                return match.group(1)
        return "Nie można ustalić"
    except:
        return "Błąd"


def get_dns_servers():
    """Próbuje znaleźć serwery DNS (tylko Windows)"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
            output = result.stdout

            # Szukamy DNS Servers
            dns_matches = re.findall(r'DNS Servers.*: ([\d.]+)', output)
            if dns_matches:
                return dns_matches
        return ["Nie można ustalić"]
    except:
        return ["Błąd"]


def ping_test(host):
    """Testuje ping do hosta"""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False


def main():
    print_banner()

    print("📋 INFORMACJE O SYSTEMIE:")
    print(f"   System operacyjny: {platform.system()} {platform.release()}")
    print(f"   Nazwa komputera: {get_hostname()}")

    print("\n🌐 INFORMACJE O SIECI:")
    print(f"   Lokalny IP: {get_local_ip()}")
    print(f"   Brama domyślna: {get_default_gateway()}")

    dns_servers = get_dns_servers()
    print(f"   Serwery DNS:")
    for dns in dns_servers:
        print(f"     • {dns}")

    print("\n🔍 TEST ŁĄCZNOŚCI:")

    test_hosts = [
        ("Google DNS", "8.8.8.8"),
        ("Cloudflare DNS", "1.1.1.1"),
        ("Brama domyślna", get_default_gateway())
    ]

    for name, host in test_hosts:
        if host and host not in ["Nie można ustalić", "Błąd"]:
            print(f"   Ping {name} ({host})...", end=" ")
            if ping_test(host):
                print("✅ OK")
            else:
                print("❌ BŁĄD")

    print("\n" + "=" * 60 + "\n")

    # Dodatkowe opcje
    print("🔧 DODATKOWE OPCJE:")
    print("   1 - Sprawdź konkretny adres")
    print("   2 - Rozwiąż nazwę domenową")
    print("   q - Wyjście")

    choice = input("\nWybierz opcję: ").strip()

    if choice == '1':
        host = input("Podaj adres IP lub domenę: ").strip()
        if ping_test(host):
            print(f"✅ Host {host} jest osiągalny")
        else:
            print(f"❌ Host {host} nie odpowiada")

    elif choice == '2':
        domain = input("Podaj nazwę domeny: ").strip()
        try:
            ip = socket.gethostbyname(domain)
            print(f"✅ {domain} → {ip}")
        except:
            print(f"❌ Nie można rozwiązać domeny {domain}")

    print("\n👋 Dziękuję za skorzystanie z programu!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Przerwano program")