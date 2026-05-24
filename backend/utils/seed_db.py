from services.data_service import load_superstore
from models.database import get_connection


def seed_orders():
    df = load_superstore()
    with get_connection() as conn:
        df.to_sql("orders", conn, if_exists="replace", index=False)
    print(f"Seeded {len(df)} rows into SQLite.")


if __name__ == "__main__":
    seed_orders()
