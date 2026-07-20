#!/usr/bin/env python3
import argparse
import json
import logging
import re
import sys

from technitium_dns_mcp.api.api_client import Api

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DNSAdapter:
    def parse(self, file_path):
        """Parse the DNS records. Must be implemented by subclasses."""

        return []


class AdGuardAdapter(DNSAdapter):
    def parse(self, file_path):
        records = []
        logging.info("Parsing configured AdGuard rewrites file")
        with open(file_path) as f:
            data = json.load(f)

        # AdGuard can export as a list of {"domain": "...", "answer": "..."}
        entries = data if isinstance(data, list) else data.get("rewrites", [])
        for entry in entries:
            domain = entry.get("domain") or entry.get("domainName")
            answer = entry.get("answer") or entry.get("ip") or entry.get("ipAddress")
            if domain and answer:
                records.append({"domain": domain, "answer": answer, "type": "A"})
        return records


class PiholeAdapter(DNSAdapter):
    def parse(self, file_path):
        records = []
        logging.info("Parsing configured Pi-hole custom-list file")
        # Pi-hole custom list is typically standard hosts format: <ip> <domain>
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = re.split(r"\s+", line)
                if len(parts) >= 2:
                    ip, domain = parts[0], parts[1]
                    records.append({"domain": domain, "answer": ip, "type": "A"})
        return records


class BindAdapter(DNSAdapter):
    def parse(self, file_path):
        records = []
        logging.info("Parsing configured Bind9 zone file")
        # Standard zone format parser (simplified example matching basic A records)
        a_record_pattern = re.compile(
            r"^([a-zA-Z0-9_\-\.]+)\s+(?:\d+\s+)?(?:IN\s+)?A\s+([0-9\.]+)"
        )
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(";"):
                    continue
                match = a_record_pattern.match(line)
                if match:
                    domain, ip = match.group(1), match.group(2)
                    records.append({"domain": domain, "answer": ip, "type": "A"})
        return records


class GenericAdapter(DNSAdapter):
    def parse(self, file_path):
        records = []
        logging.info("Parsing configured generic DNS JSON file")
        with open(file_path) as f:
            data = json.load(f)
        for entry in data:
            domain = entry.get("domain") or entry.get("host")
            answer = entry.get("answer") or entry.get("ip") or entry.get("value")
            rtype = entry.get("type", "A")
            if domain and answer:
                records.append({"domain": domain, "answer": answer, "type": rtype})
        return records


def get_adapter(format_name):
    adapters = {
        "adguard": AdGuardAdapter,
        "pihole": PiholeAdapter,
        "bind": BindAdapter,
        "generic": GenericAdapter,
    }
    adapter_class = adapters.get(format_name.lower())
    if not adapter_class:
        raise ValueError(
            f"Unsupported DNS format: {format_name}. Supported: {list(adapters.keys())}"
        )
    return adapter_class()


def migrate_records(records, technitium_url, user, password, zone_name="arpa"):
    logging.info("Connecting to configured Technitium DNS service")
    api = Api(base_url=technitium_url)

    # Authenticate
    try:
        login_res = api.login(user=user, password=password)
        token = login_res.get("token")
        if not token:
            logging.error("Technitium authentication failed")
            sys.exit(1)
        api.token = token
        logging.info("Successfully authenticated with Technitium DNS API.")
    except Exception as e:
        logging.error(
            "Technitium connection or authentication failed: error_type=%s",
            type(e).__name__,
        )
        sys.exit(1)

    # Ensure zone exists
    try:
        zones_res = api.list_zones()
        zones = [z["name"] for z in zones_res.get("zones", [])]
        if zone_name not in zones:
            logging.info("Creating configured authoritative zone")
            api.create_zone(zone=zone_name)
        else:
            logging.info("Configured authoritative zone is already present")
    except Exception as e:
        logging.error(
            "Failed to list or create configured zone: error_type=%s",
            type(e).__name__,
        )
        sys.exit(1)

    # Migrate parsed records
    success_count = 0
    fail_count = 0
    for record in records:
        domain = record["domain"]
        answer = record["answer"]
        rtype = record["type"]

        if not domain.endswith(f".{zone_name}") and domain != zone_name:
            logging.warning("Skipping DNS record outside authoritative zone scope")
            continue

        logging.info("Adding DNS record: record_type=%s", rtype)
        try:
            res = api.add_record(
                zone=zone_name,
                domain=domain,
                type=rtype,
                ipAddress=answer,
                overwrite=True,
            )
            if res.get("status") == "ok":
                success_count += 1
            else:
                logging.error("Technitium rejected a DNS record")
                fail_count += 1
        except Exception as e:
            logging.error(
                "DNS record migration failed: error_type=%s", type(e).__name__
            )
            fail_count += 1

    logging.info(
        f"Migration Complete: Successfully loaded {success_count} records. Failed {fail_count} records."
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generalized DNS Migrator to Technitium DNS"
    )
    parser.add_argument(
        "--source-file", required=True, help="Path to input source file"
    )
    parser.add_argument(
        "--source-format",
        required=True,
        choices=["adguard", "pihole", "bind", "generic"],
        help="Format of the source file",
    )
    parser.add_argument(
        "--technitium-url",
        required=True,
        help="Base URL of Technitium DNS (e.g. http://192.0.2.199:5380)",
    )
    parser.add_argument("--user", default="admin", help="Technitium admin user")
    parser.add_argument("--password", required=True, help="Technitium admin password")
    parser.add_argument(
        "--zone", default="arpa", help="Primary authoritative zone name"
    )

    args = parser.parse_args()

    try:
        adapter = get_adapter(args.source_format)
        records = adapter.parse(args.source_file)
    except Exception as e:
        logging.error("DNS source parsing failed: error_type=%s", type(e).__name__)
        sys.exit(1)

    if not records:
        logging.warning("No records extracted from the source file. Exiting.")
        sys.exit(0)

    migrate_records(records, args.technitium_url, args.user, args.password, args.zone)


if __name__ == "__main__":
    main()
