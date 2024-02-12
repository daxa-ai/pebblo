import { MEDIA_URL } from "../constants/constant.js";

document.addEventListener("DOMContentLoaded", function () {
  const accordion = document.getElementsByClassName("accordion-summary");
  Array.from(accordion)?.forEach((acc) => {
    acc.addEventListener("click", onClick);
  });
});

function onClick(e) {
  this.classList.toggle("active");
  let panel = document.getElementById(
    `panel-${
      Number(e.target.parentElement.dataset.value) ||
      Number(e.target.dataset.value)
    }`
  );
  if (panel.style.display === "flex") {
    panel.style.display = "none";
  } else {
    panel.style.display = "flex";
  }
}

function AccordionSummary(children, id) {
  return /*html*/ ` 
       <button title="Accordion-summary" type="button" class="accordion-summary flex gap-1 items-center" data-value="${id}">
        <div>${children}</div>
        <img id="arrow-icon" src="${MEDIA_URL}/static/arrow.png" alt="Arrow icon"/>
       </button>
    `;
}

function AccordionDetails(children, id) {
  return /*html*/ `
       <div title="Accordion-details" id="${id}" class="none accordion-details">
           ${children}
       </div>
    `;
}

export { AccordionSummary, AccordionDetails };
