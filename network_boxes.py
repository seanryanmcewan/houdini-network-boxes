class network_boxes:
    def __init__(self, parent=None):
        
        # INITIALIZE VARIABLES        
        self.obj_nodes = hou.node("/obj")
        self.nodes = hou.selectedNodes()
        
        # IF NOTHING IS SELECTED, RUN ON ALL NODES ON OBJECT LEVEL.
        if not self.nodes:
            self.nodes = self.obj_nodes.children()
            
    # FUNCTION TO CREATE NETWORK BOXES AROUND INPUT NODES, SETTING THE NODE AND NETWORK BOXES COLORS AS WELL
    def build_box(self, search_names, name, node_color, box_color, ignore_names=()): 
        
        # INITIALIZE VARIABLES
        found_nodes = []    
        
        # SEARCH INPUT NODES MATCHING SEARCH_NAMES, IGNORING ANY NODES MATCHING IGNORE_NAMES
        for node in self.nodes:
            if any(search_name in node.name().lower() for search_name in search_names):
                if not any(ignore_name in node.name().lower() for ignore_name in ignore_names):
                    found_nodes.append(node) 
                    
        # SEARCH FOR PREVIOUSLY CREATED NETWORK BOX
        box = self.obj_nodes.findNetworkBox(name+"_NETWORK_BOX")
        
        # RUN IF ANY NODES WERE FOUND MATCHING SEARCH_NAMES
        if found_nodes:   
            # DESTROY NETWORK BOX IF IT WAS PREVIOUSLY BUILT
            if box:
                box.destroy()  
                
            # LAYOUT NODES
            self.obj_nodes.layoutChildren(found_nodes)    
            
            # CREATE AND NAME NETWORK BOX
            box = self.obj_nodes.createNetworkBox(name+"_NETWORK_BOX")
            box.setComment(name) 
            
            # ADD FOUND NODES TO NETWORK BOX & SET COLOR
            for found_node in found_nodes:
                found_node.setColor(node_color)
                if found_node not in box.nodes():
                    box.addNode(found_node)
                
            # RESIZE NETWORK BOX AND SET COLOR
            box.fitAroundContents()
            box.setColor(box_color)    

    def run(self):
        
        # SET NODE AND NETWORK BOX COLORS, AND SPECIFY SEARCH NAMES AND IGNORE NAMES
        light_node_color = hou.Color(1,1,0.55)
        light_box_color = hou.Color(1,1,0.3)
        light_list = ("light",)

        camera_node_color = hou.Color(0,0,0)
        camera_box_color = hou.Color(0.05,0.05,0.05)
        camera_list = ("cam",)
        
        tracking_node_color = hou.Color(0.2,0,0.4)
        tracking_box_color = hou.Color(0.45,0,0.9)
        tracking_list = ("trk",)

        assets_node_color = hou.Color(0.38,0,0)
        assets_box_color = hou.Color(0.7,0,0)
        assets_list = ("_prop","_anim","_char","_cre","_env","_ele")

        fx_node_color = hou.Color(0,0.3,0.6)
        fx_box_color = hou.Color(0,0.7,0.7)
        fx_list = ("fx",)
        fx_ignore = ("render_fx",)

        render_node_color = hou.Color(0,0.3,0)
        render_box_color = hou.Color(0,0.7,0)
        render_list = ("render",)
        render_ignore = ("render_cam",)

        # CREATE NETWORK BOX FOR EACH TYPE
        self.build_box(light_list, "LIGHTS", light_node_color, light_box_color)
        self.build_box(camera_list, "CAMERAS", camera_node_color, camera_box_color)
        self.build_box(tracking_list, "TRACKING", tracking_node_color, tracking_box_color)
        self.build_box(assets_list, "ASSETS", assets_node_color, assets_box_color)
        self.build_box(fx_list, "FX", fx_node_color, fx_box_color, ignore_names=fx_ignore)
        self.build_box(render_list, "RENDER", render_node_color, render_box_color, ignore_names=render_ignore)

