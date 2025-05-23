import bpy
from bpy.app.handlers import persistent

# Store the last known camera position
last_camera_position = None

@persistent
def update_meshes_on_camera_move(scene):
    global last_camera_position
    
    # Get the dicing camera
    dicing_camera = bpy.data.scenes["Scene"].cycles.dicing_camera
    
    if dicing_camera is None:
        return
    
    # Get current camera position
    current_position = dicing_camera.location.copy()
    
    # Check if camera position has changed
    if last_camera_position is None or current_position != last_camera_position:
        # Update all mesh objects
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.data.update()
        
        # Store the new position
        last_camera_position = current_position
        print(f"Camera moved to {current_position}, updated meshes")

# Register the handler
def register():
    bpy.app.handlers.depsgraph_update_post.append(update_meshes_on_camera_move)

def unregister():
    if update_meshes_on_camera_move in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(update_meshes_on_camera_move)

if __name__ == "__main__":
    register()