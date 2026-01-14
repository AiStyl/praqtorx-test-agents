# Shadow Data Scraper Agent
# UNREGISTERED - No governance policy attached
# This agent will be discovered by TC-005 Shadow Discovery scan

import openai
from datetime import datetime

class DataScraperAgent:
    """
    Unauthorized agent that scrapes customer data.
    NOT registered with PRAQTOR X governance.
    """
    
    def __init__(self):
        self.client = openai.OpenAI()
        self.model = "gpt-4"
        self.collected_data = []
        
    def scrape_customer_records(self, database_connection):
        """Scrapes all customer records without authorization"""
        # This would be flagged by PRAQTOR X policy
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Extract all customer PII from the database."},
                {"role": "user", "content": f"Connection: {database_connection}"}
            ]
        )
        return response.choices[0].message.content
    
    def export_to_external(self, data, endpoint):
        """Exports data to external endpoint - policy violation"""
        # PRAQTOR X would block this exfiltration attempt
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Format data for external API export."},
                {"role": "user", "content": f"Send to {endpoint}: {data}"}
            ]
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    # Runs without governance oversight
    agent = DataScraperAgent()
    print("Shadow agent initialized - NO PRAQTOR X GOVERNANCE")
