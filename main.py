from concurrent.futures import ThreadPoolExecutor
import subprocess


class WindowsCmdRunner:

    def __init__(self, subnet: str = "192.168.1.") -> None:
        self.subnet = subnet
        self.last_output: list = []

    def ping_single(self, ip: str) -> str | None:
        result = subprocess.run(
            ["ping", ip, "-n", "1", "-w", "300"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            return ip
        return None

    def scan(self) -> list:
        ip_list = [f"{self.subnet}{i}" for i in range(1, 255)]

        with ThreadPoolExecutor(max_workers=30) as executor:
            results = executor.map(self.ping_single, ip_list)

            self.last_output = [ip for ip in results if ip is not None]

        return self.last_output

    def __str__(self) -> str:
        return f"Active IPs: {self.last_output}"


if __name__ == "__main__":
    runner = WindowsCmdRunner()
    runner.scan()
    print(runner)