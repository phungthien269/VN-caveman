"""
Generate a boxplot showing token compression per skill against the terse
control arm.
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

import plotly.graph_objects as go
import tiktoken

ENCODING = tiktoken.get_encoding("o200k_base")
SNAPSHOT = Path(__file__).parent / "snapshots" / "results.json"
HTML_OUT = Path(__file__).parent / "snapshots" / "results.html"
PNG_OUT = Path(__file__).parent / "snapshots" / "results.png"


def count(text: str) -> int:
    return len(ENCODING.encode(text))


def main() -> None:
    data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    arms = data.get("arms", {})
    meta = data.get("metadata", {})
    terse_outputs = arms.get("__terse__", [])
    if not terse_outputs:
        print("Snapshot chưa có output eval thật. Chạy `python evals/llm_run.py` trước.")
        return

    terse_tokens = [count(output) for output in terse_outputs]
    rows = []
    for skill, outputs in arms.items():
        if skill in ("__baseline__", "__terse__"):
            continue
        skill_tokens = [count(output) for output in outputs]
        savings = [
            (1 - (skill_token / terse_token)) * 100 if terse_token else 0.0
            for skill_token, terse_token in zip(skill_tokens, terse_tokens)
        ]
        rows.append(
            {"skill": skill, "savings": savings, "median": statistics.median(savings)}
        )

    rows.sort(key=lambda row: -row["median"])
    fig = go.Figure()

    for row in rows:
        fig.add_trace(
            go.Box(
                y=row["savings"],
                name=row["skill"],
                boxpoints="all",
                jitter=0.4,
                pointpos=0,
                marker={"color": "#16A34A", "size": 7, "opacity": 0.7},
                line={"color": "#14532D", "width": 2},
                fillcolor="rgba(34, 197, 94, 0.18)",
                boxmean=True,
                hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>",
            )
        )

    fig.add_hline(
        y=0,
        line={"color": "black", "width": 1.5, "dash": "dash"},
        annotation_text="0% = same length as terse control",
        annotation_position="top right",
        annotation_font={"size": 11, "color": "black"},
    )

    fig.update_layout(
        title={
            "text": (
                "<b>`gon` skills shorten replies by how much?</b><br>"
                "<sub>Per-prompt savings vs system prompt = "
                "<i>'Answer concisely in Vietnamese.'</i><br>"
                f"{meta.get('model', '?')} · n={meta.get('n_prompts', '?')} prompts</sub>"
            ),
            "x": 0.5,
            "xanchor": "center",
        },
        xaxis={"title": "", "automargin": True},
        yaxis={
            "title": "↑ ngắn hơn · so với control · dài hơn ↓",
            "ticksuffix": "%",
            "zeroline": False,
            "gridcolor": "rgba(0,0,0,0.08)",
            "range": [-30, 115],
        },
        plot_bgcolor="white",
        height=560,
        width=980,
        margin={"l": 140, "r": 80, "t": 120, "b": 120},
        showlegend=False,
    )

    for row in rows:
        fig.add_annotation(
            x=row["skill"],
            y=max(row["savings"]),
            text=f"<b>{row['median']:+.0f}%</b>",
            showarrow=False,
            yshift=22,
            font={"size": 16, "color": "#14532D"},
        )

    fig.write_html(HTML_OUT)
    print(f"Wrote {HTML_OUT}")
    fig.write_image(PNG_OUT, scale=2)
    print(f"Wrote {PNG_OUT}")


if __name__ == "__main__":
    main()
