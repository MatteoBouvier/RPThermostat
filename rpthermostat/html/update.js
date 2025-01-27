function build_temp_display(temp) {
    const padding = (temp.max - temp.min) / 2;
    const before = temp.current - temp.min;
    const after = temp.max - temp.current;
    
    const total = 2 * padding + before + after;
    
    const dist = (temp.max - temp.current) < (temp.current - temp.min)
    const left = dist ? `${temp.current}°C ` : ""
    const right = dist ? "" : ` ${temp.current}°C`
    
    document.getElementById("temp_display").innerHTML = `<div class="row" style="height: 2.1em; background-color:#515151; align-items: center">
    <div id="temp_graph_before" style="position: relative; height: 1.5em; background-color:rgba(117, 213, 114, 0.5); flex:${padding / total};"></div>
    <div id="temp_graph_current" style="position: relative; height: 1.5em; padding-right: 0.5em; background-color:var(--green); color:var(--dark-grey); text-align: right; flex:${before / total};">${left}</div>
    <div id="temp_graph_current2" style="position: relative; height: 1.5em; padding-left: 0.5em; background-color:var(--dark-grey); color:var(--green); flex:${after   / total};">${right}</div>
    <div id="temp_graph_after" style="position: relative; height: 1.5em; flex:${padding / total};"></div>    
</div>
<div class="row">
    <div style="flex:${padding / total};"></div>
    <div style="flex:${before  / total}; margin-left: -1em;">${temp.min}°C</div>
    <div style="flex:${after   / total};"></div>
    <div style="flex:${padding / total};">${temp.max}°C</div>    
</div>`

    
}

const request = new Request(window.location.origin + "/api/temp");

fetch(request)
  .then((response) => response.json())
  .then((data) => {
     build_temp_display(data);
  });

