import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

registered_ports = set()

def register_ports(ports_dict):
    """Add ports from a symbol's return dictionary to the router registry."""
    for name, coord in ports_dict.items():
        registered_ports.add(coord)

def clear_ports():
    """Clear all registered ports."""
    registered_ports.clear()

def snap(val):
    """Snap coordinate to nearest 0.5 units."""
    return round(val * 2) / 2

def route(port_a, port_b):
    """
    Returns orthogonal routing points from port_a to port_b.
    Raises ValueError if either port is not registered.
    """
    if port_a not in registered_ports:
        raise ValueError(f"Start point {port_a} is not on a registered symbol port.")
    if port_b not in registered_ports:
        raise ValueError(f"End point {port_b} is not on a registered symbol port.")
        
    x1, y1 = port_a
    x2, y2 = port_b
    
    # Direct horizontal or vertical connection
    if x1 == x2 or y1 == y2:
        return [(x1, y1), (x2, y2)]
        
    # Basic orthogonal routing: horizontal to midpoint, then vertical, then horizontal
    mid_x = snap((x1 + x2) / 2)
    return [(x1, y1), (mid_x, y1), (mid_x, y2), (x2, y2)]

def add_marks(ax, points, mark):
    """Add repeating marks along the route segments."""
    for i in range(len(points)-1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        
        length = np.hypot(x2 - x1, y2 - y1)
        if length <= 0.5:
            continue
            
        num_marks = int(length / 0.75)
        if num_marks == 0:
            continue
            
        for j in range(1, num_marks + 1):
            t = j / (num_marks + 1)
            mx = x1 + t * (x2 - x1)
            my = y1 + t * (y2 - y1)
            
            if mark == 'o':
                circle = patches.Circle((mx, my), 0.08, fill=True, color='white', ec='black', zorder=5)
                ax.add_patch(circle)
            elif mark == 'x':
                ax.text(mx, my, 'x', ha='center', va='center', fontsize=9, weight='bold', zorder=5)
            elif mark == '//':
                dx = x2 - x1
                dy = y2 - y1
                angle = np.degrees(np.arctan2(dy, dx))
                ax.text(mx, my, '//', ha='center', va='center', fontsize=8, rotation=angle, zorder=5)

def add_flow_arrow(ax, points):
    """Add an arrowhead at the midpoint of the longest segment."""
    if len(points) < 2:
        return
    
    max_len = -1
    best_segment = None
    for i in range(len(points)-1):
        p1 = points[i]
        p2 = points[i+1]
        l = np.hypot(p2[0] - p1[0], p2[1] - p1[1])
        if l > max_len:
            max_len = l
            best_segment = (p1, p2)
            
    if best_segment and max_len > 0:
        p1, p2 = best_segment
        mx, my = (p1[0] + p2[0])/2, (p1[1] + p2[1])/2
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        
        length = np.hypot(dx, dy)
        dx, dy = dx/length, dy/length
        
        arrow_size = 0.25
        angle = np.arctan2(dy, dx)
        pt1 = (mx + arrow_size * np.cos(angle), my + arrow_size * np.sin(angle))
        pt2 = (mx + arrow_size * np.cos(angle + 2.5), my + arrow_size * np.sin(angle + 2.5))
        pt3 = (mx + arrow_size * np.cos(angle - 2.5), my + arrow_size * np.sin(angle - 2.5))
        
        arrow = patches.Polygon([pt1, pt2, pt3], fill=True, color='black', zorder=6)
        ax.add_patch(arrow)

def draw_line(ax, points, style="process", add_arrow=False):
    """Draw a routed line with a specific ISA 5.1 style."""
    xs, ys = zip(*points)
    
    if style == "process":
        ax.plot(xs, ys, linestyle='-', color='black', linewidth=2.0, zorder=2)
        if add_arrow:
            add_flow_arrow(ax, points)
    elif style == "electrical":
        ax.plot(xs, ys, linestyle='--', color='black', linewidth=1.2, zorder=2)
    elif style == "pneumatic":
        ax.plot(xs, ys, linestyle='-', color='black', linewidth=1.2, zorder=2)
        add_marks(ax, points, mark='//')
    elif style == "data":
        ax.plot(xs, ys, linestyle='-', color='black', linewidth=1.2, zorder=2)
        add_marks(ax, points, mark='o')
    elif style == "capillary":
        ax.plot(xs, ys, linestyle='-', color='black', linewidth=1.2, zorder=2)
        add_marks(ax, points, mark='x')
    else:
        # Default fallback
        ax.plot(xs, ys, linestyle='-', color='black', linewidth=1.0, zorder=2)
