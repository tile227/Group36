
# **Facade Area Analyzer**

*Group 36*
Katharina Gertrud Voll | s242086
Tilemachos Tsontakis | s242775
Focus Area: LCA


## **Overview**
This script calculates the window-to-wall ratio by analyzing 3D building façades in Blender, distinguishing glass from non-glass surfaces. It automates accurate calculations, providing planners with critical insights to optimize design, energy efficiency, and sustainability in building models.


## **Summary**
This script is a tool for analyzing the façade of 3D building models in Blender, focusing on calculating the window-to-wall ratio. It identifies and measures façade surfaces, distinguishing between glass and non-glass materials, while excluding irrelevant parts like roofs, basements, or non-vertical faces. 
The code creates significant value by automating the analysis of complex 3D models and offering critical insights for architects and designers. The window-to-wall ratio is an essential metric for evaluating a building’s thermal performance, energy efficiency, and natural lighting. With this tool, users can optimize their designs to balance aesthetics, functionality, and sustainability. It supports data-driven design iteration, enabling quick testing of material configurations and façade designs. Additionally, the script’s outputs can be directly applied to simulations such as thermal or energy modeling, making it indispensable for modern, sustainable architectural practices.


## **Tutorial** 

How to get started: 

### **Step 1: Install Blender 4.3.0**
1.	Visit the official Blender website: Blender Download.
2.	Download version 4.3.0, which is compatible with the Bonsai add-on.
3.	Install Blender by following the instructions provided on the website or in the installer.

### **Step 2: Install the Bonsai Add-on**
1.	Visit the Bonsai add-on website: Bonsai Add-on.
2.	Download the latest version of the add-on as a ZIP file.
3.	Open Blender and navigate to Edit > Preferences > Add-ons.
4.	Click Install and select the downloaded ZIP file.
5.	Enable the Bonsai add-on by ticking the checkbox in the add-on list.



*Once you have done these steps, you can follow the Tutorial.*



VIDEO 


### **Step 1: How to Open Blender**
- For macOS:
To open Blender on macOS, you first need to launch it through the terminal. Press “Command + Space Bar”, type “Terminal”, and press Enter. Navigate to the Blender installation path, which may vary but is typically: 
*/Applications/Blender.app/Contents/MacOS/Blender*

- For Windows:
Simply open Blender as you normally would by clicking its icon.

### **Step 2: How to Open the IFC**
- In Blender, click on File > Open IFC Project and select the IFC file you want to load.

### **Step 3: Scripting**
- Navigate to the Scripting tab, which can be found in the top menu bar.
- Here, you have two options:
1.	Click New to manually enter or paste the Python code.
2.	Click Open to upload an existing Python file from your computer.

### **Step 4: Running the Script**
- Run the script by clicking the triangle icon at the top of the Scripting window.
- On a MacBook, the result of the script will be displayed in the terminal.






## **Python-Code**

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



## **Description of the code**


This script is designed to analyze a 3D scene in Blender and calculate the façade area of objects within the scene, distinguishing between surfaces made of glass and those made of other materials. The calculation involves using raycasting to identify vertical, exterior surfaces while excluding irrelevant areas such as roofs, basements, and non-vertical faces. Additionally, the script calculates the proportion of glass façade area relative to the total façade area, known as the window-to-wall ratio.
The main functionality of the script is implemented through three key components: determining if an object is made of glass, calculating the façade area of individual objects, and processing the entire scene to print the results.
The function calculate_facade_area is responsible for determining the façade area of a given object. To achieve this, it first evaluates the object’s geometry using Blender, ensuring the geometry reflects any applied modifiers. A bounding box is then created to determine the spatial extent of the object, and any part of the object below ground level (z<0) is excluded from the calculations. For objects that partially intersect the ground, only the portion above ground is considered.
To identify relevant faces for the façade calculation, raycasting is employed. Rays are cast from various positions around the object, including along its sides and diagonals, 8 sides in total, toward the object’s surfaces. Each face of the object is analyzed based on its orientation and position. Specifically, the script excludes faces below ground level, roofs (faces with normals primarily pointing upward), and basement or bottom surfaces (faces with normals primarily pointing downward). Non-vertical faces, where the face’s normal has a significant vertical component, are also excluded. For eligible faces, the script casts a ray toward the face center. If the ray intersects the face, its area is added to the total façade area. The rays always stop at the first objects they intersect with. To avoid redundant calculations, faces that have already been processed are skipped. The total façade area for the object is then returned.
The is_glass_object function determines whether a given object is made of glass by analyzing its materials. If the object has no materials, it is classified as non-glass. Otherwise, each material is checked to see if its name contains the word “glass” (case-insensitive). If this criterion is met, the object is considered to be made of glass.
Finally, the process_scene function iterates through all objects in the Blender scene to calculate the total façade areas for both glass and non-glass objects. For each object, the function checks if it is a mesh and processes it only once to prevent duplicate calculations. Using the is_glass_object function, the script classifies the object as glass or non-glass. It then calculates the façade area of the object using the calculate_facade_area function and accumulates the results in separate totals for glass and non-glass areas. The total façade area is also calculated as the sum of these two categories.
After processing all objects, the script calculates the window-to-wall ratio, which is the proportion of the total glass façade area relative to the total façade area, expressed as a percentage. This ratio provides a measure of how much of the building’s façade is made of glass. The results, including the façade areas for individual objects, the total areas, and the window-to-wall ratio, are displayed in the console.
In summary, this script provides a comprehensive method for analyzing building façades in Blender, identifying relevant surfaces through raycasting and material analysis, and computing a range of metrics that are useful for evaluating the design and material composition of the structure.


