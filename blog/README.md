# Building Trustworthy AI for Business Efficiency  
## Using the BeeAI Framework and IBM Granite Models

In today's rapidly evolving AI landscape, the promise of intelligent systems is immense—but so is the responsibility to ensure they are safe, ethical, and compliant. With AI systems integrated into critical business processes (like loan approvals), issues such as bias, errors, security vulnerabilities, and ethical dilemmas can have major repercussions.

This tutorial demonstrates how to build a robust Safety and Governance layer using the BeeAI Framework. Our goal is to develop an AI‐driven loan approval system that not only automates business workflows but also ensures fairness, transparency, and regulatory compliance. By harnessing IBM Granite models, we create a solution that supports scalable growth and smarter operations—exactly what the hackathon challenge calls for.

---

## Overview and Objectives

**Hackathon Challenge Objectives:**

- **Harness IBM Granite Models:** Integrate IBM Granite’s capabilities into our AI solution to tailor it for real-world business applications.
- **Focus on Efficiency:** Automate workflows, optimize operations, and improve productivity.
- **Innovate for Impact:** Create a groundbreaking solution that revolutionizes business processes across industries.

**Key Success Criteria:**

- **Application of Technology:** Seamless integration of IBM Granite and BeeAI components.
- **Business Value:** High potential impact and practical value.
- **Originality:** Unique and creative approach to AI safety and governance.
- **Presentation:** Clarity and effectiveness in conveying the solution.

---

## 1. Building the Core Governance & Safety Agents

The first step in our solution is to create a layered governance system. We implement four core agents:

### 1.1 Safety & Control Agent

This agent continuously monitors loan applications for bias, errors, or adversarial behavior.

```python
class SafetyControlAgent:
    def monitor_loan_data(self, loan_applications):
        """Monitors loan applications for potential bias."""
        demographic_data = self._extract_demographic_data(loan_applications)
        bias_detected = self._analyze_for_bias(demographic_data)
        if bias_detected:
            self._trigger_alert(f"Potential bias detected: {bias_detected}")
        else:
            print("SafetyControlAgent: No bias detected in loan approvals.")

    def _extract_demographic_data(self, loan_applications):
        # Extract demographic information from each loan application
        print("SafetyControlAgent: Extracting demographic data...")
        return {"demographics": [app["demographic"] for app in loan_applications]}

    def _analyze_for_bias(self, demographic_data):
        # Simple logic: if group_A appears disproportionately, flag potential bias
        print("SafetyControlAgent: Analyzing for bias...")
        if demographic_data["demographics"].count("group_A") > 2:
            return "Disproportionate rejection rate for group A"
        return None

    def _trigger_alert(self, message):
        # Trigger an alert (this could be integrated with a messaging or logging system)
        print(f"SafetyControlAgent ALERT: {message}")

# Example usage:
safety_agent = SafetyControlAgent()
loan_data = [
    {"applicant_id": 1, "demographic": "group_A", "loan_status": "rejected"},
    {"applicant_id": 2, "demographic": "group_B", "loan_status": "approved"},
    {"applicant_id": 3, "demographic": "group_A", "loan_status": "rejected"},
    {"applicant_id": 4, "demographic": "group_B", "loan_status": "approved"},
    {"applicant_id": 5, "demographic": "group_A", "loan_status": "rejected"}
]
safety_agent.monitor_loan_data(loan_data)
```

*Explanation:*  
This agent extracts demographic information from each loan application and uses a simple logic to detect bias. If a disproportionate number of applicants from "group_A" are rejected, it triggers an alert.

---

### 1.2 Ethics & Responsible AI Agent

This agent reviews the decision criteria used by the AI to ensure fairness and transparency.

```python
class EthicsAgent:
    def review_decision_criteria(self, loan_criteria):
        """Reviews loan decision criteria for ethical alignment."""
        ethical_guidelines = self._load_ethical_guidelines()
        unethical_criteria = self._identify_unethical_criteria(loan_criteria, ethical_guidelines)
        if unethical_criteria:
            self._flag_criteria(unethical_criteria)
        else:
            print("EthicsAgent: Loan criteria align with ethical guidelines.")

    def _load_ethical_guidelines(self):
        # Load guidelines that ensure decisions are made fairly and transparently
        print("EthicsAgent: Loading ethical guidelines...")
        return [
            "Do not discriminate based on protected characteristics",
            "Ensure transparency",
            "Promote fairness"
        ]

    def _identify_unethical_criteria(self, loan_criteria, ethical_guidelines):
        # Check if any criterion is unethical based on our guidelines
        print("EthicsAgent: Identifying unethical criteria...")
        unethical = []
        for criterion in loan_criteria:
            if criterion in ["Zip Code Risk Score", "Name Ethnicity Score"]:
                unethical.append(criterion)
        return unethical

    def _flag_criteria(self, unethical_criteria):
        print(f"EthicsAgent ALERT: Unethical criteria identified: {unethical_criteria}")

# Example usage:
ethics_agent = EthicsAgent()
loan_criteria = ["Credit Score", "Income", "Loan Amount", "Zip Code Risk Score"]
ethics_agent.review_decision_criteria(loan_criteria)
```

*Explanation:*  
The Ethics Agent loads ethical guidelines and compares them against the loan decision criteria. If any criterion is flagged (e.g., “Zip Code Risk Score”), it alerts the system.

---

### 1.3 Regulatory Compliance Agent

This agent audits decisions to ensure compliance with legal and industry standards.

```python
class ComplianceAgent:
    def audit_for_compliance(self, loan_decisions):
        """Audits loan decisions for regulatory compliance."""
        regulations = self._load_regulations()
        non_compliant_decisions = self._check_compliance(loan_decisions, regulations)
        if non_compliant_decisions:
            self._generate_report(non_compliant_decisions)
        else:
            print("ComplianceAgent: Loan decisions are compliant with regulations.")

    def _load_regulations(self):
        # Load financial regulations for audit purposes
        print("ComplianceAgent: Loading financial regulations...")
        return {"Consumer Protection Law": "Rule X", "Anti-Discrimination Act": "Rule Y"}

    def _check_compliance(self, loan_decisions, regulations):
        print("ComplianceAgent: Checking compliance...")
        non_compliant = []
        for decision in loan_decisions:
            if decision.get("reason") == "discriminatory_criterion":
                non_compliant.append(decision)
        return non_compliant

    def _generate_report(self, non_compliant_decisions):
        print(f"ComplianceAgent ALERT: Compliance Report generated for non-compliant decisions: {non_compliant_decisions}")

# Example usage:
compliance_agent = ComplianceAgent()
loan_decisions = [
    {"applicant_id": 1, "decision": "rejected", "reason": "discriminatory_criterion"},
    {"applicant_id": 2, "decision": "approved", "reason": "credit_score"},
    {"applicant_id": 3, "decision": "rejected", "reason": "income_level"}
]
compliance_agent.audit_for_compliance(loan_decisions)
```

*Explanation:*  
The Compliance Agent checks loan decisions against a set of loaded regulations. If any decision is non-compliant (e.g., using a discriminatory criterion), it generates a report.

---

### 1.4 Human-AI Collaboration Agent

This agent enables human loan officers to review and override AI decisions when necessary.

```python
class HumanCollaborationAgent:
    def facilitate_human_review(self, loan_application, ai_decision):
        """Facilitates human review and potential override of AI decisions."""
        print("HumanCollaborationAgent: Loan application flagged for human review.")
        human_override = self._get_human_override_decision(loan_application, ai_decision)
        if human_override:
            final_decision = human_override
            print("HumanCollaborationAgent: Human override applied.")
        else:
            final_decision = ai_decision
            print("HumanCollaborationAgent: AI decision confirmed.")
        self._record_final_decision(loan_application, final_decision)

    def _get_human_override_decision(self, loan_application, ai_decision):
        # Simulate human loan officer review (in practice, this could be a GUI or API call)
        print("HumanCollaborationAgent: Initiating human loan officer review process...")
        user_input = input(f"Review loan application for applicant {loan_application['applicant_id']} (AI decision: {ai_decision}). Override? (yes/no): ")
        if user_input.lower() == 'yes':
            return "approved"
        return None

    def _record_final_decision(self, loan_application, final_decision):
        print(f"HumanCollaborationAgent: Final loan decision for applicant {loan_application['applicant_id']} recorded as: {final_decision}")

# Example usage:
human_agent = HumanCollaborationAgent()
loan_app = {"applicant_id": 6, "details": "complex case"}
ai_initial_decision = "rejected"
human_agent.facilitate_human_review(loan_app, ai_initial_decision)
```

*Explanation:*  
The Human-AI Collaboration Agent simulates a human review process. A loan officer (or a simulated input) can override the AI decision. This ensures that human judgment can complement the automated process when needed.

---

## 2. Leveraging BeeAI Framework Components for Business Efficiency

Now that we’ve built our core safety and governance agents, we move on to demonstrating how to integrate IBM Granite models and other BeeAI components to build a scalable business solution.

### 2.1 Prompt Templates

Prompt templates allow you to format and structure data before sending it to the language model. Here’s how to create a Retrieval-Augmented Generation (RAG) template:

```python
from pydantic import BaseModel
from beeai_framework.utils.templates import PromptTemplate

# Define the input schema for our prompt template
class RAGTemplateInput(BaseModel):
    question: str
    context: str

# Create a prompt template that uses Mustache syntax
rag_template: PromptTemplate = PromptTemplate(
    schema=RAGTemplateInput,
    template="""
Context: {{context}}
Question: {{question}}

Provide a concise answer based on the context. Avoid phrases such as 'Based on the context'.""",
)

# Render the prompt using example input
prompt = rag_template.render(
    RAGTemplateInput(
        question="What is the capital of France?",
        context="France is a country in Europe. Its capital city is Paris, known for its culture and history.",
    )
)
print(prompt)
```

*Explanation:*  
This code shows how to dynamically generate prompts with user input. The rendered prompt is then sent to our IBM Granite-powered ChatModel.

---

### 2.2 The ChatModel and IBM Granite Integration

We use the IBM Granite model via the BeeAI ChatModel interface to interact with our prompts. This is key to automating decision-making processes.

```python
from beeai_framework.backend.message import UserMessage
from beeai_framework.backend.chat import ChatModel, ChatModelInput, ChatModelOutput

# Create a ChatModel instance using IBM Granite (via Ollama provider)
model = ChatModel.from_name("ollama:granite3.1-dense:8b")

# Create a user message and get a response from the model
user_message = UserMessage(content="Hello! Can you tell me what is the capital of France?")
output: ChatModelOutput = await model.create(ChatModelInput(messages=[user_message]))
print("IBM Granite Response:", output.get_text_content())
```

*Explanation:*  
The ChatModel instance communicates with the Granite model to generate responses. In our business scenario, Granite’s power will help automate tasks like generating compliance reports or refining search queries.

---

### 2.3 Memory for Conversation History

To ensure context is maintained, BeeAI’s memory module stores previous messages.

```python
from beeai_framework.backend.message import AssistantMessage
from beeai_framework.memory.unconstrained_memory import UnconstrainedMemory

memory = UnconstrainedMemory()
await memory.add_many([
    user_message,
    AssistantMessage(content=output.get_text_content()),
    UserMessage(content="What should be improved in our loan approval process?")
])
output: ChatModelOutput = await model.create(ChatModelInput(messages=memory.messages))
print("Memory-based Response:", output.get_text_content())
```

*Explanation:*  
Memory enables our agent to keep track of the conversation history, ensuring that each new decision or query benefits from prior context.

---

### 2.4 Workflows: End-to-End Process Automation

Workflows in BeeAI allow you to define a series of steps (or states) that guide your agent through complex processes. Below is an end-to-end workflow for our AI-driven loan approval system.

#### Workflow State and Basic Step

```python
import traceback
from pydantic import BaseModel, ValidationError
from beeai_framework.workflows.workflow import Workflow, WorkflowError

# Define a simple state for our workflow
class MessageState(BaseModel):
    message: str

# A simple workflow step that appends text to the message state
async def my_first_step(state: MessageState) -> None:
    state.message += " World"
    print("Running first step!")
    return Workflow.END

try:
    basic_workflow = Workflow(schema=MessageState, name="MyWorkflow")
    basic_workflow.add_step("my_first_step", my_first_step)
    basic_response = await basic_workflow.run(MessageState(message="Hello"))
    print("State after workflow run:", basic_response.state)
except (WorkflowError, ValidationError):
    traceback.print_exc()
```

*Explanation:*  
This basic workflow demonstrates state modification. In a real-world scenario, each step might represent a phase in the loan approval process.

#### Multi-Step Workflow with Web Search Integration

For our use case, we integrate a web search step to simulate gathering external data (e.g., market trends) that might influence the loan decision.

```python
from langchain_community.utilities import SearxSearchWrapper
from pydantic import Field
from beeai_framework.backend.chat import ChatModel, ChatModelOutput, ChatModelStructureOutput
from beeai_framework.backend.message import UserMessage
from beeai_framework.utils.templates import PromptTemplate

# Define the workflow state for a search agent
class SearchAgentState(BaseModel):
    question: str
    search_results: str | None = None
    answer: str | None = None

# Create a ChatModel instance using IBM Granite
model = ChatModel.from_name("ollama:granite3.1-dense:8b")

# Set up the SearxSearch tool (ensure your local SearXNG instance is running)
search_tool = SearxSearchWrapper(searx_host="http://127.0.0.1:8888")

# Define prompt templates for generating search queries and answers
class QuestionInput(BaseModel):
    question: str

class SearchRAGInput(BaseModel):
    question: str
    search_results: str

search_query_template = PromptTemplate(
    schema=QuestionInput,
    template="""Convert the following question into a concise, effective web search query:
Question: {{question}}""",
)

search_rag_template = PromptTemplate(
    schema=SearchRAGInput,
    template="""Search results:
{{search_results}}

Question: {{question}}
Provide a concise answer based on these results. If insufficient, say 'I don't know.'""",
)

class WebSearchQuery(BaseModel):
    query: str = Field(description="The web search query.")

# Step 1: Generate a search query and run a search
async def web_search(state: SearchAgentState) -> str:
    print("Step: web_search")
    prompt = search_query_template.render(QuestionInput(question=state.question))
    response: ChatModelStructureOutput = await model.create_structure(
        {"schema": WebSearchQuery, "messages": [UserMessage(prompt)]}
    )
    state.search_results = search_tool.run(response.object["query"])
    return "generate_answer"

# Step 2: Generate an answer using the search results
async def generate_answer(state: SearchAgentState) -> str:
    print("Step: generate_answer")
    prompt = search_rag_template.render(
        SearchRAGInput(
            question=state.question,
            search_results=state.search_results or "No results available."
        )
    )
    output: ChatModelOutput = await model.create({"messages": [UserMessage(prompt)]})
    state.answer = output.get_text_content()
    return Workflow.END

try:
    search_agent_workflow = Workflow(schema=SearchAgentState, name="WebSearchAgent")
    search_agent_workflow.add_step("web_search", web_search)
    search_agent_workflow.add_step("generate_answer", generate_answer)

    search_response = await search_agent_workflow.run(
        SearchAgentState(question="What is the term for a baby hedgehog?")
    )
    print("*****")
    print("Question:", search_response.state.question)
    print("Answer:", search_response.state.answer)
except (WorkflowError, ValidationError):
    traceback.print_exc()
```

*Explanation:*  
This multi-step workflow first generates a search query (using the Granite model) and then uses the retrieved search results to generate an answer. This simulates a process where external data is incorporated into the decision-making process.

---

### 2.5 ReAct Agents: Intelligent Reasoning and Acting

The ReAct agent pattern separates reasoning from actions. BeeAI provides pre-canned ReAct agents that can be extended with custom tools. For example:

```python
from typing import Any
from beeai_framework.agents.bee.agent import BeeAgent
from beeai_framework.agents.types import BeeInput, BeeRunInput, BeeRunOutput
from beeai_framework.emitter.emitter import Emitter, EventMeta
from beeai_framework.emitter.types import EmitterOptions
from beeai_framework.memory.unconstrained_memory import UnconstrainedMemory

chat_model: ChatModel = ChatModel.from_name("ollama:granite3.1-dense:8b")
agent = BeeAgent(bee_input=BeeInput(llm=chat_model, tools=[], memory=UnconstrainedMemory()))

async def process_agent_events(event_data: dict[str, Any], event_meta: EventMeta) -> None:
    if event_meta.name == "error":
        print("Agent 🤖:", event_data["error"])
    elif event_meta.name == "retry":
        print("Agent 🤖: retrying the action...")
    elif event_meta.name == "update":
        print(f"Agent update: {event_data['update']['parsedValue']}")

async def observer(emitter: Emitter) -> None:
    emitter.on("*.*", process_agent_events, EmitterOptions(match_nested=True))

result: BeeRunOutput = await agent.run(
    run_input=BeeRunInput(prompt="What chemical elements make up a water molecule?")
).observe(observer)
```

*Explanation:*  
The ReAct agent continuously reasons about its input, takes action, and learns from its results. This is crucial for building a dynamic system that adapts to business needs.

---

## 3. Integrating IBM Granite Models for Scalable Business Solutions

By utilizing IBM Granite models (accessed here via “ollama:granite3.1-dense:8b”), our solution gains the following advantages:

- **Scalability:** Granite models are designed to handle complex reasoning and generate high-quality responses.
- **Efficiency:** The power of Granite allows rapid processing of tasks like generating compliance reports or automating workflow steps.
- **Business Value:** Tailoring responses to specific business queries (e.g., loan approvals, market analysis) creates practical, real-world impact.

*Tip for the Hackathon:* Emphasize how the integration of IBM Granite with BeeAI not only automates workflows but also provides a safety net (through our governance agents) that ensures every automated decision is ethically sound and legally compliant.

---

## 4. Bringing It All Together: End-to-End Loan Approval System

Now, let’s combine everything into one cohesive system. This end-to-end solution uses governance agents, chat models, memory, workflows, and ReAct agents to automate and secure the loan approval process.

```python
import traceback
from pydantic import BaseModel, ValidationError
from beeai_framework.workflows.workflow import Workflow, WorkflowError
from beeai_framework.backend.message import UserMessage, AssistantMessage, SystemMessage
from beeai_framework.memory.unconstrained_memory import UnconstrainedMemory

# Define the overall workflow state for the loan approval system
class LoanApprovalState(BaseModel):
    applicant_id: int
    demographic: str
    loan_status: str = "pending"
    risk_flag: str | None = None
    final_decision: str | None = None

# Define a workflow step that uses the SafetyControlAgent
async def monitor_application(state: LoanApprovalState) -> str:
    safety_agent = SafetyControlAgent()
    # In a real scenario, you might process a batch of applications.
    # Here we simulate checking one application.
    safety_agent.monitor_loan_data([{
        "applicant_id": state.applicant_id,
        "demographic": state.demographic,
        "loan_status": state.loan_status
    }])
    # If a risk is detected, flag it (this is simplified)
    if state.demographic == "group_A":
        state.risk_flag = "Potential bias detected for group A"
    return "review_decision"

# Define a step where a human operator or a ReAct agent can review and finalize the decision
async def review_decision(state: LoanApprovalState) -> str:
    human_agent = HumanCollaborationAgent()
    # Simulate using the agent to review and possibly override the decision
    human_agent.facilitate_human_review(
        {"applicant_id": state.applicant_id, "details": "Complex case"}, 
        state.loan_status
    )
    # For this demo, we assume the final decision is updated by human input
    state.final_decision = "approved" if state.risk_flag is None else "requires further review"
    return Workflow.END

try:
    # Create the overall workflow for loan approval
    loan_workflow = Workflow(schema=LoanApprovalState, name="LoanApprovalWorkflow")
    loan_workflow.add_step("monitor_application", monitor_application)
    loan_workflow.add_step("review_decision", review_decision)

    # Simulate a loan application
    loan_state = LoanApprovalState(applicant_id=101, demographic="group_A")
    final_response = await loan_workflow.run(loan_state)
    print("Final Loan Application State:", final_response.state)
except (WorkflowError, ValidationError):
    traceback.print_exc()
```

*Explanation:*  
This complete workflow demonstrates how an incoming loan application is first monitored for potential bias (using our SafetyControlAgent) and then reviewed by a human or intelligent ReAct agent. The system logs risk flags and updates the final decision accordingly.

---

## 5. Final Remarks and Hackathon Pitch

- **Application of Technology:**  
  By seamlessly integrating IBM Granite models with BeeAI’s powerful components (governance agents, templates, memory, and workflows), our solution automates a critical business process while ensuring ethical and legal compliance.

- **Business Value:**  
  This AI-driven loan approval system minimizes risk, enhances operational efficiency, and maintains a high level of trust—all of which directly contribute to scalable business growth.

- **Originality:**  
  Our approach uniquely blends cutting-edge language models with proactive safety and governance measures, providing a comprehensive solution rarely seen in traditional AI implementations.

- **Presentation:**  
  The solution is structured, modular, and thoroughly documented, making it clear how each component contributes to building a trustworthy and efficient AI system.

---

## Conclusion

In this tutorial, we walked through the entire process of building a Trustworthy AI solution using the BeeAI Framework. From developing dedicated governance agents to leveraging IBM Granite models for scalable performance, every component was designed to ensure fairness, safety, and efficiency in a high-stakes business environment. With this comprehensive system, you are well-equipped to tackle the hackathon challenge and deliver an innovative, impactful solution.

**Ready to Build Trustworthy AI?**  
Explore our documentation, join our community, and start integrating these techniques into your projects to revolutionize business processes.

---

## Acknowledgements

We sincerely thank our contributors, researchers, and supporters who have helped shape BeeAI. Special thanks to the open-source community for their invaluable feedback and contributions.
