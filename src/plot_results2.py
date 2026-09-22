"""
plot_timeline.py
Message-level timeline showing exactly where TCP breaks the session
during handover, vs QUIC keeping the same session throughout.
"""
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'DejaVu Sans'

fig, ax = plt.subplots(figsize=(11, 5))
msg_idx = list(range(10))

# ---- TCP row: two separate sessions ----
tcp_y = 1
session1_color = "#E74C3C"
session2_color = "#F5A78B"

ax.plot(msg_idx[:5], [tcp_y]*5, 'o-', color=session1_color, markersize=10, linewidth=2.5, zorder=3)
ax.plot(msg_idx[5:], [tcp_y]*5, 'o-', color=session2_color, markersize=10, linewidth=2.5, zorder=3)
ax.plot(4.5, tcp_y, marker='X', color='black', markersize=16, zorder=5)
ax.annotate("Connection closed\n+ new handshake", xy=(4.5, tcp_y), xytext=(4.5, tcp_y+0.35),
            ha='center', fontsize=9, color="#992D22", fontweight='bold')
ax.text(2, tcp_y-0.28, "Session ID: A", ha='center', fontsize=9.5, color=session1_color, fontweight='bold')
ax.text(7, tcp_y-0.28, "Session ID: B (new!)", ha='center', fontsize=9.5, color="#C0392B", fontweight='bold')

# ---- QUIC row: one continuous session ----
quic_y = 0
quic_color = "#27AE60"
ax.plot(msg_idx, [quic_y]*10, 'o-', color=quic_color, markersize=10, linewidth=2.5, zorder=3)
ax.plot(4.5, quic_y, marker='|', color='black', markersize=22, mew=2.5, zorder=5)
ax.annotate("Local port changed\n(Wi-Fi \u2192 Cellular)", xy=(4.5, quic_y), xytext=(4.5, quic_y-0.42),
            ha='center', fontsize=9, color="#1D6C3E", fontweight='bold')
ax.text(4.5, quic_y+0.28, "Same Connection ID throughout", ha='center', fontsize=9.5,
        color=quic_color, fontweight='bold')

# styling
ax.set_yticks([quic_y, tcp_y])
ax.set_yticklabels(["QUIC", "TCP"], fontsize=13, fontweight='bold')
ax.set_xticks(msg_idx)
ax.set_xticklabels([f"#{i}" for i in msg_idx], fontsize=10)
ax.set_xlabel("Heartbeat message sent by the ambulance device", fontsize=11, fontweight='bold')
ax.set_ylim(-0.8, 1.8)
ax.set_xlim(-0.6, 9.6)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.grid(axis='x', linestyle=':', alpha=0.4)

ax.set_title("Message-Level Timeline: TCP vs QUIC During Simulated Ambulance Handover",
             fontsize=13, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig("timeline_result.png", dpi=200, bbox_inches='tight', facecolor='white')
print("Done! Saved as timeline_result.png")
plt.show()