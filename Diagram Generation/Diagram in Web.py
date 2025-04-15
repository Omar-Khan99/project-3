from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import webbrowser
import re

load_dotenv("API.env")

llm = ChatGroq(model="llama3-70b-8192", temperature=0.3)

topic = input("Enter what you want to learn: ")

# Generate an explanation
prompt_content = f"""
You are an AI assistant. Your task is to generate an explanation about "{topic}".
This explanation will be converted into a diagram using Mermaid.js.
"""

content = llm.invoke([SystemMessage(content=prompt_content)])
print("\nGenerated Explanation:\n", content.content)

# Generate Mermaid diagram code
prompt_sys = f"""
Generate a valid Mermaid.js diagram based on this explanation:

Content:
{content.content}

Make sure:
- The code follows Mermaid.js syntax strictly.
- No syntax errors are present.
- Return only the Mermaid diagram (no extra text).

Example:
graph TD; A["Start"] --> B["Process"]; B --> C["End"];

Now return only the correct Mermaid code:
"""

response = llm.invoke([HumanMessage(content=topic), SystemMessage(content=prompt_sys)])
mermaid_code = response.content.strip()

# Ask LLM to fix errors if they occur
validation_prompt = f"""
Check this Mermaid.js code for syntax errors:

{mermaid_code}

If there are errors, return a corrected version. If it's correct, return the same code.
"""

validated_response = llm.invoke([HumanMessage(content=validation_prompt)])
validated_mermaid_code = validated_response.content.strip()
validated_mermaid_code = re.sub(r'\bmermaid\b', '', validated_mermaid_code, flags=re.IGNORECASE)


# Create an HTML file with Mermaid diagram
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mermaid Diagram</title>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: false }});

        function renderMermaid() {{
            const diagramElement = document.querySelector(".mermaid");
            try {{
                mermaid.parse(diagramElement.textContent);  // Validate syntax
                mermaid.init(undefined, diagramElement);    // Render the diagram
            }} catch (error) {{
                console.error("Mermaid Syntax Error:", error);
                document.querySelector(".error-message").innerText = "Syntax Error: " + error.message;
            }}
        }}

        document.addEventListener("DOMContentLoaded", renderMermaid);
    </script>
</head>
<body>
    <h2>Mermaid Diagram for: {topic}</h2>
    <div class="mermaid">
        {validated_mermaid_code}
    </div>
    <p class="error-message" style="color: red; font-weight: bold;"></p>
</body>
</html>
"""


# Save and open the HTML file
html_path = os.path.abspath("diagram.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

webbrowser.open(f"file://{html_path}")

print(f"\n✅ Mermaid diagram saved to {html_path} and opened in your browser!")
