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
        Customers with low numbers are therfore more important than customers with high numbers.

        Returns:
            list[str]: List of all customers from database
        """

        response = self.supabase_client.table("customer").select("*").execute()

        if len(response.data) > 0:
            return response.data
        else:
            return "No customers found."
        
    def create_new_customer(self, firstname: str, lastname: str, age: int, priority: int, note: str) -> str:
        """
        Creates a new customer in the database.

        Args:
            firstname (str): The firstname of the customer
            lastname (str): The lastname of the customer
            age (int): The age of the customer, has to be from 1 to 100
            priority (int): The priority of the customer, choose a value based on his matchin interests to AI, MUST BE between 1 and 5. 1 is a high priority, 5 is a low priority.
            note (str): Note to the customer, tells what the customer is interested in
        
        Returns:
            str: Success message when creating the customer. If an error has occurred, a negative success message is returned.
        """

        customer = {
            "id": 17, # Special customer with ID 17. This customer will be replaced each time.
            "firstname": firstname,
            "lastname": lastname,
            "age": age,
            "priority": priority,
            "note": note
        }

        try:
            self.supabase_client.table("customer").upsert(customer).execute()
        except Exception as e:
            print(str(e))
            return f"An error occurred while creating the customer: {str(e)}"
    
        return "Customer created successfully."
