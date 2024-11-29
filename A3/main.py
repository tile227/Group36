import ifcopenshell
from bonsai.bim.ifc import IfcStore
from ifcopenshell.util.element import get_psets
import bpy
import mathutils


def calculate_facade_area(target_object, is_glass):
    """
    Calculate the facade area of a building object using raycasting.
    :param target_object: The building object to analyze.
    :param is_glass: Boolean indicating if the object is glass or not.
    :return: Total facade area for the object.
    """
    # Prepare for raycasting
    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated_object = target_object.evaluated_get(depsgraph)

    # Create a bounding box around the object
    min_coords = mathutils.Vector(target_object.bound_box[0])
    max_coords = mathutils.Vector(target_object.bound_box[6])

    # Exclude objects below Z = 0
    if max_coords.z < 0:
        return 0.0
    if min_coords.z < 0:
        min_coords.z = 0  # Clip to ground level

    bounding_center = (max_coords + min_coords) / 2

    # Define raycast origins: Include diagonals and sides
    raycast_origins = [
        mathutils.Vector((max_coords.x + 1, bounding_center.y, bounding_center.z)),  # Right
        mathutils.Vector((min_coords.x - 1, bounding_center.y, bounding_center.z)),  # Left
        mathutils.Vector((bounding_center.x, max_coords.y + 1, bounding_center.z)),  # Front
        mathutils.Vector((bounding_center.x, min_coords.y - 1, bounding_center.z)),  # Back
        mathutils.Vector((max_coords.x + 1, max_coords.y + 1, bounding_center.z)),  # Front-right diagonal
        mathutils.Vector((min_coords.x - 1, max_coords.y + 1, bounding_center.z)),  # Front-left diagonal
        mathutils.Vector((max_coords.x + 1, min_coords.y - 1, bounding_center.z)),  # Back-right diagonal
        mathutils.Vector((min_coords.x - 1, min_coords.y - 1, bounding_center.z)),  # Back-left diagonal
    ]

    # Initialize total area
    total_area = 0.0
    processed_faces = set()

    # Raycast from each origin towards the object
    for origin in raycast_origins:
        for face in target_object.data.polygons:
            if face.index in processed_faces:
                continue  # Skip faces already processed

            # Transform face center and normal to world space
            face_center_world = target_object.matrix_world @ face.center
            face_normal_world = target_object.matrix_world.to_3x3() @ face.normal

            # Exclude faces below Z = 0
            if face_center_world.z < 0:
                continue

            # Exclude roof:
            if face_normal_world.z > 0.5:
                continue  # Skip upward-facing faces (roof)

            # Exclude basement:
            if face_normal_world.z < -0.5:
                continue  # Skip downward-facing faces (basement or bottom surfaces)

            # Include only vertical faces:
            if abs(face_normal_world.z) > 0.5:
                continue  # Exclude non-vertical faces

            # Compute ray direction
            ray_direction = (face_center_world - origin).normalized()

            # Cast ray
            result, location, normal, index = evaluated_object.ray_cast(origin, ray_direction)

            # If the ray hits, add the face area
            if result and index == face.index:
                total_area += face.area
                processed_faces.add(face.index)  # Mark face as processed

    return total_area


def is_glass_object(target_object):
    """
    Determine if the object is made of glass based on material names.
    :param target_object: The object to check.
    :return: True if the object is glass, False otherwise.
    """
    if not target_object.data.materials:
        return False
    for material in target_object.data.materials:
        if material and "glass" in material.name.lower():
            return True
    return False


def process_scene():
    """
    Process all objects in the scene to calculate the total facade area for glass and non-glass objects.
    """
    # Initialize total areas
    total_glass_area = 0.0
    total_non_glass_area = 0.0
    processed_objects = set()

    # Loop through all objects in the scene
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and obj.name not in processed_objects:  # Process each object only once
            is_glass = is_glass_object(obj)
            facade_area = calculate_facade_area(obj, is_glass)
            if facade_area > 0:
                if is_glass:
                    total_glass_area += facade_area
                    print(f"Glass facade area for {obj.name}: {facade_area:.2f} square units")
                else:
                    total_non_glass_area += facade_area
                    print(f"Non-glass facade area for {obj.name}: {facade_area:.2f} square units")
            processed_objects.add(obj.name)  # Mark object as processed

    # Calculate total facade area
    total_facade_area = total_glass_area + total_non_glass_area

    # Display results
    print(f"\nTotal facade area of glass objects: {total_glass_area:.2f} square units")
    print(f"Total facade area: {total_facade_area:.2f} square units")

    # Calculate and display the window-to-wall ratio
    if total_facade_area > 0:
        window_to_wall_ratio = (total_glass_area / total_facade_area) * 100
        print(f"Window-to-wall ratio = {window_to_wall_ratio:.2f}%")
    else:
        print("Window-to-wall ratio = Undefined (no facade area)")


# Execute the process
if __name__ == "__main__":
    process_scene()
()
