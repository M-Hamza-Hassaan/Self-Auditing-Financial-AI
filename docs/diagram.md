```mermaid
flowchart TD
    A[User / Client] --> B[Loan Application Interface]
    B --> C[Workflow Engine]
    
    subgraph Governance & Safety Layer
        D1[Safety & Control Agent]
        D2[Ethics & Responsible AI Agent]
        D3[Compliance Agent]
        D4[Human-AI Collaboration Agent]
    end
    
    C --> D[Governance & Safety Layer]
    D --> D1
    D --> D2
    D --> D3
    D --> D4
    
    C --> E[IBM Granite ChatModel]
    E --> F[Prompt Templates]
    E --> G[Memory Module]
    C --> H[ReAct Agent]
    
    E --> I[Decision Output]
    D1 -.-> I
    D2 -.-> I
    D3 -.-> I
    D4 -.-> I
    H --> E
    F --> E
    H --> I
```

This diagram shows how a user's loan application flows through the system, with the Workflow Engine coordinating interactions between the Governance & Safety Layer (which includes the key agents), the IBM Granite ChatModel (enhanced with prompt templates and memory), and the ReAct agent to produce a final decision output.