const NIGHT_COLOR = "#042C64";
const MORNING_COLOR = "#0C6DFD";
const DAY_COLOR = "#F8F9FA";

export function fillSlider(rise, set) {
    const range_distance = set.max - set.min;
    const rise_position = rise.value - set.min;
    const set_position = set.value - set.min;

    rise.style.background = "transparent";
    set.style.background = `linear-gradient(
      to right,
      ${NIGHT_COLOR} 0%,
      ${MORNING_COLOR} ${rise_position / range_distance * 100}%,
      ${DAY_COLOR} ${(rise_position / range_distance) * 100}%,
      ${DAY_COLOR} ${set_position / range_distance * 100}%, 
      ${MORNING_COLOR} ${set_position / range_distance * 100}%, 
      ${NIGHT_COLOR} 100%)`;
}

function getParsed(rise, set) {
    const rise_v = parseFloat(rise.value, 10);
    const set_v = parseFloat(set.value, 10);
    return [rise_v, set_v];
}

export function control_sliders(rise, set, rise_time, set_time) {
    const [rise_v, set_v] = getParsed(rise, set);
    fillSlider(rise, set);

    if (rise_v > set_v) {
        rise.value = set_v;
    } else if (set_v < rise_v) {
        set.value = rise_v;
    }

    rise_time.innerText = `${parseInt(rise_v, 10)}:${
        rise_v % 1 == 0 ? "00" : "30"
    }`;
    set_time.innerText = `${parseInt(set_v, 10)}:${
        set_v % 1 == 0 ? "00" : "30"
    }`;
}
