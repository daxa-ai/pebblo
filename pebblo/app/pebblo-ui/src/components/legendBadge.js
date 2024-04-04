import { waitForElement } from "../util.js";

export const LegendBadge = (props) => {
  const { color, label, value } = props;
  const elementId = `#legend-${label}-${value}`;
  waitForElement(elementId, 1000).then(function () {
    const legendChip = document.querySelector(elementId);
    legendChip.style.backgroundColor = color;
  });

  return /*html*/ `
    <div class="flex gap-2 inter font-13 items-center">
      <span class="legend-badge" id=${`legend-${label}-${value}`}></span>
      <span class="surface-10-opacity-50">${label}</span>
      <span class="surface-10">${value}</span>
    </div>
    `;
};
