import streamlit as st
import plotly.graph_objects as go

DATA = [
    {
        "category": "28.11 Judgement\nmethodology - Without\nFWO - Pay Period",
        "value": 1668147026.75,
        "color": "#10b981",
        "title": "Scenario A",
        "features": [
            "Clause 28.11 Approach: Judgement-Based Approach",
            "Losses overlapping with FWO claim: Not Deducted",
            "Set-Off Approach: Pay Period",
        ],
    },
    {
        "category": "28.11 Judgement\nmethodology - Without\nFWO - Bi Annual",
        "value": 1371946816.29,
        "color": "#06b6d4",
        "title": "Scenario B",
        "features": [
            "Clause 28.11 Approach: Judgement-Based Approach",
            "Losses overlapping with FWO claim: Not Deducted",
            "Set-Off Approach: Bi-Annual",
        ],
    },
    {
        "category": "28.11 Judgement\nmethodology - With\nFWO - Bi Annual",
        "value": 213397928.90,
        "color": "#f59e0b",
        "title": "Scenario C",
        "features": [
            "Clause 28.11 Approach: Judgement-Based Approach",
            "Losses overlapping with FWO claim: Deducted",
            "Set-Off Approach: Bi-Annual",
        ],
    },
    {
        "category": "28.11 Coles\nmethodology - With\nFWO - Bi Annual",
        "value": 56690258.85,
        "color": "#8b5cf6",
        "title": "Scenario D",
        "features": [
            "Clause 28.11 Approach: Coles Based Approach",
            "Losses overlapping with FWO claim: Deducted",
            "Set-Off Approach: Bi-Annual",
        ],
    },
]

DATA2 = [
    {
        "category": "28.11 Judgement - Pay period - 557C on non-clocked shifts",
        "value": 690773333.38,
        "color": "#06b6d4",
        "title": "Scenario A",
        "features": [
            "Clause 28.11 Approach: Judgement-Based Approach",
            "Set-Off Approach: Pay period",
            "557C condition on non-clocked shifts",
        ],
    },
    {
        "category": "28.11 Judgement - Pay period - 557C non-clocked - After FWO",
        "value": 282887638.08,
        "color": "#3b82f6",
        "title": "Scenario B",
        "features": [
            "Clause 28.11 Approach: Judgement-Based Approach",
            "Set-Off Approach: Pay period",
            "557C condition on non-clocked shifts",
            "FWO overlap deducted",
        ],
    },
    {
        "category": "28.11 Coles - Annual - 557C on all shifts - After FWO",
        "value": 214695100.81,
        "color": "#f59e0b",
        "title": "Scenario C",
        "features": [
            "Clause 28.11 Approach: Coles Based Approach",
            "Set-Off Approach: Annual",
            "557C condition on all shifts",
            "FWO overlap deducted",
        ],
    },
    {
        "category": "28.11 Coles - Annual - 557C non-clocked - After FWO",
        "value": 26617692.75,
        "color": "#8b5cf6",
        "title": "Scenario D",
        "features": [
            "Clause 28.11 Approach: Coles Based Approach",
            "Set-Off Approach: Annual",
            "557C condition on non-clocked shifts",
            "FWO overlap deducted",
        ],
    },
]

# =========================
# Helpers
# =========================
def format_currency(value: float) -> str:
    return f"A${value:,.2f}"


def format_short(value: float) -> str:
    if value >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    return format_currency(value)


def render_section(
    data,
    header_title: str,
    header_sub: str,
    panel_title: str = "Comparative Analysis",
    notes=None,  # <-- FIX: now accepts notes
):
    # ---------- Header ----------
    st.markdown(
        f"""
        <div class="hdr-wrap">
          <div class="hdr-row">
            <div class="hdr-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="#60a5fa" stroke-width="2"/>
                <path d="M14 2v6h6" stroke="#60a5fa" stroke-width="2"/>
                <path d="M8 13h8M8 17h8" stroke="#60a5fa" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <div class="hdr-title">{header_title}</div>
          </div>
          <div class="hdr-sub">{header_sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Notes (NEW) ----------
    if notes:
        notes_html = "".join(
            [
                f"<div style='margin:6px 0; color: rgba(226,232,240,0.80); font-size:0.95rem;'>• {n}</div>"
                for n in notes
            ]
        )
        st.markdown(
            f"<div style='text-align:center; margin:-0.5rem 0 1.2rem 0;'>{notes_html}</div>",
            unsafe_allow_html=True,
        )

    # ---------- Main panel ----------
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">{panel_title}</div>', unsafe_allow_html=True)

    # ---------- Chart ----------
    values = [d["value"] for d in data]
    max_val = max(values) if values else 0

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=list(range(len(data))),
            y=values,
            marker=dict(color=[d["color"] for d in data]),
            width=0.42,
            hovertemplate="<b>%{customdata}</b><br>Total: %{y:,.2f} AUD<extra></extra>",
            customdata=[d.get("title", d.get("category", "")).replace("\n", " ") for d in data],
        )
    )

    for i, d in enumerate(data):
        fig.add_annotation(
            x=i,
            y=d["value"],
            yshift=22,
            text=f"<b><span style='color:{d['color']}'>{format_short(d['value'])}</span></b>",
            showarrow=False,
            align="center",
            font=dict(size=12, color=d["color"]),
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="rgba(255,255,255,0.65)",
            borderwidth=1,
            borderpad=6,
        )

    fig.update_layout(
        height=520,
        margin=dict(l=40, r=40, t=20, b=85),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickmode="array",
            tickvals=list(range(len(data))),
            ticktext=[d.get("title", d.get("category", "")) for d in data],
            tickfont=dict(color="rgba(226,232,240,0.92)", size=11),
        ),
        yaxis=dict(
            range=[0, (max_val * 1.18) if max_val else 1],
            showgrid=False,
            zeroline=False,
            ticks="",
            showticklabels=False,
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------- Cards row ----------
    cols = st.columns(len(data), gap="medium")

    for col, d in zip(cols, data):
        title_src = d.get("title", d.get("category", ""))
        title_html = title_src.replace("\n", "<br>")

        features_html = "".join(
            [
                "<div class='card-li'>"
                f"<div class='dot' style='color:{d['color']}'>●</div>"
                f"<div class='li-text'>{f}</div>"
                "</div>"
                for f in d.get("features", [])
            ]
        )

        card_html = f"""
        <div class="card" style="border: 2px solid {d['color']};">
          <div class="card-hdr" style="border-bottom-color: {d['color']}22;">
            <div class="swatch" style="background:{d['color']};"></div>
            <div class="card-title">{title_html}</div>
          </div>

          <div>{features_html}</div>

          <div class="card-ft">
            <div class="ft-lbl">Total Amount</div>
            <div class="ft-val" style="color:{d['color']};">{format_currency(d['value'])}</div>
          </div>
        </div>
        """
        with col:
            st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)


# =========================
# Page config + CSS
# =========================
st.set_page_config(page_title="Sensitivity Analysis", layout="wide")

st.markdown(
    """
<style>
.stApp {
  background: radial-gradient(1200px 700px at 20% 0%, rgba(59,130,246,0.20), rgba(0,0,0,0) 55%),
              radial-gradient(900px 600px at 100% 10%, rgba(16,185,129,0.18), rgba(0,0,0,0) 55%),
              linear-gradient(135deg, #0b1220 0%, #0f172a 45%, #0b1220 100%);
  color: #e5e7eb;
}
.block-container { padding-top: 2.0rem; padding-bottom: 2.5rem; }

.hdr-wrap { text-align: center; margin-bottom: 1.5rem; }
.hdr-row  { display: inline-flex; align-items: center; gap: 14px; }
.hdr-icon {
  width: 44px; height: 44px; border-radius: 12px;
  background: rgba(59,130,246,0.12);
  border: 1px solid rgba(59,130,246,0.30);
  display: grid; place-items: center;
  box-shadow: 0 12px 30px rgba(0,0,0,0.25);
}
.hdr-title { font-size: 2.05rem; font-weight: 800; color: #ffffff; line-height: 1.15; }
.hdr-sub   { color: rgba(226,232,240,0.80); font-size: 1.05rem; margin-top: 0.35rem; }

.panel {
  background: linear-gradient(135deg, rgba(30,41,59,0.60), rgba(2,6,23,0.55));
  border: 1px solid rgba(148,163,184,0.20);
  border-radius: 18px;
  box-shadow: 0 18px 45px rgba(0,0,0,0.35);
  padding: 22px 22px 18px 22px;
}

.panel-title {
  font-size: 1.35rem;
  font-weight: 750;
  color: #ffffff;
  margin: 0 0 1.0rem 0;
}

.card {
  background: rgba(255,255,255,0.97);
  border-radius: 14px;
  box-shadow: 0 10px 26px rgba(0,0,0,0.28);
  padding: 14px 14px 12px 14px;
}
.card-hdr {
  display: flex; align-items: flex-start; gap: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(15,23,42,0.12);
  margin-bottom: 10px;
}
.swatch { width: 11px; height: 11px; border-radius: 3px; margin-top: 4px; }
.card-title { font-weight: 800; color: #0f172a; font-size: 0.80rem; line-height: 1.2; }
.card-li { display: flex; gap: 8px; align-items: flex-start; margin-bottom: 8px; }
.dot { font-size: 0.85rem; line-height: 1; margin-top: 1px; }
.li-text { font-size: 0.76rem; color: rgba(15,23,42,0.75); line-height: 1.25; }
.card-ft {
  border-top: 1px solid rgba(15,23,42,0.12);
  margin-top: 10px; padding-top: 10px;
}
.ft-lbl { font-size: 0.72rem; font-weight: 750; color: rgba(15,23,42,0.55); }
.ft-val { font-size: 1.05rem; font-weight: 900; margin-top: 2px; }
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# Render BOTH sections
# =========================
render_section(
    DATA,
    header_title="Woolworths Class Action: Whole Class Sensitivity Analysis",
    header_sub="Methodology Comparison",
    panel_title="Comparative Analysis",
    notes=[
        "These figures include group member losses and interest, but do not include an amount for penalties. The amount of penalties is subject to counsel advice, which is currently in progress.",
        "The budget for the Coles class action, excluding the penalties hearing, is $5,810,631.",
    ],
)

render_section(
    DATA2,
    header_title="Coles Class Action: Whole Class Sensitivity Analysis",
    header_sub="Methodology Comparison",
    panel_title="Comparative Analysis",
    notes=[
        "These figures include group member losses and interest, but do not include an amount for penalties. The amount of penalties is subject to counsel advice, which is currently in progress.",
        "The budget for the Woolworths class action, excluding the penalties hearing, is $8,367,690.",
    ],
)



