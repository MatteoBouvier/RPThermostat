import { control_sliders, fillSlider } from "./slider.js";
import { build_temp_display } from "./temp_display.js";

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
            .then((data) => callback(data, event));
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
const slider_sun_rise = [...document.querySelectorAll(".slider_sun_rise")];
const slider_sun_set = [...document.querySelectorAll(".slider_sun_set")];
const sun_rise_time = [...document.querySelectorAll(".sun_rise_time")];
const sun_set_time = [...document.querySelectorAll(".sun_set_time")];

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
        document.getElementById("current_temp").style.color =
            data.current < data.min
                ? "var(--blue)"
                : data.current > data.max
                ? "var(--red)"
                : "var(--green)";
    });

request = new Request(SERVER_URL + "/api/days");

fetch(request)
    .then((response) => response.json())
    .then((data) => {
        document.querySelectorAll(".slider_sun_rise").forEach((s) => {
            const day = s.id.split("_")[1];
            s.value = data[day][0];
        });

        document.querySelectorAll(".slider_sun_set").forEach((s) => {
            const day = s.id.split("_")[1];
            s.value = data[day][1];
            fillSlider(document.getElementById("ssr_" + day), s);
        });
    });

// === Events =================================================================
main_switch.addEventListener("change", (event) => {
    post(
        SERVER_URL + "/api/status",
        JSON.stringify({
            active: event.currentTarget.checked,
        }),
        event,
        (data, event) => {
            if (data.active != event.currentTarget.checked) {
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
            (data, event) => {
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
            (data, event) => {
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
            (data, event) => {
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
            (data, event) => {
                if (data.night.min == event.currentTarget.checked) {
                    event.currentTarget.classList.add("is-valid");
                }
            },
        );
    }
});

slider_sun_rise.map((ssr, i) => {
    const sss = slider_sun_set[i];

    fillSlider(
        ssr,
        sss,
    );

    ssr.oninput = () =>
        control_sliders(
            ssr,
            sss,
            sun_rise_time[i],
            sun_set_time[i],
        );
    sss.oninput = () =>
        control_sliders(
            ssr,
            sss,
            sun_rise_time[i],
            sun_set_time[i],
        );
});
