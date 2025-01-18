import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='DECT Class Diagram')
dot.attr(rankdir='TB', size='8,8')

# Add classes
dot.node('DECT', 'DECT')
dot.node('BaseCommand', 'BaseCommand')
dot.node('VariableSizeCommand', 'VariableSizeCommand')
dot.node('InfoElement', 'InfoElement')
dot.node('ApiCodecInfoType', 'ApiCodecInfoType')
dot.node('ApiCodecListType', 'ApiCodecListType')
dot.node('ApiCallingPartyNumber', 'ApiCallingPartyNumber')
dot.node('ApiCallingPartyName', 'ApiCallingPartyName')

# Add relationships
dot.edge('VariableSizeCommand', 'BaseCommand', 'inherits')
dot.edge('ApiCodecListType', 'InfoElement', 'inherits')
dot.edge('ApiCallingPartyNumber', 'InfoElement', 'inherits')
dot.edge('ApiCallingPartyName', 'InfoElement', 'inherits')

# Add associations
dot.edge('DECT', 'BaseCommand', 'uses')
dot.edge('DECT', 'VariableSizeCommand', 'uses')
dot.edge('DECT', 'InfoElement', 'uses')
dot.edge('ApiCodecListType', 'ApiCodecInfoType', 'contains')

# Generate the diagram
dot.render('dect_class_diagram', format='png', cleanup=True)
print("Class diagram generated as 'dect_class_diagram.png'")
