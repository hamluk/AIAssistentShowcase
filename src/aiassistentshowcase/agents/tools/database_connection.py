
class DatabaseConnection:
    def list_all_customer(self) -> list[str]:
        """
        Lists all current customers

        Returns:
            [Customers]: List of all customers from database
        """

        return "To be done"
        
    def create_new_customer(self, firstname: str, lastname: str, age: int, priority: int, note: str) -> str:
        """
        Creates a new customer

        Args:
            firstname (str): The firstname of the customer
            lastname (str): The lastname of the customer
            age (int): The age of the customer, has to be from 1 to 100
            priority (int): The priority of the customer, choose a value based on the given note, MUST BE between 1 and 5
            note (str): Note to the customer, tells what the customer is interested in

        Returns:
            str: Success message when creating the customer. If an error has occurred, a negative success message is returned.
        """

        return "To be done"