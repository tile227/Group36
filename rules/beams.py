def Beam_count(model):
    beam = model.by_type('IfcBeam')
    
    result = f"Beam: {len(beam)}"
    
    return result
