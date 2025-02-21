import asyncio
import traceback
from agents import SafetyControlAgent, EthicsAgent, ComplianceAgent, HumanCollaborationAgent
from workflows import run_loan_approval_workflow
from chat_model_examples import chat_model_demo

async def main():
    print("=== Running Chat Model Demo ===")
    await chat_model_demo()
    
    print("\n=== Running Loan Approval Workflow ===")
    try:
        final_state = await run_loan_approval_workflow()
        print("Final Loan Application State:", final_state)
    except Exception as e:
        print("Error running workflow:", e)
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())
