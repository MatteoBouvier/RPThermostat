function build_temp_display(temp) {
    const padding = (temp.max - temp.min) / 2;
    const before = temp.current - temp.min;
    const after = temp.max - temp.current;

    const total = 2 * padding + before + after;

    const dist = (temp.max - temp.current) < (temp.current - temp.min);
    const left = dist ? `${temp.current}°C ` : "";
    const right = dist ? "" : ` ${temp.current}°C`;

    document.getElementById("temp_display").innerHTML =
        `<div class="row" style="height: 2.1em; background-color:#515151; align-items: center">
        <div id="temp_graph_before" style="position: relative; height: 1.5em; background-color:rgba(117, 213, 114, 0.5); flex:${
            padding / total
        };"></div>
        <div id="temp_graph_current" style="position: relative; height: 1.5em; padding-right: 0.5em; background-color:var(--green); color:var(--dark-grey); text-align: right; flex:${
            before / total
        };">${left}</div>
        <div id="temp_graph_current2" style="position: relative; height: 1.5em; padding-left: 0.5em; background-color:var(--dark-grey); color:var(--green); flex:${
            after / total
        };">${right}</div>
        <div id="temp_graph_after" style="position: relative; height: 1.5em; flex:${
            padding / total
        };"></div>    
    </div>
    <div class="row">
        <div style="flex:${padding / total};"></div>
        <div style="flex:${
            before / total
        }; margin-left: -1em;">${temp.min}°C</div>
        <div style="flex:${after / total};"></div>
        <div style="flex:${padding / total};">${temp.max}°C</div>    
    </div>`;
}

/**
 * @param {string} url
 * @param {string} body
 * @param {Event} event
 */
function post(url, body, event, callback) {
    try {
        fetch(url, {
            method: "POST",
            body: body,
            headers: {
                "Content-type": "application/json; charset=UTF-8",
            },
        })
            .then((response) => response.json())
            .then((data) => callback(data));
    } catch (err) {
        event.preventDefault();
        console.log(err);
    }
}

const SERVER_URL = globalThis.location.origin;

// === Elements ===============================================================
const main_switch = document.getElementById("main_switch");
const input_day_min = document.getElementById("day_min");
const input_day_max = document.getElementById("day_max");
const input_night_min = document.getElementById("night_min");
const input_night_max = document.getElementById("night_max");

// === Requests ===============================================================
let request = new Request(SERVER_URL + "/api/status");

fetch(request)
    .then((response) => response.json())
    .then((data) => {
        main_switch.checked = data.active;
    });

request = new Request(SERVER_URL + "/api/temp");

fetch(request)
    .then((response) => response.json())
    .then((data) => {
        build_temp_display(data);
    });

// === Events =================================================================
main_switch.addEventListener("change", (event) => {
    post(
        SERVER_URL + "/api/status",
        JSON.stringify({
            active: event.currentTarget.checked,
        }),
        event,
        (data) => {
            if (data[active] != event.currentTarget.checked) {
                event.preventDefault();
            }
        },
    );
});

input_day_min.addEventListener("change", (event) => {
    if (event.currentTarget.value >= input_day_max.value) {
        input_day_min.classList.add("is-invalid");
    } else {
        input_day_min.classList.remove("is-invalid");
        post(
            SERVER_URL + "/api/temp",
            JSON.stringify({ day: { min: event.currentTarget.value } }),
            event,
            (data) => {
                if (data.day.min == event.currentTarget.checked) {
                    event.currentTarget.classList.add("is-valid");
                }
            },
        );
    }
});

input_night_min.addEventListener("change", (event) => {
    if (event.currentTarget.value >= input_night_max.value) {
        input_night_min.classList.add("is-invalid");
    } else {
        input_night_min.classList.remove("is-invalid");
        post(
            SERVER_URL + "/api/temp",
            JSON.stringify({ night: { min: event.currentTarget.value } }),
            event,
            (data) => {
                if (data.night.min == event.currentTarget.checked) {
                    event.currentTarget.classList.add("is-valid");
                }
            },
        );
    }
});

input_day_max.addEventListener("change", (event) => {
    if (event.currentTarget.value <= input_day_min.value) {
        input_day_max.classList.add("is-invalid");
    } else {
        input_day_max.classList.remove("is-invalid");
        post(
            SERVER_URL + "/api/temp",
            JSON.stringify({ day: { max: event.currentTarget.value } }),
            event,
            (data) => {
                if (data.day.max == event.currentTarget.checked) {
                    event.currentTarget.classList.add("is-valid");
                }
            },
        );
    }
});

input_night_max.addEventListener("change", (event) => {
    if (event.currentTarget.value <= input_night_min.value) {
        input_night_max.classList.add("is-invalid");
    } else {
        input_night_max.classList.remove("is-invalid");
        post(
            SERVER_URL + "/api/temp",
            JSON.stringify({ night: { max: event.currentTarget.value } }),
            event,
            (data) => {
                if (data.night.min == event.currentTarget.checked) {
                    event.currentTarget.classList.add("is-valid");
                }
            },
        );
    }
});
