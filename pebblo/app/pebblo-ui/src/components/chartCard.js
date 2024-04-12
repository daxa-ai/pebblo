import { SORT_DATA } from "../util.js";
import { EmptyState } from "./emptyState.js";
import { BubbleChart, LegendBadge } from "./index.js";

export const ChartCard = (props) => {
  const { title, chartLegends, chartData, error } = props;
  let sortedData = [];
  let showTitlesForValues = [];
  if (chartData?.length > 0) {
    sortedData = SORT_DATA([...chartData], "desc", "value");
    if (sortedData?.length > 1) {
      showTitlesForValues = [sortedData[0]?.value, sortedData[1]?.value];
    } else if (sortedData?.length === 1) {
      showTitlesForValues = [sortedData[0]?.value];
    }
  }
  return /*html*/ `
    <div class="flex flex-col w-100 gap-4">
    <div class="inter surface-10 font-16 medium">${title}</div>
    ${
      error
        ? EmptyState({ variant: error })
        : `<div class="flex flex-col gap-6">     
          ${BubbleChart({ ...props, showTitlesForValues })}
          <div class="flex gap-2">
                  ${chartLegends?.myMap(function (legend) {
                    return `${LegendBadge(legend)}`;
                  })}

                  <div class="divider bg-surface-10"></div>
                  <div class="inter font-13 surface-10-opacity-50">Circle size represents the number of snippets</div>
                </div>
          </div>`
    }
    </div>
  `;
};
