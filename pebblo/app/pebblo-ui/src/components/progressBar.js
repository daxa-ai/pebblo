import { waitForElement } from "../util.js";

export function ProgressBar(props) {
  const { progress, color, id, value } = props;

  if (id) {
    waitForElement(`#inner-${id}`, 1500).then(function () {
      const innerRect = document.getElementById(`inner-${id}`);
      innerRect.style.width = `${progress}%`;
      innerRect.style.backgroundColor = color;
    });
  }

  return /*html*/ `
  <div class="flex items-center gap-2 w-fit">
    <div>${value}</div>
    <div class="barOuterRect" id='${id}-outer'>
      <div class="barInnerRect" id='inner-${id}'></div>
    </div>
  </div>`;
}
