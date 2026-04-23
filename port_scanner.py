# port_scanner.py
import socket
import sys
from datetime import datetime


def scan_port(target, port):
    """
    Sprawdza czy port jest otwarty
    """
    try:
        # Tworzymy socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout 1 sekunda

        # Próbujemy połączyć
        result = sock.connect_ex((target, port))
        sock.close()

        return result == 0  # True jeśli port otwarty
    except socket.gaierror:
        print("❌ Nie można rozwiązać nazwy hosta")
        return False
    except socket.error:
        print("❌ Błąd połączenia")
        return False


def get_service_name(port):
    """
    Zwraca nazwę popularnej usługi dla danego portu
    """
    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        8080: "HTTP-Proxy"
    }
    return services.get(port, "Unknown")


def print_banner():
    print("\n" + "=" * 60)
    print("🔍  SIMPLE PORT SCANNER  🔍")
    print("    By Hubert Zieliński")
    print("=" * 60 + "\n")
    print("⚠️  UWAGA: Skanuj tylko własne systemy!")
    print("    Skanowanie cudzych systemów bez zgody jest nielegalne!\n")


def main():
    print_banner()

    # Pobierz cel
    target = input("Podaj adres IP lub domenę (np. 127.0.0.1): ").strip()

    if not target:
        print("❌ Musisz podać cel skanowania!")
        sys.exit()

    # Spróbuj rozwiązać nazwę hosta
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"❌ Nie można rozwiązać adresu: {target}")
        sys.exit()

    print(f"\n🎯 Cel: {target} ({target_ip})")
    print(f"⏰ Rozpoczęto: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    # Popularne porty do skanowania
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080]

    open_ports = []

    print("\n🔎 Skanowanie portów...\n")

    for port in common_ports:
        if scan_port(target_ip, port):
            service = get_service_name(port)
            print(f"✅ Port {port:5d} OTWARTY  - {service}")
            open_ports.append((port, service))
        else:
            print(f"❌ Port {port:5d} ZAMKNIĘTY", end='\r')  # Nadpisuje linię

    # Podsumowanie
    print("\n" + "-" * 60)
    print(f"\n📊 PODSUMOWANIE:")
    print(f"   Przeskanowano portów: {len(common_ports)}")
    print(f"   Otwartych portów: {len(open_ports)}")

    if open_ports:
        print("\n🔓 Otwarte porty:")
        for port, service in open_ports:
            print(f"   • Port {port} - {service}")
    else:
        print("\n🔒 Nie znaleziono otwartych portów")

    print(f"\n⏰ Zakończono: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Przerwano skanowanie przez użytkownika")
        sys.exit()