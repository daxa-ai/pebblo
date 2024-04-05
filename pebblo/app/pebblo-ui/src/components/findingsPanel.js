import {
  LegendBadge,
  ChartCard,
  ApplicationsList,
} from "../components/index.js";
import { EmptyState } from "./emptyState.js";

export const FindingsPanel = (props) => {
  const { error, title } = props;
  return /*html*/ `
    <div class="flex flex-col gap-6">
       ${
         error
           ? /*html*/ `
           <div class="tab_panel flex flex-col gap-6">
            <div class="inter surface-10 font-16 medium">${title}</div>
           ${EmptyState({ variant: error })}
           </div>`
           : ` <div class="tab_panel">
       ${ChartCard(props?.findingsMap)}
       </div>
       ${ApplicationsList(props?.findingsTable)}`
       }
    </div>
  `;
};
