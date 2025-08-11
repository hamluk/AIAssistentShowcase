from supabase import create_client

import os

class DatabaseConnection:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("Supabase URL and Key must be set in environment variables.")
        
        self.supabase_client = create_client(url, key)

    def list_all_customer(self) -> list[str]:
        """
        Lists all current customers.
        The priority is sorted from 1 to 5, where 1 is the highest priority and 5 is the lowest priority.

        Returns:
            [Customers]: List of all customers from database
        """

        response = self.supabase_client.table("customer").select("*").execute()

        if len(response.data) > 0:
            return response.data
        else:
            return "No customers found."
