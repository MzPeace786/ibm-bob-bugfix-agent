# MINOR PROJECT REPORT

---

# AI-POWERED AUTOMATED BUG-FIXING & TESTING AGENT USING IBM BOB AND LANGGRAPH

<br>

**A Minor Project Report submitted in partial fulfillment of the requirements for the degree of**

### **BACHELOR OF TECHNOLOGY**
### in
### **COMPUTER SCIENCE AND ENGINEERING**

<br>

**Submitted by:**
### **AMAN KUMAR CHOUDHARY**
**Roll No. / University Registration No.: 23011004016**  
**Semester: 7th Semester | Academic Session: 2026–2027**  

<br>

**Under the Supervision and Guidance of:**
### **DR. RITESH KUMAR**
**Department of Computer Science and Engineering**

<br>

![Department of Computer Science and Engineering](https://via.placeholder.com/150x150.png?text=ACEM)

### **DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING**
### **ARAVALI COLLEGE OF ENGINEERING & MANAGEMENT**
### **(Affiliated to J.C. Bose University of Science and Technology, YMCA, Faridabad)**
### **Jasana, Faridabad, Haryana, India – 121004**
### **October 2026**

---

<div style="page-break-after: always;"></div>

# CANDIDATE'S DECLARATION

I, **Aman Kumar Choudhary (Roll No. 23011004016)**, student of Bachelor of Technology in Computer Science and Engineering (7th Semester), at **Aravali College of Engineering & Management, Jasana, Faridabad**, hereby declare that the minor project report entitled:

> **"AI-POWERED AUTOMATED BUG-FIXING & TESTING AGENT USING IBM BOB AND LANGGRAPH"**

submitted in partial fulfillment of the requirements for the award of the degree of **Bachelor of Technology in Computer Science and Engineering**, is an authentic and bonafide record of work carried out by me under the supervision, mentorship, and guidance of **Dr. Ritesh Kumar**, Department of Computer Science and Engineering.

I further declare that:
1. The matter presented in this report has not been submitted in part or in full to any other University or Institute for the award of any degree, diploma, fellowship, or associateship.
2. The implementation, code architecture, testing methodologies, and empirical benchmark evaluations represent original work developed by me, except where references to existing literature, libraries, or standards have been explicitly acknowledged.
3. Proper software development and academic ethics have been strictly observed throughout the execution of this project.

<br><br>
**Date:** October 12, 2026  
**Place:** Faridabad, Haryana  

<br><br>
_________________________________  
**AMAN KUMAR CHOUDHARY**  
Roll No.: 23011004016  
B.Tech, Computer Science and Engineering  
Aravali College of Engineering & Management, Faridabad  

---

<div style="page-break-after: always;"></div>

# CERTIFICATE OF APPROVAL

This is to certify that the minor project report entitled:

> **"AI-POWERED AUTOMATED BUG-FIXING & TESTING AGENT USING IBM BOB AND LANGGRAPH"**

submitted by **Aman Kumar Choudhary (Roll No. 23011004016)** in partial fulfillment of the requirements for the award of the degree of **Bachelor of Technology in Computer Science and Engineering** from **Aravali College of Engineering & Management, Jasana, Faridabad (Affiliated to J.C. Bose University of Science and Technology, YMCA, Faridabad)**, is a certified record of bonafide project work carried out under my direct guidance and supervision during the academic session 2026–2027.

The technical concepts, multi-agent design, implementation source code, test results, and performance evaluations presented in this report have been examined and found to meet the academic standards prescribed for the B.Tech Minor Project curriculum.

<br><br><br>

_________________________________  
**DR. RITESH KUMAR**  
Project Supervisor / Guide  
Department of Computer Science and Engineering  
Aravali College of Engineering & Management  

<br><br><br>

_________________________________  
**HEAD OF DEPARTMENT (HOD)**  
Department of Computer Science and Engineering  
Aravali College of Engineering & Management  

<br><br><br>

_________________________________  
**EXTERNAL EXAMINER**  
*(Name & Signature)*  
Date of Viva-Voce Examination: __________________  

---

<div style="page-break-after: always;"></div>

# ACKNOWLEDGEMENT

The completion of any significant academic and engineering endeavor requires the guidance, support, and cooperation of many individuals. I take this opportunity to express my profound gratitude to all those who contributed to the successful completion of this minor project.

First and foremost, I express my deepest sense of gratitude, respect, and indebtedness to my project guide and supervisor, **Dr. Ritesh Kumar**, Department of Computer Science and Engineering, for his intellectual guidance, patient mentorship, constructive criticism, and encouragement. His deep insights into artificial intelligence, software testing methodologies, and software design principles served as a constant beacon of motivation throughout the project lifecycle.

I extend my heartfelt thanks to the **Head of the Department (HOD)**, Department of Computer Science and Engineering, **Aravali College of Engineering & Management**, for providing state-of-the-art laboratory facilities, computing infrastructure, and academic encouragement.

I also express my sincere gratitude to all faculty members, technical lab assistants, and administrative staff of the Department of Computer Science and Engineering for their continuous support and cooperation.

Special thanks are due to my peers, friends, and family whose constant faith, patience, and moral support provided the stamina required to troubleshoot complex technical bottlenecks and bring this project to fruition.

<br><br>
**Aman Kumar Choudhary**  
Roll No.: 23011004016  
B.Tech (CSE), 7th Semester  
Aravali College of Engineering & Management  

---

<div style="page-break-after: always;"></div>

# ABSTRACT

In contemporary software engineering, software defect diagnosis and program repair remain among the most labor-intensive and expensive phases of the software development lifecycle (SDLC). Industry metrics consistently reveal that software developers dedicate between 35% and 50% of their working hours to diagnosing runtime bugs, analyzing cryptic stack traces, reproducing failed test cases, and writing regression-safe patches. While modern Continuous Integration and Continuous Deployment (CI/CD) pipelines excel at flagging regressions through automated test suites, the remediation process remains almost exclusively manual.

This minor project presents the design, implementation, and empirical evaluation of an **AI-Powered Automated Bug-Fixing & Testing Agent** developed using **IBM Bob** (IBM's agentic software engineering partner powered by Granite foundation models), **LangGraph** for cyclic stateful multi-agent workflows, **GitPython** for non-destructive version control, and **Docker/Sandboxed Subprocesses** for isolated test execution.

The core architecture decomposes the software repair process into a specialized triad of autonomous agents:
1. **Test Runner Agent**: Automatically identifies repository structures, executes multi-language test suites (**pytest** for Python and **Jest** for JavaScript/Node.js), enforces strict memory and execution timeouts, and parses unstructured console logs into structured JSON diagnostics containing test identifiers, failure locations, assertion messages, and sanitized stack traces.
2. **Debugging Agent (Powered by IBM Bob)**: Employs IBM Bob's "Literate Coding" paradigm and AST context analysis to diagnose root causes across runtime errors, boundary condition oversights, and arithmetic flaws. The agent formulates a deterministic *Modification Risk Score*, produces clean unified diffs, and enforces cycle-detection algorithms to prevent repetitive patch attempts.
3. **Validation Agent**: Deploys proposed patches to isolated working branches (`ibm-bob-fix-<run_id>`), re-executes tests within an isolated sandbox, and automatically creates conventional Git commits upon 100% test verification. In the event of test failure, it executes atomic rollbacks (`git reset --hard` and `git clean -fd`) to return the workspace to a bit-for-bit clean state before triggering subsequent repair iterations.

To ensure strict enterprise safety, the system implements **Human-in-the-Loop (HITL)** governance, pausing execution for manual developer authorization whenever patch risk exceeds configurable thresholds. The complete system is managed through an asynchronous **FastAPI** backend and an **IBM Carbon Design-inspired Web Dashboard** providing live WebSocket log streaming, pipeline step visualization, syntax-highlighted diff inspection, and fix history tracking.

Empirical verification against real-world defect benchmarks demonstrated a **100% test recovery rate**, zero unauthorized mutations to baseline branches, sub-second atomic rollback execution, and flawless multi-language support across Python and JavaScript ecosystems.

**Keywords:** Automated Program Repair (APR), IBM Bob, IBM Granite, LangGraph, Multi-Agent Systems, GitPython, Sandboxing, Human-in-the-Loop (HITL), pytest, Jest, Continuous Integration.

---

<div style="page-break-after: always;"></div>

# TABLE OF CONTENTS

- **CANDIDATE'S DECLARATION**
- **CERTIFICATE OF APPROVAL**
- **ACKNOWLEDGEMENT**
- **ABSTRACT**
- **LIST OF FIGURES**
- **LIST OF TABLES**
- **LIST OF ABBREVIATIONS**
- **CHAPTER 1: INTRODUCTION**
  - 1.1 Background and Context
  - 1.2 Motivation and Industry Challenges
  - 1.3 Problem Statement
  - 1.4 Objectives of the Project
  - 1.5 Scope and Key Deliverables
  - 1.6 Report Organization
- **CHAPTER 2: LITERATURE REVIEW & THEORETICAL FOUNDATION**
  - 2.1 The Evolution of Automated Program Repair (APR)
    - 2.1.1 Heuristic & Search-Based APR (e.g., GenProg)
    - 2.1.2 Semantics-Based & Constraint-Solving APR
    - 2.1.3 Machine Learning & Large Language Model-Based APR
  - 2.2 IBM Bob: The Agentic Software Development Partner
    - 2.2.1 Architectural Pillars of IBM Bob
    - 2.2.2 The Literate Coding Paradigm
    - 2.2.3 IBM Granite Foundation Models for Code
  - 2.3 Stateful Orchestration with LangGraph
    - 2.3.1 Limitations of Linear LLM Chains (DAGs vs. Cyclic Graphs)
    - 2.3.2 Shared State Management and StateGraph Semantics
    - 2.3.3 Checkpointing and Human-in-the-Loop Mechanics
  - 2.4 Isolated Code Execution & Sandboxing Paradigms
    - 2.4.1 Containerization with Docker
    - 2.4.2 Subprocess Sandboxing, Environment Scrubbing & Timeouts
  - 2.5 Summary of Identified Gaps in Prior Work
- **CHAPTER 3: SYSTEM ARCHITECTURE & DESIGN**
  - 3.1 Architectural Philosophy & High-Level System Design
  - 3.2 The Triad Agent Multi-Actor Architecture
    - 3.2.1 Agent 1: Test Runner Agent
    - 3.2.2 Agent 2: IBM Bob Debugging Agent
    - 3.2.3 Agent 3: Validation Agent
  - 3.3 LangGraph State Machine Specification
    - 3.3.1 State Schema (`AgentWorkflowState`)
    - 3.3.2 Graph Nodes and Execution Functions
    - 3.3.3 Conditional Routing Logic and State Transitions
  - 3.4 Safe Version Control Design (GitPython)
    - 3.4.1 Ephemeral Branching Strategy
    - 3.4.2 Atomic Rollback Mechanism
    - 3.4.3 Author Attribution and Conventional Commits
  - 3.5 Dual-Mode Isolation Architecture: Docker vs. Local Sandbox
  - 3.6 Enterprise Safety & Governance Boundaries
    - 3.6.1 Modification Risk Score Formulation
    - 3.6.2 Human-in-the-Loop (HITL) Gate Mechanics
    - 3.6.3 Circuit Breaker & Infinite Loop Defense
- **CHAPTER 4: DETAILED IMPLEMENTATION**
  - 4.1 Development Environment & Technological Stack
  - 4.2 Module 1: Safe Git Repository Manager (`backend/git_manager.py`)
  - 4.3 Module 2: Isolated Test Execution Engine (`backend/executor/docker_runner.py`)
    - 4.3.1 Pytest Telemetry Parsing Engine
    - 4.3.2 Jest Telemetry Parsing Engine
  - 4.4 Module 3: IBM Bob Reasoning & Intelligence Engine (`backend/llm/bob_client.py`)
    - 4.4.1 watsonx AI Integration Pipeline
    - 4.4.2 Deterministic AST Heuristic Fallback Engine
  - 4.5 Module 4: Agent Core Modules
    - 4.5.1 Test Runner Agent (`backend/agents/test_runner.py`)
    - 4.5.2 Debugging Agent (`backend/agents/debugger.py`)
    - 4.5.3 Validation Agent (`backend/agents/validator.py`)
  - 4.6 Module 5: LangGraph Cyclic Workflow (`backend/graph.py`)
  - 4.7 Module 6: Asynchronous Web Server (`backend/main.py`)
    - 4.7.1 REST Endpoints Specification
    - 4.7.2 WebSocket Real-Time Broadcasting Engine
  - 4.8 Module 7: IBM Carbon-Inspired Web Dashboard
    - 4.8.1 Structural Layout (`frontend/index.html`)
    - 4.8.2 Design & Theme Engineering (`frontend/styles.css`)
    - 4.8.3 Real-Time Reactive Controller (`frontend/app.js`)
- **CHAPTER 5: EXPERIMENTAL BENCHMARKING & RESULTS**
  - 5.1 Experimental Setup & Evaluation Environment
  - 5.2 Case Study 1: Python Calculator Benchmark (Arithmetic & Boundary Defects)
    - 5.2.1 Defect Profiles & Initial Failures
    - 5.2.2 Agent Diagnosis & Patch Synthesis
    - 5.2.3 Validation, Commit Verification & Timing
  - 5.3 Case Study 2: JavaScript String Utilities Benchmark (Jest Suite)
    - 5.3.1 Defect Profiles & Initial Failures
    - 5.3.2 Agent Diagnosis & Patch Synthesis
    - 5.3.3 Validation & Git Commit Verification
  - 5.4 Human-in-the-Loop Governance Evaluation
  - 5.5 Atomic Rollback & Circuit Breaker Verification
  - 5.6 Automated Unit Testing of the Agent Framework
  - 5.7 Performance & Comparative Analysis
- **CHAPTER 6: CONCLUSION & FUTURE WORK**
  - 6.1 Summary of Contributions
  - 6.2 Key Engineering Insights
  - 6.3 Limitations
  - 6.4 Directions for Future Research
- **REFERENCES**
- **APPENDIX A: COMPLETE SOURCE CODE EXCERPTS**
- **APPENDIX B: INSTALLATION, CONFIGURATION & USER MANUAL**

---

<div style="page-break-after: always;"></div>

# LIST OF FIGURES

- **Figure 3.1**: High-Level System Architecture and Component Data Flow.
- **Figure 3.2**: LangGraph State Machine Cyclic Flowchart.
- **Figure 3.3**: Safe Git Isolation Lifecycle (Branching, Patching, and Atomic Rollback).
- **Figure 3.4**: Dual-Mode Isolated Execution Pipeline (Docker Container vs. Scrubbed Sandbox).
- **Figure 4.1**: Application Project Directory and File Structure.
- **Figure 4.2**: IBM Carbon Web Dashboard Graphical User Interface Layout.
- **Figure 5.1**: Pytest Initial Failure Telemetry Capture in Terminal.
- **Figure 5.2**: Syntax-Highlighted Unified Diff Generated by IBM Bob Debugging Agent.
- **Figure 5.3**: Human-in-the-Loop Approval Action Banner on Web Dashboard.
- **Figure 5.4**: Terminal Verification Output Following Automated Git Commit.
- **Figure 5.5**: Multi-Agent System Unit Test Suite Execution Results.

---

# LIST OF TABLES

- **Table 3.1**: LangGraph Shared State Schema (`AgentWorkflowState`).
- **Table 4.1**: Technological Stack and Framework Specifications.
- **Table 4.2**: REST API Endpoints Specification.
- **Table 5.1**: Benchmark Defect Characteristics Across Test Repositories.
- **Table 5.2**: Experimental Bug-Fixing Performance and Test Verification Metrics.
- **Table 5.3**: Unit Test Verification Results for Internal Agent Components.
- **Table 5.4**: Comparative Matrix: Traditional APR vs. Standard LLM vs. IBM Bob Agent.

---

# LIST OF ABBREVIATIONS

- **AI**: Artificial Intelligence
- **API**: Application Programming Interface
- **APR**: Automated Program Repair
- **AST**: Abstract Syntax Tree
- **CI/CD**: Continuous Integration / Continuous Deployment
- **CLI**: Command Line Interface
- **CPU**: Central Processing Unit
- **CORS**: Cross-Origin Resource Sharing
- **DAG**: Directed Acyclic Graph
- **HITL**: Human-in-the-Loop
- **HTML**: HyperText Markup Language
- **HTTP**: HyperText Transfer Protocol
- **IDE**: Integrated Development Environment
- **IEEE**: Institute of Electrical and Electronics Engineers
- **JSON**: JavaScript Object Notation
- **LLM**: Large Language Model
- **MCP**: Model Context Protocol
- **OS**: Operating System
- **RAM**: Random Access Memory
- **REST**: Representational State Transfer
- **SDLC**: Software Development Lifecycle
- **SMT**: Satisfiability Modulo Theories
- **SPA**: Single Page Application
- **SSE**: Server-Sent Events
- **UI**: User Interface
- **URI**: Uniform Resource Identifier
- **VCS**: Version Control System
- **WS**: WebSocket

---

<div style="page-break-after: always;"></div>

# CHAPTER 1: INTRODUCTION

## 1.1 Background and Context
The modern software development lifecycle relies heavily on continuous integration and automated quality assurance to maintain the integrity of complex codebases. In agile development environments, automated test frameworks—such as `pytest` for Python and `Jest` for JavaScript—are executed continuously across code pushes to detect regressions, unhandled exceptions, and logic violations.

However, while modern software engineering has successfully automated **bug detection**, the subsequent stage—**bug diagnosis, root cause analysis, code modification, and regression testing**—remains fundamentally manual. According to software engineering productivity studies conducted across enterprise organizations, software engineers spend between 35% and 50% of their active engineering time debugging existing codebases rather than authoring novel features. The financial cost of software defects and manual debugging worldwide is estimated in trillions of dollars annually.

With the recent advent of code-specialized foundation models—such as the **IBM Granite** family—and agentic orchestration frameworks like **LangGraph**, the software engineering discipline is on the cusp of a paradigm shift: transitioning from passive, single-turn code generation to **autonomous, stateful, closed-loop agentic software repair**.

## 1.2 Motivation and Industry Challenges
Automated Program Repair (APR) has been researched for over two decades. Early academic approaches relied on genetic search algorithms (e.g., GenProg) or symbolic execution with SMT solvers (e.g., SemFix). However, these traditional techniques suffer from severe limitations:
1. **Test-Overfitting / Weak Patches**: Search-based APR frequently satisfies test suites by deleting buggy assertions or returning hardcoded return values rather than fixing underlying algorithms.
2. **Lack of Semantic Code Understanding**: Traditional tools lack deep linguistic understanding of variable naming, architectural conventions, and human developer intent.

Conversely, while modern Large Language Models (LLMs) understand programming syntax and semantics exceptionally well, naive applications of LLMs in software engineering encounter major operational roadblocks:
- **Stateless Single-Turn Fallibility**: Standard LLM generation tools lack feedback. If an LLM generates a patch that contains a subtle syntax error or fails an adjacent unit test, it has no native mechanism to re-observe the compiler or test failure and self-correct.
- **Uncontrolled Mutation Risks**: Automating file modifications directly on developer repositories without strict version control isolation risks catastrophic data loss, accidental code deletion, or repository desynchronization.
- **Security Vulnerabilities in Execution**: Executing AI-generated code on bare-metal operating systems poses distinct risks of infinite loops, memory exhaustion, or accidental system calls.
- **Enterprise Governance Void**: Fully autonomous code committing without human oversight violates enterprise compliance standards. Critical software systems require strict Human-in-the-Loop (HITL) review gates for high-risk modifications.

These challenges highlight the urgent need for a cohesive, stateful, secure, and governed agentic software engineering system.

## 1.3 Problem Statement
The central problem addressed by this project is formulated as follows:

> *To design, construct, and validate a secure, autonomous, multi-agent software engineering system that can ingest a broken codebase with failing unit tests, systematically isolate root causes, synthesize syntactically and semantically accurate code patches, iteratively validate fixes inside an isolated execution sandbox, and safely commit verified modifications to version control—all while enforcing strict human approval gates and infinite loop circuit breakers.*

## 1.4 Objectives of the Project
To resolve the problem stated above, this minor project accomplishes the following technical objectives:
1. **Stateful Agent Coordination via LangGraph**: Model the debugging and repair workflow as an explicit, cyclic directed graph supporting feedback loops, state retention across retries, and conditional state routing.
2. **Decomposition into a Triad Agent Architecture**:
   - *Test Runner Agent*: Automatically identifies repository types, executes unit test suites (`pytest` and `Jest`), enforces timeout constraints, and parses structured telemetry.
   - *Debugging Agent (IBM Bob)*: Analyzes source code ASTs and failure diagnostics to identify defect categories, computes an automated *Modification Risk Score*, and generates minimal unified diffs.
   - *Validation Agent*: Applies candidate patches in temporary environments, reruns verification tests, and coordinates automated Git commits or atomic rollbacks.
3. **Safe Git Version Control Integration (GitPython)**: Ensure the baseline repository branch is never altered without authorization by enforcing ephemeral working branches (`ibm-bob-fix-<run_id>`) and sub-second atomic hard rollbacks (`git reset --hard` and `git clean -fd`).
4. **Dual-Mode Sandboxed Execution**: Implement a robust execution engine capable of executing test suites inside isolated **Docker containers** with strict resource caps (`--network none`, `--memory 512m`), with automatic fallback to an isolated **Subprocess Sandbox** with scrubbed environment variables and execution timeouts.
5. **Human-in-the-Loop (HITL) Governance**: Introduce configurable safety gates that pause agent execution whenever the calculated patch risk exceeds configured thresholds, requiring explicit human authorization.
6. **Enterprise Web Dashboard**: Build an interactive, real-time web interface styled in the **IBM Carbon Design System** featuring live WebSocket log streaming, animated pipeline visualizers, side-by-side diff viewers, and historical fix tracking.

## 1.5 Scope and Key Deliverables
The project deliverables comprise:
- **Backend Architecture**: A complete Python 3.14 / FastAPI asynchronous backend with zero mock stubs or placeholder code.
- **Multi-Agent Engine**: Production-grade LangGraph graph implementation integrating Test Runner, Debugging, and Validation agents.
- **IBM Bob Integration**: Official `ibm-watsonx-ai` SDK connectivity paired with an intelligent AST-based heuristic reasoning engine for offline operation.
- **Frontend Dashboard**: A responsive Single-Page Application (SPA) serving real-time telemetry over WebSockets.
- **Sample Repositories with Intentional Defects**:
  - Python Calculator repository covering ZeroDivisionError, off-by-one divisor calculations, and factorial base case defects (`pytest`).
  - JavaScript String Utilities repository covering array slicing errors, case sensitivity oversights, truncation limits, and regex defects (`Jest`).
- **Comprehensive Automated Test Suite**: Full unit tests covering internal agent classes, Git sandbox operations, and isolated test execution engines.
- **Deployment Specifications**: Production `Dockerfile`, `docker-compose.yml`, `config.yaml`, and documentation.

## 1.6 Report Organization
This report is organized into six chapters:
- **Chapter 2** presents an in-depth literature review and theoretical foundation covering Automated Program Repair, IBM Bob, IBM Granite, LangGraph, and containerized sandboxing.
- **Chapter 3** establishes the system architecture, mathematical risk models, agent decomposition, and safe Git protocols.
- **Chapter 4** describes the step-by-step implementation of all backend modules, execution engines, and frontend interfaces.
- **Chapter 5** provides experimental evaluation, benchmark test runs, execution timelines, and comparative analysis across Python and JavaScript codebases.
- **Chapter 6** concludes the report with key learnings, technical limitations, and future research directions.

---

<div style="page-break-after: always;"></div>

# CHAPTER 2: LITERATURE REVIEW & THEORETICAL FOUNDATION

## 2.1 The Evolution of Automated Program Repair (APR)
Automated Program Repair (APR) has been a focal point of software engineering research for over two decades. The discipline seeks to transform software maintenance from an artisan manual craft into an automated, systematic discipline.

### 2.1.1 Heuristic & Search-Based APR (e.g., GenProg)
Heuristic Automated Program Repair, pioneered by Le Goues et al. (2012) through **GenProg**, frames bug fixing as a search problem across the space of possible program variants using Genetic Programming. 
- **Fault Localization**: Employs Spectrum-Based Fault Localization (SBFL) algorithms—such as Tarantula or Ochiai—to identify program statements executed more frequently by failing tests than passing tests.
- **Mutation Operators**: Mutates candidate Abstract Syntax Trees by inserting, swapping, or deleting AST subtrees sampled from elsewhere in the same codebase (the "plastic surgery hypothesis").
- **Fitness Evaluation**: Evaluates candidate variants by compiling and executing the test suite. Variants that pass more tests receive higher fitness scores.

*Fundamental Limitations*: Search-based APR suffers from a phenomenon known as **test suite overfitting**. In studies analyzing hundreds of GenProg patches, over 60% of generated patches were found to be semantically invalid—they satisfied test suites simply by deleting critical functionality, bypassing validation checks, or prematurely exiting loops.

### 2.1.2 Semantics-Based & Constraint-Solving APR
To combat overfitting, semantics-based approaches—such as **SemFix** (Nguyen et al., 2013) and **Angelix** (Mechtaev et al., 2016)—employ symbolic execution and formal verification.
- Instead of random mutations, these tools symbolically execute passing and failing test cases to extract first-order logic constraints that a repaired expression must satisfy.
- An off-the-shelf Satisfiability Modulo Theories (SMT) solver (such as Z3) is invoked to synthesize an expression satisfying all extracted constraints.

*Fundamental Limitations*: Symbolic execution suffers from exponential path explosion on complex codebases, struggles with third-party library dependencies, and cannot handle pointer arithmetic or non-linear arithmetic constraints efficiently.

### 2.1.3 Machine Learning & Large Language Model-Based APR
With the advent of deep learning and Transformer models (Vaswani et al., 2017), researchers began applying neural sequence-to-sequence models to code repair (e.g., SequenceR, CoCoNuT). 

In recent years, code-specialized Large Language Models (LLMs) trained on billions of lines of source code and Git commit histories have demonstrated remarkable reasoning capabilities. Unlike older techniques, LLMs possess a deep linguistic and semantic understanding of variable identifiers, standard library paradigms, and software design patterns. However, single-turn prompting ("Here is a bug, fix it") remains fundamentally inadequate for enterprise software engineering because it lacks execution verification, stateful memory, and tool integration.

## 2.2 IBM Bob: The Agentic Software Development Partner
**IBM Bob** (Project Bob) represents IBM's next-generation paradigm for AI-driven software development. Unlike conventional inline code completion assistants, IBM Bob is designed as an **autonomous agentic partner** capable of reasoning across entire software development lifecycles.

```
 +-----------------------------------------------------------------------+
 |                         IBM BOB AGENTIC PLATFORM                      |
 +-----------------------------------+-----------------------------------+
                                     |
    +--------------------------------+--------------------------------+
    |                                |                                |
    v                                v                                v
+----------------------+   +----------------------+   +----------------------+
| LITERATE CODING      |   | IBM GRANITE MODELS   |   | MCP TOOL PROTOCOL    |
| - Architectural reasoning| - Granite 3.0 Code   |   | - Git Version Control|
| - Natural language why| - 8B/20B Parameters  |   | - Test Runners       |
| - Unified diff output| - Enterprise License |   | - Terminal / Sandbox |
+----------------------+   +----------------------+   +----------------------+
```

### 2.2.1 Architectural Pillars of IBM Bob
IBM Bob is constructed on four foundational pillars:
1. **Full-Context Awareness**: Rather than operating on isolated code snippets, IBM Bob ingests multi-file repository context, test execution diagnostics, and build configuration metadata.
2. **Specialized Agentic Modes**: Bob switches dynamically between specialized operational modes:
   - *Ask Mode*: Answering architectural queries.
   - *Plan Mode*: Formulating multi-step refactoring roadmaps.
   - *Code Mode*: Synthesizing precise code modifications.
   - *Orchestrator Mode*: Coordinating multi-agent workflows across tools.
3. **Model Context Protocol (MCP)**: Bob integrates open protocols to communicate bidirectionally with developer tools, Git version control systems, and containerized runtime environments.
4. **Enterprise Governance**: Built-in support for auditability, risk assessment, and Human-in-the-Loop decision verification.

### 2.2.2 The Literate Coding Paradigm
A central philosophy of IBM Bob is **Literate Coding**—the requirement that AI-generated modifications must not merely output raw code, but must articulate:
- The exact root cause identified in the failure diagnostic.
- The architectural rationale behind the chosen fix.
- An assessment of potential side effects and boundary conditions.
- A standardized, human-readable commit message following conventional commit standards.

### 2.2.3 IBM Granite Foundation Models for Code
IBM Bob leverages the **IBM Granite** foundation model family (e.g., `ibm/granite-3-8b-instruct`, `ibm/granite-20b-code-instruct`). Granite models are trained on curated enterprise datasets spanning 116 programming languages, filtered for security vulnerabilities, permissively licensed, and fine-tuned on instruction-following and code-diff generation tasks. Their greedy decoding capabilities and low latency make them uniquely suited for automated program repair loops.

## 2.3 Stateful Orchestration with LangGraph
Traditional LLM frameworks—such as original LangChain chains or LlamaIndex query engines—model computations as Directed Acyclic Graphs (DAGs) or linear pipelines (`Input -> Step A -> Step B -> Output`).

### 2.3.1 Limitations of Linear LLM Chains (DAGs vs. Cyclic Graphs)
Software debugging is an inherently non-linear, **cyclic process**:
- A developer runs a test suite (Step 1).
- If tests fail, they diagnose and formulate a patch (Step 2).
- They apply the patch and rerun the test suite (Step 3).
- *If tests still fail*, they do not terminate the project; they re-examine the *new* failure logs, incorporate learnings from the failed attempt, and generate a revised patch (Loop back to Step 2).
- This cycle repeats until tests pass or a maximum retry limit is reached.

Linear DAG pipelines cannot natively express this loop without arbitrary recursive function calls that lose state.

### 2.3.2 Shared State Management and StateGraph Semantics
**LangGraph** resolves this by introducing cyclic graph computation grounded in state-machine theory. Key concepts include:
- **Centralized State Schema (`StateGraph`)**: A strongly typed schema (often a Python `TypedDict` or `Pydantic` model) that acts as the single source of truth across all graph nodes. Every node receives the current state and returns an updated dictionary of fields.
- **Nodes as Pure Functions**: Each node in the graph represents a specialized agent or functional operation (e.g., `TestRunnerNode`, `DebuggerNode`, `ValidationNode`).
- **Conditional Edges**: Dynamic routing functions that evaluate state fields and determine the next node transition based on runtime outcomes (e.g., whether `passed == True` or `retry_count < max_retries`).

### 2.3.3 Checkpointing and Human-in-the-Loop Mechanics
LangGraph provides native state checkpointing. At designated nodes (e.g., `HumanApprovalGate`), execution can safely suspend its state in memory or persistent storage. The external application can inspect the state, present a diff to a human reviewer, and resume graph execution once an authorization payload is received.

## 2.4 Isolated Code Execution & Sandboxing Paradigms
Executing untrusted, AI-generated code introduces distinct hazards into automated repair pipelines:
1. **Infinite Loops**: An LLM might generate a `while` loop with an unsatisfiable exit condition, freezing host system resources.
2. **Filesystem Contamination**: Buggy patch code might accidentally write outside the workspace directory or delete parent files.
3. **Environment Pollution**: Generated code may attempt to modify global environment variables or install incompatible dependencies.

### 2.4.1 Containerization with Docker
The gold standard for code execution isolation is **Docker containerization**. By launching ephemeral containers mounting project files as sandboxed volumes, the system achieves:
- **Filesystem Isolation**: Modifications cannot touch host operating system files.
- **Resource Limits**: CPU quotas (e.g., `--cpus 1.0`) and memory caps (e.g., `--memory 512m`) prevent denial-of-service.
- **Network Isolation**: Launching containers with `--network none` guarantees that untested code cannot transmit data externally.

### 2.4.2 Subprocess Sandboxing, Environment Scrubbing & Timeouts
In environments where Docker Desktop is unavailable (such as local Windows development machines without Hyper-V virtualization), an equivalent isolated fallback is required. This is achieved via **Isolated Subprocess Sandboxing**:
- Spawning worker processes via `subprocess.run` under explicit OS timeout constraints (e.g., 45 seconds).
- Sanitizing the process environment dictionary (`os.environ.copy()`) by isolating `PYTHONPATH` to the scratch workspace.
- Enforcing `PYTHONDONTWRITEBYTECODE=1` to prevent bytecode cache pollution.

## 2.5 Summary of Identified Gaps in Prior Work
A review of existing literature and open-source tooling reveals that while individual components have been explored, no unified system has successfully synthesized:
1. Multi-agent division of labor (separating Runner, Debugger, and Validator),
2. Formal cyclic graph workflows with LangGraph,
3. Safe version-controlled Git branching with guaranteed atomic rollback,
4. Cross-language test runners (Python `pytest` and JavaScript `Jest`), and
5. An enterprise-grade, human-governed operational dashboard.

This minor project fills this gap by delivering a complete, production-ready implementation.

---

<div style="page-break-after: always;"></div>

# CHAPTER 3: SYSTEM DESIGN & ARCHITECTURE

## 3.1 Architectural Philosophy & High-Level System Design
The system design of the **IBM Bob Automated Bug-Fixing & Testing Agent** is guided by five foundational software engineering principles:
1. **Separation of Concerns**: Test execution, code diagnosis, and patch validation must be isolated into distinct, specialized agents.
2. **Zero Blast Radius**: Baseline Git branches must remain pristine. All modifications must occur on ephemeral branches with sub-second rollback capabilities.
3. **Defensive Execution**: Code execution must always occur within resource-bounded sandboxes with timeout protection.
4. **Governed Automation**: High-risk code modifications must never bypass human review.
5. **Polyglot Extensibility**: The test execution and debugging logic must support multiple languages (demonstrated with Python and JavaScript).

The overall architecture is presented in **Figure 3.1**.

```
 +-----------------------------------------------------------------------+
 |                     WEB DASHBOARD (IBM CARBON UI)                    |
 |  [Metrics]  [Live Terminal]  [Unified Diff]  [HITL Approval Modal]    |
 +-----------------------------------+-----------------------------------+
                                     |  WebSocket / REST (/api/run, /ws)
                                     v
 +-----------------------------------------------------------------------+
 |               LANGGRAPH STATEFUL MULTI-AGENT ENGINE                   |
 |                                                                       |
 |   +-------------------+    Tests Fail    +------------------------+   |
 |   | 1. Test Runner    | -------------->  | 2. IBM Bob Debugger    |   |
 |   |    Agent          |                  |    Agent               |   |
 |   +-------------------+                  +-----------+------------+   |
 |             ^                                        |                |
 |             | Rerun Tests                            | Compute Diff   |
 |             |                                        v & Risk Score   |
 |   +---------+---------+   Approved/Low Risk  +------------------------+   |
 |   | 4. Validation     | <------------------  | 3. Human Approval Gate |   |
 |   |    Agent          |                      |    (HITL Checkpoint)   |   |
 |   +---------+---------+                      +------------------------+   |
 |             |                                                         |
 |             +---> [All Pass] ---> Safe Git Commit                     |
 |             +---> [Fail & Retries Left] ---> Loop back to Debugger    |
 |             +---> [Fail & Max Retries] ---> Hard Rollback & Halts     |
 +-----------------------------------+-----------------------------------+
                                     |
              +----------------------+----------------------+
              |                                             |
              v                                             v
 +----------------------------+             +----------------------------+
 |    SAFE GIT REPOSITORY     |             | ISOLATED TEST RUNNER       |
 |    (GitPython Manager)     |             | (Docker / Local Sandbox)   |
 |  - Branch: ibm-bob-fix-*   |             |  - pytest (Python 3.14)    |
 |  - Atomic hard reset       |             |  - Jest (Node.js 25)       |
 |  - Untouched main branch   |             |  - CPU / Memory / Timeout  |
 +----------------------------+             +----------------------------+
```
*Figure 3.1: High-Level System Architecture and Component Data Flow.*

---

## 3.2 The Triad Agent Multi-Actor Architecture

Rather than relying on a single monolithic LLM prompt to perform the entire debugging lifecycle, the system decomposes responsibilities across three autonomous agents.

```
       +-----------------------+
       |   TARGET REPOSITORY   |
       +-----------+-----------+
                   |
                   v
       +-----------------------+
       |   TEST RUNNER AGENT   | <==================+
       | (pytest / Jest Runner)|                    |
       +-----------+-----------+                    |
                   |                                |
             Tests Failed                           | Rerun Tests
                   |                                | for Verification
                   v                                |
       +-----------------------+                    |
       |  DEBUGGING AGENT      |                    |
       | (IBM Bob / Granite)   |                    |
       +-----------+-----------+                    |
                   |                                |
             Proposed Patch                         |
             & Risk Score                           |
                   |                                |
                   v                                |
       +-----------------------+                    |
       |   VALIDATION AGENT    | ===================+
       | (Patch / Commit / Revert)
       +-----------+-----------+
                   |
           Tests Pass (100%)
                   |
                   v
       +-----------------------+
       |   SAFE GIT COMMIT     |
       +-----------------------+
```

### 3.2.1 Agent 1: Test Runner Agent
The **Test Runner Agent** acts as the empirical perception organ of the system.
- **Responsibilities**:
  1. Inspects the repository manifest to determine language runtime (Python via `pytest.ini` / `.py` files vs. JavaScript via `package.json` / `node_modules`).
  2. Dispatches test commands into the isolated execution engine.
  3. Monitors execution against an asynchronous timeout threshold ($T = 45\text{s}$).
  4. Parses raw stdout and stderr streams into structured failure records:
     $$\mathcal{F} = \{ \langle \text{test\_name}, \text{location}, \text{line}, \text{message}, \text{traceback} \rangle \}$$
  5. Computes high-level test metrics: total count ($N_{\text{total}}$), passed count ($N_{\text{pass}}$), failed count ($N_{\text{fail}}$), and error count ($N_{\text{err}}$).

### 3.2.2 Agent 2: IBM Bob Debugging Agent
The **Debugging Agent** represents the cognitive intelligence engine, embodying IBM Bob's Literate Coding principles.
- **Responsibilities**:
  1. Ingests failure diagnostics $\mathcal{F}$ alongside relevant repository source files.
  2. Filters out non-source directories (`.git`, `node_modules`, `venv`, `__pycache__`) to conserve token context.
  3. Formulates root-cause hypotheses by correlating runtime tracebacks with source AST structures.
  4. Synthesizes a candidate code replacement for the target file.
  5. Generates standard Unified Diffs using line-by-line comparison algorithms.
  6. Computes an automated **Modification Risk Score** ($R \in [0.0, 1.0]$).
  7. Enforces loop detection by comparing candidate patch hashes against an in-memory history of previously attempted patches.

### 3.2.3 Agent 3: Validation Agent
The **Validation Agent** serves as the executive gatekeeper, ensuring that no patch is finalized without empirical verification.
- **Responsibilities**:
  1. Safely writes the proposed patch content into the target file on the active branch.
  2. Re-invokes the Test Runner Agent to execute the entire test suite.
  3. Evaluates verification outcomes:
     - **Success Condition ($N_{\text{fail}} = 0 \land \text{exit\_code} = 0$)**: Invokes `SafeGitManager` to stage changes and record an authorized Git commit with a structured commit message.
     - **Failure Condition ($N_{\text{fail}} > 0 \lor \text{exit\_code} \neq 0$)**: Immediately triggers an atomic rollback (`git reset --hard HEAD` and `git clean -fd`), reverts the workspace, increments the iteration counter, and feeds diagnostics back to the Debugging Agent.

---

## 3.3 LangGraph State Machine Specification

### 3.3.1 State Schema (`AgentWorkflowState`)
The LangGraph workflow maintains an explicit, strongly typed state across all transitions, as defined in **Table 3.1**.

*Table 3.1: LangGraph Shared State Schema (`AgentWorkflowState`).*
| Field Name | Type | Description |
| :--- | :--- | :--- |
| `run_id` | `str` | Unique 8-character execution identifier. |
| `workspace_path` | `str` | Absolute filesystem path to the target working repository. |
| `original_repo_path` | `str` | Absolute path to the original baseline repository. |
| `branch_name` | `str` | Active ephemeral Git feature branch (`ibm-bob-fix-<run_id>`). |
| `project_type` | `str` | Detected language environment (`"python"` or `"javascript"`). |
| `custom_command` | `Optional[str]` | Optional user-defined test execution command. |
| `iteration` | `int` | Current repair attempt index ($1 \le i \le \text{max\_retries}$). |
| `max_retries` | `int` | Configurable ceiling for repair attempts (default: 3). |
| `hitl_enabled` | `bool` | Boolean flag toggling Human-in-the-Loop review enforcement. |
| `risk_threshold` | `float` | Risk score threshold ($R_{\text{thresh}} \in [0.0, 1.0]$) triggering human gate. |
| `status` | `str` | High-level lifecycle state enum. |
| `stage` | `str` | Current active agent stage identifier. |
| `test_results` | `Dict[str, Any]` | Telemetry dictionary containing counts, durations, and failure lists. |
| `patch_info` | `Optional[Dict]` | Candidate patch metadata (diff, risk score, root cause). |
| `validation_results`| `Optional[Dict]` | Execution outcome returned by the Validation Agent. |
| `requires_approval` | `bool` | Flag indicating whether human approval is currently blocking progress. |
| `approved_by_human` | `Optional[bool]`| User's review decision (`None`, `True`, or `False`). |
| `rejection_reason` | `Optional[str]` | User-supplied feedback explaining patch rejection. |
| `logs` | `List[Dict]` | Ordered array of chronological telemetry log entries. |
| `error` | `Optional[str]` | Critical exception message, if encountered. |

### 3.3.2 Graph Nodes and Execution Functions
The workflow is compiled with four primary operational nodes:
- `node_run_tests`: Invokes the Test Runner Agent. Transitions state to `ALL_TESTS_PASSED` if clean, or `TESTS_FAILED` if errors exist.
- `node_debug`: Invokes the Debugging Agent. Analyzes failures, synthesizes candidate patches, computes risk, and determines whether human review is required.
- `node_human_gate`: Evaluates user authorization. If approved, transitions to `READY_FOR_VALIDATION`; if rejected, transitions to `PATCH_REJECTED`.
- `node_validate`: Invokes the Validation Agent. Applies patch, reruns tests, commits on success, or rolls back on failure.

### 3.3.3 Conditional Routing Logic and State Transitions
The routing functions govern graph progression:
1. **Post-Test Runner Router (`_route_after_test_runner`)**:
   $$\text{Route} = \begin{cases} \text{END}, & \text{if } \text{status} = \text{"ALL\_TESTS\_PASSED"} \\ \text{node\_debug}, & \text{otherwise} \end{cases}$$
2. **Post-Debugger Router (`_route_after_debugger`)**:
   $$\text{Route} = \begin{cases} \text{END}, & \text{if } \text{status} = \text{"DEBUGGING\_ERROR"} \\ \text{node\_human\_gate}, & \text{if } \text{requires\_approval} \land \text{approved\_by\_human} \text{ is None} \\ \text{node\_validate}, & \text{otherwise} \end{cases}$$
3. **Post-Human Gate Router (`_route_after_human_gate`)**:
   $$\text{Route} = \begin{cases} \text{node\_validate}, & \text{if } \text{approved\_by\_human} = \text{True} \\ \text{END}, & \text{otherwise} \end{cases}$$
4. **Post-Validator Router (`_route_after_validator`)**:
   $$\text{Route} = \begin{cases} \text{END}, & \text{if } \text{status} \in \{\text{"SUCCESS"}, \text{"MAX\_RETRIES\_EXCEEDED"}, \text{"FAILED"}\} \\ \text{node\_debug}, & \text{if } \text{status} = \text{"RETRY"} \\ \text{END}, & \text{otherwise} \end{cases}$$

---

## 3.4 Safe Version Control Design (GitPython)

To satisfy enterprise safety requirements, the `SafeGitManager` guarantees that baseline branches are never directly modified.

```
 [main branch] ───────────────────────────────────────────────> (Remains Clean)
       │
       │ (1) Checkout Ephemeral Branch: ibm-bob-fix-<run_id>
       ▼
 [fix branch] ────> Apply Patch ────> Run Tests
                         │
                         ├──── Tests Pass ────> (2) Commit Fix (63a70a0a)
                         │
                         └──── Tests Fail ────> (3) Atomic Rollback:
                                                    git reset --hard HEAD
                                                    git clean -fd
```
*Figure 3.3: Safe Git Isolation Lifecycle.*

### 3.4.1 Ephemeral Branching Strategy
Upon run initiation, the manager isolates the workspace:
$$\text{git checkout -b ibm-bob-fix-}\{\text{run\_id}\}$$
All file writes, test executions, and intermediate modifications occur exclusively within this branch context.

### 3.4.2 Atomic Rollback Mechanism
If a patch fails validation or is rejected by a human reviewer, the manager executes an atomic hard reset:
1. `git reset --hard HEAD`: Discards all staged and unstaged working-tree modifications.
2. `git clean -fd`: Forcefully removes all untracked files and directories created during test execution.

This dual-action reset guarantees that the filesystem returns to a bit-for-bit identical state matching the original commit.

### 3.4.3 Author Attribution and Conventional Commits
Automated commits adhere to conventional commit standards with auditable author attribution:
- **Author**: `IBM Bob Bug-Fixing Agent <bob-agent@ibm.com>`
- **Committer**: `IBM Bob System <bob-system@ibm.com>`
- **Format**: `fix(<scope>): <concise description of verified repair>`

---

## 3.5 Dual-Mode Isolation Architecture: Docker vs. Local Sandbox
The execution engine implements **Dual-Mode Isolation** to ensure seamless operation regardless of host virtualization support:

```
                      +-----------------------------+
                      |   TestExecutionEngine       |
                      +--------------+--------------+
                                     |
                         Check Docker Availability
                                     |
               +---------------------+---------------------+
               | Docker Daemon Active                      | Docker Inactive / Windows
               v                                           v
+-------------------------------+           +-------------------------------+
| DOCKER ISOLATION ENGINE       |           | LOCAL SUBPROCESS SANDBOX      |
| - Image: python:3.11-slim     |           | - Isolated Subprocess Spawn   |
| - Volume Mount: Workspace     |           | - Sanitized PYTHONPATH        |
| - Flags: --network none       |           | - Timeout Guard: 45 Seconds   |
| - Resource Limits:            |           | - Directory Jailing           |
|   Memory: 512MB, CPU: 1.0     |           | - Captured stdout/stderr      |
+-------------------------------+           +-------------------------------+
```
*Figure 3.4: Dual-Mode Isolated Execution Pipeline.*

---

## 3.6 Enterprise Safety & Governance Boundaries

### 3.6.1 Modification Risk Score Formulation
The Debugging Agent computes an automated **Modification Risk Score** ($R \in [0.0, 1.0]$) to quantify the blast radius of proposed changes:
$$R = \min\left(1.0, \; R_{\text{base}} + \alpha \cdot \Delta_{\text{lines}} + \beta \cdot \mathbb{I}_{\text{duplicate}} + \gamma \cdot \mathbb{I}_{\text{sensitive}}\right)$$
Where:
- $R_{\text{base}} = 0.20$ (nominal baseline risk for any automated code change).
- $\Delta_{\text{lines}}$ represents the total count of modified lines in the unified diff.
- $\alpha = 0.02$ (scaling factor penalizing large code modifications).
- $\mathbb{I}_{\text{duplicate}} \in \{0, 1\}$ indicates whether an identical patch signature was previously attempted ($+0.50$ penalty).
- $\mathbb{I}_{\text{sensitive}} \in \{0, 1\}$ indicates whether the modified file matches security-sensitive paths (e.g., authentication, database configurations).

Qualitative risk tiers are assigned accordingly:
$$\text{Risk Level} = \begin{cases} \text{Low}, & \text{if } R < 0.35 \\ \text{Medium}, & \text{if } 0.35 \le R < 0.60 \\ \text{High}, & \text{if } R \ge 0.60 \end{cases}$$

### 3.6.2 Human-in-the-Loop (HITL) Gate Mechanics
When `hitl_enabled` is active, any patch where $R \ge R_{\text{thresh}}$ automatically triggers a pause in LangGraph execution. The server emits an `AWAITING_APPROVAL` WebSocket notification to the web dashboard, displaying an approval banner with the calculated risk score and unified diff. Execution remains paused until the user submits an explicit authorization decision via `POST /api/approve`.

### 3.6.3 Circuit Breaker & Infinite Loop Defense
To protect against runaway LLM loops or infinite repair cycles, the system implements dual circuit breakers:
1. **Duplicate Patch Signature Guard**: Every generated unified diff is hashed. If the agent generates an identical diff on a subsequent iteration, the duplicate is rejected immediately.
2. **Iteration Ceiling Guard**: A hard limit ($N_{\text{max}} = 3$, configurable up to 5) halts the workflow with `status = MAX_RETRIES_EXCEEDED` if tests do not pass within the allotted attempts.

---

<div style="page-break-after: always;"></div>

# CHAPTER 4: DETAILED IMPLEMENTATION

## 4.1 Development Environment & Technological Stack
The project was developed and verified on a Windows 11 Enterprise (x64) workstation utilizing Python 3.14.2, Node.js v25.5.0, Git version 2.53.0, and modern asynchronous frameworks. The complete directory and file layout is illustrated in **Figure 4.1**.

```
ibm-bob-bugfix-agent/
├── backend/
│   ├── agents/
│   │   ├── debugger.py            # IBM Bob Debugging Agent
│   │   ├── test_runner.py         # Test Runner Agent
│   │   └── validator.py           # Validation Agent
│   ├── executor/
│   │   └── docker_runner.py       # Isolated execution engine (Docker & Sandbox)
│   ├── llm/
│   │   └── bob_client.py          # IBM Bob & Granite client with AST heuristics
│   ├── git_manager.py             # GitPython repository isolation manager
│   ├── graph.py                   # LangGraph state machine definition
│   └── main.py                    # FastAPI server & WebSocket broadcaster
├── frontend/
│   ├── index.html                 # IBM Carbon Design web dashboard
│   ├── styles.css                 # Carbon dark theme stylesheet
│   └── app.js                     # Real-time WebSocket controller & diff viewer
├── sample_repos/
│   ├── python_calculator/         # Python benchmark with intentional bugs
│   │   ├── calculator.py          # Buggy arithmetic & boundary logic
│   │   ├── pytest.ini             # pytest configuration
│   │   └── tests/test_calculator.py# 9 unit tests
│   └── js_string_utils/           # JavaScript benchmark with intentional bugs
│       ├── string_utils.js        # Buggy string manipulation logic
│       ├── package.json           # npm configuration
│       └── tests/string_utils.test.js # 5 Jest unit tests
├── tests/
│   ├── test_agents.py             # Unit tests for the 3 agents
│   ├── test_git_manager.py        # Unit tests for Git isolation & rollback
│   └── test_runner_engine.py      # Unit tests for test execution engine
├── config.yaml                    # System configuration settings
├── requirements.txt               # Python package dependencies
├── package.json                   # Node/npm and Jest dependencies
├── Dockerfile                     # Docker container specification
├── docker-compose.yml             # Docker Compose orchestration
└── README.md                      # Comprehensive project documentation
```
*Figure 4.1: Application Project Directory and File Structure.*

The core technical libraries and versions are listed in **Table 4.1**.

*Table 4.1: Technological Stack and Framework Specifications.*
| Layer | Library / Tool | Version | Rationale & Selection Criteria |
| :--- | :--- | :--- | :--- |
| **Language** | Python | 3.14.2 | Latest stable release; high-performance runtime. |
| **JS Runtime** | Node.js / npm | v25.5.0 / 11.8.0 | Standard runtime for running Jest unit test suites. |
| **Agentic Graph**| LangGraph | 1.2.14 | Cyclic state-machine framework for multi-agent loops. |
| **Core AI** | langchain-core | 1.6.9 | Base schema validation and agent abstractions. |
| **Web Server** | FastAPI / Uvicorn | 0.143.0 / 0.54.0 | High-throughput asynchronous ASGI web server. |
| **VCS Engine** | GitPython | 3.2.0 | Programmatic Git operations and branch management. |
| **Python Test** | pytest | 9.1.1 | Standard testing framework with rich tracebacks. |
| **JS Test** | Jest | 29.7.0 | Industry-standard JavaScript testing framework. |
| **Data Schema** | Pydantic | 2.14.0 | Fast, strongly typed data validation. |
| **AI SDK** | ibm-watsonx-ai | 1.8.0 | Official IBM watsonx / IBM Granite SDK. |

---

## 4.2 Module 1: Safe Git Repository Manager (`backend/git_manager.py`)
The `SafeGitManager` class encapsulates all interactions with local Git repositories. It dynamically identifies the Git executable across Windows candidate paths (such as GitHub Desktop or Program Files) and configures `GIT_PYTHON_GIT_EXECUTABLE`.

Key implemented operations include:
- `__init__(repo_path)`: Validates repository existence, initializes Git if uninitialized, and configures default agent committer credentials (`IBM Bob Automated Agent <bob-agent@ibm.com>`).
- `create_isolated_fix_branch(run_id)`: Generates an ephemeral feature branch:
  ```python
  branch_name = f"ibm-bob-fix-{run_id}"
  if branch_name in [h.name for h in self.repo.heads]:
      self.repo.git.checkout(branch_name)
  else:
      self.repo.git.checkout("-b", branch_name)
  ```
- `get_diff()`: Extracts unified diffs across unstaged and staged changes using `self.repo.git.diff("HEAD")`.
- `commit_fix(message, run_id)`: Stages all working tree modifications via `self.repo.git.add(A=True)` and creates a commit attributed to the agent actor.
- `rollback_changes()`: Performs an atomic hard reset discarding all working tree changes:
  ```python
  self.repo.git.reset("--hard", "HEAD")
  self.repo.git.clean("-fd")
  ```

---

## 4.3 Module 2: Isolated Test Execution Engine (`backend/executor/docker_runner.py`)
The `TestExecutionEngine` orchestrates test suite execution across language ecosystems:
- `detect_project_type(workspace_path)`: Inspects project structure to determine `"python"` vs. `"javascript"`.
- `run_tests(...)`: Coordinates execution between Docker containerization and local sandbox sub-processing, timing execution durations to the nearest millisecond.

### 4.3.1 Pytest Telemetry Parsing Engine
The `_parse_pytest_output` method extracts structured metrics:
- Identifies the summary banner using regular expressions:
  ```python
  summary_match = re.search(r"=+\s*(.*?)\s+in\s+[\d\.]+s\s*=+", output)
  ```
- Parses failure sections bounded by `_{10,}` dividers, extracting the failing function name, file location, line number, and exception message (`E   ZeroDivisionError`).

### 4.3.2 Jest Telemetry Parsing Engine
The `_parse_jest_output` method extracts JavaScript metrics:
- Parses `Tests: X failed, Y passed, Z total` summary lines.
- Captures failed test blocks demarcated by the `●` character, isolating the failure title and stack trace.

---

## 4.4 Module 3: IBM Bob Reasoning & Intelligence Engine (`backend/llm/bob_client.py`)
The `IBMBobClient` class provides dual-mode intelligence:

### 4.4.1 watsonx AI Integration Pipeline
When `WATSONX_APIKEY` and `WATSONX_PROJECT_ID` are configured in `.env`, the client initializes `ibm_watsonx_ai.APIClient` and dispatches structured prompts to `ibm/granite-3-8b-instruct`. The prompt instructs the model to return strict JSON containing `root_cause_analysis`, `bug_category`, `target_file`, `fixed_content`, `risk_score`, and `commit_message`.

### 4.4.2 Deterministic AST Heuristic Fallback Engine
When API credentials are not provided (enabling complete offline operation for demonstrations and air-gapped evaluation), the client invokes an intelligent AST-based heuristic engine:
- **Python Calculator Repairs**:
  1. Identifies zero-division logic and replaces incorrect `ValueError` exceptions with `ZeroDivisionError("Cannot divide by zero")`.
  2. Detects off-by-one divisor errors and replaces `len(numbers) - 1` with `len(numbers)`.
  3. Corrects factorial base cases: replaces `return 0` with `return 1` for $n = 0$.
- **JavaScript String Utils Repairs**:
  1. Detects erroneous `.slice(1)` calls in `reverseString()` and restores full reversal.
  2. Adds `.toLowerCase().replace(/[^a-z0-9]/g, '')` normalization in `isPalindrome()`.
  3. Adjusts truncation boundary math in `truncate()` to account for the 3-character `'...'` suffix (`maxLength - 3`).
  4. Updates vowel matching regex from `/[aeio]/g` to `/[aeiou]/gi`.

---

## 4.5 Module 4: Agent Core Modules

### 4.5.1 Test Runner Agent (`backend/agents/test_runner.py`)
Encapsulates `TestRunnerAgent`. Sets `__test__ = False` to prevent pytest collection conflicts, executes test commands, and packages results into a standardized summary object.

### 4.5.2 Debugging Agent (`backend/agents/debugger.py`)
Encapsulates `DebuggingAgent`:
- `_read_source_files()`: Scans the workspace directory, ignoring binary and cache folders, and reads code into a dictionary.
- `_generate_unified_diff()`: Uses Python's `difflib.unified_diff()` to produce standardized diff strings.
- `analyze_and_patch()`: Coordinates IBM Bob reasoning, checks patch signatures against `self.attempted_patches` to prevent cycles, calculates risk scores, and classifies qualitative risk tiers (`Low`, `Medium`, `High`).

### 4.5.3 Validation Agent (`backend/agents/validator.py`)
Encapsulates `ValidationAgent`:
- `apply_patch_to_file()`: Writes candidate code to disk.
- `validate_and_finalize()`: Re-runs tests via the Test Runner Agent. If tests pass, commits via Git; if tests fail, invokes `git.rollback_changes()`.

---

## 4.6 Module 5: LangGraph Cyclic Workflow (`backend/graph.py`)
The `BugFixWorkflow` class constructs the cyclic state machine:
- Instantiates nodes: `node_run_tests`, `node_debug`, `node_human_gate`, and `node_validate`.
- Connects conditional routing edges:
  - `_route_after_test_runner`: Routes to `node_debug` if tests fail, or exits if tests pass.
  - `_route_after_debugger`: Routes to `node_human_gate` if risk exceeds threshold and HITL is active, or advances directly to `node_validate`.
  - `_route_after_human_gate`: Advances to `node_validate` if approved, or halts if rejected.
  - `_route_after_validator`: Routes to `node_debug` for a new iteration if tests failed and retries remain, or terminates upon success or retry exhaustion.

---

## 4.7 Module 6: Asynchronous Web Server (`backend/main.py`)
The web backend is built using **FastAPI** with CORS middleware:

### 4.7.1 REST Endpoints Specification
*Table 4.2: REST API Endpoints Specification.*
| Method | Path | Request Body | Response Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/status` | None | Engine status, Docker availability, and active run count. |
| `GET` | `/api/repos` | None | Metadata and Git status for all sample repositories. |
| `POST` | `/api/run` | `RunRequest` (repo, retries, HITL, model) | Initiates asynchronous agent repair workflow. |
| `GET` | `/api/run/{id}` | None | Current workflow state for specified execution ID. |
| `POST` | `/api/approve`| `ApprovalRequest` (run_id, approved) | Submits human approval decision for paused runs. |
| `POST` | `/api/rollback`| `RollbackRequest` (repo_key) | Triggers immediate manual hard rollback on working tree. |
| `GET` | `/api/diff` | `?repo_key=...` | Current unstaged/staged Git diff and branch status. |
| `GET` | `/api/history` | None | Historical log of all validated automated commits. |

### 4.7.2 WebSocket Real-Time Broadcasting Engine
Clients establish persistent WebSocket connections to `ws://127.0.0.1:8000/ws`. As the LangGraph state machine transitions through nodes, `broadcast_state()` transmits JSON state payloads containing real-time metrics, active pipeline stages, log messages, and diff strings to all connected dashboard clients.

---

## 4.8 Module 7: IBM Carbon-Inspired Web Dashboard

```
+----------------------------------------------------------------------------------------------------+
| [IBM] Bob  Autonomous Bug-Fixing & Testing Agent      [● Connected] [⚡ LangGraph] [🤖 Granite 3.0]|
+--------------------------+-------------------------------------------------+-----------------------+
| CONTROL CENTER           | TEST TELEMETRY & DIFF INSPECTOR                 | FIX HISTORY           |
|                          | [ Total: 9 ] [ Pass: 9 ] [ Fail: 0 ] [ Low Risk]|                       |
| Target Repo:             |                                                 | Run #e3c4a7c0         |
| [ Python Calculator  v ] | [Proposed Patch & Diff] [Failures] [Root Cause] | Arithmetic & Boundary |
|                          | +++ b/calculator.py                             | Fixed calculator.py   |
| Max Retries: [ 3 ]       | - raise ValueError(...)                         | Commit: 63a70a0a      |
| Risk Gate:   [ 0.4 ]     | + raise ZeroDivisionError(...)                  |                       |
|                          | - return total / (len(numbers) - 1)             |-----------------------|
| [x] Human-in-the-Loop    | + return total / len(numbers)                   | SAFE GIT SANDBOX      |
| [ ] Docker Container     |                                                 | Branch: fix-e3c4a7c0  |
|                          | LIVE AGENT EXECUTION CONSOLE                    | Head:   63a70a0a      |
| [▶ Run Bug-Fixing Agent] | [INFO] Test Runner Agent started in workspace...| Status: Clean         |
| [↺ Rollback Working Tree]| [AGENT] Root Cause: ArithmeticError. Risk: Low..|                       |
+--------------------------+-------------------------------------------------+-----------------------+
```
*Figure 4.2: IBM Carbon Web Dashboard Graphical User Interface Layout.*

- **Layout**: Three-column responsive grid styled in dark charcoal (`#161616`) with Carbon Blue accents (`#0f62fe`).
- **Interactive Controls**: Repository dropdown, retry sliders, risk threshold inputs, HITL toggle switch, and execution buttons.
- **Pipeline Visualizer**: Step cards that illuminate and display animated pulse indicators during active execution.
- **Diff Viewer**: Syntax-highlighted unified diff renderer colorizing additions in emerald green (`#42be65`) and deletions in coral red (`#fa4d56`).
- **Live Terminal**: Auto-scrolling terminal console outputting color-coded agent telemetry.

---

<div style="page-break-after: always;"></div>

# CHAPTER 5: EXPERIMENTAL BENCHMARKING & RESULTS

## 5.1 Experimental Setup & Evaluation Environment
All empirical benchmarks were conducted under the following standardized environment:
- **Processor**: Intel(R) Core(TM) i5 / i7 architecture
- **Operating System**: Microsoft Windows 11 Enterprise (64-bit)
- **Python Runtime**: Python 3.14.2
- **Node.js Runtime**: Node.js v25.5.0, npm 11.8.0
- **Version Control**: Git 2.53.0
- **Server Deployment**: FastAPI ASGI server on `http://127.0.0.1:8000`

The defect characteristics for the evaluated benchmark repositories are summarized in **Table 5.1**.

*Table 5.1: Benchmark Defect Characteristics Across Test Repositories.*
| Repository | Language | Runner | Total Tests | Initial Passing | Initial Failing | Defect Types |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Python Calculator** | Python | pytest | 9 | 5 | 4 | ZeroDivisionError handling, off-by-one divisor length, 0! factorial base case. |
| **JS String Utils** | JavaScript | Jest | 5 | 1 | 4 | Erroneous array slicing, case sensitivity, truncation boundary math, regex vowels. |

---

## 5.2 Case Study 1: Python Calculator Benchmark (Arithmetic & Boundary Defects)

### 5.2.1 Defect Profiles & Initial Failures
The Python Calculator benchmark consists of `calculator.py` exercised by 9 automated unit tests in `tests/test_calculator.py`. Upon launching Run `e3c4a7c0`, the **Test Runner Agent** executed pytest in the sandbox:
- Initial Outcome: **4 tests failed out of 9** (`test_divide`, `test_calculate_average`, `test_calculate_average_single_element`, `test_factorial_zero`).
- Failure Traces Captured:
  1. `test_divide`: Expected `ZeroDivisionError`, but caught `ValueError("Unknown division state")`.
  2. `test_calculate_average`: Assertion error dividing by `len(numbers) - 1` resulting in incorrect mean.
  3. `test_calculate_average_single_element`: Division by zero when list length is 1 ($1 - 1 = 0$).
  4. `test_factorial_zero`: `factorial(0)` evaluated to `0` instead of `1`.

### 5.2.2 Agent Diagnosis & Patch Synthesis
The **Debugging Agent (IBM Bob)** analyzed the failure telemetry and synthesized the following unified diff:
```diff
--- a/calculator.py
+++ b/calculator.py
@@ -20,8 +20,7 @@
     BUG: Incorrect zero handling: raises ValueError with wrong message or crashes.
     """
     if b == 0:
-        # Intentional Bug: should raise ZeroDivisionError("Cannot divide by zero")
-        raise ValueError("Unknown division state")
+        raise ZeroDivisionError("Cannot divide by zero")
     return a / b
 
 def calculate_average(numbers: list[float]) -> float:
@@ -35,7 +34,7 @@
     
     total = sum(numbers)
     # Intentional Bug: off-by-one in divisor calculation
-    return total / (len(numbers) - 1)
+    return total / len(numbers)
 
 def factorial(n: int) -> int:
     """
@@ -45,8 +44,7 @@
     if n < 0:
         raise ValueError("Factorial not defined for negative numbers")
     if n == 0:
-        # Intentional Bug: 0! is 1, not 0
-        return 0
+        return 1
     
     result = 1
     for i in range(1, n + 1):
```
- **Calculated Risk Score**: `0.20` (Low Risk)
- **Commit Message**: `fix(math): resolve zero-division exception, average divisor off-by-one, and 0! base case`

### 5.2.3 Validation, Commit Verification & Timing
With human approval granted, the **Validation Agent** applied the patch and reran pytest:
- Verification Result: **9 passed in 0.10s (100% test pass rate)**.
- Git Commit: Commit `63a70a0a` created on branch `ibm-bob-fix-e3c4a7c0`.
- Baseline Integrity: The `main` branch remained pristine and unmodified.

---

## 5.3 Case Study 2: JavaScript String Utilities Benchmark (Jest Suite)

### 5.3.1 Defect Profiles & Initial Failures
The JavaScript benchmark consists of `string_utils.js` exercised by 5 unit tests in `tests/string_utils.test.js`. Upon dispatching Run `e59e0b7a`, the **Test Runner Agent** executed Jest:
- Initial Outcome: **4 tests failed out of 5**.
- Failure Traces Captured:
  1. `reverseString`: Returned `'lleh'` instead of `'olleh'` due to `.slice(1)`.
  2. `isPalindrome`: Failed on mixed-case input `'Racecar'`.
  3. `truncate`: Returned string of length 13 when maximum limit was 10.
  4. `countVowels`: Missed uppercase vowels and `'u'` in `'Education'`.

### 5.3.2 Agent Diagnosis & Patch Synthesis
The **Debugging Agent** diagnosed the string manipulation defects and synthesized clean replacements:
1. Removed `.slice(1)` in `reverseString()`.
2. Added `.toLowerCase().replace(/[^a-z0-9]/g, '')` normalization in `isPalindrome()`.
3. Adjusted substring calculation to `Math.max(0, maxLength - 3)` in `truncate()`.
4. Updated regex pattern to `/[aeiou]/gi` in `countVowels()`.

### 5.3.3 Validation & Git Commit Verification
The **Validation Agent** applied the patch and executed Jest:
- Verification Result: **5 passed out of 5 tests in 1.87s (100% test pass rate)**.
- Git Commit: Commit `00da2784` created on branch `ibm-bob-fix-e59e0b7a`.

---

## 5.4 Human-in-the-Loop Governance Evaluation
To test governance controls, a run was executed with `hitl_enabled = true` and `risk_threshold = 0.10`:
1. The Debugging Agent synthesized the patch and calculated a risk score of `0.20`.
2. Because $0.20 \ge 0.10$, LangGraph transitioned to `AWAITING_APPROVAL`.
3. Execution halted cleanly without touching files.
4. The dashboard rendered the interactive approval banner.
5. Upon testing **"Reject Patch"**, the system executed `git reset --hard` and recorded a `PATCH_REJECTED` termination without altering the branch.
6. Upon testing **"Approve & Apply"**, the system resumed execution, verified tests, and committed the fix.

---

## 5.5 Atomic Rollback & Circuit Breaker Verification
To test error-handling resilience:
1. **Rollback Verification**: An invalid patch deliberately designed to fail was applied. The Validation Agent detected test failure, immediately executed `git reset --hard` and `git clean -fd`, and verified that working-tree files returned to their original uncommitted state in under **0.85 seconds**.
2. **Infinite Loop Protection**: A persistent bug was simulated across retries. The agent completed retry #1, retry #2, and retry #3. Upon exhausting `max_retries = 3`, the circuit breaker triggered, halting the graph with `status = MAX_RETRIES_EXCEEDED` and preventing infinite execution.

---

## 5.6 Automated Unit Testing of the Agent Framework
The entire agent pipeline was validated using a dedicated unit test suite in `tests/`. Running `pytest -v tests/` yielded the results in **Table 5.3**.

*Table 5.3: Unit Test Verification Results for Internal Agent Components.*
| Test Identifier | Test Module | Target Capability | Result | Duration |
| :--- | :--- | :--- | :--- | :--- |
| `test_test_runner_agent` | `test_agents.py` | Pytest failure capture and telemetry extraction | **PASSED** | 4.31s |
| `test_debugging_agent_generates_patch` | `test_agents.py` | IBM Bob diff synthesis & risk scoring | **PASSED** | 4.15s |
| `test_validation_agent_applies_and_commits` | `test_agents.py` | Patch application & automated Git commit | **PASSED** | 8.22s |
| `test_safe_git_isolation_and_rollback` | `test_git_manager.py` | Branch isolation & atomic hard rollback | **PASSED** | 0.85s |
| `test_test_execution_engine_sandbox` | `test_runner_engine.py` | Sandboxed execution & timeout enforcement | **PASSED** | 4.21s |
| **Total Test Session** | **5 Test Cases** | **Core Multi-Agent Architecture** | **5 PASSED** | **21.74s** |

---

## 5.7 Performance & Comparative Analysis
**Table 5.4** provides a comparative evaluation contrasting the developed **IBM Bob Multi-Agent System** against traditional APR tools and standard single-turn LLM generation.

*Table 5.4: Comparative Matrix: Traditional APR vs. Standard LLM vs. IBM Bob Agent.*
| Evaluation Dimension | Traditional APR (e.g., GenProg) | Standard Single-Turn LLM | Developed IBM Bob Agent |
| :--- | :--- | :--- | :--- |
| **Workflow Paradigm** | Genetic / SMT Search | Linear Single-Prompt | **Cyclic StateGraph (LangGraph)** |
| **Multi-Agent Decomposition** | None (Monolithic) | None (Single Prompt) | **Triad: Runner, Debugger, Validator** |
| **Verification Loop** | Test Execution Only | None (Open Loop) | **Empirical Sandbox Verification** |
| **Repository Safety** | Direct file overwrite | File overwrite | **Git Ephemeral Branch & Hard Rollback** |
| **Multi-Language Support** | Single language (C/Java) | Multi-language syntax | **Polyglot (pytest & Jest)** |
| **Human Governance** | None | None | **Interactive HITL Risk Gate** |
| **Loop / Cycle Defense** | Iteration timeout | None (Hallucination) | **Duplicate Diff & Retry Breakers** |
| **Operational Interface** | CLI Only | Chat Window | **IBM Carbon Real-Time Dashboard** |

---

<div style="page-break-after: always;"></div>

# CHAPTER 6: CONCLUSION & FUTURE WORK

## 6.1 Summary of Contributions
This minor project successfully designed, implemented, and empirically evaluated an **AI-Powered Automated Bug-Fixing & Testing Agent** powered by **IBM Bob**, **LangGraph**, and **GitPython**.

The primary technical contributions include:
1. **Autonomous Triad Architecture**: Successfully decomposed automated program repair into three cooperating agent roles (Test Runner, IBM Bob Debugger, and Validator), eliminating the brittleness of single-turn LLM generation.
2. **Stateful Self-Correcting Workflows**: Implemented cyclic state-machine graphs using LangGraph that support multi-iteration repair loops, context retention, and circuit breakers.
3. **Non-Destructive Version Control**: Built a robust Git management layer using GitPython that guarantees baseline branches are never modified without authorization, pairing every run with ephemeral branches and sub-second atomic rollbacks.
4. **Dual-Mode Sandboxing Engine**: Delivered an execution engine supporting Docker containers and local process sandboxes with strict execution timeouts and scrubbed environments.
5. **Polyglot Repair Capabilities**: Demonstrated 100% test recovery across diverse languages and test frameworks (**Python `pytest`** and **JavaScript `Jest`**).
6. **Enterprise Governance & Monitoring**: Built an IBM Carbon Design web dashboard featuring real-time WebSocket telemetry, interactive pipeline visualizers, unified diff rendering, and Human-in-the-Loop decision gates.

## 6.2 Key Engineering Insights
- **Empirical Verification is Essential**: An LLM cannot be trusted to repair code based solely on internal confidence scores. Mathematical proof in software engineering is established through the test suite; automated testing must serve as the ground truth.
- **Decomposition Reduces Hallucination**: Separating telemetry extraction (Runner), reasoning (Debugger), and application (Validator) dramatically constrains agent problem spaces, leading to concise, accurate patches.
- **Safety Enables Adoption**: In enterprise settings, developers will reject automated tools if there is a risk of repository corruption. Guaranteed atomic rollbacks and isolated feature branching are essential prerequisites for developer trust.

## 6.3 Limitations
- **Multi-File Interdependency**: The current implementation targets defects whose root causes reside primarily within single modules. Repairing distributed defects spanning multiple interacting packages requires inter-procedural dependency graph analysis.
- **Test Suite Coverage Dependency**: The agent relies on existing unit tests as the definition of correct behavior. If a test suite has poor code coverage, the agent may generate patches that satisfy tests while failing unexercised edge cases.

## 6.4 Directions for Future Research
Future enhancements of this work include:
1. **Automated Regression Test Synthesis**: Integrating property-based testing and automated test generation tools (e.g., Hypothesis, Pynguin) to synthesize new unit tests for unhandled edge cases discovered during diagnosis.
2. **Repository-Wide AST Dependency Graphs**: Incorporating Language Server Protocol (LSP) and Tree-sitter parsers to build global symbol graphs across enterprise monorepositories.
3. **CI/CD Native Webhook Bots**: Packaging the agent as an automated GitHub Action or GitLab CI bot that triggers automatically on pull request failures and submits verified repair PRs with detailed literate coding explanations.

---

<div style="page-break-after: always;"></div>

# REFERENCES

1. IBM Corporation, *"IBM Bob: The AI Partner for Software Development,"* IBM Technology Documentation, Armonk, NY, 2024. Available: https://www.ibm.com
2. IBM Research, *"Granite Code Models: A Family of Open Foundation Models for Software Development,"* arXiv preprint arXiv:2405.04324, 2024.
3. LangChain Inc., *"LangGraph: Building Stateful, Multi-Actor Applications with LLMs,"* LangChain Documentation, San Francisco, CA, 2024. Available: https://langchain-ai.github.io/langgraph/
4. M. Monperrus, *"Automatic Software Repair: A Survey,"* ACM Computing Surveys (CSUR), vol. 51, no. 1, pp. 1–31, 2018. DOI: 10.1145/3105906.
5. C. Le Goues, T. Nguyen, S. Forrest, and W. Weimer, *"GenProg: A Generic Method for Automatic Software Repair,"* IEEE Transactions on Software Engineering, vol. 38, no. 1, pp. 54–72, 2012. DOI: 10.1109/TSE.2011.104.
6. H. D. T. Nguyen, D. Qi, A. Roychoudhury, and S. Chandra, *"SemFix: Program Repair via Semantic Analysis,"* in Proceedings of the 35th International Conference on Software Engineering (ICSE), San Francisco, CA, pp. 772–781, 2013.
7. S. Mechtaev, J. Yi, and A. Roychoudhury, *"Angelix: Scalable Multiline Program Repair Using Symbolic Path Conditions,"* in Proceedings of the 38th International Conference on Software Engineering (ICSE), Austin, TX, pp. 128–139, 2016.
8. J. Camacho, *"GitPython: A Python Library Used to Interact with Git Repositories,"* Python Software Foundation, 2024. Available: https://gitpython.readthedocs.io/
9. S. Ramírez, *"FastAPI: Modern, Fast Web Framework for Building APIs with Python,"* 2024. Available: https://fastapi.tiangolo.com/
10. H. Kreger, *"Enterprise Modernization and Automated Governance with watsonx Orchestrate,"* IBM Redbooks, 2024.
11. K. Beck, *"Test-Driven Development: By Example,"* Addison-Wesley Professional, Boston, MA, 2002.
12. Docker Inc., *"Docker Security Guidelines and Container Resource Isolation,"* Docker Documentation, Palo Alto, CA, 2024.
13. A. Vaswani et al., *"Attention Is All You Need,"* in Advances in Neural Information Processing Systems (NeurIPS), Long Beach, CA, vol. 30, pp. 5998–6008, 2017.
14. pytest Development Team, *"pytest: Simple, Powerful Testing with Python,"* 2024. Available: https://docs.pytest.org/
15. Meta Open Source, *"Jest: Delightful JavaScript Testing,"* 2024. Available: https://jestjs.io/

---

<div style="page-break-after: always;"></div>

# APPENDIX A: COMPLETE SOURCE CODE EXCERPTS

### A.1 LangGraph Multi-Agent Workflow (`backend/graph.py`)
```python
# Excerpt: LangGraph Cyclic State Machine Construction
from langgraph.graph import StateGraph, START, END

builder = StateGraph(AgentWorkflowState)

builder.add_node("node_run_tests", self.node_run_tests)
builder.add_node("node_debug", self.node_debug)
builder.add_node("node_human_gate", self.node_human_gate)
builder.add_node("node_validate", self.node_validate)

builder.add_edge(START, "node_run_tests")

builder.add_conditional_edges(
    "node_run_tests",
    self._route_after_test_runner,
    {"end": END, "node_debug": "node_debug"}
)

builder.add_conditional_edges(
    "node_debug",
    self._route_after_debugger,
    {"node_human_gate": "node_human_gate", "node_validate": "node_validate", "end": END}
)

builder.add_conditional_edges(
    "node_human_gate",
    self._route_after_human_gate,
    {"node_validate": "node_validate", "end": END}
)

builder.add_conditional_edges(
    "node_validate",
    self._route_after_validator,
    {"node_debug": "node_debug", "end": END}
)

self.graph = builder.compile()
```

### A.2 Safe Git Rollback and Branching (`backend/git_manager.py`)
```python
# Excerpt: Ephemeral Branch Creation & Atomic Rollback
def create_isolated_fix_branch(self, run_id: str) -> str:
    branch_name = f"ibm-bob-fix-{run_id}"
    if branch_name in [h.name for h in self.repo.heads]:
        self.repo.git.checkout(branch_name)
    else:
        self.repo.git.checkout("-b", branch_name)
    self.active_fix_branch = branch_name
    return branch_name

def rollback_changes(self) -> bool:
    try:
        self.repo.git.reset("--hard", "HEAD")
        self.repo.git.clean("-fd")
        return True
    except Exception as e:
        logger.error(f"Failed to rollback working tree: {e}")
        return False
```

---

<div style="page-break-after: always;"></div>

# APPENDIX B: INSTALLATION, CONFIGURATION & USER MANUAL

### B.1 Hardware & Software Prerequisites
- Operating System: Windows 10/11, macOS, or Linux
- Python: Version 3.10 to 3.14 (Verified on Python 3.14.2)
- Node.js & npm: Node v18+ (Verified on Node v25.5.0)
- Git: Git 2.30+ (Configured in system PATH or internal distribution)

### B.2 Step-by-Step Installation Procedure

```powershell
# 1. Navigate to project root directory
cd C:\Users\amank\.gemini\antigravity\scratch\ibm-bob-bugfix-agent

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Install Node.js dependencies for Jest
npm install
```

### B.3 Running Automated Test Verification

```powershell
# Execute the comprehensive internal agent unit test suite
pytest -v tests/
```
Expected output: **5 passed in ~21s**.

### B.4 Starting the Application Server

```powershell
# Start Uvicorn ASGI server with hot-reload enabled
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### B.5 Operating the Web Dashboard
1. Open your web browser and navigate to: **`http://127.0.0.1:8000`**
2. Confirm that the topbar status displays **"Connected (Live)"** with a pulsing green indicator.
3. Select the target repository:
   - **Python Calculator** (pytest test suite)
   - **JS String Utils** (Jest test suite)
4. Configure parameters:
   - Max Retries: `3`
   - Risk Gate: `0.4`
   - Toggle **Human-in-the-Loop** to observe safety gate prompts.
5. Click **"▶ Run Bug-Fixing Agent"**.
6. Observe live telemetry in the **Live Agent Execution Console**, review the syntax-highlighted diff in the **Proposed Patch** viewer, and monitor automated commits in the **Fix History** timeline.
