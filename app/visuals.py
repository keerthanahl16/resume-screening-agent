import plotly.graph_objects as go

def candidate_radar_chart(candidate):
    labels = ["Embedding Match", "Skill Match", "Experience Match", "Skill Richness"]
    values = [
        candidate["embed_score"],
        candidate["skill_score"],
        candidate["exp_score"],
        len(candidate.get("skills", [])) / 20
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill='toself',
        name="Candidate Profile"
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False,
        height=350
    )

    return fig
