import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines

def snap(val):
    """Snap coordinate to nearest 0.5 units."""
    return round(val * 2) / 2

def draw_tank(ax, x, y, width=1.5, height=3.0):
    x, y, width, height = snap(x), snap(y), snap(width), snap(height)
    
    rect = patches.Rectangle((x - width/2, y - height/2), width, height, fill=False, lw=1.5)
    ax.add_patch(rect)
    
    return {
        "top": (x, y + height/2),
        "bottom": (x, y - height/2),
        "left": (x - width/2, y),
        "right": (x + width/2, y)
    }

def draw_pump(ax, x, y, radius=0.75):
    x, y, radius = snap(x), snap(y), snap(radius)
    
    circle = patches.Circle((x, y), radius, fill=False, lw=1.5)
    ax.add_patch(circle)
    
    tri = patches.Polygon([[x - radius*0.4, y + radius*0.4],
                           [x - radius*0.4, y - radius*0.4],
                           [x + radius*0.6, y]], fill=False, lw=1.5)
    ax.add_patch(tri)
    
    base = lines.Line2D([x - radius*0.5, x + radius*0.5], [y - radius, y - radius], color='black', lw=1.5)
    ax.add_line(base)
    
    return {
        "top": (x, y + radius),
        "bottom": (x, y - radius),
        "left": (x - radius, y),
        "right": (x + radius, y)
    }

def draw_valve_body(ax, x, y, width=1.0, height=0.5):
    left_tri = patches.Polygon([[x - width/2, y + height/2],
                                [x - width/2, y - height/2],
                                [x, y]], fill=False, lw=1.5)
    right_tri = patches.Polygon([[x + width/2, y + height/2],
                                 [x + width/2, y - height/2],
                                 [x, y]], fill=False, lw=1.5)
    ax.add_patch(left_tri)
    ax.add_patch(right_tri)

def draw_gate_valve(ax, x, y, width=1.0, height=0.5):
    x, y, width = snap(x), snap(y), snap(width)
    draw_valve_body(ax, x, y, width, height)
    return {
        "top": (x, y + height/2),
        "bottom": (x, y - height/2),
        "left": (x - width/2, y),
        "right": (x + width/2, y)
    }

def draw_globe_valve(ax, x, y, width=1.0, height=0.5):
    x, y, width = snap(x), snap(y), snap(width)
    draw_valve_body(ax, x, y, width, height)
    
    dot = patches.Circle((x, y), height*0.3, fill=True, color='black')
    ax.add_patch(dot)
    
    return {
        "top": (x, y + height/2),
        "bottom": (x, y - height/2),
        "left": (x - width/2, y),
        "right": (x + width/2, y)
    }

def draw_check_valve(ax, x, y, width=1.0, height=0.5):
    x, y, width = snap(x), snap(y), snap(width)
    draw_valve_body(ax, x, y, width, height)
    
    line = lines.Line2D([x, x - width*0.3], [y, y + height*0.6], color='black', lw=1.5)
    ax.add_line(line)
    
    return {
        "top": (x, y + height/2),
        "bottom": (x, y - height/2),
        "left": (x - width/2, y),
        "right": (x + width/2, y)
    }

def draw_control_valve(ax, x, y, width=1.0, height=0.5):
    x, y, width = snap(x), snap(y), snap(width)
    draw_valve_body(ax, x, y, width, height)
    
    stem_len = 0.5
    stem = lines.Line2D([x, x], [y, y + stem_len], color='black', lw=1.5)
    ax.add_line(stem)
    
    cap_width = 0.8
    cap = patches.Arc((x, y + stem_len), cap_width, cap_width*0.5, theta1=0, theta2=180, lw=1.5)
    ax.add_patch(cap)
    cap_line = lines.Line2D([x - cap_width/2, x + cap_width/2], [y + stem_len, y + stem_len], color='black', lw=1.5)
    ax.add_line(cap_line)
    
    return {
        "top": (x, y + stem_len + cap_width*0.25),
        "bottom": (x, y - height/2),
        "left": (x - width/2, y),
        "right": (x + width/2, y)
    }

def draw_instrument_bubble(ax, x, y, tag, style="field"):
    x, y = snap(x), snap(y)
    radius = 0.5
    
    parts = tag.split('-')
    if len(parts) == 3:
        top_text = parts[1]
        bottom_text = f"{parts[0]}-{parts[2]}"
    else:
        top_text = tag
        bottom_text = ""
        
    if style == "plc":
        size = 1.0
        rect = patches.Rectangle((x - size/2, y - size/2), size, size, fill=True, color='white', ec='black', lw=1.5, zorder=3)
        ax.add_patch(rect)
        
        diamond = patches.Polygon([
            [x, y + size/2], [x + size/2, y], [x, y - size/2], [x - size/2, y]
        ], fill=False, ec='black', lw=1.5, zorder=4)
        ax.add_patch(diamond)
        
        if bottom_text:
            ax.text(x, y + 0.15, top_text, ha='center', va='center', fontsize=8, zorder=5)
            ax.text(x, y - 0.2, bottom_text, ha='center', va='center', fontsize=7, zorder=5)
        else:
            ax.text(x, y, top_text, ha='center', va='center', fontsize=8, zorder=5)
            
        return {
            "top": (x, y + size/2),
            "bottom": (x, y - size/2),
            "left": (x - size/2, y),
            "right": (x + size/2, y)
        }
    else:
        circle = patches.Circle((x, y), radius, fill=True, color='white', ec='black', lw=1.5, zorder=3)
        ax.add_patch(circle)
        
        if style == "control_room":
            line = lines.Line2D([x - radius, x + radius], [y, y], color='black', lw=1.5, zorder=4)
            ax.add_line(line)
            ax.text(x, y + radius*0.3, top_text, ha='center', va='center', fontsize=8, zorder=5)
            if bottom_text:
                ax.text(x, y - radius*0.3, bottom_text, ha='center', va='center', fontsize=8, zorder=5)
        else:
            if bottom_text:
                ax.text(x, y + radius*0.2, top_text, ha='center', va='center', fontsize=8, zorder=5)
                ax.text(x, y - radius*0.25, bottom_text, ha='center', va='center', fontsize=7, zorder=5)
            else:
                ax.text(x, y, top_text, ha='center', va='center', fontsize=9, zorder=5)
            
        return {
            "top": (x, y + radius),
            "bottom": (x, y - radius),
            "left": (x - radius, y),
            "right": (x + radius, y)
        }

def draw_box_unit(ax, x, y, width, height, label):
    x, y, width, height = snap(x), snap(y), snap(width), snap(height)
    
    rect = patches.Rectangle((x - width/2, y - height/2), width, height, fill=False, lw=1.5)
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center', fontsize=10, weight='bold')
    
    return {
        "top": (x, y + height/2),
        "bottom": (x, y - height/2),
        "left": (x - width/2, y),
        "right": (x + width/2, y)
    }

def draw_filter(ax, x, y):
    return draw_box_unit(ax, x, y, width=2.0, height=2.5, label="FILTER")

def draw_chlorine_dosing(ax, x, y):
    return draw_box_unit(ax, x, y, width=2.0, height=1.5, label="Cl2\nDOSING")
