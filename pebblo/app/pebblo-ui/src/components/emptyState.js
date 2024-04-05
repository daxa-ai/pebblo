import { EMPTY_STATES } from "../constants/constant.js";
import { Button } from "./index.js";

export const EmptyState = (props) => {
  const { image, heading, subHeading, buttonNodes } =
    EMPTY_STATES[props?.variant];

  return /*html*/ `
  <div class="inter flex flex-col gap-6 justify-center items-center">
    <img src=${image} alt="pebblo" height=${120} />
    <div class="flex flex-col gap-6">
      <div class="flex flex-col gap-3 justify-center items-center">
        <div class="font-24 medium">${heading}</div>
        <div class="font-16 surface-80 w-70 text-center">${subHeading}</div>
      </div>
      ${
        buttonNodes?.length
          ? `<div class="flex justify-center gap-2">
            ${buttonNodes?.myMap((btnDetails) => Button({ ...btnDetails }))}
          </div>`
          : ""
      }
    </div>
  </div>`;
};
