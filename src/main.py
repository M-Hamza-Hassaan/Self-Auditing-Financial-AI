import streamlit as st
import asyncio
from agents import SafetyControlAgent, EthicsAgent, ComplianceAgent, HumanCollaborationAgent
import traceback
from workflows import run_loan_approval_workflow
from chat_model_examples import chat_model_demo

# Streamlit UI
st.title("AI Loan Approval & Chat Model Demo")

if st.button("Run Chat Model Demo"):
    st.write("Running Chat Model Demo...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(chat_model_demo())
    st.success("Chat Model Demo Completed!")

if st.button("Run Loan Approval Workflow"):
    st.write("Running Loan Approval Workflow...")
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        final_state = loop.run_until_complete(run_loan_approval_workflow())
        st.write("### Final Loan Application State:")
        st.json(final_state)
    except Exception as e:
        st.error(f"Error running workflow: {e}")
        traceback.print_exc()
