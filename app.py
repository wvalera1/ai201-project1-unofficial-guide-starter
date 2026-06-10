import gradio as gr
from generator import generate

SOURCE_LABELS = {
    "source1.txt":  "Running Warehouse — Best Running Shoes of 2026",
    "source2.txt":  "Runner's World — 15 Best Running Shoes of 2026",
    "source3.txt":  "Reddit r/RunningShoeGeeks — Worst shoes ever bought",
    "source4.txt":  "Reddit r/RunningShoeGeeks — Least favorite shoes",
    "source5.txt":  "Runrepeat — 7 Best Cross Country Shoes 2026",
    "source6.txt":  "Reddit r/CrossCountry — Shoes for cross country",
    "source7.txt":  "Runrepeat — Best Treadmill Running Shoes",
    "source8.txt":  "Reddit r/AdvancedRunning — Budget running shoes",
    "source9.txt":  "Runner's World — Best Affordable Running Shoes",
    "source10.txt": "Supwell — Most Expensive Race Shoes by Brand",
}


def handle_query(question):
    result = generate(question)
    sources = "\n".join(f"• {SOURCE_LABELS.get(s, s)}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="Running Shoe Guide") as demo:
    gr.Markdown("## Running Shoe Guide\nAnswers are grounded in 10 curated sources only.")
    inp = gr.Textbox(label="Your question", placeholder="e.g. What are the best stability shoes?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()
