import {
  ACTIVE,
  CLICK,
  DOM_CONTENT_LOADED,
  FLEX,
  NONE,
} from "../constants/enums.js";
import { UpArrowIcon } from "../icons/index.js";

// Adding event to toggle accordion

document.addEventListener(DOM_CONTENT_LOADED, function () {
  const ACCORDION__BUTTON =
    document.getElementsByClassName("accordion-summary");
  Array.from(ACCORDION__BUTTON)?.forEach((acc) => {
    acc.addEventListener(CLICK, onClick);
  });
});

function onClick(evt) {
  this.classList.toggle(ACTIVE);
  let ACCORDION__PANEL = document.getElementById(
    `panel-${Number(evt.target.parentElement.dataset.value) ||
    Number(evt.target.dataset.value)
    }`
  );
  if (ACCORDION__PANEL.style.display === FLEX) {
    ACCORDION__PANEL.style.display = NONE;
  } else {
    ACCORDION__PANEL.style.display = FLEX;
  }
}

// PROPS {children: HTMLElement || string, id: string, icon?: HTMLElement }

function AccordionSummary(props) {
  const { children, id, icon = UpArrowIcon({ id: "arrow_icon" }) } = props;
  return /*html*/ ` 
      <button title="Accordion-summary" type="button" class="accordion-summary flex gap-1 items-center" data-value="${id}">
        <div>${children}</div> 
        ${icon}
      </button>
    `;
}

// PROPS {children: HTMLElement || string, id: string }

function AccordionDetails(props) {
  const { children, id } = props;
  return /*html*/ `
       <div title="Accordion-details" id="${id}" class="none accordion-details">
           ${children}
       </div>
    `;
}

export { AccordionSummary, AccordionDetails };
