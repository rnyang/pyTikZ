"""
PyTikZ

Ron Yang
2017
"""

# Class: TikZPicture
# Members:
# - points (coordinates)
# - objects

# Methods:
# - produce TeX code
# - add point (dot, no dot)
# - add line (normal, thick, dashed)
# - add label

import uuid

class TikZPicture:
    
    def __init__(self):
        self.coordinates = {}
        self.objects = []
        
    # Add named coordinates to picture
    def addCoordinate(self, x, y, name=None):
        if name == None:
            n = "c" + str(uuid.uuid1().int)[-5:]
        else:
            n = name
            
        self.coordinates[n] = (x,y)
        return n
        
    def getCoordinate(self, coordinate):
        if type(coordinate) == str:
            cname = coordinate
        else:
            cname = self.addCoordinate(coordinate[0], coordinate[1])
        return cname
        
    # Add a point with an optional label
    def addPoint(self, coordinate, label="", nodeOptions=[]):

        cname = self.getCoordinate(coordinate)
        
        p = {"kind":"point",
             "label":label,
             "coordinate":cname,
             "nodeOptions":nodeOptions}
        self.objects.append(p)
        
    # Add a label with no point
    def addLabel(self, coordinate, label, options=[]):
            
        cname = self.getCoordinate(coordinate)
            
        p = {"kind":"label",
             "label":label,
             "coordinate":cname,
             "options":options}
        self.objects.append(p)
        
        
    # Add a line with at least two points
    def addLine(self, coords, options=[], angles=[]):
        
        # For each coordinate, construct it if no name
        cs = []
        for c in coords:
            cs.append(self.getCoordinate(c))
        
        p = {"kind":"line",
             "coords":cs,
             "options":options,
             "angles":angles}
        self.objects.append(p)
        
    # Draw Axes (0,y) -> (0,0) -> (x,0)
    def addAx(self, x, y, xlabel="", ylabel="", options=[]):
        
        self.addCoordinate(0, y, "yax")
        self.addCoordinate(x, 0, "xax")
        
        p = {"kind":"axes",
             "x":"xax",
             "y":"yax",
             "xlabel":xlabel,
             "ylabel":ylabel}
        self.objects.append(p)
        
    def addPlot(self, formula, domain, options=[]):
        
        p = {"kind":"plot",
             "formula":formula,
             "domain":domain,
             "options":options}
        self.objects.append(p)
        
    # Output TikZ Code
    # do all this at end, so we build the TikZ snippet in
    # the right order because TeX is dumb
    def build(self):
        tikzString = ""
        tikzString += "\\begin{tikzpicture}\n"
        
        # Add coordinates
        for c in self.coordinates.keys():
            tikzString += "\\coordinate (%s) at (%f,%f);" \
                % (c, self.coordinates[c][0], self.coordinates[c][1]) + "\n"
        
        # Add objects
        for o in self.objects:
            
            if o['kind'] == "axes":
                tikzString += "\\draw[<->] (%s) node[above] {%s} -- (0,0) -- (%s) node[right]{%s}" \
                    % (o['y'], o['ylabel'], o['x'], o['xlabel']) + ";\n"
                    
            if o['kind'] == "point":
                tikzString += "\\filldraw [black] (%s) circle (2pt) node[" % (o['coordinate'])
                
                # Add node options
                for i, n in enumerate(o['nodeOptions']):
                    if i != 0:
                        tikzString += ", "
                    tikzString += n
                
                tikzString += "] {%s}" % (o['label']) + ";\n"
                    
            if o['kind'] == "label":
                tikzString += "\\node["
                
                for opt in o['options']:
                    tikzString += opt + ", "
                
                tikzString += "] at (%s) {%s}" % (o['coordinate'], o['label']) + ";\n"
                    
            if o['kind'] == "line":
                tikzString += "\\draw ["
                
                # Add options one by one
                
                for opt in o['options']:
                    tikzString += opt + ", "
                
                tikzString += "]  "
                
                # Add coordinates one by one
                
                # Add angles if smooth plot
                if 'smooth' in o['options']:
                    for i, c in enumerate(o['coords']):
                        if i != 0:
                            tikzString += " to [out=%f,in=%f] " % o['angles'][i-1]
                        tikzString += "(%s) " % (c)
                    
                # Add straight lines if not curved
                else:
                    for i, c in enumerate(o['coords']):
                        if i != 0:
                            tikzString += " -- "
                        tikzString += "(%s) " % (c)
                
                tikzString += ";\n"
                
            if o['kind'] == "plot":
                tikzString += "\\draw ["
                
                # Add options one by one
                
                for opt in o['options']:
                    tikzString += opt + ", "
                
                # Add domain, variable, and formula
                
                tikzString += "domain=%f:%f] plot (\\x, {%s});\n" % (o['domain'][0], o['domain'][1], o['formula'])
        
        tikzString += "\\end{tikzpicture}\n"
        
        return tikzString
