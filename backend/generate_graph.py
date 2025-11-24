"""Script to generate and save LangGraph visualization as PNG."""

from pathlib import Path

from app.agents.supervisor import agent_graph

# Output directory
output_dir = Path(__file__).parent.parent / "docs"
output_dir.mkdir(exist_ok=True)

output_path = output_dir / "agent_workflow.png"

# Generate graph visualization
try:
    # Get the graph as a Mermaid diagram
    graph_image = agent_graph.get_graph().draw_mermaid_png()

    # Save to file
    with open(output_path, "wb") as f:
        f.write(graph_image)

    print(f"✓ LangGraph diagram saved to: {output_path}")
    print(f"  Absolute path: {output_path.absolute()}")

except Exception as e:
    print(f"Error generating graph: {e}")
    print("Make sure you have the required dependencies:")
    print("  uv add --dev grandalf pygraphviz")
