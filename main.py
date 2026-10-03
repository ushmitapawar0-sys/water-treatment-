import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import symbols
import router
from tagging import TagManager
from validator import Validator

def main():
    tm = TagManager()
    router.clear_ports()
    items = []
    
    fig, ax = plt.subplots(figsize=(20, 12))
    ax.set_aspect('equal')
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 16)
    
    ax.set_xticks([x * 0.5 for x in range(0, 53)])
    ax.set_yticks([y * 0.5 for y in range(0, 33)])
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.3)
    
    # Generate Tags
    tk1 = tm.add_tag("TK-101", "equipment")
    gv1 = tm.add_tag("GV-101", "equipment")
    p1 = tm.add_tag("P-101A/B", "equipment")
    cv1 = tm.add_tag("CKV-101", "equipment")
    fl1 = tm.add_tag("FL-101", "equipment")
    cl1 = tm.add_tag("CL-101", "equipment")
    fv1 = tm.add_tag("FV-101", "equipment")
    tk2 = tm.add_tag("TK-102", "equipment")
    
    items.extend([
        {"tag": tk1, "type": "Tank"},
        {"tag": gv1, "type": "GateValve"},
        {"tag": p1, "type": "Pump"},
        {"tag": cv1, "type": "CheckValve"},
        {"tag": fl1, "type": "Filter"},
        {"tag": cl1, "type": "Dosing"},
        {"tag": fv1, "type": "ControlValve"},
        {"tag": tk2, "type": "Tank"}
    ])
    
    # Place Equipment
    p_tk1 = symbols.draw_tank(ax, 2.0, 6.0)
    router.register_ports(p_tk1)
    ax.text(2.0, 4.0, tk1, ha='center', weight='bold')
    
    p_gv1 = symbols.draw_gate_valve(ax, 5.0, 6.0)
    router.register_ports(p_gv1)
    ax.text(5.0, 5.2, gv1, ha='center', weight='bold')
    
    p_p1 = symbols.draw_pump(ax, 7.5, 6.0)
    router.register_ports(p_p1)
    ax.text(7.5, 4.8, p1, ha='center', weight='bold')
    
    p_cv1 = symbols.draw_check_valve(ax, 10.0, 6.0)
    router.register_ports(p_cv1)
    ax.text(10.0, 5.2, cv1, ha='center', weight='bold')
    
    p_fl1 = symbols.draw_filter(ax, 13.0, 6.0)
    router.register_ports(p_fl1)
    ax.text(13.0, 4.3, fl1, ha='center', weight='bold')
    
    p_cl1 = symbols.draw_chlorine_dosing(ax, 17.0, 6.0)
    router.register_ports(p_cl1)
    ax.text(17.0, 4.8, cl1, ha='center', weight='bold')
    
    p_fv1 = symbols.draw_control_valve(ax, 21.0, 6.0)
    router.register_ports(p_fv1)
    ax.text(21.0, 5.2, fv1, ha='center', weight='bold')
    
    p_tk2 = symbols.draw_tank(ax, 24.0, 6.0)
    router.register_ports(p_tk2)
    ax.text(24.0, 4.0, tk2, ha='center', weight='bold')
    
    # Route main process line
    router.draw_line(ax, router.route(p_tk1["right"], p_gv1["left"]), style="process", add_arrow=True)
    router.draw_line(ax, router.route(p_gv1["right"], p_p1["left"]), style="process", add_arrow=True)
    router.draw_line(ax, router.route(p_p1["right"], p_cv1["left"]), style="process", add_arrow=True)
    router.draw_line(ax, router.route(p_cv1["right"], p_fl1["left"]), style="process", add_arrow=True)
    router.draw_line(ax, router.route(p_fl1["right"], p_cl1["left"]), style="process", add_arrow=True)
    
    dummy_flow_port = (19.0, 6.0)
    router.registered_ports.add(dummy_flow_port)
    
    router.draw_line(ax, router.route(p_cl1["right"], dummy_flow_port), style="process")
    router.draw_line(ax, router.route(dummy_flow_port, p_fv1["left"]), style="process", add_arrow=True)
    router.draw_line(ax, router.route(p_fv1["right"], p_tk2["left"]), style="process", add_arrow=True)
    
    # TK-101 Level Loop
    lit = tm.add_tag("10-LIT-01")
    lic = tm.add_tag("10-LIC-01")
    
    p_lit = symbols.draw_instrument_bubble(ax, 2.0, 9.0, lit, style="field")
    router.register_ports(p_lit)
    p_lic = symbols.draw_instrument_bubble(ax, 5.0, 9.0, lic, style="control_room")
    router.register_ports(p_lic)
    
    router.draw_line(ax, router.route(p_lit["bottom"], p_tk1["top"]), style="process")
    router.draw_line(ax, router.route(p_lit["right"], p_lic["left"]), style="electrical")
    router.draw_line(ax, router.route(p_lic["right"], p_p1["top"]), style="electrical")
    
    tm.link_loop("10", lit, lic, p1)
    
    # FV-101 Flow Loop
    fit = tm.add_tag("20-FIT-01")
    fic = tm.add_tag("20-FIC-01")
    
    p_fit = symbols.draw_instrument_bubble(ax, 19.0, 9.0, fit, style="field")
    router.register_ports(p_fit)
    p_fic = symbols.draw_instrument_bubble(ax, 21.0, 9.0, fic, style="control_room")
    router.register_ports(p_fic)
    
    router.draw_line(ax, router.route(p_fit["bottom"], dummy_flow_port), style="process")
    router.draw_line(ax, router.route(p_fit["right"], p_fic["left"]), style="electrical")
    router.draw_line(ax, router.route(p_fic["bottom"], p_fv1["top"]), style="electrical")
    
    tm.link_loop("20", fit, fic, fv1)
    
    items.extend([{"tag": lit}, {"tag": lic}, {"tag": fit}, {"tag": fic}])
    
    # Title Block
    rect = patches.Rectangle((20, 0.5), 5.5, 2.5, fill=True, color='white', ec='black', lw=2.0, zorder=10)
    ax.add_patch(rect)
    ax.text(22.75, 2.5, "WATER TREATMENT PLANT", ha='center', va='center', weight='bold', fontsize=12, zorder=11)
    ax.text(22.75, 1.8, "P&ID DIAGRAM", ha='center', va='center', fontsize=11, zorder=11)
    ax.text(22.75, 1.1, "Project: DecodeLabs Project 4", ha='center', va='center', fontsize=9, zorder=11)
    ax.text(22.75, 0.7, "Drawn by: Antigravity AI", ha='center', va='center', fontsize=9, zorder=11)
    
    # Legend
    rect = patches.Rectangle((20, 11), 5.5, 4.5, fill=True, color='white', ec='black', lw=1.5, zorder=10)
    ax.add_patch(rect)
    ax.text(22.75, 15.0, "LEGEND", ha='center', va='center', weight='bold', fontsize=10, zorder=11)
    ax.plot([20.5, 22.0], [14.0, 14.0], linestyle='-', color='black', linewidth=2.0)
    ax.text(22.5, 14.0, "Process Line", va='center', fontsize=8)
    ax.plot([20.5, 22.0], [13.2, 13.2], linestyle='--', color='black', linewidth=1.2)
    ax.text(22.5, 13.2, "Electrical", va='center', fontsize=8)
    router.draw_line(ax, [(20.5, 12.4), (22.0, 12.4)], style='pneumatic')
    ax.text(22.5, 12.4, "Pneumatic", va='center', fontsize=8)
    router.draw_line(ax, [(20.5, 11.6), (22.0, 11.6)], style='data')
    ax.text(22.5, 11.6, "Data Link", va='center', fontsize=8)
    
    # Tag Table
    rect = patches.Rectangle((0.5, 11), 6.5, 4.5, fill=True, color='white', ec='black', lw=1.5, zorder=10)
    ax.add_patch(rect)
    ax.text(3.75, 15.0, "EQUIPMENT TAGS", ha='center', va='center', weight='bold', fontsize=10, zorder=11)
    tags_info = [
        ("TK-101", "Raw Water Tank"),
        ("GV-101", "Gate Valve"),
        ("P-101A/B", "Transfer Pumps"),
        ("CKV-101", "Check Valve"),
        ("FL-101", "Sand Filter"),
        ("CL-101", "Chlorine Dosing"),
        ("TK-102", "Treated Water Tank"),
        ("FV-101", "Flow Control Valve")
    ]
    y_pos = 14.2
    for tag, desc in tags_info:
        ax.text(1.0, y_pos, tag, weight='bold', va='center', fontsize=8, zorder=11)
        ax.text(2.5, y_pos, desc, va='center', fontsize=8, zorder=11)
        y_pos -= 0.4
        
    os.makedirs("output", exist_ok=True)
    plt.savefig("output/water_treatment_pid.png", dpi=300, bbox_inches='tight')
    plt.savefig("output/water_treatment_pid.pdf", bbox_inches='tight')
    print("Saved output/water_treatment_pid.png and .pdf")
    
    # Validate
    val = Validator(tm, router, items)
    val.validate()

if __name__ == "__main__":
    main()
