import { MEDIA_URL } from "../constants/constant.js";
import { EmptyState } from "./emptyState.js";
import { BubbleChart, LegendBadge } from "./index.js";

export const ChartCard = (props) => {
  const { title, chartLegends, error } = props;
  return /*html*/ `
    <div class="flex flex-col w-100 gap-4">
    <div class="inter surface-10 font-16 medium">${title}</div>
    ${
      error
        ? EmptyState({ variant: error })
        : `<div class="flex gap-6">
          <div class="flex flex-col gap-2">
            ${chartLegends?.myMap(function (legend) {
              return `${LegendBadge(legend)}`;
            })}
            <div class="flex gap-2 items-center">
              <img src="${MEDIA_URL}/static/bubble-icon.svg" alt="bubble-icon" />
              <div class="inter font-13 surface-10-opacity-50">N Number of Snippets</div>
            </div>
          </div>
    ${BubbleChart(props)}
    </div>`
    }
    </div>
  `;
};
