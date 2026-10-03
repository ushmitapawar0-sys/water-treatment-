import matplotlib.pyplot as plt
import os
import symbols
import router

def main():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_aspect('equal')
    
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    
    ax.set_xticks([x * 0.5 for x in range(0, 33)])
    ax.set_yticks([y * 0.5 for y in range(0, 25)])
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.5)
    
    router.clear_ports()
    
    # Place symbols
    # Tank
    tank_ports = symbols.draw_tank(ax, 2.0, 8.0)
    router.register_ports(tank_ports)
    ax.text(2.0, 6.0, "Tank", ha='center')
    
    # Pump
    pump_ports = symbols.draw_pump(ax, 7.0, 8.0)
    router.register_ports(pump_ports)
    ax.text(7.0, 6.8, "Pump", ha='center')
    
    # Control Valve
    cv_ports = symbols.draw_control_valve(ax, 12.0, 8.0)
    router.register_ports(cv_ports)
    ax.text(12.0, 6.8, "Control Valve", ha='center')
    
    # Connect Tank(right) to Pump(left)
    pts1 = router.route(tank_ports["right"], pump_ports["left"])
    router.draw_line(ax, pts1, style="process", add_arrow=True)
    
    # Connect Pump(right) to Control Valve(left)
    pts2 = router.route(pump_ports["right"], cv_ports["left"])
    router.draw_line(ax, pts2, style="process", add_arrow=True)
    
    # Test other line types with an Instrument
    ft_ports = symbols.draw_instrument_bubble(ax, 12.0, 10.5, "10-FIT-01", style="field")
    router.register_ports(ft_ports)
    
    plc_ports = symbols.draw_instrument_bubble(ax, 7.0, 10.5, "10-PLC-01", style="plc")
    router.register_ports(plc_ports)
    
    # Pneumatic
    pts3 = router.route(ft_ports["bottom"], cv_ports["top"])
    router.draw_line(ax, pts3, style="pneumatic")
    ax.text(12.2, 9.2, "Pneumatic", ha='left', fontsize=8)
    
    # Electrical
    pts4 = router.route(ft_ports["left"], plc_ports["right"])
    router.draw_line(ax, pts4, style="electrical")
    ax.text(9.5, 10.8, "Electrical", ha='center', fontsize=8)
    
    # Data link and Capillary examples on the side
    dummy_port1 = (1.0, 4.0)
    dummy_port2 = (5.0, 4.0)
    router.registered_ports.add(dummy_port1)
    router.registered_ports.add(dummy_port2)
    router.draw_line(ax, router.route(dummy_port1, dummy_port2), style="data")
    ax.text(3.0, 4.2, "Data Link", ha='center')
    
    dummy_port3 = (1.0, 3.0)
    dummy_port4 = (5.0, 3.0)
    router.registered_ports.add(dummy_port3)
    router.registered_ports.add(dummy_port4)
    router.draw_line(ax, router.route(dummy_port3, dummy_port4), style="capillary")
    ax.text(3.0, 3.2, "Capillary", ha='center')
    
    # Test error handling
    try:
        router.route((0.0, 0.0), (1.0, 1.0))
        print("Error: Router did not raise exception for unregistered ports.")
    except ValueError as e:
        print(f"Exception check passed: {e}")
        
    plt.title("Routing & Line Types Test", pad=20, fontsize=14)
    
    os.makedirs("output", exist_ok=True)
    out_path = "output/routing_test.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Saved {out_path}")
    
if __name__ == "__main__":
    main()
