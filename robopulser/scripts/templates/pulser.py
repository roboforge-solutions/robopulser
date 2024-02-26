import argparse
from robopulser import robopulser

def main():
    parser = argparse.ArgumentParser(description="Script to call robopulser.yaml_pulse function with optional arguments.")

    parser.add_argument("--yaml", type=str, default="example.yml", help="Path to YAML model configuration file")
    parser.add_argument("--conn_str", type=str, default=None, help="Connection string (alternative to remaining parameters.)")
    parser.add_argument("--driver", type=str, default=None, help="Database driver")
    parser.add_argument("--user", type=str, default=None, help="Database user")
    parser.add_argument("--host", type=str, default=None, help="Database host")
    parser.add_argument("--name", type=str, default=None, help="Database name")
    parser.add_argument("--passwd", type=str, default=None, help="Database password")
    parser.add_argument("--port", type=int, default=None, help="Database port")


    args = parser.parse_args()

    robopulser.yaml_pulse(
        yaml_model_path=args.yaml,
        conn_str=args.conn_str,
        db_driver=args.driver,
        db_user=args.user,
        db_host=args.host,
        db_name=args.name,
        db_pass=args.passwd,
        db_port=args.port,
        logger=None
    )

if __name__ == "__main__":
    main()
