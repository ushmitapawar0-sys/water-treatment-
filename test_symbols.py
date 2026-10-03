import matplotlib.pyplot as plt
import os
import symbols

def main():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_aspect('equal')
    
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    
    ax.set_xticks([x * 0.5 for x in range(0, 33)])
    ax.set_yticks([y * 0.5 for y in range(0, 25)])
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    
    syms = [
        ("Tank", symbols.draw_tank, 2.0, 9.0),
        ("Pump", symbols.draw_pump, 6.0, 9.0),
        ("Gate Valve", symbols.draw_gate_valve, 10.0, 10.0),
        ("Globe Valve", symbols.draw_globe_valve, 10.0, 8.0),
        ("Check Valve", symbols.draw_check_valve, 14.0, 10.0),
        ("Control Valve", symbols.draw_control_valve, 14.0, 8.0),
        ("Field Inst.", lambda ax, x, y: symbols.draw_instrument_bubble(ax, x, y, tag="10-LIT-01", style="field"), 2.0, 5.0),
        ("Control Room Inst.", lambda ax, x, y: symbols.draw_instrument_bubble(ax, x, y, tag="10-LIC-01", style="control_room"), 6.0, 5.0),
        ("PLC Inst.", lambda ax, x, y: symbols.draw_instrument_bubble(ax, x, y, tag="10-PLC-01", style="plc"), 10.0, 5.0),
        ("Filter", symbols.draw_filter, 3.0, 1.5),
        ("Cl2 Dosing", symbols.draw_chlorine_dosing, 9.0, 1.5)
    ]
    
    for name, func, x, y in syms:
        ports = func(ax, x, y)
        ax.text(x, y - 1.8, name, ha='center', va='top', fontsize=10, color='blue', weight='bold')
        
        for port_name, (px, py) in ports.items():
            ax.plot(px, py, 'ro', markersize=4)
            
    plt.title("P&ID Symbol Library Test", pad=20, fontsize=14)
    
    os.makedirs("output", exist_ok=True)
    out_path = "output/symbol_library.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Saved {out_path}")
    
if __name__ == "__main__":
    main()
