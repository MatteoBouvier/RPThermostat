export function build_temp_display(temp) {
    const dist = (temp.max - temp.current) < (temp.current - temp.min);
    const left = dist ? `${temp.current}°C ` : "";
    const right = dist ? "" : ` ${temp.current}°C`;

    if (temp.current > temp.max) {
        const span = temp.max - temp.min;
        const after = 0.25 * Math.min(0.5, (temp.current - temp.max) / span);
        const before = 0.25 - after;

        const COLOR_FAINT = "rgba(222, 60, 75, 0.5)";

        document.getElementById("temp_display").innerHTML =
            `<div class="row" style="height: 2.1em; background-color: var(--grey); align-items: center">
                <div id="temp_graph_before" style="position: relative; height: 1.5em; background-color:${COLOR_FAINT}; flex:0.25;"></div>
                <div id="temp_graph_current" style="position: relative; height: 1.5em; padding-right: 0.5em; background-color:var(--red); color:var(--dark-grey); text-align: right; flex:0.5;">${temp.current}°C</div>
                <div id="temp_graph_after" style="position: relative; height: 1.5em; background-color:${COLOR_FAINT}; flex:${before};"></div>
                <div id="temp_graph_after2" style="position: relative; height: 1.5em; flex:${after};"></div>
            </div>
            <div class="row">
                <div style="flex:0.25;"></div>
                <div style="flex:0.25; margin-left: -1em;">${temp.min}°C</div>
                <div style="flex:0.25;"></div>
                <div style="flex:0.25;">${temp.max}°C</div>    
            </div>`;
    } else if (temp.current < temp.min) {
        const span = temp.max - temp.min;
        const after = 0.25 * Math.min(0.5, (temp.min - temp.current) / span);
        const before = 0.25 - after;

        document.getElementById("temp_display").innerHTML =
            `<div class="row" style="height: 2.1em; background-color: var(--grey); align-items: center">
                <div id="temp_graph_before" style="position: relative; height: 1.5em; background-color:var(--blue); flex:${before};"></div>
                <div id="temp_graph_before2" style="position: relative; height: 1.5em; flex:${after};"></div>
                <div id="temp_graph_current" style="position: relative; height: 1.5em; padding-left: 0.5em; background-color:var(--dark-grey); color:var(--blue); flex:0.5;">${right}</div>
                <div id="temp_graph_after" style="position: relative; height: 1.5em; flex:0.25;"></div>
            </div>
            <div class="row">
                <div style="flex:0.25;"></div>
                <div style="flex:0.25; margin-left: -1em;">${temp.min}°C</div>
                <div style="flex:0.25;"></div>
                <div style="flex:0.25;">${temp.max}°C</div>    
            </div>`;
    } else {
        const COLOR_BEFORE = "rgba(117, 213, 114, 0.5)";

        const padding = (temp.max - temp.min) / 2;
        const before = temp.current - temp.min;
        const after = temp.max - temp.current;

        const total = 2 * padding + before + after;

        document.getElementById("temp_display").innerHTML =
            `<div class="row" style="height: 2.1em; background-color: var(--grey); align-items: center">
                <div id="temp_graph_before" style="position: relative; height: 1.5em; background-color:${COLOR_BEFORE}; flex:0.25;"></div>
                <div id="temp_graph_current" style="position: relative; height: 1.5em; padding-right: 0.5em; background-color:var(--green); color:var(--dark-grey); text-align: right; flex:${
                before / total
            };">${left}</div>
                <div id="temp_graph_current2" style="position: relative; height: 1.5em; padding-left: 0.5em; background-color:var(--dark-grey); color:var(--green); flex:${
                after / total
            };">${right}</div>
                <div id="temp_graph_after" style="position: relative; height: 1.5em; flex:0.25;"></div>
            </div>
            <div class="row">
                <div style="flex:0.25;"></div>
                <div style="flex:${
                before / total
            }; margin-left: -1em;">${temp.min}°C</div>
                <div style="flex:${after / total};"></div>
                <div style="flex:0.25;">${temp.max}°C</div>    
            </div>`;
    }
}
