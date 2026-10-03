import re

class TagManager:
    def __init__(self):
        self.tags = set()
        self.loops = {} # loop_id -> {"sensor": ..., "controller": ..., "valve": ...}
        
        # Regex for instrument: XX-YYY-ZZ (e.g. 10-LIT-01)
        # XX: 2 digits (loop number)
        # YYY: letters (starting with P,T,L,F)
        # ZZ: 2 digits (sequence)
        self.inst_regex = re.compile(r'^\d{2}-[PTLF][A-Z]{1,3}-\d{2}$')
        
        # Regex for equipment: TK-101, P-101A, P-101A/B, FV-101
        self.equip_regex = re.compile(r'^[A-Z]{1,3}-\d{3}(?:[A-Z](?:/[A-Z])?)?$')

    def validate_tag(self, tag, tag_type="instrument"):
        if tag_type == "instrument":
            return bool(self.inst_regex.match(tag))
        elif tag_type == "equipment":
            return bool(self.equip_regex.match(tag))
        return False

    def add_tag(self, tag, tag_type="instrument"):
        if not self.validate_tag(tag, tag_type):
            raise ValueError(f"Invalid {tag_type} tag format: {tag}")
        if tag in self.tags:
            raise ValueError(f"Duplicate tag: {tag}")
        self.tags.add(tag)
        return tag

    def generate_tag(self, tag_type, letters, loop="10"):
        """Auto-generates a unique tag."""
        if tag_type == "instrument":
            seq = 1
            while True:
                tag = f"{loop}-{letters}-{seq:02d}"
                if tag not in self.tags:
                    self.tags.add(tag)
                    return tag
                seq += 1
        elif tag_type == "equipment":
            seq = 101
            while True:
                tag = f"{letters}-{seq}"
                if tag not in self.tags:
                    self.tags.add(tag)
                    return tag
                seq += 1

    def link_loop(self, loop_id, sensor, controller, valve):
        """Links each instrument to its loop."""
        for t in [sensor, controller, valve]:
            if t and t not in self.tags:
                raise ValueError(f"Tag {t} not found in registered tags.")
        self.loops[loop_id] = {
            "sensor": sensor,
            "controller": controller,
            "valve": valve
        }
