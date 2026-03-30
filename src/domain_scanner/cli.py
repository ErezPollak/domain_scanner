import argparse
import asyncio
from domain_scanner.crew import DomainScanner


def main():
    """
    Command Line Interface for DomainScanner.
    This script is dedicated strictly for local interactive use.
    The CrewAI AMP deployment service will continue to target main.py natively.
    """
    parser = argparse.ArgumentParser(
        description="DomainScanner CLI: AI-Powered Web Analysis Tool"
    )

    parser.add_argument(
        "--domain",
        type=str,
        required=True,
        help="The target domain to scan (e.g., example.com)",
    )

    args = parser.parse_args()

    print(f"\n🚀 Initializing DomainScanner for target: {args.domain}")
    print("==================================================\n")

    inputs = {"domain": args.domain}

    try:
        scanner = DomainScanner()

        # Execute the AI agent workflow
        asyncio.run(scanner.crew().akickoff(inputs=inputs))

        print(
            f"\n✅ Scan completed! Check the 'reports' directory for '{args.domain}_report.md'."
        )

    except Exception as e:
        print(f"\n❌ An error occurred during execution: {e}")


if __name__ == "__main__":
    main()
