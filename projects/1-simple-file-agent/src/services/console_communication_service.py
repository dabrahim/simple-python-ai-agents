from src.contracts.communication_interface import CommunicationInterface


class ConsoleCommunicationService(CommunicationInterface):
    """
    Console-based implementation of user communication.
    Handles user interaction through standard input/output.
    """

    def ask_user(self, message: str) -> str:
        """
        Ask user for input via console with formatted prompt.
        
        Args:
            message: Question or prompt to show the user
            
        Returns:
            User's response from console input
        """
        print(f"\n{'*' * 20}")
        print('Asking for clarification...\n')
        response: str = input(f"{message} \n\nResponse: ")
        return response

    def respond_to_user(self, message: str) -> None:
        """
        Display formatted response to user via console.
        
        Args:
            message: Final response message to display
        """
        print(f"\n{'*' * 20}")
        print("AGENT RESPONSE\n")
        print(message)
        print(f"{'*' * 20}")