def inject_panels(html_file):
    panel_js_html = """
<!-- Right-Side Panel: Add Concept + Metadata + Edit + Domain Filter -->
<div id="right-panel" style="position: fixed; top:0; right:0; width:320px; height:100%; 
     background:#f5f5f5; border-left:1px solid #ccc; padding:15px; overflow-y:auto; 
     font-family:sans-serif; z-index:999; display:block;">

  <h3>Filter by Domain</h3>
  <select id="domain-filter" onchange="filterGraph()">
    <option value="all">All</option>
    <option value="Physics">Physics</option>
    <option value="Chemistry">Chemistry</option>
    <option value="Biology">Biology</option>
    <option value="Mathematics">Mathematics</option>
    <option value="Engineering">Engineering</option>
    <option value="Earth Science">Earth Science</option>
  </select>

  <h3>Add Concept</h3>
  <input id="concept_id" placeholder="Concept ID">
  <input id="source" placeholder="Source Concept">
  <input id="target" placeholder="Target Concept">
  <input id="relationship" placeholder="Relationship">
  <input id="domain" placeholder="Domain">
  <select id="scale">
    <option value="femto">femto</option>
    <option value="atomic">atomic</option>
    <option value="molecular">molecular</option>
    <option value="planetary">planetary</option>
    <option value="biological">biological</option>
    <option value="technological">technological</option>
    <option value="meta">meta</option>
  </select>
  <button onclick="submitEntry()">Add Concept</button>

  <hr>
  <h3>Concept Metadata</h3>
  <div><strong>Concept ID:</strong> <span id="meta-id"></span></div>
  <div><strong>Domain:</strong> <span id="meta-domain"></span></div>
  <div><strong>Scale:</strong> <span id="meta-scale"></span></div>
  <div><strong>Relationships:</strong> <ul id="meta-relationships"></ul></div>
  <button onclick="enableEdit()">Edit</button>
  <button onclick="saveEdit()">Save</button>
</div>

<script>
let editingNodeId = null;

// --------------------------
// Add Concept
// --------------------------
function submitEntry() {
  const payload = {
    concept_id: document.getElementById("concept_id").value,
    source: document.getElementById("source").value,
    target: document.getElementById("target").value,
    relationship: document.getElementById("relationship").value,
    domain: document.getElementById("domain").value,
    scale: document.getElementById("scale").value
  };
  fetch("/add_entry", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => {
    if(data.status==="success"){
      alert("Concept added! Reloading graph...");
      location.reload();
    } else {
      alert("Error: "+data.error);
    }
  });
}

// --------------------------
// Enable Edit
// --------------------------
function enableEdit() {
    if(editingNodeId){
        document.getElementById("domain").value = nodes.get(editingNodeId).domain || "";
        document.getElementById("scale").value = nodes.get(editingNodeId).scale || "femto";
        alert("You can now edit Domain and Scale. Click Save to update.");
    }
}

// --------------------------
// Save Edit
// --------------------------
function saveEdit() {
    if(!editingNodeId){
        alert("Click a node first to edit.");
        return;
    }
    const payload = {
        concept_id: nodes.get(editingNodeId).concept_id,
        domain: document.getElementById("domain").value,
        scale: document.getElementById("scale").value
    };
    fetch("/edit_entry", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if(data.status==="success"){
            alert("Concept updated. Reloading graph...");
            location.reload();
        } else {
            alert("Error: "+data.error);
        }
    });
}

// --------------------------
// Filter Graph by Domain
// --------------------------
function filterGraph() {
    const selectedDomain = document.getElementById("domain-filter").value;
    nodes.get().forEach(function(node){
        if(selectedDomain==="all" || node.domain===selectedDomain){
            nodes.update({id: node.id, hidden:false});
        } else {
            nodes.update({id: node.id, hidden:true});
        }
    });
    edges.get().forEach(function(edge){
        const fromNode = nodes.get(edge.from);
        const toNode = nodes.get(edge.to);
        edges.update({id: edge.id, hidden: fromNode.hidden || toNode.hidden});
    });
}

// --------------------------
// Single merged click handler for metadata + editing
// --------------------------
network.on("click", function(params){
    if(params.nodes.length===1){
        editingNodeId = params.nodes[0];
        const nodeData = nodes.get(editingNodeId);

        document.getElementById("meta-id").innerText = nodeData.concept_id || "N/A";
        document.getElementById("meta-domain").innerText = nodeData.domain || "N/A";
        document.getElementById("meta-scale").innerText = nodeData.scale || "N/A";

        const relList = document.getElementById("meta-relationships");
        relList.innerHTML = "";
        edges.get().forEach(function(edge){
            if(edge.from===editingNodeId){
                const li = document.createElement("li");
                li.innerText = `${edge.label || ""} → ${edge.to}`;
                relList.appendChild(li);
            }
        });

        document.getElementById("right-panel").style.display = "block";
    } else {
        editingNodeId = null;
        document.getElementById("right-panel").style.display = "none";
    }
});
</script>
"""

    # Inject panel + JS into HTML
    with open(html_file,"r") as f:
        html = f.read()
    html = html.replace("</body>", panel_js_html + "\n</body>")
    with open(html_file,"w") as f:
        f.write(html)



