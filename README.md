# 🧪 Self-Improving Test Generation Agent

An **Agentic AI-based software testing assistant** that analyzes source code, automatically generates unit tests, executes them, analyzes failures, and iteratively improves the generated tests.

The system follows a self-improving feedback loop:

```text
Analyze → Generate → Execute → Analyze Failure → Improve → Execute Again
```

---

## 📌 Problem Statement

Writing and maintaining unit tests manually can be time-consuming, especially when code changes frequently.

Common challenges include:

* Manually writing repetitive test cases
* Missing important edge cases
* Updating tests when source code changes
* AI-generated tests containing incorrect assumptions
* Generated tests not being validated through actual execution

Generating a test is not enough. The test should be **executed and validated**, and when it fails, the system should understand the failure and improve the test.

---

## 💡 Proposed Solution

The **Self-Improving Test Generation Agent** automates this process using Agentic AI.

The user uploads source code and selects the programming language. The agent then:

1. Analyzes the source code
2. Generates unit tests
3. Executes the generated tests
4. Checks the execution result
5. Analyzes failures
6. Improves the generated tests
7. Executes the improved tests again
8. Stops when tests pass or the retry limit is reached

This creates a feedback-driven testing loop instead of one-shot test generation.

---

## 🤖 Why Agentic AI?

A normal LLM workflow may look like:

```text
Code → LLM → Test
```

Our system uses an iterative workflow:

```text
Code
 ↓
Analyze
 ↓
Generate Test
 ↓
Execute
 ↓
 ┌───────────────┐
 │ Test Passed?  │
 └───────────────┘
      ↓       ↓
     YES      NO
      ↓       ↓
    Finish  Analyze Error
                ↓
             Improve
                ↓
             Execute
                ↓
              Again
```

The agent uses execution feedback to decide whether it needs another improvement cycle.

---

## 🏗️ System Architecture

```text
                    USER
                     │
                     ▼
              ┌─────────────┐
              │  Streamlit  │
              │     UI      │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │  LangGraph  │
              │    Agent    │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ Code        │
              │ Analyzer    │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ Test        │
              │ Generator   │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ Test Runner │
              └──────┬──────┘
                     │
                PASS / FAIL
                 │       │
              PASS       FAIL
                │         │
                ▼         ▼
              END    Error Analysis
                          │
                          ▼
                     Self-Healing
                          │
                          ▼
                     Test Runner
```

---

## 🔄 Agent Workflow

The LangGraph workflow contains the following major stages:

### 1. Code Analysis

The LLM analyzes the uploaded source code and understands:

* Functions
* Inputs and outputs
* Expected behavior
* Possible edge cases
* Important logic

### 2. Test Generation

Based on the source code and analysis, the LLM generates appropriate unit tests.

### 3. Test Execution

The generated test is sent to the appropriate test runner.

Current MVP:

```text
Python → Pytest
```

The architecture also provides language-specific runners for:

```text
JavaScript → Jest
Java → JUnit
```

These require their respective runtime/dependency environments.

### 4. Failure Analysis

If the test fails, the execution output is sent back to the LLM.

The agent analyzes:

* Assertion failures
* Syntax errors
* Runtime errors
* Incorrect assumptions
* Test implementation problems

### 5. Self-Healing

The agent generates an improved version of the test based on the failure information.

### 6. Re-Execution

The improved test is executed again.

A retry limit is used to prevent an infinite loop.

---

## 🛠️ Technology Stack

| Technology                  | Purpose                             |
| --------------------------- | ----------------------------------- |
| Python                      | Core application and agent logic    |
| Groq API                    | LLM inference                       |
| OpenAI GPT-OSS 20B via Groq | Current LLM model                   |
| LangChain                   | LLM integration                     |
| LangGraph                   | Agent workflow and state management |
| Pytest                      | Python test execution               |
| Streamlit                   | User interface                      |
| python-dotenv               | Environment variable management     |
| Jest                        | JavaScript test runner extension    |
| JUnit                       | Java test runner extension          |

---

## 📂 Project Structure

```text
self_improving_test_agent/
│
├── app.py
│
├── agent.py
│
├── prompts.py
│
├── test_runner.py
│
├── routers/
│   ├── __init__.py
│   ├── python_runner.py
│   ├── javascript_runner.py
│   └── java_runner.py
│
├── requirements.txt
│
├── .env
│
└── README.md
```

### File Responsibilities

#### `app.py`

Contains the Streamlit interface.

Responsibilities:

* Programming language selection
* Source-code upload
* Start agent workflow
* Display code analysis
* Display generated tests
* Display test results
* Display error analysis
* Display self-healing attempts

#### `agent.py`

Contains the main Agentic AI workflow.

Responsibilities:

* LLM interaction
* LangGraph state management
* Code analysis
* Test generation
* Test execution
* Error analysis
* Self-healing
* Retry control

#### `prompts.py`

Contains prompts used by the LLM for:

* Code analysis
* Test generation
* Error analysis
* Test improvement

#### `test_runner.py`

Acts as a language-based test runner router.

```text
Python      → python_runner.py
JavaScript  → javascript_runner.py
Java        → java_runner.py
```

#### `routers/python_runner.py`

Executes Python tests using Pytest.

#### `routers/javascript_runner.py`

Provides the Jest execution path for JavaScript projects where Node.js/Jest is configured.

#### `routers/java_runner.py`

Provides the Java/JUnit execution path where the required Java/JUnit environment is configured.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd self_improving_test_agent
```

### 2. Create Virtual Environment

Windows:

```powershell
python -m venv venv
```

Activate:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

### Important

Do not upload `.env` to GitHub.

Add this to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Run the Application

Start Streamlit:

```powershell
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Example

Suppose the uploaded source code is:

```python
def add(a, b):
    return a + b
```

The agent can generate a test such as:

```python
def test_add():
    assert add(2, 3) == 5
```

The test is then executed using Pytest.

If it passes:

```text
✅ Tests passed successfully!
```

If it fails, the agent analyzes the failure and attempts to improve the test.

---

## 🔁 Self-Healing Loop

The main innovation of the project is the feedback loop:

```text
             ┌──────────────────┐
             │   Source Code    │
             └────────┬─────────┘
                      ↓
             ┌──────────────────┐
             │  Generate Tests  │
             └────────┬─────────┘
                      ↓
             ┌──────────────────┐
             │  Execute Tests   │
             └────────┬─────────┘
                      ↓
                ┌─────────────┐
                │   Passed?   │
                └──────┬──────┘
                   YES │ NO
                    ↓  │
                   END │
                       ↓
              ┌─────────────────┐
              │ Analyze Failure │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Improve Tests   │
              └────────┬────────┘
                       │
                       └──────→ Execute Again
```

---

## 🎯 Key Features

* AI-powered code analysis
* Automatic unit-test generation
* Real test execution
* Failure analysis
* Self-healing test generation
* Retry mechanism
* Language-aware runner architecture
* Streamlit interface
* LangGraph-based agent workflow

---

## 🚧 Current Limitations

The current MVP primarily focuses on:

```text
Python + Pytest
```

JavaScript/Jest and Java/JUnit are supported through the runner architecture but require their respective execution environments and dependencies.

Other advanced features such as coverage-guided generation, mutation testing, and repository-wide analysis are future enhancements.

---

## 🚀 Future Scope

### 1. Coverage-Guided Test Generation

Generate tests specifically for uncovered code paths.

### 2. Mutation Testing

Introduce controlled code mutations to evaluate test quality.

### 3. GitHub Integration

Automatically analyze repositories and create/update test files.

### 4. CI/CD Integration

Run the agent automatically in development pipelines.

### 5. Repository-Level Analysis

Analyze multiple files and understand dependencies between modules.

### 6. Test Coverage Visualization

Display:

```text
Line Coverage
Branch Coverage
Function Coverage
```

using visual dashboards.

---

## 🏆 Project Highlights

The project demonstrates the combination of:

```text
LLM
 +
LangChain
 +
LangGraph
 +
Real Test Execution
 +
Feedback Loop
 =
Agentic Software Testing
```

Unlike simple test-generation tools, the system does not stop after generating a test. It uses **execution feedback** to analyze failures and improve the generated test.

---

## 🎤 Interview Explanation

### What problem does your project solve?

> Manual test creation and validation can be time-consuming, and AI-generated tests can also contain errors. Our project automates test generation and validates those tests through actual execution.

### What is the solution?

> We built an Agentic AI system that analyzes source code, generates tests, executes them, analyzes failures, and iteratively improves the tests.

### Why LangGraph?

> LangGraph allows us to represent the testing process as a stateful workflow with conditional transitions. For example, if a test fails, the workflow moves to error analysis and self-healing instead of simply stopping.

### Where is the Agentic behavior?

> The agent observes test execution results and decides whether it should finish or perform another improvement cycle. This Generate → Execute → Analyze → Improve loop makes the system iterative and feedback-driven.

### What is the role of Groq?

> Groq provides the LLM inference layer. We use the LLM for code understanding, test generation, failure analysis, and test improvement.

### What is the role of Pytest?

> Pytest actually executes the generated Python tests. The execution result becomes feedback for the agent.

---

## 📜 License

This project is developed as an academic/hackathon project.

---

## 👨‍💻 Author

**Adarsh Sharma**

B.Tech – Computer Science & Engineering
Arya College of Engineering, Jaipur
Rajasthan Technical University, Kota

---

## ⭐ Project Summary

> **Self-Improving Test Generation Agent is an Agentic AI-based software testing assistant that automatically analyzes source code, generates unit tests, executes them, analyzes failures, and improves the tests through an iterative feedback loop.**
