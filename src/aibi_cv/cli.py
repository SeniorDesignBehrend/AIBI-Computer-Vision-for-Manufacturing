"""CLI entry point for aibi-cv."""

import sys
import argparse
from pathlib import Path
from .vision_system import VisionSystem


def cmd_scan(args):
    """Run live scanning."""
    config_dir = Path(args.config_dir)
    db_path = Path(args.db_path)
    
    system = VisionSystem(
        workstation_id=args.workstation,
        config_dir=config_dir,
        db_path=db_path,
        camera_index=args.camera
    )
    
    system.run_live(display=not args.no_display)



def cmd_config(args):
    """Manage configurations."""
    from .config_manager import ConfigManager
    
    config_dir = Path(args.config_dir)
    manager = ConfigManager(config_dir)
    
    if args.list:
        print("Configured workstations:")
        for ws_id in manager.configs.keys():
            print(f"  - {ws_id}")
    elif args.create:
        config = manager.create_default_config(args.create)
        print(f"Created default config for: {args.create}")
        print(f"Config file: {config_dir / args.create}.json")


def main():
    parser = argparse.ArgumentParser(
        description="AIBI Computer Vision for Manufacturing"
    )
    
    parser.add_argument(
        "--config-dir",
        default="./data/config",
        help="Configuration directory"
    )
    parser.add_argument(
        "--db-path",
        default="./data/scans.db",
        help="Database path"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Run live scanning")
    scan_parser.add_argument(
        "--workstation",
        default="default",
        help="Workstation ID"
    )
    scan_parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Camera index"
    )
    scan_parser.add_argument(
        "--no-display",
        action="store_true",
        help="Disable video display"
    )
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configurations")
    config_parser.add_argument(
        "--list",
        action="store_true",
        help="List all workstations"
    )
    config_parser.add_argument(
        "--create",
        help="Create default config for workstation"
    )
    
    args = parser.parse_args()
    
    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "config":
        cmd_config(args)
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())