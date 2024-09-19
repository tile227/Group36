def Wall_count(model):
    wall = model.by_type('Ifcwall')
    
    result = f"Wall: {len(wall)}"
    
    return result
