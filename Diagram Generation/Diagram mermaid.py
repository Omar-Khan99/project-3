from langchain_groq import ChatGroq
from langchain.schema import HumanMessage ,AIMessage,SystemMessage
from dotenv import load_dotenv
load_dotenv("API.env")
import subprocess
import re

llm = ChatGroq(model="llama3-70b-8192", temperature=0)
topic = input("Enter what you want learn: ")
prompt_content = f"""
You are an agent working in a multi-agent system.
Your job is to provide a description that explains a {topic}
This description will be passed to create a diagram using the Mermaid language.
"""

content = llm.invoke([SystemMessage(content=prompt_content)])


prompt_sys = f"""
You are an agent working in a multi-agent system.
Your job is create a code Mermaid and sure it's right
Based on the following content, create a code Mermaid.
Your respones just code Mermaid.

content:
{content.content}

Make sure you create the code without errors and following the correct syntax.

These some Examples for code Mermaid.
EX 1:

graph TD;
    A["Input Data"] --> B["Neural Network"];
    B --> C["Hidden Layers"];
    C -->|"Weights & Biases"| D["Activation Functions"];
    D --> E["Backpropagation & Optimization"];
    E --> F["Output Predictions"];

    C --> G["Layer 1: Convolution/ Fully Connected"];
    G --> H["Layer 2: Non-Linearity (ReLU)"];
    H --> I["Layer 3: Pooling (Max/Avg)"];
    I --> J["Layer 4: Fully Connected Layer"];
    J --> K["Softmax / Sigmoid for Classification"];

    E --> L["Loss Function (MSE, Cross-Entropy)"];
    L --> M["Gradient Descent (Adam, SGD)"];
    M -->|"Adjust Weights"| C;

EX 2:
graph LR
    classDef node stroke-width:2px,stroke:#333,fill:#fff;
    classDef edge stroke-width:2px,stroke:#333;

    subgraph Input Embeddings
        Token1[Token 1]
        Token2[Token 2]
        TokenN[Token N]
    end

    subgraph QueryKeyValueMatrices
        Q[Query Matrix]
        K[Key Matrix]
        V[Value Matrix]
    end

    subgraph SelfAttentionMechanism
        AttentionWeights[Attention Weights]
        Softmax[Softmax]
        ContextVector[Context Vector]
    end

    Token1 -->| Embedding | Q
    Token2 -->| Embedding | Q
    TokenN -->| Embedding | Q

    Token1 -->| Embedding | K
    Token2 -->| Embedding | K
    TokenN -->| Embedding | K

    Token1 -->| Embedding | V
    Token2 -->| Embedding | V
    TokenN -->| Embedding | V

    Q -->| Matrix Multiplication | AttentionWeights
    K -->| Matrix Multiplication | AttentionWeights
    V -->| Matrix Multiplication | AttentionWeights

    AttentionWeights -->| Softmax | Softmax
    Softmax -->| Weighted Sum | ContextVector
"""
print(content.content)
response = llm.invoke([SystemMessage(content=prompt_sys)])
response_text = response.content
response_text = re.sub(r'\bmermaid\b', '', response.content, flags=re.IGNORECASE)

#print(f'Code: {response_text}')
mermaid_code = response_text.split('```')[1]
print(mermaid_code)
# Save to a file
with open("Diagram Generation\\mer_diagram.mmd", "w") as f:
    f.write(mermaid_code)

def check_mermaid_code(path="Diagram Generation\\mer_diagram.mmd",code=mermaid_code):
    while True:

        mmdc_path = "C:\\Users\\Windows 11\\AppData\\Roaming\\npm\\mmdc.cmd"  # Update this path!
        # Running the mermaid-cli to generate the diagram
        result =subprocess.run([mmdc_path, "-i", "Diagram Generation\\mer_diagram.mmd", "-o", "Diagram Generation\\mer_diagram.png", "-s", "4"]
                       , shell=True,
                       capture_output=True, text=True)

        # Check for errors in the Mermaid generation
        if result.returncode != 0:
            error = result.stderr.strip().split('Parser3')[0]
            print(error)
            final_code=edit_mermaid_code(error,code)
            code = final_code
            print(final_code)
        else:
            return "Diagram generated successfully",final_code

def edit_mermaid_code(error, code):
    prompt_sys = f"""
    You are an agent working in a multi-agent system.
    Your job is fix invalid Mermaid code and sure it's right.
    You will be given:
    1. An error message from Mermaid CLI.
    2. The original Mermaid code.

    Fix the code based on the error.

    ERROR:
    {error}


    These some Examples for incorrect code Mermaid ,error message and correct code.
    EX 1:
    incorect code:
    graph LR
        classDef component fill:#f9f,stroke:#2px,stroke-width:2px;
        classDef relationship fill:none,stroke:#333,stroke-width:2px;
        input[Input] -->|text| tokenization[Tokenization]
        tokenization -->|tokens| > embeddings[Embeddings]
        embeddings -->|vectors|> encoder[Encoder]
        encoder -->|context|> decoder[Decoder]
        decoder -->|generated text|> output[Output]
        pre-training[Pre-training] -.->|pre-trains|> embeddings
        fine-tuning -.->|fine-tunes|> decoder
        class input, tokenization, embeddings, encoder, decoder, output component
        class pre-training, fine-tuning relationship 

    error message:
    Error: Parse error on line 5:
    ...ization -->|tokens| > embeddings[Embeddi
    -----------------------^
    Expecting 'AMP', 'COLON', 'DOWN', 'DEFAULT', 'NUM', 'COMMA', 'NODE_STRING', 'BRKT', 'MINUS', 'MULT', 'UNICODE_TEXT', got 'TAGEND'

    correct code:
    graph LR
        classDef component fill:#f9f,stroke:#2px,stroke-width:2px;
        classDef relationship fill:none,stroke:#333,stroke-width:2px;
        input[Input] -->|text| tokenization[Tokenization]
        tokenization -->|tokens| embeddings[Embeddings]
        embeddings -->|vectors| encoder[Encoder]
        encoder -->|context| decoder[Decoder]
        decoder -->|generated text| output[Output]
        pre-training[Pre-training] -.->|pre-trains| embeddings
        fine-tuning -.->|fine-tunes| decoder
        class input,tokenization,embeddings,encoder,decoder,output component
        class pre-training,fine-tuning relationship
    """
    
    llm = ChatGroq(model="llama3-70b-8192", temperature=0)
    response = llm.invoke([
    SystemMessage(content=prompt_sys),
    HumanMessage(content=code)
    ])
    response_text = response.content
    response_text = re.sub(r'\bmermaid\b', '', response.content, flags=re.IGNORECASE)
    mermaid_code = response_text.split('```')[1]

    # Save the generated Mermaid code to a file (e.g., diagram.mmd)
    with open("Diagram Generation\\mer_diagram.mmd", "w") as file:
        file.write(mermaid_code)

    return mermaid_code

t,c = check_mermaid_code()
print(t)
print(c)
# Use full path to mmdc
#subprocess.run([mmdc_path, "-i", "diagram.mmd", "-o", "diagram.png", "-s", "4"], shell=True)

print("Mermaid diagram generated: diagram.png")

