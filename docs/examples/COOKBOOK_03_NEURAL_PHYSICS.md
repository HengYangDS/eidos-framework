# Cookbook III: Neural Physics with Eigen

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

This cookbook demonstrates how to build **AI Agents**, **RAG Pipelines**, and
**Swarms** using Eigen's neural operators.

## Scenario 1: The RAG Pipeline (Hamiltonian)

**Goal**: Retrieve relevant context from a Vector DB and answer a user query.

### 1.1 The Standard Model of RAG

```python
from eigen.core import Flow, Operator
from eigen.techne import VectorSource, LLM
from eigen.bosons import Map, Filter

# --- 1. Bosons ---

class Embed(Operator[str, list[float]]):
    async def __call__(self, text: str):
        return await openai.embeddings.create(input=text)

class Retrieve(Operator[list[float], list[str]]):
    def __init__(self, k=5): self.k = k
    async def __call__(self, vector):
        return await pinecone.query(vector, top_k=self.k)

class Generate(Operator[tuple[str, list[str]], str]):
    async def __call__(self, pair):
        query, context = pair
        prompt = f"Context: {context}\nQuestion: {query}"
        return await gpt4.complete(prompt)

# --- 2. The Pipeline ---

# We need to keep the original Query to pass to the LLM.

# We use Entanglement to Fork the flow.

RAG = (

    # Path 1: Just pass the query

    # Path 2: Embed -> Retrieve
    (Identity & (Embed() >> Retrieve())) 
    >> Generate()
)

```

## Scenario 2: The Debate Swarm (Multi-Agent)

**Goal**: Have two agents (Proponent and Opponent) debate a topic, then a Judge
decides.

```python

# --- 1. The Agents ---
Proponent = LLM(role="Proponent", temperature=0.7)
Opponent  = LLM(role="Opponent",  temperature=0.7)
Judge     = LLM(role="Judge",     temperature=0.0)

# --- 2. The Interaction (Ping Pong) ---

# We use a Feedback Loop (<<)

@atom
def CombineHistory(history, response):
    return history + [response]

DebateRound = (
    Proponent 
    >> CombineHistory 
    >> Opponent 
    >> CombineHistory
)

# --- 3. The Loop ---

# Run 3 rounds of debate
Debate = DebateRound * 3 

# --- 4. The Verdict ---
FinalSystem = Debate >> Judge

```

## Scenario 3: Self-Correction (Perturbation)

**Goal**: If the Agent generates invalid code, feed the error back to fix it.

```python

# --- 1. The Code Generator ---
Coder = LLM(system="You are a Python expert.")

# --- 2. The Executor (Measurement) ---
class PythonExec(Operator):
    async def __call__(self, code):
        try:
            exec(code)
            return Result(success=True, output=...)
        except Exception as e:
            return Result(success=False, error=str(e))

# --- 3. The Feedback Loop ---

# We use a recursive definition

@atom
def FixPrompt(result):
    return f"The previous code failed with: {result.error}. Fix it."

def SelfCorrectingCoder(max_retries=3):
    def loop(input_state, attempt):
        if attempt > max_retries:
            raise GiveUp()
            
        code = await Coder(input_state)
        result = await PythonExec(code)
        
        if result.success:
            return result
        else:

            # Recursion with new prompt
            new_input = FixPrompt(result)
            return loop(new_input, attempt + 1)
            
    return loop

```

In Eigen, this recursion can be expressed algebraically:

```python

# A = Action (Code)

# M = Measure (Exec)

# F = Feedback (Fix)

# Loop until M returns Success
StableCoder = (Coder >> M) | (F >> StableCoder)

```

## Scenario 4: Genetic Prompt Engineering (Biogenesis)

**Goal**: Evolve the System Prompt to maximize accuracy.

```python
from eigen.bio import Genome, Mutate, Select

# --- 1. The Genome ---

# The prompt is the DNA
class PromptGenome(Genome):
    content: str

# --- 2. Mutation ---

# Use an LLM to rephrase the prompt
Mutator = LLM("Rewrite this prompt to be more concise/clear.")

# --- 3. Evolution ---
def OptimizePrompt(seed_prompt, validation_set):
    population = [seed_prompt] * 10
    
    for generation in range(5):

        # 1. Evaluate
        scores = [Evaluate(p, validation_set) for p in population]
        
        # 2. Select
        survivors = Select(population, scores, top_k=2)
        
        # 3. Mutate
        population = survivors + [Mutate(p) for p in survivors]
        
    return population[0]

```

## Scenario 5: The Semantic Router (Choice)

**Goal**: Route query to Math, Coding, or General agent based on intent.

```python

# --- 1. Classification ---
Router = LLM("Classify input: [Math, Code, Chat]")

# --- 2. The Switch ---

# We use Pattern Matching on the Router output

System = Router >> (
    Case("Math") >> MathAgent |
    Case("Code") >> CodingAgent |
    Case("Chat") >> ChatAgent
)

```

This is a **Spectrum Analyzer** separating the input beam.

---
**Eigen Cosmology** | [Previous: Cookbook II](COOKBOOK_02_QUANTUM_FINANCE.md) | [Index](../00_INDEX.md) | [Next: Cookbook IV](COOKBOOK_04_SYSTEM_OPS.md) | *© 2025 The Eigen High Council*
