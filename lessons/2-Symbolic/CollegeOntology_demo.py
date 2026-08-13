"""
University Ontology Demo
========================
This script demonstrates how to load the UniversityOntology.ttl file,
run OWL-RL inference, and query it with SPARQL — following the same
pattern as the FamilyOntology.ipynb notebook.

Topic: A University domain with Students, Professors, Courses, Departments,
       and Buildings.

Run:
    python UniversityOntology_demo.py
"""

import rdflib
from owlrl import DeductiveClosure, OWLRL_Extension

# -------------------------------------------------------
# 1. Load the ontology
# -------------------------------------------------------
g = rdflib.Graph()
g.parse("E:/AI-For-Beginners/AI-For-Beginners/lessons/2-Symbolic/CollegeOntology.ttl", format="turtle")
print(f"Triplets found: {len(g)}")

# -------------------------------------------------------
# 2. Run inference (build the deductive closure)
# -------------------------------------------------------
DeductiveClosure(OWLRL_Extension).expand(g)
print(f"Triplets after inference: {len(g)}")

# -------------------------------------------------------
# 3. Query: Which students are enrolled in which courses?
# -------------------------------------------------------
print("\n--- Students and their courses ---")
qres = g.query("""
    PREFIX uni: <http://www.example.com/university.owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?studentName ?courseName
    WHERE {
        ?student uni:enrolledIn ?course .
        ?student rdfs:label ?studentName .
        ?course rdfs:label ?courseName .
    }
    ORDER BY ?studentName ?courseName
""")
for row in qres:
    print(f"  {row.studentName} is enrolled in {row.courseName}")

# -------------------------------------------------------
# 4. Query: Who teaches which course?
# -------------------------------------------------------
print("\n--- Professors and their courses ---")
qres = g.query("""
    PREFIX uni: <http://www.example.com/university.owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?profName ?courseName
    WHERE {
        ?prof uni:teaches ?course .
        ?prof rdfs:label ?profName .
        ?course rdfs:label ?courseName .
    }
    ORDER BY ?profName ?courseName
""")
for row in qres:
    print(f"  {row.profName} teaches {row.courseName}")

# -------------------------------------------------------
# 5. Query: Course prerequisites (inferred chain)
# -------------------------------------------------------
print("\n--- Course prerequisites ---")
qres = g.query("""
    PREFIX uni: <http://www.example.com/university.owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?courseName ?prereqName
    WHERE {
        ?course uni:hasPrerequisite ?prereq .
        ?course rdfs:label ?courseName .
        ?prereq rdfs:label ?prereqName .
    }
    ORDER BY ?courseName
""")
for row in qres:
    print(f"  {row.courseName} requires {row.prereqName}")

# -------------------------------------------------------
# 6. Query: Which students are in the Computer Science department?
# -------------------------------------------------------
print("\n--- CS Department students ---")
qres = g.query("""
    PREFIX uni: <http://www.example.com/university.owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?studentName
    WHERE {
        ?student a uni:Student .
        ?student uni:belongsToDepartment uni:ComputerScience .
        ?student rdfs:label ?studentName .
    }
    ORDER BY ?studentName
""")
for row in qres:
    print(f"  {row.studentName}")

# -------------------------------------------------------
# 7. Query: Which courses are located in which buildings?
# -------------------------------------------------------
print("\n--- Courses and their buildings ---")
qres = g.query("""
    PREFIX uni: <http://www.example.com/university.owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?courseName ?buildingName
    WHERE {
        ?course uni:locatedIn ?building .
        ?course rdfs:label ?courseName .
        ?building rdfs:label ?buildingName .
    }
    ORDER BY ?courseName
""")
for row in qres:
    print(f"  {row.courseName} is in {row.buildingName}")

# -------------------------------------------------------
# 8. Query: Who advises which student?
# -------------------------------------------------------
print("\n--- Student advisors ---")
qres = g.query("""
    PREFIX uni: <http://www.example.com/university.owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?studentName ?profName
    WHERE {
        ?student uni:advisedBy ?prof .
        ?student rdfs:label ?studentName .
        ?prof rdfs:label ?profName .
    }
    ORDER BY ?studentName
""")
for row in qres:
    print(f"  {row.studentName} is advised by {row.profName}")

# -------------------------------------------------------
# 9. Query: Who heads each department?
# -------------------------------------------------------
print("\n--- Department heads ---")
qres = g.query("""
    PREFIX uni: <http://www.example.com/university.owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?deptName ?profName
    WHERE {
        ?dept uni:headedBy ?prof .
        ?dept rdfs:label ?deptName .
        ?prof rdfs:label ?profName .
    }
    ORDER BY ?deptName
""")
for row in qres:
    print(f"  {row.deptName} is headed by {row.profName}")

print("\nDemo complete!")
