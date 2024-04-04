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
    </div>
    ${BubbleChart(props)}
    </div>`
    }
    </div>
  `;
};
