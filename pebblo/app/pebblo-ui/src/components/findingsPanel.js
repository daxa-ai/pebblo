import {
  LegendBadge,
  ChartCard,
  ApplicationsList,
} from "../components/index.js";

export const FindingsPanel = (props) => {
  return /*html*/ `
    <div class="flex flex-col gap-6">
        <div class="tab_panel">
        ${ChartCard(props?.findingsMap)}
        </div>
        ${ApplicationsList(props?.findingsTable)}
    </div>
  `;
};
